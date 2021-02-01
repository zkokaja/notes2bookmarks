on writeToFile(filename, filecontents)
	set the output to open for access file filename with write permission
	set eof of the output to 0
	write filecontents to the output starting at eof
	close access the output
end writeToFile

tell application "Notes"
	activate
	#display dialog "This is the export utility for Notes.app.\n\n" & "Exactly " & (count of notes) & " notes are stored in the application. " & "Each one of them will be exported as a simple HTML file stored in a folder of your choice." with title "Notes Export" buttons {"Cancel", "Proceed"} cancel button "Cancel" default button "Proceed"
	set exportFolder to choose folder
        repeat with f in folders
                set folderName to the name of f
                #set folderNameQuoted to POSIX path of folderName
		#log "mkdir -p notes/" & folderNameQuoted
		do shell script "mkdir -p 'notes/" & folderName & "'"

		repeat with nt in f's notes
			set noteName to name of nt
			set noteBody to body of nt
                        set noteNameQuoted to POSIX path of noteName
			set filename to ((exportFolder as string) & folderName & ":" & noteName & ".html")
                        #log filename
			my writeToFile(filename, noteBody as text)
		end repeat
	end repeat
	#display alert "Notes Export" message "All notes were exported successfully." as informational
end tell
