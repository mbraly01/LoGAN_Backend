from timeit import default_timer as timer
import os
import paramiko
import pysftp
import time
import shutil

def upload_loGAN():
    #needed to install tensorflow==2.0, keras, tensorflow-gpu==2.0.0
    print('runs2')
    ssh = paramiko.SSHClient()
    user_name="ubuntu"
    instance_id="i-024a94e8116283b00"
    public_ip="3.87.115.233"
    pem_addr="/home/mbraly/python-for-byte-academy/Final_Project/paramiko_test.pem"
    aws_region="us-east-1a"

    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    privkey = paramiko.RSAKey.from_private_key_file(pem_addr)
    ssh.connect(hostname=public_ip, username=user_name,pkey = privkey)

    ftp_client=ssh.open_sftp()
    counter = 1
    while counter <= 10:
        stdin,stdout,stderr=ssh.exec_command(f"rm img{counter}.jpg")
        counter +=1
    ftp_client.put('/home/mbraly/python-for-byte-academy/Final_Project/Website/ifp/ifp.npy','ifp.npy')
    ftp_client.put('/home/mbraly/python-for-byte-academy/Final_Project/Website/models/loGan.py','loGAN.py')
    stdin,stdout,stderr=ssh.exec_command("python3 loGAN.py")
    print(stdout, "+", stderr)
    ftp_client.close()
    ssh.close()


def download_images():
    print('runs3')
    ssh = paramiko.SSHClient()
    user_name="ubuntu"
    instance_id="i-024a94e8116283b00"
    public_ip="3.87.115.233"
    pem_addr="/home/mbraly/python-for-byte-academy/Final_Project/paramiko_test.pem"
    aws_region="us-east-1a"


    start = timer()
    
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    privkey = paramiko.RSAKey.from_private_key_file(pem_addr)
    ssh.connect(hostname=public_ip, username=user_name,pkey = privkey)

    ftp_client=ssh.open_sftp()
    counter = 1
    while counter < 20:
        try:
            ftp_client.get(f'img{counter}.jpg', f'/home/mbraly/python-for-byte-academy/Final_Project/Website/matapp/my-app/src/output/img{counter}.jpg')
            ftp_client.get(f'img{counter}.jpg', f'/home/mbraly/python-for-byte-academy/Final_Project/Website/output/img{counter}.jpg')
            stdin,stdout,stderr=ssh.exec_command(f"rm img{counter}.jpg")
            counter += 1
        except:
            pass
        time.sleep(1) 
    ftp_client.close()
    ssh.close() 
    end = timer()
    print(end - start)

