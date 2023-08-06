#!/usr/bin/env python
"""Entry point for mhclovac-build"""

from mhclovac import get_profile
from mhclovac.argument_parser import parse_build_args
from mhclovac.misc import encode_schema
import pandas as pd
import numpy as np
from scipy.stats import norm, skewnorm
import sys
import h5py


def worker(argv):
    args = parse_build_args(argv)
    for k, v in vars(args).items():
        sys.stdout.write('{}: {}\n'.format(k, v))

    data = pd.read_table(args.input_data)
    data = data[data['species'] == args.species]
    rand_idx = np.random.randint(0, len(data)-1, args.null_set_size)
    null_set = data.iloc[rand_idx]

    f = h5py.File(args.output, 'a')

    schemas_dict = {}
    for item in args.schemas:
        k, v = item.split(':')
        schemas_dict[k] = v

    prof_len_set = f.create_dataset('profile_length', (1,), dtype='i')
    prof_len_set[...] = int(args.profile_length)
    scale_set = f.create_dataset('dist_scale', (1,), dtype='f')
    scale_set[...] = float(args.dist_scale)
    f.attrs['schema_keys'] = ','.join([k for k in schemas_dict])

    for schema in schemas_dict:
        # Create group for schema, eg. hydrophobicity etc.
        f.create_group(schema)
        # Add base64 encoded schema to the schema group
        f[schema].attrs['schema'] = encode_schema(schemas_dict[schema])

        for hla in data.mhc.unique():
            sys.stdout.write('Processing {} for schema {}\n'.
                             format(hla, schema))
            tmp_df = data[(data['mhc'] == hla) &
                          (data['meas'] <= args.ic50_threshold)]
            if len(tmp_df) < 10:
                sys.stdout.write('Number of ligands for {} is {}. Skipping.\n'
                                 .format(hla, len(tmp_df)))
                continue

            # Now create group for schema, only if more than 10 true ligands
            f.create_group(schema + '/' + hla)

            # Get HLA profile and store it in HDF5 file
            ps = tmp_df['sequence'].apply(
                lambda x: get_profile(x, pd.read_csv(schemas_dict[schema]),
                                      scale=args.dist_scale,
                                      normalize=True,
                                      vector_length=args.profile_length))
            p = np.mean(ps, axis=0)
            p_set = f.create_dataset(schema + '/' + hla + '/profile',
                                     (args.profile_length,),
                                     dtype='f')
            p_set[...] = p

            # If --no_fit, than skip this following step
            if not args.no_fit:
                null_ps = null_set['sequence'].apply(
                    lambda x: get_profile(x, pd.read_csv(schemas_dict[schema]),
                                          scale=args.dist_scale,
                                          normalize=True,
                                          vector_length=args.profile_length))

                ts = [np.corrcoef(p,k)[0][1] for k in ps]
                ns = [np.corrcoef(p,k)[0][1] for k in null_ps]

                if args.fit_dist == 'norm':
                    truth_param = norm.fit(ts)
                    null_param = norm.fit(ns)
                elif args.fit_dist == 'skewnorm':
                    truth_param = skewnorm.fit(ts)[1:]
                    null_param = skewnorm.fit(ns)[1:]
                else:
                    raise KeyError('Unrecognized value for --fit_dist {}'
                                   .format(args.fit_dist))

                t_set = f.create_dataset(schema+'/'+hla+'/truth_param',
                                         (2,),
                                         dtype='f')
                n_set = f.create_dataset(schema+'/'+hla+'/null_param',
                                         (2,),
                                         dtype='f')
                t_set[...] = truth_param
                n_set[...] = null_param

    f.close()
    return


def main():
    # Entry point for mhclovac-build
    sys.exit(worker(sys.argv[1:]))
