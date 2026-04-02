import re
import warnings
import pandas as pd
import pickle
from flatten_dict import unflatten

def read_define(excelfile, key_val):
    data_define = pd.ExcelFile(excelfile).parse(index_col=0)
    data_define = data_define.loc[data_define.index.notna()]
    data_define.index = [s + '/' + key_val for s in data_define.index]
    dict_tmp = data_define.to_dict('dict')
    dict_path = unflatten(dict_tmp[key_val], splitter='path')
    return dict_path

def dict_to_table(current_dict, key_val, names=[], paths=[]):
    if len(current_dict.keys())==1 and list(current_dict.keys())[0]==key_val:
        yield [names, paths]
    else:
        for child_name, child_dict in current_dict.items():
            if child_name==key_val:
                continue
            yield from dict_to_table(child_dict, key_val, names + [child_name], paths + [child_dict[key_val]])

def add_ns_pref(xpath, pref):
    parts = xpath.split('/')
    new_parts = []
    for p in parts:
        if not p:
            new_parts.append('')
        elif ':' in p:
            new_parts.append(p)
        elif p.startswith('@') or p.strip() == '(':
            new_parts.append(p)
        else:
            new_parts.append('{}:{}'.format(pref, p))
    return '/'.join(new_parts)

def _localname(tag):
    return re.sub(r'\{[^}]*\}', '', tag)

def _collect_all(node, names):
    children = list(node)
    if not children:
        text = (node.text or '').strip()
        if text:
            yield [names, node.text]
    else:
        for i, child in enumerate(children):
            yield from _collect_all(child, names + [_localname(child.tag) + '_' + str(i)])

def _direct_child_localname(xpath, is_root_call):
    parts = [p for p in xpath.replace('./', '/').split('/') if p]
    idx = 1 if is_root_call else 0
    if idx >= len(parts):
        return None
    tag = re.sub(r'\[.*', '', parts[idx])
    return tag.split(':', 1)[1] if ':' in tag else tag

def read_xml(current_dict, current_node, ns, pref_default, key_val, names=[]):
    if len(current_dict.keys())==1:
        text = current_node.text
        yield [names, text]
    else:
        is_root_call = (len(names) == 0)
        matched_tags = set()

        for child_name, child_dict in current_dict.items():
            if child_name==key_val:
                continue

            xpath = child_dict[key_val]
            tag = _direct_child_localname(xpath, is_root_call)
            if tag:
                matched_tags.add(tag)

            xpath = add_ns_pref(xpath, pref_default)
            if len(names)>0:
                xpath = '.' + xpath
            child_nodes = current_node.xpath(xpath, namespaces=ns)

            for i, child_node in enumerate(child_nodes):
                yield from read_xml(child_dict, child_node, ns, pref_default, key_val, names + [child_name + '_' + str(i)])

        for i, child in enumerate(current_node):
            if _localname(child.tag) not in matched_tags:
                child_name = _localname(child.tag) + '_' + str(i)
                for row in _collect_all(child, names + [child_name]):
                    yield row

def reorder_dict(template, target):
    if not isinstance(target, dict):
        return target

    result = {}
    matched_keys = set()

    for key in template:
        keys_target = [k for k in target if k.startswith(key)]
        for key_target in sorted(keys_target):
            matched_keys.add(key_target)
            result[key_target] = reorder_dict(template[key], target[key_target])

    for key in target:
        if key not in matched_keys:
            result[key] = target[key]

    return result

def list_merge_vertical(ws, col, start_row, end_row):
    merge_start = start_row
    merge_end = start_row

    list_merge = []
    for row in range(start_row + 1, end_row + 1):
        if getcell(ws, row, col) is None or getcell(ws, row, col) == '':
            continue

        if getcell(ws, row, col) == getcell(ws, row - 1, col):
            if col == 1 or (col > 1 and getcell(ws, row, col - 1) == getcell(ws, row - 1, col - 1)):
                merge_end = row
        else:
            if merge_end > merge_start:
                list_merge.append([merge_start, merge_end])
            merge_start = row

    if merge_end > merge_start:
        list_merge.append([merge_start, merge_end])

    return list_merge

def dict_merge_horizontal(ws, start_row, end_row, start_col, end_col):
    dict_merge = {}
    for row in range(start_row, end_row + 1):
        list_row = []
        for col in range(start_col + 1, end_col + 1):
            if getcell(ws, row, col) is None or getcell(ws, row, col) == '':
                list_row = [col - 1, end_col]
                break

        dict_merge[row] = list_row

    return dict_merge

def getcell(ws, row, col):
    cell = ws.cell(row=row, column=col)
    val = cell.value
    return val

def data_to_str(data, str_none=''):
    data_str = data.astype('str')
    with warnings.catch_warnings():
        warnings.simplefilter('ignore', FutureWarning)
        mask = data_str.applymap(lambda x: x.lower()=='nan' or x.lower()=='none')
    data_mask = data_str.mask(mask, str_none)
    return data_mask

def pickle_dump(obj,path):
    with open(path,mode='wb') as f:
        pickle.dump(obj,f)

def pickle_load(path):
    with open(path,mode='rb') as f:
        data = pickle.load(f)
        return data
