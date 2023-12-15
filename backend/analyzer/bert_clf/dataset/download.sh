#!/bin/bash

export KAGGLE_USERNAME=uiucgroup
export KAGGLE_KEY=46f20bf227e43375e74948f8a705ba30

dataset=amazonreviews
dir=.

source ../../../venv/bin/activate

kaggle datasets download -d bittlingmayer/$dataset

unzip $dir/amazonreviews.zip -d $dir
rm $dir/amazonreviews.zip

bzip2 -d train.ft.txt.bz2 
bbzip2 -d test.ft.txt.bz2 

rm $dir/*ft.txt.bz2