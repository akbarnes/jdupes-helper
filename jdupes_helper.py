import argparse, os.path, logging

logging.basicConfig(level=logging.DEBUG)

parser = argparse.ArgumentParser()
parser.add_argument('duplicates')
parser.add_argument('-m','--master', default='C:\\')
parser.add_argument('-b','--batch')
args = parser.parse_args()

# master_path = args.master.replace('\\','\\\\')
master_path = args.master
logging.debug('master_path = ' + master_path)

with open(args.duplicates) as f:
    dups_str = f.read()

dup_set_strs = dups_str.split('\n\n')


for dset in dup_set_strs:
    logging.debug('dset = {}'.format(dset))
# dup_sets = [x.split('\r\n') for x in dup_set_strs]

# # import ipdb; ipdb.set_trace()

# matching_sets = []

# for dset in dup_sets:
#     for dpath in dset:
#         logging.debug('dpath = ' + dpath)
#         if dpath.startswith(master_path):
#             matching_sets.append(dset)
#             logging.debug('Duplicate set includes master:')
#             logging.debug('dest = {}'.format(dset))
#             print('')
#             break
    
#     # logging.debug('')
        


# if args.batch is None:
#     dups_base, dups_ext = os.path.splitext(args.duplicates)
#     batch_file = '{}_del.bat'.format(dups_base)
# else:
#     batch_file = args.batch

# logging.debug('batch_file = ' + batch_file)

# with open(batch_file, 'w') as f:
#     for match_set in matching_sets:
#         for dpath in match_set:
#             if dpath.startswith(master_path):
#                 print('# {}'.format(dpath))
#             else:    
#                 print('del {}'.format(dpath))

#         print('')