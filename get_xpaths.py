import fire
from pathlib import Path
import pandas as pd
import xmltodict
import yaml

def get_xpaths(*xmldirs, outname='xpaths_from_xml', printfile=False):
    xmlfiles = []
    for d in xmldirs:
        files = sorted(Path(d).rglob('*.xml'))
        xmlfiles.extend(files)
    
    seen = set()
    xpaths_merge = []

    for xmlfile in xmlfiles:
        if printfile:
            print(xmlfile)

        xpaths = get_xpaths_single(xmlfile)
        for p in xpaths:
            if p not in seen:
                seen.add(p)
                xpaths_merge.append(p)

    pd.Series(xpaths_merge).to_excel(f'{outname}.xlsx', index=False, header=False)

    tree = build_tree(xpaths_merge)
    with open(f'{outname}.yaml', 'w', encoding='utf-8') as f:
        yaml.dump(tree, f, allow_unicode=True, sort_keys=False)

    return tree

def get_xpaths_single(xmlfile):
    xpaths = []
    with open(xmlfile, 'r', encoding='utf-8') as f:
        data = xmltodict.parse(f.read())
        xpaths = flatten_keys(data)
        xpaths_unique = list(dict.fromkeys(xpaths))
    return xpaths_unique

def flatten_keys(d, parent_key='', sep='/'):
    keys = []
    if isinstance(d, dict) and len(d)>0:
        for k, v in d.items():
            new_key = parent_key + sep + k if parent_key else k
            keys.extend(flatten_keys(v, new_key))
    elif isinstance(d, list) and len(d)>0:
        for v in d:
            keys.extend(flatten_keys(v, parent_key))
    else:
        keys.append(parent_key)
    return keys

def build_tree(paths, sep='/'):
    tree = {}
    for p in paths:
        keys = p.split(sep)
        d = tree

        for k in keys:
            if k not in d:
                d[k] = {}
            elif not isinstance(d[k], dict):
                d[k] = {}

            d = d[k]
    return tree

if __name__ == "__main__":
    fire.Fire(get_xpaths)
