import pandas as pd
import pickle
from flatten_dict import unflatten

def read_define(excelfile):
    data_define = pd.ExcelFile(excelfile).parse(index_col=0)
    data_define.index = [s + '/XPath' for s in data_define.index]
    dict_tmp = data_define.to_dict('dict')
    dict_path = unflatten(list(dict_tmp.values())[0], splitter='path')
    return dict_path

def read_xml(current_dict, current_node, ns, names=[]):
    if len(current_dict.keys())==1:
        text = current_node.text
        yield [names, text]
    else:
        for child_name, child_dict in current_dict.items():
            if child_name=='XPath':
                continue

            xpath = child_dict['XPath']
            if len(names)>0:
                xpath = '.' + xpath
            child_nodes = current_node.xpath(xpath, namespaces=ns)
            for i, child_node in enumerate(child_nodes):
                name = child_name if len(child_nodes)==1 else child_name + '_' + str(i)
                yield from read_xml(child_dict, child_node, ns, names + [name])

def dict_to_table(current_dict, names=[], path=''):
    if len(current_dict.keys())==1:
        yield [names, path]
    else:
        for child_name, child_dict in current_dict.items():
            if child_name=='XPath':
                continue
            yield from dict_to_table(child_dict, names + [child_name], path + child_dict['XPath'])

def pickle_dump(obj,path):
    with open(path,mode='wb') as f:
        pickle.dump(obj,f)

def pickle_load(path):
    with open(path,mode='rb') as f:
        data = pickle.load(f)
        return data
