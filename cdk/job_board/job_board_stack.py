from typing import List

from aws_cdk import (
    Stack,
    aws_apigateway,
    aws_certificatemanager,
    aws_cloudfront,
    aws_cloudfront_origins,
    aws_dynamodb,
    aws_lambda,
    aws_route53,
    aws_s3,
)
from constructs import Construct


class JobBoardStack(Stack):
    def __init__(self, scope: Construct, uid: str, **kwargs) -> None:
        super().__init__(scope, uid, **kwargs)
        tables = self.create_tables()
        self.create_lambda_gateway(tables)
        self.cloudfront_distribution = self.create_cloudfront()

    def create_lambda_gateway(self, tables: List[aws_dynamodb.Table]) -> None:
        my_lambda = aws_lambda.Function(
            self,
            "APICallHandler",
            runtime=aws_lambda.Runtime.PYTHON_3_7,
            code=aws_lambda.Code.from_asset("./lambda.zip"),
            handler="main.handler",
        )
        for table in tables:
            table.grant_read_write_data(my_lambda)

        aws_apigateway.LambdaRestApi(
            self,
            "Endpoint",
            handler=my_lambda,
        )

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

    def create_cloudfront(self) -> aws_cloudfront.Distribution:
        s3_bucket = aws_s3.Bucket(
            self,
            "yyj-job-board-bucket",
            bucket_name="yyjtechjobboard.ca",
        )
        s3_bucket.grant_public_access()

        ## NEEDS TO BE IN us-east-1
        # myHostedZone = aws_route53.HostedZone(
        #     self, 'HostedZone',
        #     zone_name="yyjtechjobboard.ca",
        # )
        #
        # cert = aws_certificatemanager.Certificate(self, 'Certificate',
        #     domain_name="*.yyjtechjobboard.ca",
        #     validation=aws_certificatemanager.CertificateValidation.from_dns(myHostedZone),
        # )
        #

        return aws_cloudfront.Distribution(
            self,
            "yyj-job-board-distribution",
            default_behavior=aws_cloudfront.BehaviorOptions(
                origin=aws_cloudfront_origins.S3Origin(s3_bucket),
                viewer_protocol_policy=aws_cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
            ),
            # domain_names=["www.yyjtechjobboard.ca"],
            # certificate=cert,
            price_class=aws_cloudfront.PriceClass.PRICE_CLASS_100,
        )
