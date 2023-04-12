from aws_cdk import Stack, aws_certificatemanager, aws_route53
from constructs import Construct


class JobBoardUSEastStack(Stack):
    def __init__(self, scope: Construct, uid: str, **kwargs) -> None:
        super().__init__(scope, uid, **kwargs)

        # NEEDS TO BE IN us-east-1
        myHostedZone = aws_route53.HostedZone(
            self,
            "HostedZone",
            zone_name="yyjtechjobboard.ca",
        )

        self.cert = aws_certificatemanager.Certificate(
            self,
            "Certificate",
            domain_name="*.yyjtechjobboard.ca",
            validation=aws_certificatemanager.CertificateValidation.from_dns(myHostedZone),
        )
