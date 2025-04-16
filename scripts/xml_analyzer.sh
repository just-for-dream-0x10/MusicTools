#!/bin/bash


input_file="./output/song5/song5_basic_pitch.musicxml"
if [ ! -f "$input_file" ]; then
  echo "error: musicxml  $input_file does not exist"
  exit 1
fi

# apply Erhu timbre
output_file="./output/song5_erhu.musicxml"
python ./musicxml_analyzer.py apply-erhu-timbre "$input_file" --output "$output_file"