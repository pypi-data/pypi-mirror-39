import argparse
import logging
import os
import pwd
import sys
import traceback

import psycopg2

from . import log
from .config import load_config
from .errors import GitlabArtifactsError, NoProjectError, InvalidCIConfigError
from .gitaly import GitalyClient
from .projects import find_project, list_projects
from .artifacts import list_artifacts, remove_artifacts, ExpirationStrategy, ArtifactDisposition
from .utils import tabulate, humanize_datetime, humanize_size, memoize
from .version import __version__

def switch_user():
    gluser = pwd.getpwnam('git')
    os.setgid(gluser.pw_gid)
    os.setuid(gluser.pw_uid)

@memoize(
    # memoize over project_id and commit
    key=lambda args: (args[1].project.project_id, args[1].commit,)
    )
def get_ci_config(gitaly, branch):
    oid, _, data = gitaly.get_tree_entry(
        branch,
        '.gitlab-ci.yml',
        )

    # Gitaly returns an empty response if not found
    if not oid:
        return None

    return data

def filter_projects(db, project_paths, all_projects, exclude_paths):
    filtered_paths = project_paths

    if all_projects:
        filtered_paths = {
            '/'.join((p['namespace'], p['project']))
            for p in list_projects(db)
            }

    if exclude_paths:
        s_projects = set(filtered_paths)
        s_exclude = set(exclude_paths)

        # Warn user if excluded projects look bogus
        unused_excludes = s_exclude - s_projects
        for exclude in unused_excludes:
            log.warning(
                'Excluded path %s was not in the set of projects',
                exclude,
                )

        filtered_paths = s_projects - s_exclude

    return filtered_paths

def resolve_projects(db, gitaly, project_paths, all_projects=False, exclude_paths=None):
    projects = {}

    project_paths = filter_projects(db, project_paths, all_projects, exclude_paths)

    for project_path in project_paths:
        try:
            project = find_project(db, project_path)

            # Load branches
            branches = gitaly.get_branches(project)
            for name, commit in branches:
                branch = project.add_branch(name, commit)

                # Load branch jobs via .gitlab-ci.yml
                config_data = get_ci_config(gitaly, branch)
                if not config_data:
                    # No config for this branch means CI has been turned off
                    log.warning('No .gitlab-ci.yml for %s', branch.tree_path())
                else:
                    branch.load_ci_config(config_data)

                    if not branch.job_names:
                        log.warning(
                            'No jobs found in .gitlab-ci.yml for %s',
                            branch.tree_path()
                            )
        except (NoProjectError, InvalidCIConfigError) as e:
            # Continue loading projects even if a single project fails
            log.warning('Skipping %s. Reason: %s', project_path, str(e))
            log.debug(traceback.format_exc())
            continue

        projects[project.project_id] = project

    return projects

def get_args():
    parser = argparse.ArgumentParser(
        prog='glartifacts',
        description='Tools for managing GitLab artifacts')
    parser.add_argument(
        '-d', '--debug',
        action="store_true",
        help="show detailed debug information")
    parser.add_argument(
        '--verbose',
        action="store_true",
        help="show additional information")
    parser.add_argument(
        '-v', '--version',
        action='version',
        version='%(prog)s v'+__version__)

    commands = parser.add_subparsers(dest='command', title='Commands', metavar='')
    listcmd = commands.add_parser("list", help='List build artifacts')
    listcmd.add_argument(
        "projects",
        metavar='PROJECT',
        nargs='*',
        help='paths to the projects whose artifacts should be listed')
    listcmd.add_argument(
        '-a', '--all',
        action='store_true',
        help='list artifacts from all projects')
    listcmd.add_argument(
        '-e', '--exclude',
        action='store',
        nargs='+',
        metavar='PROJECT',
        help='paths to the projects whose artifacts should not by listed')
    listcmd.add_argument(
        '-s', '--short',
        action='store_true',
        help='use a short list format that only prints project names')

    removecmd = commands.add_parser("remove", help='Remove old build artifacts for a project')
    removecmd.add_argument(
        'projects',
        metavar='PROJECT',
        nargs='*',
        help='paths to the projects whose artifacts should be removed')
    removecmd.add_argument(
        '--dry-run',
        action="store_true",
        help='identify artifacts to be removed, but do not make any changes')
    removecmd.add_argument(
        '-a', '--all',
        action='store_true',
        help='remove artifacts from all projects')
    removecmd.add_argument(
        '-e', '--exclude',
        action='store',
        nargs='+',
        metavar='PROJECT',
        help='paths to the projects whose artifacts should not be removed')

    # Add arguments shared by list and remove
    for cmd in [listcmd, removecmd]:
        cmd.add_argument(
            '--strategy',
            type=ExpirationStrategy.parse,
            choices=list(ExpirationStrategy),
            default=ExpirationStrategy.LASTGOOD_PIPELINE,
            help=(
                'select the expiration strategy used to identify old artifacts '
                '(default: LASTGOOD_PIPELINE)'
                ))

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return None

    if args.debug:
        log.setLevel(logging.DEBUG)
    elif args.verbose:
        log.setLevel(logging.INFO)

    return args

def show_projects(db, short_format=False, exclude_paths=None):
    projects = list_projects(db)
    if exclude_paths:
        projects = [
            p for p in projects
            if not p['namespace']+'/'+p['project'] in exclude_paths
            ]

    if not projects:
        raise GitlabArtifactsError("No projects were found with artifacts")

    if short_format:
        names = {'/'.join((p['namespace'], p['project'])) for p in projects}
        print("\n".join(names))
        return

    rows = [['Project', 'Id', 'Jobs with Artifacts']]
    for p in projects:
        rows.append([
            '/'.join((p['namespace'], p['project'])),
            p['project_id'],
            p['artifact_count']
            ])
    tabulate(rows, sortby=dict(key=lambda r: r[0]))

def show_artifacts(projects, artifacts, scope, short_format=False, strategy=None):
    project_names = [
        '{} #{}'.format(p.full_path, project_id)
        for project_id, p in projects.items()
        ]
    projects = ", ".join(sorted(project_names))
    if not artifacts:
        raise GitlabArtifactsError("No "+scope+" were found for "+projects)

    if short_format:
        print("\n".join({r['name'] for r in artifacts}))
        return

    print("Listing", scope, "for", projects, end="")
    if strategy:
        print(" using", strategy, "strategy", end="")
    print("\n")

    rows = [[
        'Project',
        'Pipeline',
        'Job',
        '',
        'Ref',
        'Scheduled At',
        'Status',
        'Artifacts',
        'Size'
        ]]
    for r in artifacts:
        rows.append([
            '#'+str(r['project_id']),
            '#'+str(r['pipeline_id']),
            r['name'],
            '#'+str(r['job_id']),
            r['ref'],
            humanize_datetime(r['scheduled_at']),
            r['status'],
            str(ArtifactDisposition(r['disposition'])),
            humanize_size(r['size'])
            ])
    tabulate(rows, sortby=[
        dict(key=lambda r: (r[4]), reverse=True),
        dict(key=lambda r: (int(r[1][1:])), reverse=True),
        dict(key=lambda r: (int(r[0][1:])), reverse=True),
        ])

def run_command(db, gitaly, args):
    projects = {}

    if args.projects or args.all:
        projects = resolve_projects(
            db,
            gitaly,
            project_paths=args.projects,
            all_projects=args.all,
            exclude_paths=args.exclude)

        if not projects:
            raise GitlabArtifactsError('No valid projects specified')

    if args.command == 'list':
        if projects:
            artifacts = list_artifacts(
                db,
                projects,
                strategy=args.strategy
                )
            show_artifacts(projects, artifacts, "artifacts", args.short)
        else:
            show_projects(db, args.short, args.exclude)
    elif args.command == 'remove':
        if not projects:
            raise GitlabArtifactsError('No valid projects specified')

        if args.dry_run:
            artifacts = list_artifacts(
                db,
                projects,
                args.strategy,
                remove_only=True,
                )
            show_artifacts(
                projects,
                artifacts,
                "old or orphaned artifacts",
                strategy=args.strategy)
        else:
            with db:
                remove_artifacts(db, projects, args.strategy)
    else:
        raise Exception("Command {} not implemented".format(args.command))

def glartifacts():
    logging.basicConfig(
        stream=sys.stderr,
        level=logging.WARN,
        format='%(levelname)s: %(message)s')

    args = get_args()
    if not args:
        sys.exit(1)

    config = load_config()

    try:
        switch_user()
    except PermissionError:
        log.error("Permission Denied. Unable to switch to GitLab's git user.")
        return 1

    db = None
    try:
        db = psycopg2.connect(
            database=config['postgres']['dbname'],
            user=config['postgres']['user'],
            host=config['postgres']['host'],
            port=config['postgres']['port'],
            )

        with GitalyClient(config['gitaly']['address']) as gitaly:
            run_command(db, gitaly, args)

    finally:
        if db:
            db.close()

    return 0

def main():
    try:
        sys.exit(glartifacts())
    except Exception:  # pylint: disable=broad-except
        log.error(sys.exc_info()[1])
        if log.level == logging.DEBUG:
            traceback.print_exc()

        sys.exit(1)

if __name__ == '__main__':
    main()
