#!/usr/bin/env python

#-------------------------------------------------------------------------------
# The MIT License (MIT)
#
# Copyright (c) 2015 Alvin Abad
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#-------------------------------------------------------------------------------

import os, sys
import subprocess
import pprint as pp
import argparse
import json
from datetime import datetime, timedelta
from dateutil import tz

def get_branch_number(revision_number):
    try:
        revision = revision_number.split('.')
        revision[-1] = revision[-2]
        revision[-2] = '0'
        branch_number = '.'.join(revision)
    except IndexError as e:
        print e
        branch_number = None

    return branch_number

def get_branch_name(info):
    if info['head'] == info['revision']:
        return None

    branch_number = get_branch_number(info['revision'])
    for branch, number in info['symbolic names'].iteritems():
        if branch_number == number:
            return branch

    return None

def get_commit_date(line):
    """
    date: 2015-03-01 19:45:52 -0800;  author: alvin;  state: Exp;  lines: +1 -0;  commitid: 10054F3DCE94030CAE8;
    date: 2015-03-01 19:45:52 -0800;  author: alvin;  state: Exp;  commitid: 10054F3DCE94030CAE8;
    """

    commit = {}
    try:
        for line in line.split(';'):
            line = line.strip()
            if line == '':
                continue

            commit.update(get_dict(line))
    except IndexError as e:
        print e
        return None

    return commit

def get_dict(line, delimiter=':'):
    info = {}

    try:
        line = line.strip()
        line = line.split(delimiter, 1)
        key = line[0].strip()
        value = line[1:]
        value = ''.join(value)
        value = value.strip()
        info[key] = value
    except IndexError as e:
        print e
        return None

    return info

def get_rlog(filepath, revision):
    """
    Get cvs rlog information
    Input: filepath, revision_number
    Returns: Dictionary of cvs log information
    """

    cmd = "cvs rlog -r%s %s" % (revision, filepath)
    cmd = cmd.split()
    info = {}

    p = subprocess.Popen(cmd,stdout=subprocess.PIPE)
    begin_symbolic_names = False
    symbolic_names = {}
    end_of_file= False
    while not end_of_file:
        line = p.stdout.readline()
        if not line:
            break

        line = line.rstrip()

        if line.startswith('head:'):
            info.update(get_dict(line))
            continue

        if line.startswith('branch:'):
            info.update(get_dict(line))
            continue

        if line.startswith('locks:'):
            info.update(get_dict(line))
            continue

        if line.startswith('access list:'):
            info.update(get_dict(line))
            continue

        if line.startswith('symbolic names:'):
            info.update(get_dict(line))
            info['symbolic names'] = {}
            while True:
                line = p.stdout.readline()
                if not line:
                    end_of_file = True
                    break

                line = line.rstrip()

                if line.startswith('keyword substitution:'):
                    info.update(get_dict(line))
                    break

                info['symbolic names'].update(get_dict(line))
            
            continue

        if line.startswith('total revisions:'):
            info.update(get_dict(line))
            continue

        if line.startswith('revision'):
            info.update(get_dict(line, delimiter=' '))
            continue

        if line.startswith('date:'):
            cd = get_commit_date(line)
            info.update(cd)
            info['comment'] = []
            while True:
                line = p.stdout.readline()
                if not line:
                    end_of_file = True
                    break

                if line.startswith('Files Changed:'):
                    break

                line = line.strip()
                if line != '':
                    info['comment'].append(line)

            # remove last line in the comments if it contains ===
            if len(info['comment']) > 0 and info['comment'][-1].startswith('========'):
                info['comment'].pop()

            continue

    info['branch_name'] = get_branch_name(info)

    # kill process if it has not yet terminated
    if p.returncode is None:
        p.kill()
    
    return info

def get_history(start=None, files=None, branch=None, summary=False):
    cmd = 'cvs history -a -c'
    cmd = cmd.split()

    if start:
        cmd.append('-D')
        cmd.append(start)

        from_zone = tz.tzutc()
        to_zone = tz.tzlocal()
        d = datetime.strptime(start, '%Y-%m-%d %H:%M:%S')
        local_time = d.replace(tzinfo=from_zone).astimezone(to_zone)

    modules = []
    for f in files:
        if '/' not in f:
            f += '/'
        cmd.append(f)
        modules.append(f.split('/')[0])

    #print cmd
    if start:
        print "Retrieving commit history since %s. Please wait..." % (local_time)
    else:
        print "Retrieving all commit history. Please wait..."

    history = []
    p = subprocess.Popen(cmd,stdout=subprocess.PIPE)
    while True:
        line = p.stdout.readline()
        if not line:
            break

        c = {}
        line = line.strip()
        line = line.split()

        try:
            c['f_change'] = line[0]
            c['date'] = " ".join(line[1:4])
            c['author'] = line[4]
            c['version'] = line[5]
            c['filepath'] = os.path.join(line[7], line[6])
            history.append(c)
        except IndexError as e:
            continue

    # kill process if it has not yet terminated
    if p.returncode is None:
        p.kill()

    history = sorted(history, key=lambda k: k['date'], reverse=True)

    commit = {}
    for h in history:
        f_change = h['f_change']
        author = h['author']
        version = h['version']
        filepath = h['filepath']

        # discard files not belonging to module
        filepath_module = filepath.split('/')[0]
        if not filepath_module in modules:
            continue

        # get information about the file
        info = get_rlog(filepath, version)

        # skip if not the branch queried
        if branch != info['branch_name'] and f_change != 'R':
            continue

        commit_file = { 'filepath': filepath,
                        'version': version,
                        'date': info['date'],
                        'author': info['author'],
                        'commitid': info['commitid'],
                        'change': f_change, }

        commitid = info['commitid']
        # if a new commit date, create hash
        if commitid not in commit:
            commit[commitid] = {}
            commit[commitid]['commits'] = []
            # get Comment
            commit[commitid]['comment'] = info['comment']
            # get User
            commit[commitid]['author'] = author

            commit[commitid]['author'] = info['author']
            commit[commitid]['date'] = info['date']
            commit[commitid]['commitid'] = info['commitid']

        # Get the latest date
        if info['date'] > commit[commitid]['date']:
            commit[commitid]['date'] = info['date']

        # if commit is a removal of a file, don't use branch of commit
        if f_change == 'R':
            commit[commitid]['branch'] = branch
        else:
            commit[commitid]['branch'] = info['branch_name']

        # Set branch of commit
        if 'branch' not in commit[commitid]:
            commit[commitid]['branch'] = info['branch_name']

        if not summary:
            commit[commitid]['commits'].append(commit_file)

    # kill process if it has not yet terminated
    if p.returncode is None:
        p.kill()
    
    return commit

def display(history):
    history = sorted(history.items(), key=lambda (k,v): v['date'], reverse=True)
    for id,ac in history:
        if ac['branch']:
            branch = ac['branch']
        else:
            branch = 'trunk'

        print 'commit', ac['commitid'], ac['date'], ac['author'], branch
        print "%-7s %s" % ('Author:', ac['author'])
        print "%-7s %s" % ('Date:', ac['date'])
        print
        try:
            for m in ac['comment']:
                print "    %s" % m
            print

            if len(ac['commits']) > 0:
                for c in ac['commits']:
                    print "%-3s %-s %-18s %s %s" % (c['change'],
                                                    c['version'],
                                                    c['date'],
                                                    c['commitid'],
                                                    c['filepath'])
                print
        except Exception as e:
            print e

def main(args):
    files = args.files
    branch = args.branch
    
    if args.start_date:
        start_date = args.start_date
    elif args.days:
        d = datetime.utcnow() - timedelta(days=args.days)
        start_date = d.strftime('%Y-%m-%d %H:%M:%S')
    else:
        start_date = None

    history = get_history(start=start_date, files=files, branch=branch, summary=args.summary)

    if args.json:
        print json.dumps(history, sort_keys=True, indent=4)
    else:
        display(history)

def parse_cmdline():
    parser = argparse.ArgumentParser(description="Show history of cvs commits similar to git or svn")

    parser.add_argument('-n', '--days',
                        required=False,
                        action='store',
                        type=int,
                        help='Display commit history for the past n days. Warning: If not specified, it gets everything.')

    parser.add_argument('-d', '--start_date',
                        required=False,
                        action='store',
                        help='Display commit history from date in UTC. Format: yyyy-mm-dd hh:mm:ss')

    parser.add_argument('-b', '--branch',
                        required=False,
                        action='store',
                        help='CVS branch name. Omit to use main or trunk.')

    parser.add_argument('-s', '--summary',
                        action='store_true',
                        help='Summary only')

    parser.add_argument('--json',
                        action='store_true',
                        help='Display in JSON format')

    parser.add_argument('files',
                        metavar='file',
                        nargs='+',
                        help='CVS files to query.')

    args = parser.parse_args()
    return args

#-------------------------------------------------------------------------------
# START MAIN
#-------------------------------------------------------------------------------
if __name__ == '__main__':
    args = parse_cmdline()
    main(args)

