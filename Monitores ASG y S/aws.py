import boto3
import boto3.session
from concurrent import futures
import json

HOST = '[::]:8080'
my_session = boto3.session.Session()


oldInstances=[]
newInstances=[]


resource_ec2=boto3.client("ec2",
                        aws_access_key_id='ASIAVF6MNOPEDQW347AI',
                        aws_secret_access_key='PfaqtmK0Ljr2nLSZ/zgnBh34DoPQQnfNWSxSa3Rm',
                        aws_session_token='FwoGZXIvYXdzEBkaDDPhS9Xi162lqWE63SLIAQxohdZ1LU0kGI5D6a6h8sd5aWQweZTV66zwlzvkU4kzdN8h6fFtVPOeSqzVNUui081Qnx/3o3u9Ry8woo0phxGE3CW1LmW+p0yTUzgW3cO91sPeVfojyiy8XgFABVj1gZsyzvOspO9zcuXDCRsdyuMxsP4cKCRsoLr7CF92r1vrGfJfSd76NXDn1vnCTIvB8A25Nx6vkhH1r9IXURtc/5yfbhWI1j2hBOCW6yCiogUStB9heEGzYlPKpRW76SsQKIPx2sJIBg2uKNjOjqMGMi3K1U6+AIfatGpNJO9MYBAJWF9PW7bgJZkT3efI0yyrIVcqZBkcNCa9mmIBbeQ=',
                        region_name='us-east-1')  


def create_ec2_instance():
    get_old_instances()
    try:
        print ("Creating EC2 instance")
        resource_ec2.run_instances(
            ImageId="ami-0d9344ceadea301a4",
            MinCount=1,
            MaxCount=1,
            InstanceType="t2.micro",
            KeyName="TET2023")
        get_new_instance()
        
    except Exception as e:
        print(e)

def get_old_instances():
    try:
        response = resource_ec2.describe_instances()
        # Recorrer la respuesta y obtener la IP de cada instancia
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                if instance['InstanceId'] not in oldInstances:
                    oldInstances.append(instance['InstanceId'])
    except Exception as e:
        print(e)

def get_new_instance():
    try:
        response = resource_ec2.describe_instances()
        # Recorrer la respuesta y obtener la IP de cada instancia
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                actualid=instance['InstanceId']
                if actualid not in oldInstances:
                    newInstances.append(instance['InstanceId'])
    except Exception as e:
        print(e)

def get_ipv4(instance_id):
    response = resource_ec2.describe_instances(InstanceIds=[instance_id])
    ipv4_publico = response['Reservations'][0]['Instances'][0]['PublicIpAddress']
    print(f"La dirección IPv4 pública de la instancia {instance_id} es {ipv4_publico}")
    return [instance_id, ipv4_publico]

def terminate_ec2_instance(instance_id):
    try:
        print ("Terminate EC2 instance")
        print(resource_ec2.terminate_instances(InstanceIds=[instance_id]))
        newInstances.remove(instance_id)
        return "Instacia " + instance_id+ " terminada"
    except Exception as e:
        print(e)
        return 

def minimum_instances():
    if len(newInstances)<2:
        while len(newInstances)<2: 
            create_ec2_instance()

if __name__ == "__main__":
    create_ec2_instance()