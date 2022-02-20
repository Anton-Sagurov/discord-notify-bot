from boto3 import ec2


def get_ec2_instances(ec2_name):
    ec2.client('ec2')
    response = ec2.client

    return response
