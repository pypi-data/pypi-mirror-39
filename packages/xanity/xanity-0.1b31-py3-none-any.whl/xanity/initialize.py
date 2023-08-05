#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import os.path as path
import shutil
import pkg_resources
import subprocess
from xanity import xanity
from random import choice, randint
import string
import sys

helptext = '''
        initialize a new xanity directory tree, or reset an existing tree
        (will not overwrite)

        usage:  xanity init [path] [help]

        if path is provided, xanity tree will be created there
        if path is not provided, xanity tree will be created in the pwd
        '''

exclude_list = [
    '\"__pycache__\\\"',
    '*~',
]


def main():
    if xanity.args.directory:
        dirspec = xanity.args.directory
    elif xanity.unknownargs:
        dirspec = xanity.unknownargs[0]
    else:
        dirspec = ''

    if dirspec == 'help':
        print(helptext)
        sys.exit(1)

    # print(
    #     "#####################################\n"
    #     "##            xanity init          ##\n"
    #     "#####################################\n"
    # )

    if not dirspec:
        dirspec = str(os.getcwd())

    dirspec = path.expandvars(path.expanduser(dirspec))
    if os.path.isdir(dirspec):
        project_root = os.path.abspath(dirspec)
        print('Initializing xanity inside existing directory: {}.'.format(project_root))

    else:
        project_root = os.path.abspath(os.path.join(os.getcwd(), dirspec))
        print('Creating a new xanity project directory: {}.'.format(project_root))

    if not xanity.args.examples:
        exclude_list.extend(['*_EXAMPLE'])
        print('and including examples')

    skel_root = pkg_resources.resource_filename(__name__, 'skeleton')
    rsync_cmd = ['rsync', '-azhu', skel_root + os.sep, project_root + os.sep]

    rsync_cmd.extend(['--exclude={}'.format(item) for item in exclude_list])
    subprocess.call(rsync_cmd)

    if xanity.args.examples:
        # walk tree and rename _EXAMPLE files
        for base, dirs, files in os.walk(project_root):
            for item in dirs+files:

                if item.endswith('_EXAMPLE'):

                    redundancy = os.path.join(base, item.split('_EXAMPLE')[0])
                    example_path = os.path.join(base, item)

                    if item in files:
                        try:
                            os.remove(redundancy)
                        except OSError:
                            pass

                    elif item in dirs:
                        try:
                            shutil.rmtree(redundancy)
                        except Exception:
                            pass

                    os.rename(example_path, redundancy)

    else:
        # walk tree and remove any _EXAMPLE files lingering:
        del_list = []
        for base, dirs, files in os.walk(project_root):
            for item in dirs+files:
                if item in dirs:
                    type='d'
                elif item in files:
                    type='f'
                if item.endswith('_EXAMPLE'):
                    del_list.append((os.path.join(base, item), type))

        for item, type in del_list:
            if type == 'f':
                os.remove(item)
            elif type == 'd':
                try:
                    shutil.rmtree(item)
                except:
                    pass

    uuid_file = os.path.join(project_root,'.xanity','UUID')

    if not os.path.isfile(uuid_file):
        uuid = os.path.split(project_root)[-1] + '_' + "".join(choice(string.ascii_letters) for x in range(4))
        open(uuid_file, mode='w').writelines(uuid+'\n')

    opwd = os.getcwd()
    os.chdir(project_root)
    git_subroutine(project_root)
    os.chdir(opwd)


def git_subroutine(project_root):
    # print(
    #     "#####################################\n"
    #     "##               git               ##\n"
    #     "#####################################\n"
    # )

    gi_pak = path.join(project_root, '.gitignore-deploy')
    gi_exist = path.join(project_root, '.gitignore')

    if (path.isfile(gi_exist)):
        print('found existing .gitignore. NOT clobbering it')
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
    if not subprocess.call(['bash', '-c', 'type -t git'], stdout=open('/dev/null', 'w'), stderr=subprocess.STDOUT):
        # git is working 
        if not subprocess.call(['git', 'status'], stdout=open('/dev/null', 'w'), stderr=subprocess.STDOUT):
            # it is a git repo already
            print('leaving existing Git repo alone...')
        else:
            if not b'Reinitialized existing Git repository' in subprocess.check_output(['git', 'init', project_root]):
                subprocess.check_call(['git', 'add', '-A'])
                subprocess.check_call(['git', 'commit', '-am', 'xanity initial commit'], stdout=open('/dev/null', 'w'), stderr=subprocess.STDOUT)
                print('\nmade an initial commit to your new repo')
                print('use \'git status\' to see whats up\n')


if __name__ == "__main__":
    main()
