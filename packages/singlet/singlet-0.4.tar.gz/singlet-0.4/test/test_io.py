#!/usr/bin/env python
# vim: fdm=indent
'''
author:     Fabio Zanini
date:       07/08/17
content:    Tests for the library.
'''
# Modules
import os
import subprocess as sp


# Controlled sp environment
def run(script, where=None, **kwargs):
    import platform

    if where == 'local' and platform.node() != 'X260':
        return
    if where == 'remote' and platform.node() == 'X260':
        return

    env = os.environ.copy()
    env['SINGLET_CONFIG_FILENAME'] = 'example_data/config_example.yml'

    # Include local tests
    if platform.node() == 'X260':
        singlet_path = os.path.dirname(os.path.dirname(__file__))
        env['PYTHONPATH'] = singlet_path+':'+env['PYTHONPATH']
        print(singlet_path)

    return sp.check_call(
        script,
        env=env,
        shell=True,
        **kwargs)


# Script
if __name__ == '__main__':

    # Config
    run('test/io/config.py')

    # IO samplesheet
    run('test/io/samplesheet_csv_parser.py')
    run('test/io/samplesheet_googleapi_parser.py', where='local')
    run('test/io/samplesheet_parser.py')

    # IO count_table
    run('test/io/count_table_csv_parser.py')
