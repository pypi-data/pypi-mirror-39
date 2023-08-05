import subprocess
import shlex
from time import sleep

processes = list()
num = 40

for i in range(num):
    commands = 'python server.py {}'.format(2000 + i)
    commands = shlex.split(commands)
    p = subprocess.Popen(commands, stdin=subprocess.PIPE)
    processes.append(p)
    print('server listen on port {}'.format(2000 + i))
    sleep(0.2)


for i in range(num):
    commands = 'python client.py {}'.format(2000 + i)
    commands = shlex.split(commands)
    p = subprocess.Popen(commands, stdin=subprocess.PIPE)
    processes.append(p)
    print('client started {}'.format(i))
    sleep(0.2)

sleep(20.0)


for p in processes:
    p.kill()

# commands = 'fuser -k 5000/tcp'

