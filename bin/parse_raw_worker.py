import argparse
import gzip
import pickle
from pydoc import locate
import sys

def load_qtls(qtl_fname, args):
    args.val_type = locate(args.val_type)
    args.chr_col -= 1
    args.pos_col -= 1
    args.val_col -= 1

    if qtl_fname.endswith('.gz'):
        opener = gzip.open
    else:
        opener = open
    
    qtls = {}
    with opener(qtl_fname, 'r') as qtl_file:
        for pos, line in enumerate(qtl_file):
            if qtl_fname.endswith('.gz'):
                line = line.decode('utf-8')
            
            if args.skip_header and pos == 0:
                continue
            
            fields = line.replace(';', '\t').rstrip().split()
    
            # Filter on possible inputs.
            if args.val_col != None and args.val_type != None:
                if args.eq != None and \
                   args.val_type(fields[args.val_col]) != args.eq:
                    continue
                if args.lt != None and \
                   args.val_type(fields[args.val_col]) >= args.lt:
                    continue
                if args.gt != None and \
                   args.val_type(fields[args.val_col]) <= args.gt:
                    continue
                
            if args.chr_col == args.pos_col:
                chrom, pos = (fields[args.chr_col]
                              .split(args.chr_pos_delim)[:2])
            else:
                chrom = fields[args.chr_col]
                pos = fields[args.pos_col]

            if chrom.startswith('chr'):
                chrom = chrom[len('chr'):]
            try:
                pos = int(float(pos))
            except ValueError:
                continue
            
            qtls[(chrom, pos)] = args.val_type(fields[args.val_col])
    return qtls

def parse():
    parser = argparse.ArgumentParser(
        description='Turn raw QTL file (often in a BED-like format)' +
        ' into a Python object.'
    )
    parser.add_argument('in_fname', type=str, help='Input file name.')
    parser.add_argument('out_fname', type=str, help='Output file name.')
    parser.add_argument('--chr-col', type=int, default=0)
    parser.add_argument('--pos-col', type=int, default=0)
    parser.add_argument('--chr-pos-delim', type=str, default='.')
    parser.add_argument('--val-col', type=int, default=None)
    parser.add_argument('--val-type', default='float')
    parser.add_argument('--eq', default=None)
    parser.add_argument('--lt', default=None)
    parser.add_argument('--gt', default=None)
    parser.add_argument('--skip-header', type=bool, default=False)
    return parser.parse_args()

if __name__ == '__main__':
    args = parse()
    qtls = load_qtls(args.in_fname, args)
    with open(args.out_fname, 'wb') as out_file:
        pickle.dump(qtls, out_file,
                    protocol=pickle.HIGHEST_PROTOCOL)
