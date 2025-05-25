# XmlToExcel
XML形式のツリー構造データをExcelへ変換する。Convert tree-structure data in XML files to Excel.

- xml_to_excel.py: メインプログラム
- module.py: サブモジュール
- examples, examples.sh: 使用例

## 動作確認環境
python 3.10.11
# ライブラリ
fire==0.7.0
flatten_dict==0.4.2
lxml==4.9.2
pandas==2.0.2
pickle

## 使い方
# ヘルプ表示
bashで
```
python xml_to_excel.py --help
```
pythonで
```
import xml_to_excel
help(xml_to_excel)
```

