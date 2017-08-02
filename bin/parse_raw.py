import json
import subprocess
import sys

N_WORKERS = 5

def worker(in_fname, out_fname, **kwargs):
    command = (
        'python bin/parse_raw_worker.py {} {}' +
        '--chr-col {} --pos-col {} --chr-pos-delim {} ' +
        '--val-col {} --val-type {} --eq {} --lt {} --gt {}' +
        '--skip-header {}'
    ).format(
        in_fname, out_fname,
        kwargs['chr_col'], kwargs['pos_col'], kwargs['chr_pos_delim'],
        
    )

if __name__ == '__main__':
    conf_fname = sys.argv[1]
    with open(conf_fname, 'r') as conf_file:
        conf = json.loads(conf_file.read())
