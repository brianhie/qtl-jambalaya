import argparse
import pickle

def load_qtls(qtl_fname, **kwargs):
    qtls = {}
    with open(qtl_fname, 'r') as qtl_file:
        for pos, line in enumerate(qtl_file):
            if kwargs['skip_header'] and pos == 0:
                continue
            
            fields = line.rstrip().split()
    
            # Filter on possible inputs.
            if kwargs['val_col'] != None and kwargs['val_type'] != None:
                if kwargs['eq'] != None and \
                   kwargs['val_type'](fields[kwargs['val_col']]) != kwargs['eq']:
                    continue
                if kwargs['lt'] != None and \
                   kwargs['val_type'](fields[kwargs['val_col']]) >= kwargs['lt']:
                    continue
                if kwargs['gt'] != None and \
                   kwargs['val_type'](fields[kwargs['val_col']]) <= kwargs['gt']:
                    continue
                
            if kwargs['chr_col'] == kwargs['pos_col']:
                chrom, pos = (fields[kwargs['chr_col']]
                              .split(kwargs['chr_pos_delim'])[:2])
            else:
                chrom = fields[kwargs['chr_col']]
                pos = fields[kwargs['pos_col']]

            if chrom.startswith('chr'):
                chrom = chrom[len('chr'):]
            try:
                pos = int(float(pos))
            except ValueError:
                continue
            
            qtls[(chrom, pos)] = kwargs['val_type'](fields[kwargs['val_col']])
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
    parser.add_argument('--val-type', default=None)
    parser.add_argument('--eq', default=None)
    parser.add_argument('--lt', default=None)
    parser.add_argument('--gt', default=None)
    parser.add_argument('--skip-header', type=bool, default=False)
    return parser.parse_args()

if __name__ == '__main__':
    args = parse()
    qtls = load_qtls(args.in_fname, **args)
    with open(args.out_fname, 'wb') as out_file:
        pickle.dump(qtls, out_file,
                    protocol=pickle.HIGHEST_PROTOCOL)
