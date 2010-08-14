import subprocess
cmd = ['sound.sh']
p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
print p.pid
