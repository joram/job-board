#!/usr/bin/env python3

import aws_cdk as cdk
from job_board.job_board_stack import JobBoardStack
from job_board.job_board_us_east_stack import JobBoardUSEastStack

app = cdk.App()
us_east = JobBoardUSEastStack(app, "yyjtech-job-board-us-east", env=cdk.Environment(region="us-east-1"))
ca_central = JobBoardStack(app, "yyjtech-job-board", env=cdk.Environment(region="ca-central-1"), cert=us_east.cert)

app.synth()
