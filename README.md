# notes2bookmarks
Sync you Note links with your browser bookmarks.

## Description

If you save links in your notes, wiki, or a knowledge base, then you probably
don't want to maintain two separate stores of links. This tool generates a
bookmarks file (to be imported into the browser) from all the URLs it finds
in your notes. This is done in two stages:

1. Export all Apple Notes to `html` files using an AppleScript: `export-notes.scpt`.
2. Find all URLs in the files and generate one bookmarks file that follows the folder
   structure presented in the notes. In addition, it can create one bookmark folder
   per notes file for more organization.

The second step can be performed independently of Apple Notes, thus run on any
plain text files with links.

## Running

Simply run `run.sh`. It will export all notes as html to a `notes/` directory,
and then it generate `bookmarks.html` to be imported to a browser.

## Limtations

One limitation with Apple Notes export is that it does not preserve rich-text URLs,
so currently the script uses a simple regex to find `http[s]://*` type links.
It may be possible to parse the Note's database at
`~/Library/Group\ Containers/group.com.apple.notes/NoteStore.sqlite`, and retrieve
rich-text links, but it requires a bigger time investment and is prone to breaking
upon changes.

## References
The export script was written while referencing these sources:

- https://github.com/cfenollosa/NotesAppExport/blob/master/Backup%20Notes.scpt
- https://github.com/robertgaal/notes-export/blob/master/notesExport.applescript
- https://github.com/yifaneye/macos-notes-exporter/blob/master/exporter.js
- https://bear.app/faq/Import%20&%20export/Migrate%20from%20Apple%20Notes/
- https://macmost.com/export-all-of-the-notes-on-your-mac-using-a-script.html
- https://developer.apple.com/library/archive/documentation/LanguagesUtilities/Conceptual/MacAutomationScriptingGuide/index.html
