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

from collections import OrderedDict
from datetime import datetime
from pathlib import Path
from pybtex.database import parse_file

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
template = '''\
Content-Type: text/x-zim-wiki
Wiki-Format: zim 0.6
Creation-Date: {isodate}

====== {bibkey} ======
Created {subdate}

@{bibtype}
'''

# Read and parse bibtex file
bibdata = parse_file(bibfile)

# Loop over entries in bibtex file
for bibkey, entry in bibdata.entries.items():

    # Skip references without author
    if bibkey.startswith('noauthor'):
        continue

    # Print bibkey to terminal
    print(bibkey)

    # Define subfolder using the bibkey's first letter
    subfolder = bibkey.upper()[0]

    # Define path for subfolder
    subpath = root / subfolder

    # Create subfolder (A, B, C, etc...)
    Path.mkdir(subpath, exist_ok=True)


    # Define filename using the bibkey
    filename = f'{bibkey}.txt'

    # Define full file path
    filepath = subpath / filename

    # Create file using bibkey as name
    zimfile = open(filepath, 'w')


    # Get entry type
    bibtype = entry.type

    # Get authors list (key + ordered dictionary)
    bibpersons = entry.persons

    # Get entry fields (ordered dictionary)
    bibfields = OrderedDict(entry.fields)

    # Get full entry in BibTeX format
    bibtex = entry.to_string('bibtex')


    # Get datetime now
    now = datetime.now()
    isodate = now.astimezone().replace(microsecond=0).isoformat()
    subdate = now.strftime('%A %d %B %Y')

    # Save main page content
    page = template.format(bibkey=bibkey,
                           bibtype=bibtype,
                           isodate=isodate,
                           subdate=subdate)

    # Loop for bypassing the author key
    person_dict = {}
    for person_key, persons in bibpersons.items():
        person_list = [str(person) for person in persons]
        person_string = '; '.join(person_list)
        person_dict.update({person_key: person_string})

    # Add authors to the fields dictionary at the second position
    bibfields.update(person_dict)
    if 'editor' in person_dict.keys():
        bibfields.move_to_end('editor', last=False)
    if 'author' in person_dict.keys():
        bibfields.move_to_end('author', last=False)
    bibfields.move_to_end('title', last=False)


    # Print fields to page
    for field, value in bibfields.items():
        page = page + f'\n**{field}:** {value}'

    # Add raw BibTeX at the end
    # page = page + f"\n\n'''\n{bibtex}'''"

    # Write page to file (returns number of characters written)
    characters = zimfile.write(page)


    # Close file
    zimfile.close()

