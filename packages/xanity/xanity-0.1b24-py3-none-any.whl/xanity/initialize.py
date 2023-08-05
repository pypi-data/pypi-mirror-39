#!/usr/bin/env python
import os
import os.path as path
import argparse
import pkg_resources
import subprocess

#from .cli_wrapper import orient

helptext =  '''
initialize a new xanity directory tree, or reset an existing tree
(will not overwrite)

usage:  xanity init [path] [help]

if path is provided, xanity tree will be created there
if path is not provided, xanity tree will be created in the pwd

\'help\' will print this help message
'''

exclude_list=[
        '\"__pycache__\\\"',
        ]

def main(arg_list=None):
    """ must be called from inside a xanity tree """
    print(
"""
#####################################
##             xanity              ##
#####################################""")
    args = clarg_subroutine(arg_list)

    skel_root = pkg_resources.resource_filename(__name__, 'skeleton')
    rsync_cmd = ['rsync','-azhu',skel_root+os.sep, xanity_path+os.sep]
    
    print('merging xanity skeleton into {}'.format(xanity_path))
    if not (args.with_examples or args.examples):
        rsync_cmd.extend(['--exclude={}'.format(item) for item in exclude_list])
    else:
        print('and including examples')
    
    subprocess.call(rsync_cmd)

    opwd =os.getcwd()
    try:
        os.chdir(xanity_path)
        git_subroutine()

    finally:
        os.chdir(opwd)


def clarg_subroutine(arg_list=None):
    global xanity_path
    global exclude_list

    parser = argparse.ArgumentParser(description='initialize a new xanity project')
    parser.add_argument('directory', type=str, nargs='?', help=helptext)
    parser.add_argument('--examples', action='store_true',
                        help='include example experiments and analyses')
    parser.add_argument('--with-examples', action='store_true',
                        help='include example experiments and analyses')
    
    args = parser.parse_args(arg_list)

    if args.directory:
        if args.directory == 'help':
            print(helptext)
            return 1

        dirspec = path.expandvars(path.expanduser(args.directory))
        if dirspec.startswith('/'):
            # absolute path given
            xanity_path = path.join(dirspec)
        else:
            # relative path given
            xanity_path = path.join(os.getcwd(),dirspec)
    else:
      # assume that the pwd is the xanity root
      xanity_path = os.getcwd()
    
    if not args.examples or args.with_examples:
        exclude_list.extend(['experiment*.py', 'analysis*.py',])
    
    return args

def git_subroutine():

    print(
"""
#####################################
##               git               ##
#####################################""")

    gi_pak = path.join(xanity_path,'.gitignore-deploy')
    gi_exist = path.join(xanity_path,'.gitignore')
    
    if (path.isfile(gi_exist)):
        print('found existing .gitignore will not clobber it')
        os.remove(gi_pak)
        
#        # check ages
#        gi_pak_age = os.stat(gi_pak).st_mtime
#        gi_exist_age =  os.stat(gi_exist).st_mtime
#    
#        # overwrite existing
#        os.remove(gi_exist)
#            
    else:
        os.rename(gi_pak, gi_exist)
        print('deployed xanity\'s .gitignore')

    # initialize a git repo
    if not subprocess.call(['bash','-c','type -t git'], stdout=open('/dev/null','bw') , stderr=subprocess.STDOUT):
        # git is working 
        if not subprocess.call(['git','status'], stdout=open('/dev/null','bw'), stderr=subprocess.STDOUT):
            # it is a git repo already
            print('leaving existing repo alone...')
        else:
            if not b'Reinitialized existing Git repository' in subprocess.check_output(['git','init',xanity_path]):
                subprocess.call(['git','add','-A'])
                subprocess.call(['git','commit','-am','xanity initial commit'])
                print('made an initial commit to your new repo')
                print('use \'git status\' to see whats up')


if __name__ == "__main__":
    main()
