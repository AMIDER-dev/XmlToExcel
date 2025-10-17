import fire
from pathlib import Path
import pandas as pd
import xmltodict
from flatten_dict import unflatten
from deepmerge import Merger

def get_xpaths(xmldir):
    xmlfiles = list(Path(xmldir).rglob('*.xml'))
    merger = Merger([(dict, ['merge'])], ['override'], ['override'])

    xpaths_merge = {}
    for xmlfile in xmlfiles:
        xpaths_dict = get_xpaths_single(xmlfile)
        xpaths_merge = merger.merge(xpaths_merge, xpaths_dict)

    xpaths_list = flatten_keys(xpaths_merge)
    pd.Series(xpaths_list).to_excel('xpaths_from_xml.xlsx', index=False, header=False)

    return xpaths_list

def get_xpaths_single(xmlfile):
    xpaths = []
    with open(xmlfile, 'r', encoding='utf-8') as f:
        data = xmltodict.parse(f.read())
        xpaths = flatten_keys(data)
        xpaths_unique = list(dict.fromkeys(xpaths))
        xpaths_dict = unflatten({tuple(p.split('/')): {} for p in xpaths_unique})
    return xpaths_dict

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

if __name__ == "__main__":
    fire.Fire(get_xpaths)
