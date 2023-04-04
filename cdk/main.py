#!/usr/bin/env python
import os

from cdktf import App, CloudBackend, NamedCloudWorkspace, TerraformStack
from cdktf_cdktf_provider_aws.provider import AwsProvider
from constructs import Construct
from job_board.index import JobBoard


class JobPostingsStack(TerraformStack):
    job_board: JobBoard

    def __init__(self, scope: Construct, name: str, environment: str, user: str):
        super().__init__(scope, name)

        AwsProvider(
            self,
            "aws",
            region="ca-central-1",
            access_key=os.environ.get("AWS_ACCESS_KEY_ID"),
            secret_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        )

        self.job_board = JobBoard(self, "posts", environment=environment, userSuffix=user)


app = App()
stack = JobPostingsStack(app, "cdk", "dev", "johno")
CloudBackend(
    stack,
    hostname="app.terraform.io",
    organization="johno",
    workspaces=NamedCloudWorkspace("Job-Board"),
)

app.synth()
