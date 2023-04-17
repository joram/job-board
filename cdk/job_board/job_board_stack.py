from typing import List

from aws_cdk import (
    Duration,
    Stack,
    aws_apigateway,
    aws_certificatemanager,
    aws_cloudfront,
    aws_cloudfront_origins,
    aws_dynamodb,
    aws_lambda,
    aws_s3,
    aws_secretsmanager,
)
from constructs import Construct


class JobBoardStack(Stack):
    def __init__(self, scope: Construct, uid: str, cert_arn, **kwargs) -> None:
        super().__init__(scope, uid, **kwargs)
        tables = self.create_tables()
        self.create_lambda_gateway(tables)
        self.cloudfront_distribution = self.create_cloudfront(cert_arn)

    def create_lambda_gateway(self, tables: List[aws_dynamodb.Table]) -> None:
        secrets = aws_secretsmanager.Secret(self, "Secrets", secret_name="job_board_secrets")

        my_lambda = aws_lambda.Function(
            self,
            "APICallHandler",
            runtime=aws_lambda.Runtime.PYTHON_3_7,
            code=aws_lambda.Code.from_asset("./lambda.zip"),
            handler="main.handler",
        )
        for table in tables:
            table.grant_read_write_data(my_lambda)
        secrets.grant_read(my_lambda)

        gateway = aws_apigateway.LambdaRestApi(
            self,
            "Endpoint",
            handler=my_lambda,
            default_cors_preflight_options=aws_apigateway.CorsOptions(
                allow_origins=aws_apigateway.Cors.ALL_ORIGINS, allow_methods=aws_apigateway.Cors.ALL_METHODS
            ),
        )
        gateway.root.add_method("GET")
        gateway.root.add_method("POST")
        gateway.root.add_method("PUT")

    def create_tables(self) -> List[aws_dynamodb.Table]:
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
            partition_key=aws_dynamodb.Attribute(
                name="id",
                type=aws_dynamodb.AttributeType.STRING,
            ),
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

        return [user_table, auth_token_table, company_table, posting_table]

    def create_cloudfront(self, cert_arn) -> aws_cloudfront.Distribution:
        s3_bucket = aws_s3.Bucket(
            self,
            "yyj-job-board-bucket",
            bucket_name="yyjtechjobboard.ca",
        )
        s3_bucket.grant_public_access()

        cert = aws_certificatemanager.Certificate.from_certificate_arn(
            self,
            "yyj-job-board-cert",
            certificate_arn=cert_arn,
        )

        distribution = aws_cloudfront.Distribution(
            self,
            "yyj-job-board-distribution",
            default_behavior=aws_cloudfront.BehaviorOptions(
                origin=aws_cloudfront_origins.S3Origin(s3_bucket),
                viewer_protocol_policy=aws_cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
                allowed_methods=aws_cloudfront.AllowedMethods.ALLOW_ALL,
            ),
            domain_names=["www.yyjtechjobboard.ca"],
            certificate=cert,
            default_root_object="/index.html",
            price_class=aws_cloudfront.PriceClass.PRICE_CLASS_100,
            error_responses=[
                aws_cloudfront.ErrorResponse(
                    http_status=403,
                    response_http_status=200,
                    response_page_path="/index.html",
                    ttl=Duration.minutes(30),
                ),
                aws_cloudfront.ErrorResponse(
                    http_status=404,
                    response_http_status=200,
                    response_page_path="/index.html",
                    ttl=Duration.minutes(30),
                ),
            ],
        )
        return distribution
