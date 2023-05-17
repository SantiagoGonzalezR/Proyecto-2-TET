import boto3
import boto3.session
from concurrent import futures
import json
import time

HOST = '[::]:8080'
my_session = boto3.session.Session()


data={}
oldInstances=[]
newInstances=[]
path = 'C:\\Users\\santi\\Desktop\\Universidad\\Semestre 7\\Proyecto 2 top telem\\Proyecto-2-TET\\Monitores ASG y S\\maquinas.json'


resource_ec2=boto3.client("ec2",
                        aws_access_key_id='ASIAVF6MNOPEBIH2HSFV',
                        aws_secret_access_key='iCziLijyAjP1neT0ABcAg5LLzlbUWvRhStm/sgKe',
                        aws_session_token='FwoGZXIvYXdzECMaDIRfPbYuDYYmHRfYmCLIAcYPRI0UZSYmT/84bQqXTik0Dv5LGEcn1IbSj7yQ42ZyMhWuflz/ncqvkgDjMNbTkP6HyK904aJBFHx1rMMU9XoUX2BIQM7+pNzHOOeml4SuasQUMFMi8m//H6ugoHQ45xA/mMMBnhTa9qnA56H0GcN1wSYR4oU6tBn1LGYNlMBj/iezHCB87eHRU4BXAFdhPef0x2gphoexMEMjcnYn0kb/y1xe7NURZpjQExqK2BC93VhncDEo/WHdWAOrSRS1hLMuFLbwc8LrKJDWkKMGMi1qMQbvPlQTbedF2lH9k5gUtMNcvVagL3o7j7QC4USjeJyHM8PeIsOuF0ZakVM=',
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
                # Guardar la ip en el .json para usar conjunto a server.js
                if actualid not in oldInstances:
                    time.sleep(60)
                    ip=get_ipv4(instance['InstanceId'])
                    data[ip[0]]=0
                    with open(path, 'w') as json_file:
                        json.dump(data, json_file)
                    newInstances.append(instance['InstanceId'])
    except Exception as e:
        print(e)

def terminate_with_ip(ipv4_pub):
    filters = [
    {
        'Name': 'instance-state-name',
        'Values': ['running']
    }
]
    response = resource_ec2.describe_instances(Filters=filters)
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            if 'PublicIpAddress' in instance and instance['PublicIpAddress'] == ipv4_pub:
                # La instancia con la dirección IP deseada fue encontrada
                instance_id = instance['InstanceId']
                try:
                    print ("Terminate EC2 instance")
                    print(resource_ec2.terminate_instances(InstanceIds=[instance_id]))
                    newInstances.remove(instance_id)
                    return "Instance " + instance_id+ " terminated"
                except Exception as e:
                    print(e)
                    return 
            
    print("Couldn't find any instance with that Public IP Address")

def get_ipv4(instance_id):
    response = resource_ec2.describe_instances(InstanceIds=[instance_id])
    ipv4_publico = response['Reservations'][0]['Instances'][0]['PublicIpAddress']
    print(f"La dirección IPv4 pública de la instancia {instance_id} es {ipv4_publico}")
    return [ipv4_publico]


if __name__ == "__main__":
    #Limpieza del json
    with open(path, 'r') as json_file:
        data = json.load(json_file)
    for values in data:
        del data[values]
    #Inicializacion del ciclo del auto scaling
    while True:
        with open(path, 'r') as json_file:
            data = json.load(json_file)
        if len(data) < 5:
            create_ec2_instance()
            time.sleep(3)
        for key,  value in data.items():
            if value >= 60:
                terminate_with_ip(key)
                del data[key]
                with open(path, 'w') as json_file:
                    json.dump(data, json_file)