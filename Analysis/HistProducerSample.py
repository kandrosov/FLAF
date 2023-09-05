import ROOT
import sys
import os
import math
import shutil
from RunKit.sh_tools import sh_call
if __name__ == "__main__":
    sys.path.append(os.environ['ANALYSIS_PATH'])

# HistProducerSample.py --histDir my/hist/dir --outDir my/out/dir --hists m_tautau,tau1_pt --file-name-pattern 'nano_{id}.root' --file-ids '0-100'

import Common.Utilities as Utilities
from Analysis.HistHelper import *

if __name__ == "__main__":
    import argparse
    import yaml
    parser = argparse.ArgumentParser()
    parser.add_argument('--histDir', required=True, type=str)
    parser.add_argument('--test', required=False, type=bool, default=False)
    parser.add_argument('--remove-files', required=False, type=bool, default=False)
    parser.add_argument('--outDir', required=True, type=str)
    parser.add_argument('--hists', required=False, type=str, default='bbtautau_mass,dR_tautau,tautau_m_vis,tau1_pt')
    parser.add_argument('--file-name-pattern', required=False, type=str, default="nano_{id}.root")
    parser.add_argument('--file-ids', required=False, type=str, default='')

    args = parser.parse_args()

    # 1 list files :

    all_vars = args.hists.split(',')
    start_end_idx = args.hists.split('-')
    all_files = {}
    for var in all_vars:
        all_files[var] = []
        file_name = args.file_name_pattern
        if(len(start_end_idx) > 1):
            for idx in range(start_end_idx[0],start_end_idx[1]):
                file_name = file_name.format(id=idx)
                all_files[var].append(os.path.join(args.histDir, var, file_name))
        else:
            all_files[var].append(os.path.join(args.histDir, var, file_name))

        outFileNameFinal = f'{args.outDir}/{var}.root'
        hadd_str = f'hadd -f209 -j -O {outFileNameFinal}'
        hadd_str += ' '.join(f for f in all_files[var])
        if len(all_files[var]) > 1:
            sh_call([hadd_str], True)
        else:
            shutil.copy(all_files[var][0],outFileNameFinal)
        if os.path.exists(outFileNameFinal) and args.remove_files:
            for histFile in all_files[var]:
                if args.test : print(histFile)
                if histFile == outFileNameFinal: continue
                os.remove(histFile)
    if args.remove_files:
        shutil.rmtree(args.histDir)
