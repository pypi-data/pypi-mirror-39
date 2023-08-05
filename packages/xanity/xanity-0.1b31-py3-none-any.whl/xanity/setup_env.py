#!/usr/bin/env python

import os
import subprocess
import pkg_resources
import sys
from random import choice
import string
from xanity import xanity


helptext ="""
setup an existing xanity directory tree

usage:  xanity setup [help]

xanity setup assumes you're in a xanity tree
"""


def setup(project_root):
    # ported from bash

    # if project doesn't have a UUID make one:
    uuid_file = os.path.join(project_root, '.xanity', 'UUID')
    if not os.path.isfile(uuid_file):
        uuid = os.path.split(project_root)[-1] + '_' + "".join(choice(string.ascii_letters) for x in range(4))
        open(uuid_file, mode='w').writelines(uuid + '\n')
    else:
        uuid = str(open(uuid_file, mode='r').read()).strip()

    # check for 'conda_environment.yaml' file
    if not os.path.isfile(os.path.join(project_root,'conda_environment.yaml')):
        print('could not find environment.yaml which contains the desired conda environment.  Please make one.\n\n')
        print(
            "example environment.yaml file:\n\n"
            "    name: < my-env-name >         "
            "    channels:                     "
            "      - javascript                "
            "    dependencies:                 "
            "      - python=3.4                "
            "      - bokeh=0.9.2               "
            "      - numpy=1.9.*               "
            "      - nodejs=0.10.*             "
            "      - flask                     "
            "      - pip:                      "
            "        - Flask-Testing           "
            "        - \"--editable=git+ssh://git@gitlab.com/lars-gatech/pyspectre.git#egg=pyspectre\""
            "        - \"git+ssh://git@gitlab.com/lars-gatech/libpsf.git#egg=libpsf\""
        )
        sys.exit(1)

    else:
        print("found conda_environment.yaml file.")

    # if conda env exists:
    if uuid in subprocess.check_output([
        'bash', '-lc', 'conda env list']).decode():

        # update conda env
        subprocess.check_call([
            'bash', '-lc', 'conda env update -f conda_environment.yaml -n {}'.format(uuid)
        ])
        print('updated conda env.')

    else:
        # create conda env
        subprocess.check_call([
            'bash', '-lc', 'conda env create -f conda_environment.yaml -n {}'.format(uuid)
        ])
        print('created conda env.')

    # get xanity version
    xanityver = pkg_resources.require("xanity")[0].version
    print('xanity version {} is installed. installing that version in env'.format(xanityver))

    subprocess.check_call([
        'bash', '-lc', 'conda activate {} && pip install xanity=={}'.format(uuid, xanityver)
    ])

    open(os.path.join(project_root, '.xanity', 'setupcomplete'), mode='w').write('')

    return 0


def main():
    dirspec = xanity.args.directory

    if dirspec == 'help':
        print(helptext)
        sys.exit(1)

    # print(
    #     "#####################################\n"
    #     "##          xanity setup           ##\n"
    #     "#####################################\n"
    # )

    if not dirspec:
        dirspec = xanity.project_root

    dirspec = os.path.expandvars(os.path.expanduser(dirspec))

    if os.path.isdir(dirspec):
        if os.path.isdir(os.path.join(dirspec,'.xanity')):
            project_root = dirspec

        else:
            print('Specified directory doesn\'t seem to be a xanity project. Try running \'xanity init\'')
    else:
        print('Specified directory does not exist')
        # project_root = os.path.abspath(os.path.join(os.getcwd(), dirspec))

    setup_script = pkg_resources.resource_filename('xanity', 'bin/xanity-setup.sh')
    opwd = os.getcwd()

    os.chdir(project_root)

    if not os.path.isfile(xanity.conf_files.conda_hash):
        # result = subprocess.call(['bash', setup_script, project_root])
        result = setup(project_root)
        if result == 0:
            xanity.freeze_conda()

    else:
        print('setup has already been run. checking status...')
        if not xanity.check_conda():
            print('updating environment...')
            # result = subprocess.call(['bash', setup_script, project_root])
            result = setup(project_root)
            if result == 0:
                xanity.freeze_conda()
        else:
            print('looks like current setup is valid')

    os.chdir(opwd)


if __name__ == "__main__":
    main()
