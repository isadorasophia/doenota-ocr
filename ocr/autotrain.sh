#!/bin/bash

# to do: font_properties file

TESSDATA_LOCATION=/usr/local/share/tessdata/
FONT_NAME=not
i=0

#export TESSDATA_PREFIX=$TESSDATA_LOCATION

for x in $(ls -1 | grep tif)
do
	training[$i]=${x%.tif}

	tesseract ${training[$i]}.tif ${training[$i]} nobatch box.train
	let i++
done

for file in "${training[@]}"
do
	unicharset_extractor $file.box
	shapeclustering -F font_properties -U unicharset $file.tr
	mftraining -F font_properties -U unicharset -O $FONT_NAME.unicharset $file.tr
	cntraining $file.tr
done

cp normproto $FONT_NAME.normproto
cp inttemp $FONT_NAME.inttemp
cp pffmtable $FONT_NAME.pffmtable
cp shapetable $FONT_NAME.shapetable

combine_tessdata $FONT_NAME.
