import argparse, os.path, logging, toml, json

logging.basicConfig(level=logging.DEBUG)

parser = argparse.ArgumentParser()
parser.add_argument('duplicates')
parser.add_argument('-m','--master', default='C:\\')
parser.add_argument('-s','--slave', default='H:\\')
parser.add_argument('-b','--batch')
args = parser.parse_args()

# master_path = args.master.replace('\\','\\\\')
logging.debug('master_path = ' + args.master)
logging.debug('slave_path = ' + args.slave)

with open(args.duplicates) as f:
    dups_str = f.read()

dup_set_strs = dups_str.split('\n\n')


# for dset in dup_set_strs:
#     logging.debug('dset = {}'.format(dset))
dup_sets = [x.split('\n') for x in dup_set_strs]

# # import ipdb; ipdb.set_trace()

matching_sets = []

for dset in dup_sets:
    has_master = False
    has_slave = False

    for dpath in dset:
        # logging.debug('dpath = ' + dpath)
        if dpath.startswith(args.master):
            has_master = True

        if dpath.startswith(args.slave):
            has_slave = True

    if has_master and args.slave:
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
info['slave_path'] = args.slave
info['pattern'] = args.pattern
info['duplicates'] = matching_sets

with open('{}.json'.format(dups_base), 'w') as f:
    json.dump(info, f, indent=4)

# with open('{}.toml'.format(dups_base), 'w') as f:
#     toml.dump(matching_sets, f)

with open(batch_file, 'w') as f:
    print('REM Master path: {}'.format(args.master), file=f)
    print('REM Slave path: {}\n'.format(args.slave), file=f)

    for match_set in matching_sets:
        for dpath in match_set:
            if dpath.startswith(args.slave):
                print('del "{}"'.format(dpath), file=f)
            elif dpath.startswith(args.master):
                print('REM Master: {}'.format(dpath), file=f)
            else:
                print('REM {}'.format(dpath), file=f)

        print('', file=f)