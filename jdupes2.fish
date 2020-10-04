#!/usr/bin/fish
set del_dir "/media/art/Images Backup/Clones/Win10 VM on Cube/Users/Art/Pictures"
set keep_dir "/data/Shared/Backups/Clones/Cube/Users/Art/OneDrive/Pictures"
set results_file "vm_dupes.txt"

jdupes -r $keep_dir $del_dir >$results_file
