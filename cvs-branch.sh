#!/bin/bash

cvs -q status -l | grep 'Sticky Tag:' | head -1 | awk '{print $3}'
