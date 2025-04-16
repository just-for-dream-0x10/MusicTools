#!/bin/bash

audio_file="../wav/erhu1.wav"
if [ ! -f "$audio_file" ]; then
  echo "error: audio file  $audio_file does not exist"
  exit 1
fi

# extract timbre features
python extract_erhu_timbre.py extract "$audio_file" -o ./features