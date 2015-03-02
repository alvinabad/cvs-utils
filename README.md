# cvs-utils
Tools and Utilities for CVS

## cvs-history.py
Show history of cvs commits similar to git or svn

#### Use cases:

1. Show history of all commits in the main branch of moduleA

   ```
   cvs-history.py moduleA
   ```

   Sample output:
   ```
   Retrieving all commit history. Please wait...
   commit 10054F260D4309DE913 2015-03-01 00:44 +0000 trunk
   Author: alvin
   Date:   2015-02-28 16:44:10 -0800

       Added method_2C

   M   1.4 2015-02-28 16:44:10 -0800 10054F260D4309DE913 hello_cvs/hello2.py

   commit 10054F25F4F304394C0 2015-03-01 00:37 +0000 trunk
   Author: alvin
   Date:   2015-02-28 16:37:50 -0800

       Added method_1C
       Fixed method_1B

   M   1.7 2015-02-28 16:37:50 -0800 10054F25F4F304394C0 hello_cvs/hello1.py

   commit 10054F254CA252915B7 2015-02-28 23:52 +0000 trunk
   Author: alice
   Date:   2015-02-28 15:52:57 -0800

       Added method_1B

   M   1.6 2015-02-28 15:52:57 -0800 10054F254CA252915B7 hello_cvs/hello1.py

   commit 10054F253B823F0AC16 2015-02-28 23:48 +0000 trunk
   Author: alice
   Date:   2015-02-28 15:48:17 -0800

       branches:  1.3.2;
       Added method_2B

   M   1.3 2015-02-28 15:48:17 -0800 10054F253B823F0AC16 hello_cvs/hello2.py
   ```

2. Show history of commits in feature_branch of moduleA

   ```
   cvs-history.py -b feature_branch moduleA
   ```

   Sample output:
   ```
   Retrieving all commit history. Please wait...
   commit 10054F346CD380B8032 2015-03-01 17:05 +0000 feature_branch
   Author: alice
   Date:   2015-03-01 09:05:26 -0800

       Added comment for method_2B

   M   1.3.2.1 2015-03-01 09:05:26 -0800 10054F346CD380B8032 hello_cvs/hello2.py

   commit 10054F260803096D9AE 2015-03-01 00:42 +0000 feature_branch
   Author: alice
   Date:   2015-02-28 16:42:49 -0800

       Added doc for method_3A

   M   1.1.2.2 2015-02-28 16:42:49 -0800 10054F260803096D9AE hello_cvs/hello3.py

   commit 10054F25F773051D68F 2015-03-01 00:38 +0000 feature_branch
   Author: alice
   Date:   2015-02-28 16:38:21 -0800

       Added hello3.py

   A   1.1.2.1 2015-02-28 16:38:21 -0800 10054F25F773051D68F hello_cvs/hello3.py
   ```

3. Show history of commits for the last 5 days in feature_branch of moduleA

   If you have a long history of commits, the tool might take a long time to run.
   If you only want to see the history for the past 5 days, you can supply that option.

   ```
   cvs-history.py -n 5 -b feature_branch moduleA
   ```

#### Complete syntax

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
