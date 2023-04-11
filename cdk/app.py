#!/usr/bin/env python3

import aws_cdk as cdk
from job_board.job_board_stack import JobBoardStack

app = cdk.App()
JobBoardStack(app, "yyjtech-job-board", env=cdk.Environment(region="ca-central-1"))
app.synth()
