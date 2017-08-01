import argparse

def load_qtls(qtl_fname, **kwargs):
    qtls = {}
    with open(qtl_fname, 'r') as qtl_file:
        for pos, line in enumerate(qtl_file):
            if skip_header and pos == 0:
                continue
            
            fields = line.rstrip().split()
    
            # Filter on possible inputs.
            if kwargs['val_col'] != None and kwargs['val_type'] != None:
                if eq != None and \
                   kwargs['val_type'](fields[kwargs['val_col']]) != eq:
                    continue
                if lt != None and \
                   kwargs['val_type'](fields[kwargs['val_col']]) >= lt:
                    continue
                if gt != None and \
                   kwargs['val_type'](fields[kwargs['val_col']]) <= gt:
                    continue
                
            if kwargs['chr_col'] == kwargs['pos_col']:
                chrom, pos = fields[kwargs['chr_col']].split(chr_pos_delim)[:2]
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

def load_qtls(qtl_fname, kwargs['chr_col']=0, kwargs['pos_col']=1, chr_pos_delim='.'
              kwargs['val_col']=None, kwargs['val_type']=None, eq=None, lt=None, gt=None,
              skip_header=False):
    pass
if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Turn raw QTL file (often in a BED-like format)' +
        ' into a Python object.'
    )
    parser.add_argument('in_fname', type=str)
    parser.add_argument('out_fname', type=str)
    parser.add_argument('--chr-col', type=int, default=0)
    parser.add_argument('--pos-col', type=int, default=0)
    parser.add_argument('--chr-pos-delim', type=str, default='.')
    parser.add_argument('--val-col', type=int, default=None)
    parser.add_argument('--val-type', default=None)
    parser.add_argument('--eq', default=None)
    parser.add_argument('--lt', default=None)
    parser.add_argument('--gt', default=None)
    parser.add_argument('--skip-header', type=bool, default=False)
    args = parser.parse_args()

    qtls = load_qtls(args.in_fname, **args)
