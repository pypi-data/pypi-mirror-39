#!usr/bin/env python
"""Entry point for mhclovac"""

import sys
from mhclovac import *
from mhclovac.argument_parser import parse_args
import h5py
import os


def worker(sequence, seq_name, args, output):
    sequence = str(sequence).upper()
    seq_name = str(seq_name)

    if args.reference_data in ['human', 'chimpanzee', 'macaque', 'mouse']:
        ref_dir = os.path.dirname(__file__)
        ref_file_path = '/'.join([ref_dir,
                                  'reference_data',
                                  args.reference_data+'.hdf5'])
        h5file = h5py.File(ref_file_path, 'r')
    else:
        h5file = h5py.File(args.reference_data, 'r')

    schemas = args.schema_keys or load_schema_keys(h5file)

    profile_length = load_profile_length(h5file)
    dist_scale = load_dist_scale(h5file)

    schemas_dict = {x: load_schema(h5file, x) for x in schemas}
    weights_dict = {x: 1 for x in schemas}
    if args.weights:
        for element in args.weights:
            wk, wv = element.split(':')
            try:
                weights_dict[wk] = float(wv)
            except KeyError:
                raise KeyError('Unknown schema {}'.format(wk))

    for i in range(len(sequence) - args.peptide_length + 1):
        peptide_score = []
        peptide = sequence[i: i+args.peptide_length]
        for skey in schemas:

            p = load_hla_profile(h5file, skey, args.hla)
            pp = get_profile(peptide,
                             schemas_dict[skey],
                             scale=dist_scale,
                             vector_length=profile_length,
                             normalize=True)

            w = weights_dict[skey]
            if args.dynamic_weights:
                try:
                    t, n = load_hla_params(h5file, skey, args.hla)
                except KeyError:
                    raise KeyError('Truth and null distribution parameters '
                                   'not avaliable in reference data {}. '
                                   'Cannot use dynamic weights.'
                                   .format(args.reference_data))

                if args.weight_type == 'sigmoid':
                    w = sigmoid_weight(t,
                                       n,
                                       k=args.sigmoid_weight_steepness,
                                       x0=args.sigmoid_weight_threshold,
                                       std_weighted=args.std_accounted_weights)
                elif args.weight_type == 'relu':
                    w = relu_weight(t,
                                    n,
                                    std_weighted=args.std_accounted_weights)
                elif args.weight_type == 'linear':
                    w = linear_weight(t,
                                      n,
                                      std_weighted=args.std_accounted_weights)
                else:
                    raise ValueError('Unknown weight type {}'.
                                     format(args.weight_type))
            s = get_profile_score(pp, p, w)

            # If args.relu_score than return only above 0
            s = max(0, s) if args.relu_score else s
            peptide_score.append(s)

        total_score = sum(peptide_score)
        if args.score_breakdown:
            base = '\t'.join([seq_name, args.hla, peptide])
            scols = '\t'.join([str(x) for x in peptide_score])
            line = '\t'.join([base, scols, str(total_score)])
        else:
            line = '\t'.join([seq_name,
                              args.hla,
                              peptide,
                              str(total_score)])
        output.write(line + '\n')
    return


def run():
    args = parse_args(sys.argv[1:])
    output = open(args.output, 'a') if args.output else sys.stdout

    if args.print_header:
        print_header(args, output)

    if args.fasta:
        for seq_name, sequence in fasta_reader(args.fasta):
            worker(sequence, seq_name, args, output)

    elif args.sequence:
        seq_name = args.sequence_name or 'unknown'
        worker(args.sequence, seq_name, args, output)

    else:
        raise RuntimeError('Must provide sequence or fasta file')


def main():
    # Entry point for mhclovac
    sys.exit(run())
