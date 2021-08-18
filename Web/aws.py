import boto3
import os
import paramiko
import pysftp

##create new user
##grant administrator access
##add to ~/.aws/credentials files

#create instance of resource class
s3=boto3.resource("s3")
s3_client = boto3.client("s3")
#get all buckets


# #print('Loading function')

# paramiko.util.log_to_file("/tmp/Dawny.log")

# # List of EC2 variables
# region = 'us-east-1'
# image = 'ami-07ebfd5b3428b6f4d'
# keyname = 'paramiko_test'

# ec2 = boto3.resource('ec2')


# #use this to create instances
# instances = ec2.create_instances(ImageId = "ami-07ebfd5b3428b6f4d", MinCount=1, MaxCount=1, InstanceType = 't2.micro', KeyName=keyname)

# instance = instances[0]
# instance.wait_until_running()


# instance.load()

# print(instance.public_dns_name)
'''
#create new bucket
s3.create_bucket(Bucket="logala2")

bucket = s3.Bucket(name="logala")

#add files to bucket
#for file in os.listdir('/home/mbraly/Downloads/Test')
s3_client.upload_file("/home/mbraly/Downloads/Test","logala","test.jpg")

s3_obj = s3.Object("logala", "test.jpg")

#download file and add it to new bucket
s3.meta.client.download_file("logala","test.jpg","/home/mbraly/python-for-byte-academy/Final_Project/test.jpg")
s3_client.upload_file("/home/mbraly/python-for-byte-academy/Final_Project/test.jpg","logala2","test.jpg")
os.remove("/home/mbraly/python-for-byte-academy/Final_Project/test.jpg")

#empties bucket
bucket.objects.all().delete()
#deletes bucket
bucket.delete()
#finding files from buckets, downloading them, reuploading them based on SQL database

ec2 = boto3.resource("ec2")
response = ec2.describe_key_pairs()
print(response)
user_name="ubuntu"
instance_id="i-068e608a8549c75f9"
pem_addr="/paramiko_test.pem"
aws_region="us-east-1"

instances = ec2.instances.filter(Filters=[{"Name": "instance-state-name", "Values": ["running"]}])
for instance in instances:
    if (instance.id==instance_id):
        p2_instance=instance
        break


ssh = paramiko.SSHClient()

def run_paramiko(ssh):
    user_name="ubuntu"
    instance_id="i-0151928d47a7befa3"
    public_ip="3.86.3.118"
    pem_addr="paramiko_test.pem"
    aws_region="us-east-1"

#     # cnopts = sftp.CnOpts(knownhosts= '/home/mbraly/python-for-byte-academy/Final_Project/paramiko_test.pem')

    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    privkey = paramiko.RSAKey.from_private_key_file(pem_addr)
    ssh.connect(hostname=public_ip, username=user_name,pkey = privkey)

    try:
            # Execute a command(cmd) after connecting/ssh to an instance
        # stdin, stdout, stderr=ssh.exec_command("python3 test.py")
        # print(stdout.read())
        # print(stderr.read())
        stdin, stdout, stderr=ssh.exec_command("ls")
        print(stdout.read())
#         #stdin, stdout, stderr = ssh.exec_command("sudo apt install python3 -y")
#          stdin, stdout, stderr = ssh.exec_command("suod apt install python3-pip")
#         stdin, stdout, stderr=ssh.exec_command("pip3 install tensorflow")
#         stdin, stdout, stderr=ssh.exec_command("sudo pip3 install keras")
#         stdin, stdout, stderr=ssh.exec_command("sudo pip3 install numpy")
#         stdin, stdout, stderr=ssh.exec_command("sudo pip3 install Pillow")
# #        stdin,stdout,stderr=ssh.exec_command("mkdir loGAN")
#         stdin,stdout,stderr=ssh.exec_command("ls")
#         #stdin,stdout,stderr=ssh.exec_command("mkdir loGAN")
#         print(stdout.readlines())

#         print (stdout.read())



    except:
        print("error")
    
    ftp_client=ssh.open_sftp()
    #ftp_client.chdir("loGAN")
    #stdin,stdout,stderr=ssh.exec_command("mkdir loGAN")
    ftp_client.put('/home/mbraly/python-for-byte-academy/Final_Project/get-pip.py','get-pip.py')
    stdin,stdout,stderr=ssh.exec_command("python3 get-pip.py")

    # stdin,stdout,stderr=ssh.exec_command("ls")
    # print(stdout.readlines())
    # stdin,stdout,stderr=ssh.exec_command("python3 loGAN.py")
    # print(stdout.read())
    # print(stderr.read())
    #ftp_client.close()
    #ssh.close()

#     ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#     privkey = paramiko.RSAKey.from_private_key_file(pem_addr)
#     ssh.connect(hostname=public_ip, username=user_name,pkey = privkey)
    #ftp_client=ssh.open_sftp()
#     #ftp_client.chdir('/loGAN')
    ftp_client.get('loGAN.py','/home/mbraly/python-for-byte-academy/Final_Project/loGAN.py')
#     ftp_client.close()
#     ftp_client.close()
#     ssh.close()
run_paramiko(ssh)

# close the client connection once the job is done

run_paramiko(ssh)

'''
# get the bucket
bucket = s3.Bucket('logala')
bucket.objects.all().delete()
#deletes bucket
bucket.delete()
'''
# use loop and count increment
count_obj = 0
for i in bucket.objects.all():
    count_obj = count_obj + 1
print(count_obj)

s3_client = boto3.client("s3")
s3.create_bucket(Bucket="logala2")
filename = "test.jpg"
for file in os.listdir('/home/mbraly/Downloads/Test')
s3_client.upload_file("/home/mbraly/Downloads/Test","logala", filename)

bucket = s3.Bucket(name="logala")
#with key value pari and go to putty
bucket.objects.all().delete()
bucket.delete()

s3.create_bucket(Bucket="logala")
'''



# def HailMary():
#     #cnopts = pysftp.CnOpts(knownhosts= '/home/mbraly/python-for-byte-academy/Final_Project/paramiko_test.pem')
#     cnopts = pysftp.CnOpts()
#     cnopts.hostkeys = None
#     with pysftp.Connection(host='3.91.186.92', username='ubuntu', password='blank', cnopts=None) as sftp:
#         sftp.put('/home/mbraly/python-for-byte-academy/Final_Project/Website/models/loGan.py', confirm=True)
#         sftp.get('loGan.py')

#     # remotepath='/loGAN/loGAN.py'
#     # localpath='/home/mbraly/python-for-byte-academy/Final_Project/Website/models/loGan.py'

#     # s.put(localpath, remotepath)

#     # s.close()

# HailMary()

'''
~/python-for-byte-academy/Final_Project$ sudo scp -i /home/mbraly/python-for-byte-academy/Final_Project/paramiko_test.pem /home/mbraly/python-for-byte-academy/Final_Project/test.py ubuntu@ec2-3-91-186-92.compute-1.amazonaws.com:~/
'''