#!/bin/bash
echo "Updating addon submodules"
git submodule init
git submodule update
git submodule foreach git pull origin master

