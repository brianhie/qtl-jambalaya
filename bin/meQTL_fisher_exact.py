import sys
from scipy.stats import fisher_exact

if __name__ == '__main__':
    for line in open(sys.argv[1], 'r'):
        fields = line.rstrip().split()

        ref_methyl = int(float(fields[4]))
        alt_methyl = int(float(fields[5]))
        ref_unmeth = int(float(fields[6]))
        alt_unmeth = int(float(fields[7]))

        p = fisher_exact([
            [ ref_methyl, alt_methyl ],
            [ ref_unmeth, alt_unmeth ]
        ])[1]
        fields.append(str(p))

        print('\t'.join(fields))
