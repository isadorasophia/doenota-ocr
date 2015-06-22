#!/bin/bash

ASSETS_PATH=/home/isadora/projects/doenota-ocr/assets/notas-binarized/
OUTPUT_PATH=/home/isadora/projects/doenota-ocr/assets/ocr-results/

# DF = default
# TS01 = first training set
# TS02 = second training set

for i in $(ls $ASSETS_PATH -1)
do
	tesseract $ASSETS_PATH$i $OUTPUT_PATH${i%.*}\_DF -l por
	tesseract $ASSETS_PATH$i $OUTPUT_PATH${i%.*}\_TS01 -l not
	tesseract $ASSETS_PATH$i $OUTPUT_PATH${i%.*}\_TS02 -l not2
done
