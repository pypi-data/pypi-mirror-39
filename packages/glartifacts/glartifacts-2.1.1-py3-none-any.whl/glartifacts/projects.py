import psycopg2
import psycopg2.extras
import yaml

from .errors import GitlabArtifactsError, NoProjectError, InvalidCIConfigError

GITLAB_CI_RESERVED = [
    'image',
    'services',
    'stages',
    'types',
    'before_script',
    'after_script',
    'variables',
    'cache',
    ]

def ishidden(name):
    return name.startswith('.')

def isreserved(name):
    return name.lower() in GITLAB_CI_RESERVED

class Project():
    def __init__(self, project_id, path, storage):
        self.project_id = project_id
        self.storage = storage
        self.full_path = path
        self.disk_path = self.full_path + '.git'
        self.gl_repository = 'project-{}'.format(project_id)
        self.branches = []

    def add_branch(self, name, commit):
        branch = Branch(self, name, commit)
        self.branches.append(branch)

        return branch

    def tree_path(self, ref):
        return '{}/tree/{}'.format(
            self.full_path,
            ref.name if isinstance(ref, Ref) else ref,
            )

class Ref():
    def __init__(self, project, name, commit):
        self.project = project
        self.name = name
        self.commit = commit

    def tree_path(self):
        return self.project.tree_path(self)

class Branch(Ref):
    def __init__(self, project, name, commit):
        self.job_names = []

        super().__init__(project, name, commit)

    def load_ci_config(self, config_data):
        try:
            config = yaml.safe_load(config_data)
        except yaml.YAMLError:
            raise InvalidCIConfigError(self)

        jobs = list(filter(
            lambda key: not ishidden(key) and not isreserved(key),
            config.keys()
            ))

        # gitlab-ci.yml must have at least one job
        if not jobs:
            raise InvalidCIConfigError(self)

        self.job_names = jobs

def _get_project(db, path, parent_id):
    project = None

    with db:
        with db.cursor() as cur:
            cur.execute(Query.get_project, dict(path=path, parent_id=parent_id))
            project = cur.fetchone()

    if not project:
        raise NoProjectError(path)

    return project

def _get_namespace_id(db, path_component, parent_id):
    ns = None
    with db:
        with db.cursor() as cur:
            cur.execute(Query.get_namespace, dict(path=path_component, parent_id=parent_id))
            ns = cur.fetchone()

    return ns[0] if ns else None

def _walk_namespaces(db, namespaces, project_path, parent_id=None):
    if not namespaces:
        return _get_project(db, project_path, parent_id)

    ns_path = namespaces.pop(0)
    ns_id = _get_namespace_id(db, ns_path, parent_id)
    if not ns_id:
        raise GitlabArtifactsError('No namespace "{}"'.format(ns_path))

    return _walk_namespaces(db, namespaces, project_path, ns_id)

def find_project(db, full_path):
    namespaces = full_path.split('/')
    try:
        project_path = namespaces.pop()
        project_id, storage = _walk_namespaces(
            db,
            namespaces,
            project_path
            )
    except:
        raise NoProjectError(full_path)

    return Project(
        project_id,
        full_path,
        storage
        )

def list_projects(db):
    with db:
        with db.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute(Query.projects_with_artifacts)
            return cur.fetchall()

class Query():
    projects_with_artifacts = """
with recursive ns_paths(id, parent_id, path) as (
    select n.id, n.parent_id, n.path::text
        from namespaces as n
        where n.parent_id is NULL
    union all
    select c.id, c.parent_id, (p.path || '/' || c.path)::text as path
        from namespaces as c
        inner join ns_paths as p on p.id=c.parent_id
)
select a.project_id, p.path as project, n.path as namespace,
    count(distinct a.job_id) as artifact_count
from ci_job_artifacts as a
inner join projects as p on p.id=a.project_id
left join ns_paths as n on p.namespace_id=n.id
where a.file_type <> 3
group by a.project_id, p.path, n.path
"""

    get_namespace = """
select id from namespaces where path=%(path)s and
    (%(parent_id)s is null or parent_id=%(parent_id)s)
"""

    get_project = """
select id, repository_storage
from projects
where path=%(path)s and
    (%(parent_id)s is null or namespace_id=%(parent_id)s)
"""
