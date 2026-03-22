#!/usr/bin/env python3
from __future__ import annotations
import argparse, importlib.util, json, os, sys
from collections import Counter

MODULE_PATH = os.path.join('/mnt/data', 'enumerate_760_claude_like_decompositions.py')
spec = importlib.util.spec_from_file_location('enum760', MODULE_PATH)
mod = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = mod
spec.loader.exec_module(mod)


def parse_ms(text: str):
    vals=[]
    for x in text.split(','):
        x=x.strip()
        if not x: continue
        m=int(x)
        if m<3 or m%2==0: raise ValueError(f'bad m={m}')
        vals.append(m)
    return vals


def main():
    ap=argparse.ArgumentParser(description='Analyze chirality extrema over all 760 generalizable decompositions.')
    ap.add_argument('--ms', default='3,5,7', help='comma-separated odd m values')
    ap.add_argument('--write-json', default='')
    args=ap.parse_args()
    ms=parse_ms(args.ms)

    print('[1/4] Enumerating m=3 Hamiltonian cycles...')
    cycles_m3 = mod.enumerate_hamiltonian_cycles_m3()
    rules=[]
    print('[2/4] Filtering the 996 generalizable cycles...')
    for cyc in cycles_m3:
        rule = mod.rule_from_cycle_m3(cyc)
        if mod.generalize_cycle(rule,5) is not None and mod.generalize_cycle(rule,7) is not None:
            rules.append(rule)
    rules=list(dict.fromkeys(rules))
    print(f'      generalizable cycles = {len(rules)}')
    print('[3/4] Recovering the 760 exact-cover decompositions...')
    rows=[mod.arc_columns_for_rule(r) for r in rules]
    decomps=mod.exact_cover_solutions(rows, 81)
    print(f'      decompositions = {len(decomps)}')

    out={'ms':ms,'stats':{}}
    print('[4/4] Computing chirality extrema...')
    for m in ms:
        spectra=[]
        max_abs=-1
        argmax=[]
        for dec in decomps:
            chis=[]
            for ridx in dec:
                gc=mod.generalize_cycle(rules[ridx], m)
                chi=mod.cyclic_chirality_from_directions(gc.directions)
                chis.append(chi)
            chis_sorted=tuple(sorted(chis))
            spectra.append(chis_sorted)
            dom=max(abs(x) for x in chis)
            if dom>max_abs:
                max_abs=dom
                argmax=[{'decomposition':dec,'chis':chis_sorted}]
            elif dom==max_abs:
                argmax.append({'decomposition':dec,'chis':chis_sorted})
        cnt=Counter(spectra)
        common=cnt.most_common(10)
        print(f'\nm={m}')
        print(f'  max dominant |chi| = {max_abs}')
        print(f'  number attaining max = {len(argmax)}')
        print(f'  one maximizing spectrum = {argmax[0]["chis"]}')
        print('  top 10 spectra by frequency:')
        for spec,n in common:
            print(f'    {spec}: {n}')
        out['stats'][str(m)]={
            'max_dominant_abs_chirality': max_abs,
            'num_attaining_max': len(argmax),
            'one_maximizer': argmax[0],
            'top10_spectra': [{'spectrum': list(spec), 'count': n} for spec,n in common],
        }

    if args.write_json:
        with open(args.write_json,'w') as f:
            json.dump(out,f,indent=2)
        print(f'\nWrote {args.write_json}')

if __name__=='__main__':
    main()
