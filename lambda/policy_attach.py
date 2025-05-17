from os import environ

import boto3
import logging
logger = logging.getLogger()
logger.setLevel('INFO')

def lambda_handler(event, context):
    try:
        instance_profile_name = event.get('detail', {}).get('requestParameters', {}).get('iamInstanceProfile', {}).get('name','')
        if instance_profile_name == '':
            logger.warning('No instance profile name found in event. Attaching default')
            instance_profile_name = environ.get('DEFAULT_INSTANCE_PROFILE_NAME')

            for instance in event.get('detail', {}).get('responseElements', {}).get('instancesSet', {}).get('items', []):
                instance_id = instance.get('instanceId', '')
                if instance_id != '':
                    attach_instance_profile_to_ec2(instance_profile_name, instance_id)
            return

        iam_client = boto3.client('iam')
        response = iam_client.get_instance_profile(
            InstanceProfileName=instance_profile_name
        )

        role_arn = response['InstanceProfile']['Roles'][0]['Arn']
        response = iam_client.attach_role_policy(
            RoleName=role_arn.split('/')[1],
            PolicyArn='arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore'
        )
        print(response)
    except Exception as e:
        print(e)


def attach_instance_profile_to_ec2(instance_profile_name, instance_id):
    ec2_client = boto3.client('ec2')
    response = ec2_client.associate_iam_instance_profile(
        IamInstanceProfile={
            'Name': instance_profile_name
        },
        InstanceId=instance_id
    )
    logger.info(response)