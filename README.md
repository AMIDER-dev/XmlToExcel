[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.15622039.svg)](https://doi.org/10.5281/zenodo.15622039)

Please follow the license and cite the DOI when you use this software.

# XmlToExcel
XML形式のツリー構造データをExcelテーブル形式へ変換する。Convert tree-structure data in XML files to the Excel table structure. 複数のXMLファイルをExcelテーブルへ統合できる。

- xml_to_excel.py: メインプログラム
- module.py: サブモジュール
- examplesフォルダ, examples.sh: 使用例

## 動作確認環境
- python 3.10.11
- ライブラリ
  - fire 0.7.0
  - flatten_dict 0.4.2
  - lxml 4.9.2
  - pandas 2.0.2

## 入力データ
### XMLファイル
- examples/xml/metadata1.xml, metadata2.xml

### 要素名定義テーブル
- examples/ElementDefine.xlsx

データテーブルの要素名とサンプルXMLの各XPathの対応付けを定義する。要素名の階層構造はスラッシュ（/）で表す。[ExcelToXml](https://github.com/AMIDER-dev/ExcelToXml)と同じものを使用できる。

<table border="1" cellspacing="0" cellpadding="5">
  <thead style="background-color:#3f66a7; color:white;">
    <tr>
      <th>Element Name</th>
      <th>XPath</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>要素名A-1</td>
      <td>パスA-1</td>
    </tr>
    <tr>
      <td>要素名A-2</td>
      <td>パスA-2</td>
    </tr>
    <tr>
      <td>要素名A-2/要素名A-2-2</td>
      <td>パスA-2-2（パスA-2の続き）</td>
    </tr>
    <tr>
      <td>…</td>
      <td></td>
    </tr>
    <tr>
      <td>要素名B-1</td>
      <td>パスB-1</td>
    </tr>
    <tr>
      <td>…</td>
      <td></td>
    </tr>
  </tbody>
</table>

## 出力
- examples/output/table.xlsx: 要素名定義テーブルに従いExcelテーブル形式へ変換したXMLデータ
- examples/output/table.pkl: Excel化する前のPython PandasデータをPickleで保存したもの
- examples/output/table_path.xlsx: 要素名定義テーブルを処理の際に整形したものをExcelで保存したもの

## ヘルプ表示
bashで
```
python xml_to_excel.py --help
```
pythonで
```
import xml_to_excel
help(xml_to_excel)
```

## examplesの実行方法
```
./examples.sh
```

## License

This software is released under the [MIT License](LICENSE).

It also makes use of the following third-party libraries, each of which is distributed under its own open-source license:

- [fire](https://github.com/google/python-fire) — Apache License 2.0  
- [flatten_dict](https://github.com/ianlini/flatten-dict) — MIT License  
- [lxml](https://lxml.de/) — BSD-style License  
- [pandas](https://pandas.pydata.org/) — BSD License

## AMIDERプロジェクト
- [分野横断型研究データベースAMIDER](https://amider.rois.ac.jp/)
- 論文[AMIDER: A Multidisciplinary Research Database and Its Application to Promote Open Science](https://doi.org/10.5334/dsj-2025-007)
