# cvs-utils
Tools and Utilities for CVS

## cvs-history.py
Show history of cvs commits similar to git or svn

### Use cases:

1. Show history of all commits in the main branch of moduleA

```
cvs-history.py moduleA
```

2. Show history of commits in feature_branch of moduleA

```
cvs-history.py -b feature_branch moduleA
```

3. Show history of commits for the last 5 days in feature_branch of moduleA

If you have a long history of commits, the tool might take a long time to run. 
If you only want to see the history for the past 5 days, you can supply that option.

```
cvs-history.py -n 5 -b feature_branch moduleA
```

### Complete syntax

```
./cvs-history.py -h
usage: cvs-history.py [-h] [-n DAYS] [-d START_DATE] [-b BRANCH] [-s] [--json]
                      file [file ...]

Show history of cvs commits similar to git or svn

positional arguments:
  file                  CVS files to query.

optional arguments:
  -h, --help            show this help message and exit
  -n DAYS, --days DAYS  Display commit history for the past n days. Warning:
                        If not specified, it gets everything.
  -d START_DATE, --start_date START_DATE
                        Display commit history from date in UTC. Format: yyyy-
                        mm-dd hh:mm:ss
  -b BRANCH, --branch BRANCH
                        CVS branch name. Omit to use main or trunk.
  -s, --summary         Summary only
  --json                Display in JSON format
```
