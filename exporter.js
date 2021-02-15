let app = Application.currentApplication();
app.includeStandardAdditions = true;

let notesApp = Application('Notes');
notesApp.includeStandardAdditions = true;

main()

function main() {
    let rootFolder = notesApp.defaultAccount.name();

    let pwd = app.doShellScript('pwd');
    let exportDir = `${pwd}/notes`;
    app.doShellScript('mkdir -p notes');

    let folders = notesApp.folders;
    for (var i=0; i<folders.length; i++) {
        if (folders[i].container().name() === rootFolder) {
            handle(folders[i], exportDir);
        }
    }
}

function handle(item, from) {

    let itemName = item.name();
    //console.log(`mkdir -p ${from}/${itemName}`);
    app.doShellScript(`mkdir -p '${from}/${itemName}'`);

    let itemFolders = item.folders;
    for (var i=0; i<itemFolders.length; i++) {
        let folderName = itemFolders[i].name();
        handle(itemFolders[i], `${from}/${itemName}`)  // NOTE - recursion
        //console.log('\t' + itemFolders[i].name());
    }

    let itemNotes = item.notes;
    for (var i=0; i<itemNotes.length; i++) {
        let noteName = itemNotes[i].name();
        let filepath = `${from}/${itemName}/${noteName}.html`;
        //console.log('\t' + filepath);
        writeNote(itemNotes[i], filepath);
    }
}

function writeNote(note, filepath) {
    let text = note.body();  // Use .plaintext() for txt instead of html

    let file = app.openForAccess(Path(filepath), {writePermission: true});
    app.write(text, {to: file});
    app.closeAccess(file);

    // TODO - use Finder to set modification date of file
}
