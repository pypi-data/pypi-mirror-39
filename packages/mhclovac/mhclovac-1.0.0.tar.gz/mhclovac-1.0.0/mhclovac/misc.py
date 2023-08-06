import io
import base64
import pandas as pd
import h5py
import os
import numpy as np


def fasta_reader(fasta_path):
    with open(fasta_path, 'r') as f:
        seq_name = ''
        sequence = ''
        write_flag = 0
        for line in f:
            if line.startswith('>'):
                if write_flag:
                    write_flag = 0
                    yield(seq_name, sequence)
                seq_name = line.split()[0][1:]
                sequence = ''
            else:
                sequence += line.strip()
                write_flag = 1
        yield (seq_name, sequence)


def load_schema(h5handle, skey):
    blob = h5handle[skey].attrs['schema']
    df = pd.read_csv(io.BytesIO(base64.b64decode(blob)))
    return df


def load_schema_keys(h5handle):
    keys = h5handle.attrs['schema_keys']
    return keys.split(',')


def load_hla_profile(h5handle, skey, hla):
    p = h5handle[skey + '/' + hla + '/profile'][:]
    return p


def load_hla_params(h5handle, skey, hla):
    t = h5handle[skey+'/'+hla+'/truth_param'][:]
    n = h5handle[skey+'/'+hla+'/null_param'][:]
    return t, n


def load_profile_length(h5handle):
    p = h5handle['profile_length'][0]
    return p


def load_dist_scale(h5handle):
    d = h5handle['dist_scale'][0]
    return d


def print_header(args, output):
    if args.reference_data in ['human',]:
        ref_dir = os.path.dirname(__file__)
        ref_file_path = '/'.join([ref_dir,
                                  'reference_data',
                                  args.reference_data+'.hdf5'])
        h5file = h5py.File(ref_file_path, 'r')
    else:
        h5file = h5py.File(args.reference_data, 'r')
    schemas = args.schema_keys or load_schema_keys(h5file)
    if args.score_breakdown:
        base = '\t'.join(['seq_name','hla','peptide'])
        scols = '\t'.join([x for x in schemas])  # Unpack schemas
        line = '\t'.join([base, scols, 'total_score'])
    else:
        line = '\t'.join(['seq_name',
                          'hla',
                          'peptide',
                          'total_score'])
    output.write(line + '\n')
    h5file.close()
    return


def encode_schema(fpath):
    """
    Convert file to base64 bytestring. Used for storing in hdf5 files.
    :param fpath: File path
    :return: base64 bytestring
    """
    with open(fpath, 'r') as f:
        bstr = b''
        for c in f.read():
            bstr += c.encode('ascii')
        return base64.b64encode(bstr)


def norm_array(array, x, y):
    """
    Normalize array to arbitrary range [x, y]
    :param array: list, array
    :param x: bound 1
    :param y: bound 2
    :return: normalized numpy array
    """
    array = np.array(array)
    array = (array-min(array))/(max(array)-min(array))
    return array*(np.abs(x-y))+min([x,y])
