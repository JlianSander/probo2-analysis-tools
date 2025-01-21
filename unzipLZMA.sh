#!/bin/bash
#set -x
for file in "$1"/*.lzma; do
    unlzma $file
done