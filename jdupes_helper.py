import argparse, os.path

parser = argparse.ArgumentParser()
parser.add_argument('duplicates')
parser.add_argument('master')
parser.add_argument('-b','--batch')
args = parser.parse_args()


with open(args.duplicates) as f:
    dups_str = f.read()

dup_set_strs = dups_str.split('\r\n\r\n')
dup_sets = [set(x.split('\r\n')) for x in dup_set_strs]

matching_sets = [x for x in dup_sets if args.master in x]

if args.batch is None:
    dups_base, dups_ext = os.path.splitex(args.duplicates)
    batch_file = '{}_del.bat'.format(dups_base)
else:
    batch_file = args.batch

master_set = set(args.master)

with open(batch_file, 'w') as f:
    for match_set in matching_sets:
        del_set = match_set.difference(master_set)

        for del_path in del_set:
            print('del {}'.format(del_path))

