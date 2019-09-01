#!/usr/bin/env python3

import sys
import os
import instance
import boto3
import time
import webbrowser

def xx():
    os.system('clear')
    ec2 = boto3.resource('ec2')

    print ('''
     ===========================================
                   List of Instances
     ===========================================
     ''')

    ints = []
    for i in ec2.instances.all():
        ints.append(i)

    for x in range (0, len(ints)):
        print (' Index ', x + 1, '=>\t', ints[x].id, " is ", ints[x].state)

    print ("\nEneter the index of desired instance:")
    index = input (' >>> ')

    instance = ints[int(index) - 1]
    print(instance)

# ----------------------------- keys -------------------------------------
def delete_keys():
    list_keys()
    print ("\nEnter name of key you wish to delete: ")
    delKey = input(" >>> ")

    if os.path.exists(delKey):
        os.remove(delKey)
        print ("\n\nYAYYYYY! key successfully deleted")
    else:
        print("The file does not exist")

def list_keys():
    os.system('clear')
    print ('''
     ===========================================
                Listing all keys
     ===========================================
     ''')
    path = "/Users/esedicol/Desktop/DevOps"
    for file in os.listdir(path):
        if file.endswith(".pem"):
            print("File name => ",file)

def new_key(): 
    os.system('clear')
    print ('''
     ===========================================
                Creating new pem key
     ===========================================
     ''')
    list_keys()
    print ("\n Please enter new key name (make sure to add '.pem' or else empty key is created")
    key = input(' >>> ')
    if(key == ''):
        new_key()
    else:
        try:
            create_key(key)

        except Exception as error:
            print('\n< ----- !!!!OPSIES something went wrong!!!!! ----- >\n\n')
            print(error)

def create_key(key):
    ec2 = boto3.resource('ec2')

    print ("\nCreating new key ......................\n")

    outfile = open(key,'w')

    # call the boto ec2 function to create a key pair
    key_pair = ec2.create_key_pair(KeyName=key)

    # capture the key and store it in a file
    KeyPairOut = str(key_pair.key_material)
    print (KeyPairOut)
    print ("\n < ------ Key Name : ", key, " succesfully created...YAY!!!!!! ------->\n\n")
    outfile.write(KeyPairOut)

# ---------------------------- tags ----------------------------------
def tags():
    os.system('clear')
    ec2 = boto3.resource('ec2')
    print ('''
         ===========================================
                    Creating instance tag
         ===========================================
         ''')

    print('Enter name for instance: ')
    name = input(' >>> ')
    name_tag = {'Key': 'Name', 'Value': name}

    ints = []
    for i in ec2.instances.all():
        ints.append(i)

    for x in range (0, len(ints)):
        print (' Index ', x + 1, '=>\t', ints[x].id, " is ", ints[x].state)

    print ("\nEneter the index of desired instance:")
    index = input (' >>> ')

    instance = ints[int(index) - 1]

    try:
        instance.create_tags(Tags=[name_tag])
        print ("\n------------------ Well Done a Tag has been added to: ", instance, "------------------\n\n")


    except Exception as error:
        print ("< ----- ERROR ----- >")
        print(error)

# ---------------------------- ssh ----------------------------------

# def ssh():
#     os.system('clear')
#     ec2 = boto3.resource('ec2')

#     ints = []
#     for i in ec2.instances.all():
#         ints.append(i)

#     for x in range (0, len(ints)):
#         print (' Index ', x + 1, '=>\t', ints[x].id, " is ", ints[x].state)

#     print ("\nEneter the index of desired instance:")
#     index = input (' >>> ')

#     instance = ints[int(index) - 1]

#     print("Enter key: ")
#     key = input(' >>>  ')

#     print("Enter command line  command: ")
#     cmd = input(' >>> ')

#     cmd1 = "ssh -t -o StrictHostKeyChecking=no -i" + key + "ec2-user@" + instance.public_ip_address + " 'sudo pwd'"

#     try:
#         (status, output) = subprocess.getstatusoutput(cmd1)
#         if(status > 0):
#             print('\n< ----- !!!!OPSIES something went wrong!!!!! ----- >\n\n')
#         else:
#             print("Command worked. \n",output)
#     except Exception as error:
#         print ("< ----- ERROR ----- >")
#         print(error)


# ----------------------------create instances ----------------------------------
def create_instance():
    os.system('clear')
    print ('''
         ===========================================
                    Creating new instance
         ===========================================
         ''')

    print('Enter name for instance: ')
    name = input(' >>> ')
    name_tag = {'Key': 'Name', 'Value': name}

    print('\nEnter a valid key name')
    key = input(' >>> ')

    key_def = 'mawe-key.pem'
    if(key == ''):
        key = key_def
    else:
        create(key)

    print('Please enter the name of your choice of security group or press enter to select the default group')
    group = input(' >>> ')

    default = 'sg-0481913632091c4c1'
    if(group == ''):
        group = default

def create(key):
    try: 
        ec2 = boto3.resource('ec2')
        instance = ec2.create_instances(
            ImageId='ami-0bbc25e23a7640b9b',
            KeyName = key,                                # my key name
            MinCount=1,
            MaxCount=1,
            SecurityGroupIds=[group],    # my HTTP/SSH sec group
            UserData='''#!/bin/bash
                        sudo yum update -y
                        sudo yum install python3 -y
                        sudo amazon-linux-extras install nginx1.12 -y
                        sudo service nginx start
                        chkconfig nginx on''',  # to check all ok
            InstanceType='t2.micro')

        print ("------------------ Well Done a new instance has been created ------------------\n\n")
        print ("\nInstance Id : " , instance[0].id)
        print ("Instance Status : ", instance[0].state)
        print ("Instance IPv4 : ", instance[0].public_ip_address)
        time.sleep(5)
        instance[0].reload()

    except Exception as error:
        print('\n< ----- !!!!OPSIES something went wrong!!!!! ----- >')
        print(error)


# ----------------------------list instances ----------------------------------
def list_instance():
    os.system('clear')
    ec2 = boto3.resource('ec2')

    print ('''
     ===========================================
                 Listing instances
     ===========================================
     ''')

    for instance in ec2.instances.all():
        instance.reload()
        print ("\nInstance ID => ", instance.id)
        print ("Instance Status => ", instance.state)
        print ("Instance IPv4 Addrress => ", instance.public_ip_address)


# ------------------------ start instances ----------------------------------
def start_instance():
    os.system('clear')
    ec2 = boto3.resource('ec2')

    print ('''
     ===========================================
                 Starting instances
     ===========================================
     ''')

    ints = []
    for i in ec2.instances.all():
        ints.append(i)

    for x in range (0, len(ints)):
        print (' Index ', x + 1, '=>\t', ints[x].id, " is ", ints[x].state)

    print ("\nEneter the index of desired instance:")
    index = input (' >>> ')

    instance = ints[int(index) - 1]

    try:
        if (instance.state == 'running'):
            print ("Instance already Running")
        else:
            instance.reload()
            instance.start()
            print ("< ------ Instance running!! ------>")

    except Exception as error:
        print ("< ----- ERROR ----- >")


# ------------------------ stop instances ----------------------------------
def stop_instance():
    os.system('clear')
    ec2 = boto3.resource('ec2')

    print ('''
     ===========================================
                 Stopping Instance
     ===========================================
     ''')

    ints = []
    for i in ec2.instances.all():
        ints.append(i)

    for x in range (0, len(ints)):
        print (' Index ', x + 1, '=>\t', ints[x].id, " is ", ints[x].state)

    print ("\nEneter the index of desired instance:")
    index = input (' >>> ')

    instance = ints[int(index) - 1]

    try:
        if (instance.state == 'stopped'):
            print ("Instance is already stopped")
        else:
            instance.reload()
            instance.stop()
            print ("< ------ Instance stopping!! ------>")

    except Exception as error:
        print ("< ----- ERROR ----- >")


# ------------------------ stop instances ----------------------------------
def terminate_instance():
    os.system('clear')
    ec2 = boto3.resource('ec2')

    print ('''
     ===========================================
                 Terminate Instance
     ===========================================
     ''')

    ints = []
    for i in ec2.instances.all():
        ints.append(i)

    for x in range (0, len(ints)):
        print (' Index ', x + 1, '=>\t', ints[x].id, " is ", ints[x].state)

    print ("\nEneter the index of desired instance:")
    index = input (' >>> ')

    instance = ints[int(index) - 1]

    try:
        if (instance.state == 'terminated'):
            print ("Instance is already terminated")
        else:
            instance.reload()
            instance.terminate()
            print ("< ------ Instance terminating!! ------>")

    except Exception as error:
        print ("< ----- ERROR ----- >")


def create_file():
    os.system('clear')

    print ('''
     ===========================================
                   Create File
     ===========================================
     ''')
    print ("\nEnter new file name, make sure put a (.txt) extension: ")
    fileIn = input(" >>> ")

    f= open(fileIn,"w+")
    print ("\nFile succesfully created")
    print (f)


def list_file():
    os.system('clear')

    print ('''
     ===========================================
                   List File
     ===========================================
     ''')

    path = "/Users/esedicol/Desktop/DevOps"
    for file in os.listdir(path):
        if file.endswith(".txt"):
            print("\nFile name => ",file)



def del_file():
    os.system('clear')

    print ('''
     ===========================================
                   Delete File
     ===========================================
     ''')
    list_file()

    print ("\nEnter name of file you wish to delete: ")
    delFile = input(" >>> ")

    if os.path.exists(delFile):
        os.remove(delFile)
        print ("\n\nYAYYYYY! File successfully deleted")
    else:
        print("The file does not exist")


def add_file():
    os.system('clear')
    ec2 = boto3.resource('ec2')

    print ('''
     ===========================================
                   Add File
     ===========================================
     ''')

    ints = []
    for i in ec2.instances.all():
        ints.append(i)

    for x in range (0, len(ints)):
        print (' Index ', x + 1, '=>\t', ints[x].id, " is ", ints[x].state)

    print ("\nEneter the index of desired instance:")
    index = input (" >>> ")

    instance = ints[int(index) - 1]

    print("Please enter key:")
    key = input(" >>> ")

    list_file()

    print("Please enter file name:")
    file = input(" >>> ")
    command = 'scp -i ' + key + ' ' + file + ' ' + 'ec2-user@' + instance.public_ip_address 
    try:
        (status, output) = subprocess.getstatusoutput(command)
        if(status > 0):
            print("Failed to add file", output)
        else:
            print('File uploaded wohoooooo :)')
    except Exception as error:
        print('Aww snap something went wrong :(')
        print(error)
    return (status, output)




















