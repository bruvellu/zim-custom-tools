#!/bin/python

# Zim Custom Tool by Bruno C. Vellutini
# https://brunovellutini.com

# Import bibtex entries as zimwiki pages

# Requirements:
#
# - Python
# - Pybtex https://pybtex.org/

# Install:
#
# 1. Copy this script somewhere
# 2. Open Zim > Tools > Custom Tools
# 3. Add new custom tool
# 4. Fill in details
#   a. Name: Update References
#   b. Description: Import bibtex entries as Zim pages
#   c. Command: python /your/home/bin/import_bibtex.py --bibfile /your/home/references.bib --outdir %d
#
# Note: "%d" stands for the attachment directory of the current page.

# Usage:
#
# 1. Define a base page to store the references as sub-pages
# 2. Go to Tools > Update References
# 3. BibTeX entries will be converted to sub-pages
#
# Note: Zim may become unresponsive for a couple of minutes if the bibfile is large.

# TODO:
#
# - Handle entry update and deletion

# biber --tool -V paperpile.bib > biberrors.txt

from datetime import datetime
from pybtex.database import parse_file
from pathlib import Path

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-o', '--outdir', help='output directory', required=True)
parser.add_argument('-b', '--bibfile', help='bib file', required=True)
args = parser.parse_args()

# Bibtex file
bibfile = args.bibfile

# Folder root
root = Path(args.outdir)
Path.mkdir(root, exist_ok=True)
print(f'Converting "{bibfile}" to "{root}" directory...')

# Page template
template = '''Content-Type: text/x-zim-wiki
Wiki-Format: zim 0.6
Creation-Date: {isodate}

====== {bibkey} ======
Created {subdate}

{entry}
'''

# Read and parse bibtex file
bibdata = parse_file(bibfile)

# Loop over entries in bibtex file
for bibkey, values in bibdata.entries.items():

    # Skip references without author
    if bibkey.startswith('noauthor'):
        continue

    # Define page folder using first author letter
    folder = root / bibkey[0]

    # Define filename using the bibkey
    filename = f'{bibkey}.txt'

    # Define filepath
    filepath = folder / filename

    # Create directory
    Path.mkdir(folder, exist_ok=True)

    # Create file using bibkey as name
    zimfile = open(filepath, 'w')

    # Save entry values in bibtex format
    entry = values.to_string('bibtex')

    # Get datetime now
    now = datetime.now()
    isodate = now.astimezone().replace(microsecond=0).isoformat()
    subdate = now.strftime('%A %d %B %Y')

    # Save final content of the page
    page = template.format(bibkey=bibkey, entry=entry, isodate=isodate,
            subdate=subdate)

    # Write page to file (returns number of characters written)
    characters = zimfile.write(page)

    # Close file
    zimfile.close()

    # Print bibkey to terminal
    print(bibkey)

