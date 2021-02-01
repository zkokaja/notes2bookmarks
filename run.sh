#!/usr/bin/env bash

# 1. Export notes
# TODO - make heirarchical
# NOTE - this does not handle rich text links in Notes
# rm -rf notes
# mkdir -p notes
# osascript export-notes.scpt

# 2. Convert notes to bookmarks
python create-bookmarks.py \
    --titles safari-bookmarks.html notes-bookmarks.html \
    --json-out bookmarks.json \
    --folder-per-note \
    notes bookmarks.html


# find notes -iname "*sauces*.html" -type f -exec \
#     sh -c 'pandoc \
#         -f html-native_divs-native_spans \
#         -t markdown-escaped_line_breaks \
#         -o "${0%.html}.md" \
#         "$0"' {} \;

# find . -name \*.html -type f | \
# (while read file; do
# iconv -f UTF-16 -t UTF-8 "$file" > "${file%.xxx}-utf8.html";
# done);
