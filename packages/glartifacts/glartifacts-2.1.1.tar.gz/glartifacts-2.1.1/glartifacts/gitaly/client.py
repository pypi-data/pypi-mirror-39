import grpc

from .proto import (
    ref_pb2, ref_pb2_grpc,
    commit_pb2, commit_pb2_grpc,
    blob_pb2_grpc,
    )
from .proto import shared_pb2
from ..errors import GitlabArtifactsError

GITALY_ADDR = 'unix:/var/opt/gitlab/gitaly/gitaly.socket'

def _gitaly_repo(project):
    return shared_pb2.Repository(
        storage_name=project.storage,
        relative_path=project.disk_path,
        gl_repository=project.gl_repository,
        )


class GitalyClient():
    def __init__(self, addr=GITALY_ADDR):
        self.addr = addr
        self._channel = None
        self._refsvc = None
        self._commitsvc = None
        self._blobsvc = None

    def __enter__(self):
        self._channel = grpc.insecure_channel(self.addr)
        self._refsvc = ref_pb2_grpc.RefServiceStub(self._channel)
        self._commitsvc = commit_pb2_grpc.CommitServiceStub(self._channel)
        self._blobsvc = blob_pb2_grpc.BlobServiceStub(self._channel)

        return self

    def __exit__(self, *args):
        self._channel.close()

    def get_branches(self, project):
        repository = _gitaly_repo(project)
        request = ref_pb2.FindAllBranchesRequest(
            repository=repository
            )

        try:
            response = list(self._refsvc.FindAllBranches(request))
            assert len(response) == 1 # Shouldn't this be Unary?
        except grpc.RpcError as e:
            raise GitlabArtifactsError(
                'RefSvc.FindAllBranches failed with error {}:{}'.format(
                    e.code(),
                    e.details()
                    )
                )

        branches = []
        for branch in response[0].branches:
            ref = (
                branch.name.decode('utf-8').split('/')[-1],
                branch.target.id,
                )
            branches.append(ref)
        assert branches # Safety check for failed requests

        return branches

    def get_tree_entry(self, ref, path):
        repository = _gitaly_repo(ref.project)

        request = commit_pb2.TreeEntryRequest(
            repository=repository,
            revision=ref.commit.encode('utf-8'),
            path=path.encode('utf-8'),
            limit=0,
            )

        try:
            # This should raise RpcError - on notfound, but it doesn't?
            response = list(self._commitsvc.TreeEntry(request))
            assert len(response) == 1 # Shouldn't this be Unary?
        except grpc.RpcError as e:
            raise GitlabArtifactsError(
                'CommitSvc.TreeEntry failed with error {}:{}'.format(
                    e.code(),
                    e.details()
                    )
                )

        entry = response[0]

        # Ensure we receive type=BLOB, failed requests return type=COMMIT
        blob = None
        if entry.type == 1:
            blob = (
                entry.oid,
                entry.size,
                entry.data,
                )

        return blob if blob else (None,)*3
