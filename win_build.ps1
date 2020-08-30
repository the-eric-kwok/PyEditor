pyinstaller -w -F --icon='Icon.ico' --add-binary 'img/about.gif;img' `
--add-binary 'img/copy.gif;img' --add-binary 'img/cut.gif;img' `
--add-binary 'img/editor.ico;img' --add-binary 'img/find_text.gif;img' `
--add-binary 'img/new_file.gif;img' --add-binary 'img/open_file.gif;img' `
--add-binary 'img/paste.gif;img' --add-binary 'img/redo.gif;img' `
--add-binary 'img/save.gif;img' --add-binary 'img/undo.gif;img' PyEditor.pyw
pause