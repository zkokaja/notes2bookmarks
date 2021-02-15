#!/usr/bin/env bash

set -e

# 0. Backup existing exported notes, then remove them.
if [ -d notes ]
then
    tar cjf "notes-$(date +%Y%m%d_%s).bzip2.tar" notes
    rm -r notes
fi

# 1. Export notes
# NOTE - this does not handle rich text links in Notes. Also it will fail if
# a note has a forward slash in its title.
osascript exporter.js

# 2. Convert notes to bookmarks
python create-bookmarks.py \
    --titles safari-bookmarks.html notes-bookmarks.html \
    --json-out bookmarks.json \
    --folder-per-note \
    notes bookmarks.html


# 3. Convert notes to markdown
# find notes -iname "*.html" -type f -exec \
#     sh -c 'pandoc \
#         -f html-native_divs-native_spans \
#         -t markdown-escaped_line_breaks \
#         -o "${0%.html}.md" \
#         "$0"' {} \;

# find . -name \*.html -type f | \
# (while read file; do
# iconv -f UTF-16 -t UTF-8 "$file" > "${file%.xxx}-utf8.html";
# done);
