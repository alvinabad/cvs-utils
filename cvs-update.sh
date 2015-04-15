#!/bin/bash

usage() {
    cat <<EOF
CVS Update
Usage:
    `basename $0` [-y]

options:
    -y    skip dry-run
EOF
    exit 1
}

if [ "$1" = "-y" ]; then
    cvs -q update -Pd 2>/dev/null
else
    cvs -nq update -Pd 2>/dev/null
    echo "Dry run only. Add -y option to perform update." 
fi
