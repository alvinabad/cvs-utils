#!/bin/bash

usage() {
    cat <<EOF
Usage:
    `basename $0` module
EOF
    exit 1
}

[ $# -ne 0 ] || usage

cvs -q rlog -h -l $1 | grep -P '\.0\.' | awk -F: '{print $1}' | sort | uniq
