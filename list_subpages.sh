#!/bin/bash

# Zim Custom Tool by Bruno C. Vellutini
# https://brunovellutini.com

# Generate list of sub-pages with links

# Requirements:
#
# - Bash

# Install:
#
# 1. Copy this script somewhere
# 2. Open Zim > Tools > Custom Tools
# 3. Add new custom tool
# 4. Fill in details
#   a. Name: List Sub-Pages
#   b. Description: Create list with links to sub-pages 
#   c. Command: ~/somewhere/zim_list_subpages.sh %d
# 5. Check "Output should replace current selection"
# 6. Go to Preferences > Key bindings and set CTRL+ALT+L to
#    <Actions>/custom_tools/list sub-pages-usercreated
#
# Note: "%d" stands for the attachment directory of the current page.

# Usage:
#
# 1. Open a page that has sub-pages
# 2. Put your cursor where you want your list
# 3. Go to Tools > List Sub-Pages (or press shortcut)
# 4. An unformatted list will appear
# 5. Reload the page to render the links (CTRL+R)
#
# Note: If there are no sub-pages, nothing will be printed.

# TODO:
#
# - Option to use numbered lists
# - Recursive sub-pages with indentation
# - Option to reverse sort and sort by date

# Get attachment directory of current page
DIR=$1

# Get sub-pages in directory
for i in `ls ${DIR}/*.txt`; do
  # Strip extension out of page name
  subpage=`basename ${i} .txt`
  # Replace underscores with spaces
  subpage=${subpage//_/ }
  # Generate list item with link to sub-page
  echo "* [[+${subpage}|${subpage}]]"
done

