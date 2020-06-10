from fbs.cmdline import command
from os.path import dirname

import fbs.cmdline

@command
def hi():
    print('Hello World!')

if __name__ == '__main__':
    project_dir = dirname(__file__)
    fbs.cmdline.main(project_dir) 
