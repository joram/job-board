#!/usr/bin/env python3

import aws_cdk as cdk
from job_board.job_board_stack import JobBoardStack

app = cdk.App()
JobBoardStack(
    app,
    "Cdk2Stack",
)

app.synth()
