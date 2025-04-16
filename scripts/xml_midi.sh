#!/bin/bash


input_file="./output/song5/song5_basic_pitch.musicxml"
if [ ! -f "$input_file" ]; then
  echo "error: input file  $input_file does not exist"
  exit 1
fi

#  transfer MusicXML到MIDI
output_file="./output/song5_basic_pitch.midi"
python musicxml_to_midi.py "$input_file" -o "$output_file"