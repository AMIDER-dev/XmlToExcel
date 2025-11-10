from pathlib import Path
import fire
import pandas as pd
from lxml import etree
import module

def replace_element(excel_rep: str, col_path: str, col_from: str, col_to: str, indir: str, outdir: str):
    """
    Replace xml elements as defined by excel_rep table. Input directory structure is copied to output directory.
    
    Parameters
    ----------
    excel_rep: str
        Escel table defining each XPath and replacement value pairs
    col_path: str
        Column name in excel_rep for XPath data
    col_from: str
        Column name in excel_rep for element values to be subject of the replacement
    col_to: str
        Column name in excel_rep for replaced values
    indir: str
        Input directory of xml files. The sub directories are also surveyed. 
    outdir: str
        Output directory of xml files. The input subdirectory structure is copied.
    ----------
    """
    print('Read replacement table')
    dict_define = module.read_define(excel_rep, col_path)
    data_define = module.dict_to_table(dict_define, col_path)
    list_name = []
    list_path = []
    for l in data_define:
        list_name.append('/'.join([s.strip() for s in l[0]]))
        list_path.append(''.join(['({})'.format(s.strip()) if '|' in s else s.strip() for s in l[1]]))

    data_path = pd.DataFrame({'XPath': list_path}, index=list_name)

    table_rep = pd.ExcelFile(excel_rep).parse(index_col=0)
    table_rep.index = pd.Series(table_rep.index).ffill()
    table_rep = table_rep.drop(columns=[col_path])
    table_rep = table_rep.dropna()

    data_rep = pd.merge(table_rep, data_path, left_index=True, right_index=True, how='left')
    print(data_rep)
    print()

    print('Edit XML files')
    pref_default = '_ns'
    for inpath in Path(indir).rglob('*.xml'):
        relpath = inpath.relative_to(indir)
        outpath = outdir / relpath
        outpath.parent.mkdir(parents=True, exist_ok=True)

        xml = etree.parse(inpath)
        root = xml.getroot()
        ns_tmp = root.nsmap
        ns = {}
        for key_tmp in ns_tmp:
            key = pref_default if not key_tmp else key_tmp
            ns[key] = ns_tmp[key_tmp]
        
        n_rep = 0
        for index, row in data_rep.iterrows():
            xpath = module.add_ns_pref(row[col_path], pref_default)
            elems = root.xpath(xpath, namespaces=ns)
            for elem in elems:
                if elem.text is not None and elem.text.strip()==str(row[col_from]).strip():
                    elem.text = str(row[col_to]).strip()
                    n_rep += 1

        xml.write(outpath, encoding='utf-8', xml_declaration=True, pretty_print=True)
        print('{} -> {}: {} elements replaced'.format(inpath, outpath, n_rep))

if __name__ == "__main__":
    fire.Fire(replace_element)
