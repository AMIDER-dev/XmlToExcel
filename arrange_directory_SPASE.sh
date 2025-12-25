#!/bin/bash
indir=./
outdir=./

echo $locale
for cat in NumericalData DisplayData Instrument Observatory Person Repository; do
    echo $cat
    xpath=/Spase/${cat}/ResourceID
    echo $xpath

    python arrange_directory.py ${xpath} ${indir} ${outdir}
done

