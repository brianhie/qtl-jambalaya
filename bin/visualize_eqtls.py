from math import log
import numpy as np
import sys
import pickle

from tsne import tsne

if __name__ == '__main__':
    with open(sys.argv[1], 'rb') as p_file:
        qtl_to_p = pickle.load(p_file)

    n_qtl_types = len(next(iter(qtl_to_p.values())))
    X = np.zeros((
        len(qtl_to_p), n_qtl_types
    ))
    for row, qtl in enumerate(sorted(qtl_to_p.keys())):
        X[row, :] = qtl_to_p[qtl]
#        X[row, :] = [ -log(q) if q != 0 else 308
#                      for q in qtl_to_p[qtl] ]

    Y = tsne(X, no_dims=3, initial_dims=n_qtl_types)

    name = sys.argv[1].split('/')[-1]
    if name.endswith('.pickle'):
        name = name[:-len('.pickle')]
    np.savetxt('target/visualize/{}.txt'.format(name), Y, delimiter='\t')
