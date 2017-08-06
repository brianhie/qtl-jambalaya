import json
from math import log
import numpy as np
import sys
import pickle

from tsne import tsne

P_VAL_CUTOFF = 0.0001

if __name__ == '__main__':
    # Open a dictionary from QTL locations to a list of p-values
    # corresponding to different phenotypes.
    with open(sys.argv[1], 'rb') as p_file:
        qtl_to_p = pickle.load(p_file)

    # Get the namespaces that correspond to the joined p-values.
    conf_name = sys.argv[1].split('/')[-1].split('.')[0]
    if conf_name.startswith('eqtls_'):
        conf_name = conf_name[len('eqtls_'):]
    with open('conf/{}.json'.format(conf_name), 'r') as conf_file:
        joined_namespaces = json.loads(conf_file.read())

    # Initialize the matrix of the number of QTLs by the number of QTL
    # phenotypes.
    n_qtl_types = len(next(iter(qtl_to_p.values())))
    X = np.zeros((
        len(qtl_to_p), n_qtl_types
    ))
    for row, qtl in enumerate(sorted(qtl_to_p.keys())):
        # Fill in the matrix.
        X[row, :] = qtl_to_p[qtl]

        # Label a SNP as a QTL if the p-value is less than some arbitrary
        # value.
        labels = []
        for pos, q in enumerate(qtl_to_p[qtl]):
            if q < P_VAL_CUTOFF:
                labels.append(joined_namespaces[pos])
                
        # Print to stdout, which can be used as metadata file for the
        # visualization.
        print('> {0}:{1} {2}'.format(qtl[0], qtl[1], labels))

    exit()

    # Visualize the 3D space after doing a t-SNE dimensionality reduction.
    Y = tsne(X, no_dims=3, initial_dims=n_qtl_types)

    # Save the t-SNE projecte coordinates to a file.
    name = sys.argv[1].split('/')[-1]
    if name.endswith('.pickle'):
        name = name[:-len('.pickle')]
    np.savetxt('target/visualize/{}.txt'.format(name), Y, delimiter='\t')
