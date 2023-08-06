#!/usr/bin/python

######################################
# Author:   Chris Grabosky
# Email:    chris.grabosky@mongodb.com
# GitHub:   graboskyc
# About:    deploys a blueprint
# Deps:     boto3, ConfigParser, paramiko, scp pkgs installed. 
#           aws config file installed for user via aws cli tools `aws configure`
#           Config file in ~/.gskyaws.conf
#           Need ~/.ansible.cfg with [defaults] host_key_checking = False
# Refs:     https://github.com/graboskyc/MongoDBInit
#           https://raw.githubusercontent.com/graboskyc/MongoDBInit/master/updateAWSSG.sh
######################################

import os
import sys
import datetime
import uuid
from ConfigParser import SafeConfigParser
import argparse
import yaml
import urllib
import time
from Table import Table
from ChangeManagement import ChangeManagement
from AWS import AWS
from Tasks import Tasks
from Logger import Logger
from Atlas import Atlas

# recusrsive function to check to make sure instances are up
def r_checkStatus(region, uid):
    up=True
    aws = AWS(region)
    reservations = aws.getInstances([{"Name":"tag:use-group", "Values":[uid]}])
    for r in reservations["Reservations"]:
        for i in r["Instances"]:
            if i["State"]["Name"] != "running":
                up=False
    
    if(not up):
        time.sleep(10)
        sys.stdout.write(".")
        sys.stdout.flush()
        r_checkStatus(region, uid)

    return reservations

def cli():
    # Create your blueprint. if not specified, this is what we deploy.
    blueprint = []
    blueprint.append({"name":'DB1', "os":"ubuntu", "size":"t2.micro"})
    blueprint.append({"name":'DB2', "os":"ubuntu", "size":"t2.micro"})
    blueprint.append({"name":'DB3', "os":"ubuntu", "size":"t2.micro"})
    blueprint.append({"name":'Ops Mgr', "os":"ubuntu", "size":"t2.large"})
    bpname = "Sample"
    bpdesc = ""

    # parse cli arguments
    parser = argparse.ArgumentParser(description='CLI Tool to easily deploy a blueprint to AWS instances or MongoDB Atlas clusters')
    parser.add_argument('-b', action="store", dest="blueprint", help="path to the blueprint")
    parser.add_argument("-s", "--sample", help="download a sample blueprint yaml", action="store_true")
    parser.add_argument('-d', action="store", dest="days", help="how many days should we reserve this for before reaping")
    parser.add_argument('-k', action="store", dest="keypath", help="ssh private key location, required if using tasks")
    parser.add_argument("-l", "--list", help="instead of deploying, just list deployed instances for a given deployment (use -u flag or defaults to your user)", action="store_true")
    parser.add_argument('-u', action="store", dest="uuid", help="when listing or deleting, the uuid of the deployment")
    arg = parser.parse_args()

    # list a running blueprint
    if arg.list:
        cp = SafeConfigParser()
        cp.read(os.path.expanduser('~') + "/.aws/config")
        region = cp.get("default","region")
        aws = AWS(region)
        if arg.uuid != None:
            reservations = aws.getInstances([{"Name":"tag:use-group", "Values":[arg.uuid]}])
        else:
            conf = {}
            with open(os.path.expanduser('~') + "/.gskyaws.conf", 'r') as cf:
                for line in cf:
                    temp = line.split("=")
                    conf[temp[0]] = temp[1].replace('"',"").replace("\n","")
            reservations = aws.getInstances([{"Name":"tag:owner", "Values":[conf["name"]]}])
        print ""
        print "Here is your existing deployment:"
        tbl = Table()
        tbl.AddHeader(["Name", "Pub DNS Name", "Public Addr", "Private Addr", "Deployment ID", "BP Name", "Expires"])
        for r in reservations["Reservations"]:
            for i in r["Instances"]:
                did=""
                name=""
                expire=""
                bpn=""
                for tag in i["Tags"]:
                    if tag["Key"] == "use-group":
                        did=tag["Value"]
                    if tag["Key"] == "blueprint-name":
                        bpn=tag["Value"]
                    if tag["Key"] == "Name":
                        name=tag["Value"]
                    if tag["Key"] == "expire-on":
                        expire=tag["Value"]
                tbl.AddRow([name, i["PublicDnsName"],i["PublicIpAddress"],i["PrivateIpAddress"],did,bpn,expire])
        tbl.Draw()
        print ""
        sys.exit(0)
                

    # pull sample yaml file from github as reference
    if arg.sample:
        print "Downloading file..."
        sfile = urllib.URLopener()
        sfile.retrieve("https://raw.githubusercontent.com/graboskyc/DeployBlueprint/master/Samples/sampleblueprint.yaml", os.path.expanduser('~') + "/sample.yaml")
        print "Check your home directory for sample.yaml"
        sys.exit(0)

    # if they specifify a yaml, use that
    # otherwise we will use the hard coded blueprint above
    if (arg.blueprint != None):
        print "Using YAML file provided."
        with open(arg.blueprint,"r") as s:
            try:
                y = yaml.load(s.read())
            except:
                print "Error parsing YAML file!"
                sys.exit(2)
        
        if y["apiVersion"] != "v1":
            print "UNSUPPORTED VERSION OF BLUEPRINT YAML. THIS VERSION USES v1 ONLY."
            sys.exit(5)
        else:
            print "Using Blueprint format " + y["apiVersion"]

        blueprint = []
        sblueprint = []
        if "resources" in y:
            blueprint = y["resources"]
        if "services" in y:
            sblueprint = y["services"]
        if "metadata" in y:
            if "blueprint_name" in y["metadata"]:
                bpname = y["metadata"]["blueprint_name"]
            if "blueprint_description" in y["metadata"]:
                bpdesc = y["metadata"]["blueprint_description"]


    # always prepend a random 8 characters 
    # makes it easier to find and be grouped later
    # and track whether any failed deploys
    uid = str(uuid.uuid4())[:8]
    success=True
    conf = {}
    resdays = 7

    # logging tool
    log = Logger(uid)

    # default to 7 day reservation, otherwise take args
    if (arg.days != None):
        resdays = int(arg.days)

    # do not change order!
    # values get overridden below
    t = []
    t.append( {'Key':'Name', 'Value':'from the api'} )
    t.append( {'Key':'owner', 'Value':'some.guy'} )
    t.append( {'Key':'expire-on', 'Value':str(datetime.date.today()+ datetime.timedelta(days=resdays))} )
    t.append( {'Key':'use-group', 'Value':uid} )
    t.append( {'Key':'blueprint-name', 'Value':bpname})
    t.append( {'Key':'blueprint-desc', 'Value':bpdesc[:255]})

    # parse the config files
    if (os.path.isfile(os.path.expanduser('~') + "/.gskyaws.conf") and os.path.isfile(os.path.expanduser('~') + "/.aws/config")):
        # my custom config file parsing
        with open(os.path.expanduser('~') + "/.gskyaws.conf", 'r') as cf:
            for line in cf:
                temp = line.split("=")
                conf[temp[0]] = temp[1].replace('"',"").replace("\n","")
        
        # config files from aws cli utility
        cp = SafeConfigParser()
        cp.read(os.path.expanduser('~') + "/.aws/config")
        region = cp.get("default","region")

    else:
        # configs were not present
        print
        print "You need your config in ~/.gskyaws.conf."
        print "See: https://raw.githubusercontent.com/graboskyc/MongoDBInit/master/updateAWSSG.sh"
        print "Create ~/.gskyaws.conf with values:"
        print 'sgID="sg-yoursgidhere"'
        print 'keypair="yourawskeypairname"'
        print 'name="firstname.lastname"'
        print
        print "And you need to run `aws configure` to configure that as well"
        print
        sys.exit(1)


    # where to deploy
    # remember, you need ~/.aws/credentials set!
    aws = AWS(region)

    # being deployment of each instance
    print "Deploying Instances..."
    tbl = Table()
    tbl.AddHeader(["Instance ID", "Name", "Op System", "Size", "Succ/Fail"])
    for resource in blueprint:
        print "Trying to deploy " + resource["name"]
        try:
            # actually deploy
            inst = aws.makeInstance(aws.getAMI(resource["os"])["id"], resource["size"], [conf['sgID']], conf['keypair'])
            time.sleep(1)
            # update tags for tracking and reaping
            t[0] = {'Key':'Name', 'Value':uid + "_" +resource["name"]} 
            t[1] = {'Key':'owner', 'Value': conf["name"]} 
            inst[0].create_tags(Tags=t)
            resource["id"] = inst[0].id
            resource["resourcename"] = uid + "_" +resource["name"]
            resource["username"] = aws.getAMI(resource["os"])["user"]
            tbl.AddRow([inst[0].id, uid + "_" +resource["name"], resource["os"], resource["size"], "Success"])
        except:
            success=False
            tbl.AddRow([resource["name"], uid + "_" +resource["name"], resource["os"], resource["size"], "Fail"])
            log.write("ERROR!")
            log.write(str(sys.exc_info()[0]))

    print
    print "Results:"
    print

    tbl.Draw()
    log.writeSection("Deploying Instances", tbl.Return())

    tbl.Clear()
    print "Deploying services..."
    log.writeSection("Deploying Atlas", "")
    tbl.AddHeader(["Name", "Type", "Cloud", "Size", "Status"])
    atlas = Atlas(conf["atlasusername"], conf["atlasapikey"], uid)
    for service in sblueprint:
        print "Trying to deploy " + service["name"]
        log.writeTimestamp("Trying to deploy" + service["name"])
        backup = False
        bi = False
        enc = False
        if "backup" in service:
            backup = service["backup"]
        if "biconnector" in service:
            bi = service["backup"]
        if "encrypted" in service:
            enc = service["encrypted"]
        if "iops" in service:
            iops = int(service["iops"])
        if "disksize" in service:
            ds = service["disksize"]

        worked,output = atlas.createCluster(service["name"], service["groupid"], service["region"], service["type"], service["version"], service["cloud"], service["size"], service["rscount"], service["shards"], ds, iops, backup, bi, enc)

        if worked:
            tbl.AddRow([service["name"], service["type"], service["cloud"], service["size"], "Deploying..."])
        else:
            tbl.AddRow([service["name"], service["type"], service["cloud"], service["size"], "Failed!"])
            log.write("ERROR!")
            log.write(output)
    log.write(tbl.Return())
    print "Services deployed:"
    tbl.Draw()

    # wait for everything to come up
    print
    sys.stdout.write("Waiting for successfully deployed instances to come up...")
    sys.stdout.flush()
    reservations = r_checkStatus(region, uid)
    print
    print "Instances are running..."
    print
    sys.stdout.write("Waiting for successfully deployed services to come up...")
    sys.stdout.flush()
    clusters = atlas.r_waitForCluster()
    print "Everything is ready."
    print "Building Post-Configuration Plan..."
    print

    # build the task list
    tasks=Tasks()
    time.sleep(5)
    reservations = r_checkStatus(region, uid)
    clusters = atlas.r_waitForCluster()
    for resource in blueprint:
        i=0
        # find the DNS Name
        for r in reservations["Reservations"]:
            for i in r["Instances"]:
                if i["InstanceId"] == resource["id"]:
                    resource["dns"] = i["PublicDnsName"]
        
        if "tasks" in resource:
            tl=[]
            for task in resource["tasks"]:
                task["resourceid"] = resource["id"]
                task["resourcedeployedname"] = resource["resourcename"]
                task["resourcename"] = resource["name"]
                task["dns"] = resource["dns"]
                task["status"] = "Pending"
                task["username"] = resource["username"]
                tl.append(task)
            tasks.addTaskGroup(int(resource["postinstallorder"]), tl)
    for service in sblueprint:
        if "tasks" in service:
            tl=[]
            for task in service["tasks"]:
                task["resourceid"] = ""
                task["resourcedeployedname"] = service["name"]
                task["resourcename"] = service["name"]
                task["dns"] = ""
                task["status"] = "Pending"
                task["username"] = ""
                tl.append(task)
            tasks.addTaskGroup(int(service["postinstallorder"]), tl)

    # draw user output
    i=1
    tbl.Clear()
    tbl.AddHeader(["Task Number", "Name", "ID", "Public DNS Name", "Type", "Description", "Status"])
    for tl in tasks.getTasks():
        for t in tl:
            tbl.AddRow([str(i), t["resourcedeployedname"],t["resourceid"], t["dns"], t["type"],t["description"], t["status"]])
            i=i+1
    print "Plan created:"
    print
    tbl.Draw()

    log.writeSection("Post-Deploy Plan", tbl.Return())

    if len(tasks.getTasks()) == 0:
        print 
        print "No tasks to do."
        log.write("no tasks to do.")
        print
    else:
        i=1
        cm = ChangeManagement()
        for tl in tasks.getTasks():
            for t in tl:
                print "Beginning Task %s (%s) on %s..." % (str(i), t["description"], t["resourcedeployedname"])
                if t["type"] == "playbook":
                    t["status"] = "Running"
                    try:
                        log.writeTimestamp("BEGINING TASK " + str(i))
                        result = cm.runPlaybook(t["url"], t["dns"], uid, i, arg.keypath, t["username"])
                        log.write(result)
                        t["status"] = "Completed"
                    except:
                        t["status"] = "Failed"
                        log.writeTimestamp("Tried running task " + str(i) + " on " + t["dns"])
                        log.write("ERROR:")
                        log.write(str(sys.exc_info()[0]))
                elif t["type"] == "shell":
                    t["status"] = "Running"
                    try:
                        log.writeTimestamp("BEGINING TASK " + str(i))
                        result = cm.runBashScript(t["url"], t["dns"], uid, i, arg.keypath, t["username"])
                        log.write(result)
                        t["status"] = "Completed"
                    except:
                        t["status"] = "Failed"
                        log.writeTimestamp("Tried running task " + str(i) + " on " + t["dns"])
                        log.write("ERROR:")
                        log.write(str(sys.exc_info()))
                elif t["type"] == "local":
                    t["status"] = "Running"
                    try:
                        log.writeTimestamp("BEGINING TASK " + str(i))
                        result=cm.runLocal(t["cmd"], uid, i)
                        log.write(result)
                        t["status"] = "Completed"
                    except:
                        t["status"] = "Failed"
                        log.writeTimestamp("Tried running task " + str(i) + " on " + t["resourcedeployedname"])
                        log.write("ERROR:")
                        log.write(str(sys.exc_info()))
                else:
                    t["status"] = "TypeError"
                    log.writeTimestamp("Tried running task " + str(i) + " on " + t["dns"])
                    log.write("ERROR:\nUnsupported task type.")
                i=i+1
        print

    # print results
    i=1
    tbl.Clear()
    tbl.AddHeader(["Task Number", "Name", "ID", "Public DNS Name", "Type", "Description", "Status"])
    for tl in tasks.getTasks():
        for t in tl:
            tbl.AddRow([str(i), t["resourcedeployedname"],t["resourceid"], t["dns"], t["type"],t["description"], t["status"]])
            i=i+1
    print "Plan results:"
    print
    tbl.Draw()
    log.write(tbl.Return())

    # completed
    print 
    if success:
        print "Blueprint Successfully Deployed!"
        log.writeSection("Completion", "Blueprint Successfully Deployed!")
    else:
        print "The blueprint may not have been successfully deployed."
        log.writeSection("Completion", "The blueprint may not have been successfully deployed.")
    print