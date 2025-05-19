"""Automation Lambda that attaches a ssm policy to the newly launched instances."""

import logging
import sys
from os import environ

import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger()
logger.setLevel("INFO")

def lambda_handler(event: dict, _: dict) -> None:
    """Lambda handler."""
    try:
        instance_profile_name = parse_instance_profile_name(event)
        if instance_profile_name is None:
            instance_ids = parse_instance_ids(event)
            if not instance_ids:
                logger.error("No instances found in the event %s",
                             parse_request_id(event))
                sys.exit(1)

            logger.info(
                "No instance profile attached to instances %s. "
                "Attaching the default instance profile.",
                instance_ids)
            instance_profile_name = environ.get("DEFAULT_INSTANCE_PROFILE_NAME")

            for instance_id in instance_ids:
                if instance_id != "":
                    attach_instance_profile_to_ec2(instance_profile_name, instance_id)
            return

        attach_policy_to_instance_profile_role(instance_profile_name)

    except ClientError:
        logger.exception("Client error")


def parse_request_id(event: dict) -> str or None:
    """Parse the request ID from the event."""
    return (event.get("detail", {})
            .get("responseElements", {})
            .get("requestId", None))

def parse_instance_profile_name(event: dict) -> str or None:
    """Parse the instance profile name from the event."""
    return (event.get("detail", {})
            .get("requestParameters", {})
            .get("iamInstanceProfile", {})
            .get("name", None))

def parse_instance_ids(event: dict) -> list:
    """Parse the instance IDs from the event."""
    instances = (event.get("detail", {})
                 .get("responseElements", {})
                 .get("instancesSet", {})
                 .get("items", None))
    if instances is not None:
        return [i.get("instanceId", "") for i in instances]

    return []

def attach_instance_profile_to_ec2(
        instance_profile_name: str, instance_id: str) -> dict:
    """Attaches the instance profile to the EC2 instance."""
    ec2_client = boto3.client("ec2")
    return ec2_client.associate_iam_instance_profile(
        IamInstanceProfile={
            "Name": instance_profile_name,
        },
        InstanceId=instance_id,
    )

def attach_policy_to_instance_profile_role(instance_profile_name: str) -> None:
    """Attaches SSM IAM managed policy to the instance profile role."""
    iam_client = boto3.client("iam")
    response = iam_client.get_instance_profile(
        InstanceProfileName=instance_profile_name,
    )

    try:
        role_arn = response["InstanceProfile"]["Roles"][0]["Arn"]
        iam_client.attach_role_policy(
            RoleName=role_arn.split("/")[1],
            PolicyArn="arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore",
        )
    except KeyError:
        logger.exception(
            "Failed to retrieve instance profile role arn for instance profile %s",
            instance_profile_name)
    except ClientError:
        logger.exception(
            "Failed to attach policy to instance profile role %s",
            instance_profile_name)
