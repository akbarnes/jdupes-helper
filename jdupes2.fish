#!/usr/bin/fish
set del_dir "/media/art/Images Backup/Clones/Cube/Hard Drive"
set keep_dir "/data/Shared/Backups/Clones/Cube/Hard Drive"
set results_file "dupes/cube_hd_dupes.txt"

jdupes -r $keep_dir $del_dir >$results_file
echo "Delete: $del_dir"
echo "Keep: $keep_dir"
echo "Results: $results_file"

