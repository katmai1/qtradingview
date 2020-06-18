import sys
import os
import subprocess

try:
    cmd = "python app/main.py"
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    out, err = p.communicate()
    result = out.split('\n')
    for lin in result:
        print(lin)
    # p = subprocess.Popen("python app/main.py", shell=True)
    # for line in p.stdout.readlines():
    #     print(line)
    # p = os.popen("python app/main.py")
    # p.read()
except KeyboardInterrupt:
    print("Detenido por el usuario...")
finally:
    p.kill()
    sys.exit()
