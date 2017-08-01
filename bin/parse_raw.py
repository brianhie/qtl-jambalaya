import json
import sys

N_WORKERS = 5

def load_qtls(qtl_fname, chr_col=0, pos_col=1, chr_pos_delim='.'
              val_col=None, val_type=None, eq=None, lt=None, gt=None,
              skip_header=False):
    qtls = {}
    with open(qtl_fname, 'r') as qtl_file:
        for pos, line in enumerate(qtl_file):
            if skip_header and pos == 0:
                continue
            
            fields = line.rstrip().split()
    
            # Filter on possible inputs.
            if val_col != None and val_type != None:
                if eq != None and val_type(fields[val_col]) != eq:
                    continue
                if lt != None and val_type(fields[val_col]) >= lt:
                    continue
                if gt != None and val_type(fields[val_col]) <= gt:
                    continue


            if chr_col == pos_col:
                chrom, pos = fields[chr_col].split(chr_pos_delim)[:2]
            else:
                chrom = fields[chr_col]
                pos = fields[pos_col]

            if chrom.startswith('chr'):
                chrom = chrom[len('chr'):]
            try:
                pos = int(float(pos))
            except ValueError:
                continue
            
            qtls[(chrom, pos)] = val_type(fields[val_col])
    return qtls

if __name__ == '__main__':
    conf_fname = sys.argv[1]
    with open(conf_fname, 'r') as conf_file:
        conf = json.loads(conf_file.read())

    
