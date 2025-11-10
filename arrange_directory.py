from pathlib import Path
import shutil
import fire
from lxml import etree
import module

def arrange_directory(xpath_uri:str, indir:str, outdir: str):
    """
    Create directories and copy xml files according to URI in a specified xml element.

    Parameter
    ---------
    xpath_uri: str
    XPath where the URI is contained.

    indir: str
    Input directory where input xml files are surveyed.

    outdir: 
    Output directory.
    """
    pref_default = '_ns'
    inpaths = set(Path(indir).rglob('*.xml')) | set(Path(indir).rglob('*.xml.*'))
    for inpath in sorted(inpaths):
        if inpath.name.endswith('.swp'):
            continue

        xml = etree.parse(inpath)
        root = xml.getroot()
        ns_tmp = root.nsmap
        ns = {}
        for key_tmp in ns_tmp:
            key = pref_default if not key_tmp else key_tmp
            ns[key] = ns_tmp[key_tmp]

        xpath = module.add_ns_pref(xpath_uri, pref_default)
        elems = root.xpath(xpath, namespaces=ns)
        outpath = None
        if len(elems)>0:
            uri = elems[0].text
            path = uri.split('/',1)[1].lstrip('/') if '/' in uri else uri
            path = path.strip() + '.xml'
            outpath = Path(outdir) / path

            outpath.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(inpath, outpath)

        print('{} -> {}'.format(inpath, outpath))

if __name__ == "__main__":
    fire.Fire(arrange_directory)
