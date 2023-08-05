import sys
from bgdata.command import cmdline

# Hook script to avoid "configobj" import conflict
if __name__ == '__main__':
    sys.exit(cmdline())