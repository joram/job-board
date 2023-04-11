import aws_cdk as core
from aws_cdk import assertions

from cdk.job_board.job_board_stack import JobBoardStack


def test_sqs_queue_created():
    app = core.App()
    stack = JobBoardStack(app, "cdk")
    assertions.Template.from_stack(stack)
