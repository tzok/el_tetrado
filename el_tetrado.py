#! /usr/bin/env python
import argparse
import itertools
import json
import os
import subprocess
import shutil
import sys
import tempfile

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--json', action='store_true', help='parse input file from JSON format')
    parser.add_argument('--strict', action='store_true', help='nucleotides in tetrade linked only by cWH pairing')
    parser.add_argument('input', help='a JSON file produced by DSSR if "--json" is used, otherwise a PDB or PDBx/MMCIF file to be analyzed first by DSSR')
    args = parser.parse_args()

    if args.json:
        with open(args.input) as jsonfile:
            dssr = jsonfile.read()
    else:
        currdir = os.path.dirname(os.path.realpath(__file__))
        tempdir = tempfile.mkdtemp()
        shutil.copy(os.path.join(currdir, 'x3dna-dssr'), tempdir)
        shutil.copy(sys.argv[1], tempdir)
        dssr = subprocess.Popen(['./x3dna-dssr', '-i={}'.format(os.path.basename(sys.argv[1])), '--json', '--symmetry'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=tempdir)
        dssr, _ = dssr.communicate()
        shutil.rmtree(tempdir)

    try:
        data = json.loads(dssr)
    except:
        print('Invalid JSON in', args.input, file=sys.stderr)
        exit(1)

    if 'pairs' not in data:
        print('None')
        exit()

    nts = dict()
    for nt in data['nts']:
        nt_id = nt['nt_id']
        if nt_id.find(':') != -1:
            nt['chain_name'] = '{}:{}'.format(nt_id.split(':')[0], nt['chain_name'])
        nts[nt_id] = nt

    stacks = list()
    for stack in data['stacks']:
        stacks.append(stack['nts_long'].split(','))

    cwh = dict()
    for pair in data['pairs']:
        lw = pair['LW']
        nt1 = nts[pair['nt1']]['nt_id']
        nt2 = nts[pair['nt2']]['nt_id']

        if args.strict:
            if lw == 'cWH':
                if nt1 not in cwh:
                    cwh[nt1] = list()
                cwh[nt1].append(nt2)
            elif lw == 'cHW':
                if nt2 not in cwh:
                    cwh[nt2] = list()
                cwh[nt2].append(nt1)
        else:
            if nt1 not in cwh:
                cwh[nt1] = list()
            cwh[nt1].append(nt2)
            if nt2 not in cwh:
                cwh[nt2] = list()
            cwh[nt2].append(nt1)

    # search for a tetrade: i -> j -> k -> l -> i
    used = set()
    tetrades = list()
    for i in cwh:
        if i in used:
            continue
        for j in cwh[i]:
            if j in cwh and j not in (i) and j not in used:
                for k in cwh[j]:
                    if k in cwh and k not in (i, j) and k not in used:
                        for l in cwh[k]:
                            if l in cwh and l not in (i, j, k) and l not in used and i in cwh[l]:
                                ni, nj, nk, nl = nts[i]['index'], nts[j]['index'], nts[k]['index'], nts[l]['index']
                                nmin = min(ni, nj, nk, nl)
                                if ni == nmin:
                                    tetrade = (i, j, k, l)
                                elif nj == nmin:
                                    tetrade = (j, k, l, i)
                                elif nk == nmin:
                                    tetrade = (k, l, i, j)
                                else:
                                    tetrade = (l, i, j, k)
                                tetrades.append(tetrade)
                                used.update(tetrade)

    def check_tetrades_stacking(ti, tj):
        ti, tj = set(ti), set(tj)
        for stack in stacks:
            stack = set(stack)
            if not stack.isdisjoint(ti) and not stack.isdisjoint(tj):
                ti.difference_update(stack)
                tj.difference_update(stack)
        return len(ti) == len(tj) == 0

    stackings = dict()
    for ti, tj in itertools.combinations(tetrades, 2):
        if check_tetrades_stacking(ti, tj):
            if not ti in stackings:
                stackings[ti] = list()
            stackings[ti].append(tj)
            if not tj in stackings:
                stackings[tj] = list()
            stackings[tj].append(ti)

    quadruplexes = list()
    candidates = set(tetrades)
    while candidates:
        quadruplex = [candidates.pop()]
        changed = True
        while changed:
            changed = False
            for tetrade in quadruplex:
                if tetrade in stackings:
                    for stacked in stackings[tetrade]:
                        if stacked in candidates:
                            quadruplex.append(stacked)
                            candidates.remove(stacked)
                            changed = True
        quadruplexes.append(quadruplex)

    if len(quadruplexes) == 0:
        print('None')
        exit()

    for quadruplex in quadruplexes:
        print('{} tetrads'.format(len(quadruplex)))
        quadruplex = list(quadruplex)
        quadruplex.sort(key=lambda x: nts[x[0]]['index'])

        previous = None
        stem = []
        stem_counter = 0

        for tetrade in quadruplex:
            current = [nts[nt]['index'] for nt in tetrade]
            if not previous or not all([j - i == 1 for i, j in zip(previous, current)]):
                stem_counter += 1
                print('stem #{}'.format(stem_counter))
            previous = current

            classification = ''
            if len(set([nts[i]['chain_name'] for i in tetrade])) == 1:
                n1 = nts[tetrade[0]]['index']
                n2 = nts[tetrade[1]]['index']
                n3 = nts[tetrade[2]]['index']
                n4 = nts[tetrade[3]]['index']
                if n2 < n3 and n3 < n4:
                    classification = '+O'
                elif n2 > n3 and n3 > n4:
                    classification = '-O'
                elif n2 < n3 and n2 < n4:
                    classification = '+N'
                elif n2 < n3 and n2 > n4:
                    classification = '-N'
                elif n2 > n3 and n2 > n4:
                    classification = '+Z'
                elif n2 > n3 and n2 < n4:
                    classification = '-Z'

            print(tetrade[0], tetrade[1], tetrade[2], tetrade[3], classification)
        print()
