import json
from multiprocessing import Pool
import subprocess
import sys

N_WORKERS = 5

def conf_clean(conf):
    if not 'skip_header' in conf:
        conf['skip_header'] = False
    return conf

def worker(in_fname, out_fname, conf):
    conf = conf_clean(conf)
    
    command = (
        'python bin/parse_raw_worker.py ' +
        '--chr-col {} --pos-col {} --val-col {} --val-type {} ' +
        '--skip-header {} {} {}'
    ).format(
        conf['chr_col'], conf['pos_col'], conf['p_col'],
        'float', conf['skip_header'],
        in_fname, out_fname
    )

    ps = subprocess.check_output(command.split())
    
if __name__ == '__main__':
    conf_fname = sys.argv[1]
    with open(conf_fname, 'r') as conf_file:
        conf = json.loads(conf_file.read())

    if len(sys.argv) > 2:
        namespace = sys.argv[2]
    else:
        namespace = ''

    pool = Pool(processes=N_WORKERS)
    results = [
        pool.apply_async(worker, [
            qtl_conf['file'],
            'target/parsed/{0}.pickle'.format(qtl_conf['namespace']),
            qtl_conf
        ])
        for qtl_conf in conf
        if namespace in qtl_conf['namespace']
    ]
    ans = [ r.get() for r in results ]
        
