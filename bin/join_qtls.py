import json
import pickle
import sys

if __name__ == '__main__':
    with open(sys.argv[1], 'r') as conf_file:
        namespaces = json.loads(conf_file.read())

    qtl_to_p = {}
    print('Joining...')
    for i, namespace in enumerate(namespaces):
        print(namespace)
        # Load map from QTL to p-value.
        with open('target/parsed/{}.pickle'
                  .format(namespace), 'rb') as qtl_file:
            qtls = pickle.load(qtl_file)
        # Iterate through QTLs, adding to master list.
        for qtl in qtls:
            if not qtl in qtl_to_p:
                qtl_to_p[qtl] = [ float('nan') ] * i
            qtl_to_p[qtl].append(qtls[qtl])
        # Append NaN to QTLs in master list but not in the loaded QTL
        # file.
        for qtl in (set(qtl_to_p.keys()) - set(qtls.keys())):
            qtl_to_p[qtl].append(float('nan'))

    join_name = sys.argv[1].split('/')[-1]
    if join_name.endswith('.txt'):
        join_name = join_name[:-len('.txt')]
    if join_name.endswith('.json'):
        join_name = join_name[:-len('.json')]

    with open('target/joined/{}.pickle'
              .format(join_name), 'wb') as join_file:
        pickle.dump(qtl_to_p, join_file, protocol=pickle.HIGHEST_PROTOCOL)
