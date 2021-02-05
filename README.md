`notes2bookmarks` syncs you note's links with your browser bookmarks.

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

One limitation with Apple Notes export is that it does not preserve rich-text URLs,
so currently the script uses a simple regex to find `http[s]://*` type links.
It may be possible to parse the Note's database at
`~/Library/Group\ Containers/group.com.apple.notes/NoteStore.sqlite`, and retrieve
rich-text links, but it requires a bigger time investment and is prone to breaking
upon changes.

Useful resources:

- https://github.com/cfenollosa/NotesAppExport/blob/master/Backup%20Notes.scpt
- https://github.com/robertgaal/notes-export/blob/master/notesExport.applescript
- https://bear.app/faq/Import%20&%20export/Migrate%20from%20Apple%20Notes/
- https://macmost.com/export-all-of-the-notes-on-your-mac-using-a-script.html
