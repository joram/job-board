#!/usr/bin/env python3

import aws_cdk as cdk
from job_board.job_board_stack import JobBoardStack
from job_board.job_board_us_east_stack import JobBoardUSEastStack

app = cdk.App()
us_east = JobBoardUSEastStack(
    app,
    "yyjtech-job-board-us-east",
    env=cdk.Environment(region="us-east-1"),
)

# todo: find a better way to create a cert in us-east-1 and use it in ca-central-1
cert_arn = us_east.cert.certificate_arn
cert_arn = "arn:aws:acm:us-east-1:431568096872:certificate/382458fc-9fe8-4361-abe5-4b6d65b1baff"

ca_central = JobBoardStack(
    app,
    "yyjtech-job-board",
    env=cdk.Environment(region="ca-central-1"),
    cert_arn=cert_arn,
)

app.synth()
