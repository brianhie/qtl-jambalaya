import gzip
import math
import pickle
import sys

EQTL_TYPE = 'exon'
MISSING_PCT = 0

if __name__ == '__main__':
    with open(sys.argv[1], 'rb') as p_file:
        qtl_to_p = pickle.load(p_file)

    eqtls = set()
    for pos, line in enumerate(gzip.open('data/raw/eQTLs_{}.txt.gz'
                                         .format(EQTL_TYPE))):
        if pos == 0:
            continue
        fields = line.decode('utf-8').rstrip().split()
        eqtls.add((fields[4].replace('chr', ''), int(float(fields[6]))))

    # Remove all QTLs that are not eQTLs or that have missing data beyond
    # the `MISSING_PCT'.
    to_delete = []
    for qtl in qtl_to_p:
        if not qtl in eqtls:
            to_delete.append(qtl)
            continue
        n_nan = len([ x for x in qtl_to_p[qtl] if math.isnan(x)] )
        if n_nan / len(qtl_to_p[qtl]) > MISSING_PCT:
            to_delete.append(qtl)
    for qtl in to_delete:
        del qtl_to_p[qtl]

    name = 'eqtls_' + sys.argv[1].split('/')[-1]
    with open('target/joined/{}'.format(name), 'wb') as f:
        pickle.dump(qtl_to_p, f, protocol=pickle.HIGHEST_PROTOCOL)
