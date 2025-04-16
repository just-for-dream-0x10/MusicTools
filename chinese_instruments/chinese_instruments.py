#!/usr/bin/env python3
from music21 import instrument, pitch
from music21.instrument import StringInstrument
import random


"""
This is just a preliminary simulation implementation and will be improved later.
"""

class Erhu(StringInstrument):
    def __init__(self, **keywords):
        super().__init__(**keywords)
        self.instrumentName = "Erhu"
        self.instrumentAbbreviation = "Erhu"
        self.midiProgram = 110
        self.instrumentSound = "strings.erhu"
        # Set the lowest note to A3 based on analysis report, as A3 is one of the lower notes used
        self.lowestNote = pitch.Pitch("A3")
        # Adjust string pitches to better fit A major scale
        self._stringPitches = ["A3", "E4"]
        # Enhance vibrato and slide effects; triplets in the report suggest these techniques are important
        self.playing_techniques = {
            "vibrato": 0.9,  # Enhance vibrato effect
            "slide_speed": 0.7,  # Increase slide speed
            "pressure": 0.75,  # Increase pressure for greater expressiveness
            "bow_pressure": 0.6,  # Increase bow pressure
        }
        # Adjust timbre: increase warmth and harmonics, reduce brightness
        self.timbre_adjustments = {
            "brightness": 0.4,  # Lower brightness for a softer tone
            "warmth": 0.95,  # Increase warmth, suitable for A major
            "nasality": 0.5,  # Reduce nasality
            "harmonics": 0.4,  # Increase harmonics for richer tone
        }
        # Add more special techniques, especially slides and vibrato, which are important in Erhu performance
        self.special_techniques = [
            "glissando",
            "vibrato",
            "pizzicato",
            "harmonics",
            "portamento",
            "tremolo",
        ]


# Chinese traditional instruments
class ChineseInstruments(StringInstrument):
    """Chinese traditional instruments class"""

    @staticmethod
    def create_erhu():
        """Create Erhu instrument"""
        erhu = Erhu()
        erhu.midiChannel = 1  # Set MIDI channel
        erhu.volume = 85  # Set volume
        return erhu

    @staticmethod
    def create_pipa():
        """Create Pipa instrument (using guitar MIDI program number)"""
        pipa = instrument.StringInstrument()
        pipa.instrumentName = "Pipa"
        pipa.instrumentAbbreviation = "Pipa"
        pipa.midiProgram = 24  # Nylon string guitar MIDI program number
        pipa.midiChannel = 1  # Set MIDI channel
        pipa.volume = 80  # Set volume
        return pipa

    @staticmethod
    def create_guzheng():
        """Create Guzheng instrument (using harp MIDI program number)"""
        guzheng = instrument.StringInstrument()
        guzheng.instrumentName = "Guzheng"
        guzheng.instrumentAbbreviation = "Gzh"
        guzheng.midiProgram = 46  # Harp MIDI program number
        return guzheng

    @staticmethod
    def create_dizi():
        """Create Dizi instrument (using flute MIDI program number)"""
        dizi = instrument.WoodwindInstrument()
        dizi.instrumentName = "Dizi"
        dizi.instrumentAbbreviation = "Dizi"
        dizi.midiProgram = 73  # Flute MIDI program number
        return dizi

    @staticmethod
    def create_suona():
        """Create Suona instrument (using oboe MIDI program number)"""
        suona = instrument.WoodwindInstrument()
        suona.instrumentName = "Suona"
        suona.instrumentAbbreviation = "Suona"
        suona.midiProgram = 68  # Oboe MIDI program number
        return suona

    @staticmethod
    def create_yangqin():
        """Create Yangqin instrument (using piano MIDI program number)"""
        yangqin = instrument.StringInstrument()
        yangqin.instrumentName = "Yangqin"
        yangqin.instrumentAbbreviation = "Yqin"
        yangqin.midiProgram = 0  # Piano MIDI program number
        return yangqin
