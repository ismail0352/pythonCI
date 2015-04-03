#!/usr/bin/python
# coding=utf-8

"""
Copyright © 2014 by Adaptive Computing Enterprises, Inc. All Rights Reserved.

Stores build information in a JSON file so that it can be rendered at
runtime by the Django application.
"""

from __future__ import print_function

import errno
import json
import os
import subprocess
import sys
import time


def run_git_command(command):
    """
    Runs a git command.

    :param command: The array containing the git command to run.
    :return: The output of the git command.
    :raises Exception: If git is not installed or git cannot find a repository.
    """

    try:
        p = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
    except OSError:
        raise Exception("Git is not installed")
    out, err = p.communicate()
    if p.returncode != 0:
        raise Exception("Not a git repository")
    return out


def main():
    """
    Reads the build.default.json file, parses it, replaces some
    values with data collected at build time, and writes the file to
    build.json. Note that build.default.json contains at least one key
    (version) whose value we do not replace.

    :return: 0 on success, non-zero on failure.
    """

    infile_name = 'src/config/build.default.json'
    outfile_name = 'src/config/build.json'

    # Open the input file and load it into memory.
    try:
        infile = open(infile_name, 'r')
    except IOError as e:
        if e.errno == errno.ENOENT:
            print("This script must be run from the root of the iris repository.",
                  file=sys.stderr)
        else:
            print("Error: cannot open {0} for reading: {1}".format(infile_name, e.strerror),
                  file=sys.stderr)
        return 1
    build_data = json.load(infile)
    infile.close()

    # Retrieve data from OS and/or git.
    branch = os.environ.get('GIT_BRANCH')
    if branch is not None:
        branch = branch.replace('origin/', '')
    else:
        branch = run_git_command(
            command=['git', 'rev-parse', '--abbrev-ref', 'HEAD'])
    changeset = run_git_command(
        command=['git', 'log', '-1', '--pretty=format:%H'])
    abbreviated_changeset = run_git_command(
        command=['git', 'log', '-1', '--pretty=format:%h'])
    commit_date = run_git_command(
        command=['git', 'log', '-1', '--pretty=format:%ct'])
    build_date = time.time()

    # Replace values.
    build_data['branch'] = branch.strip()
    build_data['changeset'] = changeset
    build_data['abbreviated_changeset'] = abbreviated_changeset
    build_data['commit_date'] = int(commit_date)
    build_data['build_date'] = int(build_date)

    # Write the data to the output file.
    try:
        outfile = open(outfile_name, 'w')
    except IOError as e:
        print("Error: cannot open {0} for writing: {1}".format(outfile_name, e.strerror),
              file=sys.stderr)
        return 1
    json.dump(build_data, outfile, indent=2)
    outfile.close()

    # Minify style.css
    try:
        os.remove("src/static/css/style.min.css")
    except OSError as e:
        if e.errno != errno.ENOENT:
            raise e
    subprocess.check_call([
        "java",
        "-jar", "buildutils/yuicompressor-2.4.8.jar",
        "--type", "css",
        "--charset", "utf-8",
        "-o", "src/static/css/style.min.css",
        "src/static/css/style.css"
    ])


if __name__ == '__main__':
    sys.exit(main())
