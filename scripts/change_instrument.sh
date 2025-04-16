#!/bin/bash

input_file="./output/song5/song5_basic_pitch.musicxml"
if [ ! -f "$input_file" ]; then
  echo "error：inputs file  $input_file does not exist"
  exit 1
fi


# change instrument to Erhu
python musicxml_analyzer.py change-instrument "$input_file" Erhu