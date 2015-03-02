#!/bin/bash

cvs -q log -h -l | grep -P '\.0\.' | head -1 | awk -F: '{print $1}'
