import os
import sys
import unittest
from unittest import mock
from unittest.mock import patch

import boto3
from botocore.stub import Stubber
from policy_attach import lambda_handler

NO_EXISTING_INSTANCE_PROFILE_NO_INSTANCE_IDS_EVENT = {
    "detail": {
        "requestParameters": {
            "iamInstanceProfile": {}
        }
    }
}

NO_EXISTING_INSTANCE_PROFILE_INSTANCE_IDS_EVENT = {
    "detail": {
        "requestParameters": {
            "iamInstanceProfile": {}
        },
        "responseElements": {
            "instancesSet": {
                "items": [
                    {
                        "instanceId": "i-01234567890abcdef"
                    }
                ]
            }
        }
    }
}

EXISTING_INSTANCE_PROFILE = {
    "detail": {
        "requestParameters": {
            "iamInstanceProfile": {
                "name": "existing-instance-profile"
            }
        }
    }
}


class TestPolicyAttach(unittest.TestCase):
    def test_empty_dict(self):
        with self.assertRaises(SystemExit) as exit_exception:
            lambda_handler({},{})
        self.assertEqual(exit_exception.exception.code, 1)

    def test_no_existing_instance_profile_and_no_instance_ids_exists(self):
        with self.assertRaises(SystemExit) as exit_exception:
            lambda_handler(NO_EXISTING_INSTANCE_PROFILE_NO_INSTANCE_IDS_EVENT,{})
        self.assertEqual(exit_exception.exception.code, 1)

    def test_no_existing_instance_profile_and_instance_ids_attaches_default_instance_profile(self):
        with patch.dict(os.environ, {
            "DEFAULT_INSTANCE_PROFILE_NAME": "default"
        }, clear=True):
            ec2_client = boto3.client('ec2')
            stubber = Stubber(ec2_client)
            stubber.add_response('associate_iam_instance_profile', {},
                                 {
                                         "IamInstanceProfile": {
                                             "Name": "default"
                                         },
                                         "InstanceId": "i-01234567890abcdef"
                                     }
                                 )
            stubber.activate()
            with mock.patch('boto3.client', mock.MagicMock(return_value=ec2_client)):
                lambda_handler(NO_EXISTING_INSTANCE_PROFILE_INSTANCE_IDS_EVENT,{})


    def test_existing_instance_profile_and__attaches_ssm_policy(self):
        with patch.dict(os.environ, {
            "DEFAULT_INSTANCE_PROFILE_NAME": "default"
        }, clear=True):
            iam_client = boto3.client('iam')
            stubber = Stubber(iam_client)
            stubber.add_response('get_instance_profile', {
                "InstanceProfile": {
                    "Path": "/",
                    "InstanceProfileName": "existing-instance-profile",
                    "Arn": "arn:aws:iam::123456789012:instance-profile/existing-instance-profile",
                    "InstanceProfileId": "IPID12345678901234567",
                    "CreateDate": "2020-01-01T00:00:00+00:00",
                    "Roles": [
                        {
                            "Path": "/",
                            "RoleName": "role-name",
                            "RoleId": "AROAIID12345678901234567",
                            "CreateDate": "2020-01-01T00:00:00+00:00",
                            "Arn": "arn:aws:iam::123456789012:role/role-name",
                        }
                    ]
                }
            },{
                 "InstanceProfileName": "existing-instance-profile"
            })
            stubber.add_response('attach_role_policy', {},
                                 {
                                     "RoleName": "role-name",
                                     "PolicyArn": "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore"
                                 })
            stubber.activate()
            with mock.patch('boto3.client', mock.MagicMock(return_value=iam_client)):
                lambda_handler(EXISTING_INSTANCE_PROFILE,{})


if __name__ == "__main__":
    unittest.main()
