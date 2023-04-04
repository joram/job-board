from constructs import Construct
from job_board.api.index import PostsApi
from job_board.storage import PostsStorage


class JobBoard(Construct):
    apiEndPoint: str

    def __init__(self, scope: Construct, id: str, environment: str, userSuffix: str):
        super().__init__(scope, id)

        database = PostsStorage(self, "storage", environment=environment, userSuffix=userSuffix)

        jobPostingsApi = PostsApi(
            self,
            "api",
            environment=environment,
            table=database.table,
            userSuffix=userSuffix,
        )

        self.apiEndPoint = jobPostingsApi.apiEndPoint
