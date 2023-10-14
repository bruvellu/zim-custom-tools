#!/usr/bin/env python

'''Prepend timestamp to Zim file names.

Zim Custom Tool by Bruno C. Vellutini
https://brunovellutini.com

Install:

1. Copy this script somewhere
2. Open Zim > Tools > Custom Tools
3. Add new custom tool
4. Fill in details
  a. Name: Prepend Timestamp
  b. Description: Prepend timestamp to Zim filename
  c. Command: ~/somewhere/prepend_timestamp.py %s

Note: "%s" stands for the real page source file.

Usage:

1. Open a page
2. Go to Tools > Prepend Timestamp
3. A timestamp like YYYY-MM-DD will be prepended to the file name

Note: The page title heading remains unchanged.
Note: The page position in the index will change.
'''

import os
import sys
from datetime import datetime

def rename_zim_file(zim_file):
    # Get the creation date from the Zim file
    with open(zim_file, 'r') as f:
        for line in f:
            if line.startswith('Creation-Date:'):
                creation_date_str = line.split(':')[1].strip()
                creation_date = datetime.fromisoformat(creation_date_str)
                break

    # Rename the Zim file with the timestamp in the format YYYY-MM-DD
    new_file_name = creation_date.strftime('%Y-%m-%d') + '_' + os.path.basename(zim_file)
    os.rename(zim_file, os.path.join(os.path.dirname(zim_file), new_file_name))

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python rename_zim_file.py <zim_file>')
        sys.exit(1)

    zim_file = sys.argv[1]
    rename_zim_file(zim_file)
