__author__ = 'fengpinghu'
import paramiko

#excute command
'''
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

ssh.connect("dp0.baysensors.com", 22, "deployer")
stdin, stdout, stderr = ssh.exec_command("ls")
print stdin,
#print stdout.readlines()
ssh.close()
'''
#upload files
t = paramiko.Transport(("dp0.baysensors.com", 22))
t.connect(username="deploper")
sftp = paramiko.SFTPClient.from_transport(t)
remotepath = "/home/deployer/temp.json"
localpath = "/home/fengpinghu/workspace/github/8600066.json"
sftp.put(localpath, remotepath)
t.close()