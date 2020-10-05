import argparse, os.path, logging, toml, json

logging.basicConfig(level=logging.DEBUG)

parser = argparse.ArgumentParser()
parser.add_argument('duplicates')
parser.add_argument('-m','--master', default='C:\\')
parser.add_argument('-s','--slave', default='H:\\')
parser.add_argument('-b','--batch')
parser.add_argument('-p','--platform', default='posix')
args = parser.parse_args()

# master_path = args.master.replace('\\','\\\\')
logging.debug('master_path = ' + args.master)
logging.debug('slave_path = ' + args.slave)

comment_char = '#'
del_cmd = 'trash-put'
script_ext = '.sh'

if args.platform == 'windows':
    comment_char = 'REM'
    del_cmd = 'del'    
    script_ext = '.bat'

with open(args.duplicates) as f:
    dups_str = f.read()

dup_set_strs = dups_str.split('\n\n')


# for dset in dup_set_strs:
#     logging.debug('dset = {}'.format(dset))
dup_sets = [x.split('\n') for x in dup_set_strs]

# # import ipdb; ipdb.set_trace()

exclusions = '.git', 'Arduino', 'Processing', 'Repos', 'repos', 'Zotero', '$', 'MobileSync'
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

            for ex in exclusions:
                if ex in dpath:
                    has_slave = False
                    print("Contains {}, Skipping {}".format(ex, dpath))
            

    if has_master and has_slave:
        matching_sets.append(dset)
        # logging.debug('Duplicate set includes master & slave:')
        # logging.debug('dest = {}'.format(dset))
    
    # logging.debug('')
        


if args.batch is None:
    dups_base, dups_ext = os.path.splitext(args.duplicates)
    batch_file = '{}_del{}'.format(dups_base, script_ext)
    # info_file = '{}.json'.format(dups_base)
else:
    batch_file = args.batch

logging.debug('batch_file = ' + batch_file)

info = {}
info['master_path'] = args.master
info['slave_path'] = args.slave
info['duplicates'] = matching_sets

with open('{}.json'.format(dups_base), 'w') as f:
    json.dump(info, f, indent=4)

# with open('{}.toml'.format(dups_base), 'w') as f:
#     toml.dump(matching_sets, f)

with open(batch_file, 'w') as f:
    print('{} Master path: {}'.format(comment_char, args.master), file=f)
    print('{} Slave path: {}\n'.format(comment_char, args.slave), file=f)

    for match_set in matching_sets:
        for dpath in match_set:
            if dpath.startswith(args.slave):
                print('echo "{} {}"'.format(del_cmd, dpath), file=f)
                print('{} "{}"'.format(del_cmd, dpath), file=f)
            elif dpath.startswith(args.master):
                print('{} Master: {}'.format(comment_char, dpath), file=f)
            else:
                print('{} Other: {}'.format(comment_char, dpath), file=f)

        print('', file=f)
