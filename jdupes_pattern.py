import argparse, os.path, logging, json

logging.basicConfig(level=logging.DEBUG)

parser = argparse.ArgumentParser()
parser.add_argument('duplicates')
parser.add_argument('-m','--master', default='C:\\')
parser.add_argument('-s','--slave', default='H:\\')
parser.add_argument('-p','--pattern', default=None)
parser.add_argument('-b','--batch')
args = parser.parse_args()

# master_path = args.master.replace('\\','\\\\')
logging.debug('master_path = ' + args.master)
logging.debug('slave_path = ' + args.slave)
logging.debug('pattern = ' + args.pattern)

with open(args.duplicates) as f:
    dups_str = f.read()

dup_set_strs = dups_str.split('\n\n')


# for dset in dup_set_strs:
#     logging.debug('dset = {}'.format(dset))
dup_sets = [x.split('\n') for x in dup_set_strs]

# # import ipdb; ipdb.set_trace()

matching_sets = []

for dset in dup_sets:
    master_paths = set()
    pattern_paths = set()
    master_folders = set()

    for dpath in dset:
        dp = dpath.lower()

        # logging.debug('dpath = ' + dpath)
        if dp.startswith(args.master):
            master_paths.add(dp)
            master_folders.add(os.path.splitext(dp)[0])
            # logging.debug('Adding {} to master'.format(dpath))

        if dp.startswith(args.slave) and dp.endswith(args.pattern) and (os.path.splitext(dp)[0] in master_folders):
        # if dp.startswith(args.slave) and dp.endswith(args.pattern):
            pattern_paths.add(dp)
            logging.debug('Adding {} to slave'.format(dp))


    # ensure that there is will remain a duplicate in master
    if master_paths.difference(pattern_paths) and pattern_paths:
        matching_sets.append(dset)
        # logging.debug('Duplicate set includes master & slave:')
        # logging.debug('dest = {}'.format(dset))
    
    # logging.debug('')
        


if args.batch is None:
    dups_base, dups_ext = os.path.splitext(args.duplicates)
    batch_file = '{}_del.bat'.format(dups_base)
    # info_file = '{}.json'.format(dups_base)
else:
    batch_file = args.batch

logging.debug('batch_file = ' + batch_file)

info = {}
info['master_path'] = args.master
info['slave_path'] = args.master
info['pattern'] = args.pattern
info['duplicates'] = matching_sets

with open('{}.json'.format(dups_base), 'w') as f:
    json.dump(info, f, indent=4)

# with open('{}.toml'.format(dups_base), 'w') as f:
#     toml.dump(matching_sets, f)

with open(batch_file, 'w') as f:
    print('REM Master path: {}'.format(args.master), file=f)
    print('REM Slave path: {}\n'.format(args.slave), file=f)
    print('REM Pattern: {}\n'.format(args.pattern), file=f)

    for match_set in matching_sets:
        for dpath in match_set:
            dp = dpath.lower()

            if dp.startswith(args.slave) and dp.endswith(args.pattern):
                print('del "{}"'.format(dpath), file=f)
            elif dpath.startswith(args.master):
                print('REM Master: {}'.format(dpath), file=f)
            else:
                print('REM {}'.format(dpath), file=f)

        print('', file=f)