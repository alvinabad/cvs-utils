#!/bin/bash

cvs -nq update -Pd 2>/dev/null
cvs -q status | grep Status: | grep -v 'Up-to-date'
