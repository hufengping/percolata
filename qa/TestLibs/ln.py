import os,glob
from pexpect import *

c = spawn('bash')
c.expect('\$')
cwd = os.getcwd()
for dir in glob.glob(cwd+os.sep+'*'):
    if os.path.isfile(dir):
        (path,name)= os.path.split(dir)
        print (dir,path,name)
        c.sendline('ln -s %s ../testdir/%s'%(dir,name))
        c.expect('\$')
