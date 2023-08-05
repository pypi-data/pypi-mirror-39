#!/usr/bin/env python

import argparse
import os
import subprocess
import pkg_resources

if __name__ == '__main__':
    import xanity
else:
    from . import xanity

helptext = '''
setup an existing xanity directory tree

usage:  xanity setup [help]

xanity setup assumes you're in a xanity tree

\'help\' will print this help message
'''


def main(arg_list=None):
    """ must be called from inside a xanity tree """
    
    parser = argparse.ArgumentParser(description='setup an existing xanity project')
    parser.add_argument('help', type=str, nargs='?', help=helptext)
    
    args = parser.parse_args(arg_list)
    
    if args.help:
        if args.help == 'help':
            print(helptext)
            return 0
        else:
            print('unrecognized command')
            print(helptext)
            return 1
    
    setup_script = pkg_resources.resource_filename(__name__, 'bin/xanity-setup.sh')
    opwd = os.getcwd()
    os.chdir(xanity.project_root)
    #print('stepped inside xanity root')
    if not os.path.isfile(xanity.conf_files.conda_hash):
        if 0 == subprocess.call(['bash', setup_script, xanity.project_root]):
            xanity.freeze_conda()

    else:
        if not xanity.check_conda():
            if 0 == subprocess.call(['bash', setup_script, xanity.project_root]):
                xanity.freeze_conda()
        else:
            print('looks like setup is complete')
        
    os.chdir(opwd)


if __name__ == "__main__":
    main()
