import boto3
import yaml
import pkg_resources

class AWS:
    region = ""
    ec2 = None
    def __init__(self, region):
        self.region = region
        self.ec2 = boto3.resource('ec2', region_name=region)

    def getAMI(self, name):
        ami = {}

        resource_package = __name__ 
        resource_path = '/'+'AMIMap.yaml'
        s = pkg_resources.resource_string(resource_package, resource_path)

        y = yaml.load(s)
        for confami in y["amis"]:
            ami[confami["name"]] = confami

        if name in ami:
            return ami[name]
        else:
            raise "KeyNotFound"

    def getInstances(self, filter):
        ec2 = boto3.client('ec2', region_name=self.region)
        return ec2.describe_instances(Filters=filter)

    def makeInstance(self, ami, size, sgid, keypair):
        return self.ec2.create_instances(ImageId=ami, InstanceType=size, MinCount=1, MaxCount=1, SecurityGroupIds=sgid, KeyName=keypair)

    def something(self):
        ec2 = boto3.resource('ec2', region_name=region)