from aws_cdk import Stack
from aws_cdk import aws_apigateway as apigw
from aws_cdk import aws_lambda as _lambda
from constructs import Construct


class JobBoardStack(Stack):
    def __init__(self, scope: Construct, uid: str, **kwargs) -> None:
        super().__init__(scope, uid, **kwargs)

        my_lambda = _lambda.Function(
            self,
            "HelloHandler",
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.from_asset("./lambda.zip"),
            handler="main.handler",
        )

        apigw.LambdaRestApi(
            self,
            "Endpoint",
            handler=my_lambda,
        )
