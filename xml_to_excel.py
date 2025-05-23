import os
import sys
import fire
import pandas as pd
import collections
from lxml import etree
import module

def xml_to_excel(elem_table: str, xmldir: str, outdir: str='./'):
    """
    Convert multiple XML files into a unified Excel table.
    
    Parameters
    ----------
    elem_table: str
        Excel table defining element names in the output Excel data each corresponding to the XPath of the input XML file.
    xmldir: str
        Path to the folder containing input XML files.
    outdir: str
        Output directory. Default is './'.
    """

    print('### START ###')
    print('element define: ' + elem_table)
    print('xmldir: ' + xmldir)
    print('outdir: ' + outdir)

    if not os.path.exists(outdir):
        os.mkdir(outdir)

    list_tmp = [os.path.join(xmldir, s) for s in os.listdir(xmldir)]
    xmlfiles = sorted([s for s in list_tmp if os.path.isfile(s) ])
    print('num of xmlfiles: ' + str(len(xmlfiles)))

    print('')
    print('Read Element-Define Table')

    dict_path = module.read_define('ElementDefine_ISO.xlsx')
    table_path = [l for l in module.dict_to_table(dict_path)]
    table_name = [l[0] for l in table_path]
    data_path = pd.DataFrame(table_name)
    cols_name = list(data_path.columns)
    nlevel = len(cols_name)
    data_path['XPath'] = [l[1] for l in table_path]

    outfile = outdir + '/table_path.xlsx'
    data_path.to_excel(outfile, index=False)
    print('output: ' + outfile)

    print('')
    print('Compile XML Values')

    n = 0
    for xmlfile in xmlfiles:
        print('.', end='', flush=True)

        xml = etree.parse(xmlfile)
        root = xml.getroot()
        ns = root.nsmap

        table_xml = [l for l in module.read_xml(dict_path, root, ns)]
        table_name = [l[0] for l in table_xml]
        data_xml = pd.DataFrame(table_name)
        data_xml = data_xml.astype('str')
        data_xml.mask((data_xml=='nan') | (data_xml=='None'), '', inplace=True)
        data_xml[xmlfile.split('/')[-1]] = [l[1] for l in table_xml]
        data_xml.set_index(cols_name, inplace=True)

        if n>0:
            data = pd.merge(data, data_xml, left_index=True, right_index=True, how='outer')
        else:
            data = data_xml

        n += 1
        if n%100 == 0:
            print(n, end='')

    print('')

    data = data.astype('str')
    data.mask((data=='nan') | (data=='None'), None, inplace=True)

    outfile = outdir + '/table.pkl'
    module.pickle_dump(data, outfile)
    print('output: ' + outfile)

    outfile = outdir + '/table.xlsx'
    data.to_excel(outfile)
    print('output: ' + outfile)

    print('Finished!')

if __name__ == "__main__":
    fire.Fire(xml_to_excel)
