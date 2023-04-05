from aws_cdk import Stack, aws_apigateway, aws_dynamodb, aws_lambda
from constructs import Construct


class JobBoardStack(Stack):
    def __init__(self, scope: Construct, uid: str, **kwargs) -> None:
        super().__init__(scope, uid, **kwargs)

        user_table = aws_dynamodb.Table(
            self,
            "Users",
            partition_key={
                "name": "id",
                "type": aws_dynamodb.AttributeType.STRING,
            },
            table_name="jb-users",
        )

        auth_token_table = aws_dynamodb.Table(
            self,
            "AuthTokens",
            partition_key={
                "name": "id",
                "type": aws_dynamodb.AttributeType.STRING,
            },
            table_name="jb-auth_tokens",
        )

        company_table = aws_dynamodb.Table(
            self,
            "Companies",
            partition_key={
                "name": "id",
                "type": aws_dynamodb.AttributeType.STRING,
            },
            table_name="jb-companies",
        )

        posting_table = aws_dynamodb.Table(
            self,
            "Postings",
            partition_key={
                "name": "id",
                "type": aws_dynamodb.AttributeType.STRING,
            },
            table_name="jb-job_postings",
        )

        my_lambda = aws_lambda.Function(
            self,
            "HelloHandler",
            runtime=aws_lambda.Runtime.PYTHON_3_7,
            code=aws_lambda.Code.from_asset("./lambda.zip"),
            handler="main.handler",
        )
        user_table.grant_read_write_data(my_lambda)
        auth_token_table.grant_read_write_data(my_lambda)
        company_table.grant_read_write_data(my_lambda)
        posting_table.grant_read_write_data(my_lambda)

        aws_apigateway.LambdaRestApi(
            self,
            "Endpoint",
            handler=my_lambda,
        )
