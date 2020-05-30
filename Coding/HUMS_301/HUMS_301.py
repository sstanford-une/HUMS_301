# Functions and Packages imported
import os
import string
import itertools
import re
from music21 import *
from glob import glob
from lxml import *
from collections import Counter
from xml.etree.ElementTree import XMLParser
from openpyxl import Workbook
import winsound
import ntpath
import numpy as np
import matplotlib.pyplot as plt



class FrottalaObject:
    def __init__(frottala, title, composer, sections, phrases):
        frottala.title = title
        frottala.composer = composer
        frottala.sections = sections
        frottala.phrases = phrases

        print(frottala.title, "by", frottala.composer, "has been recorded.")

class SectionObject:
    def __init__(section):
        section.phrases = 0
        section.measures = 0
        section.notes = 0
        section.duration = 0
        section.syllables = 0

class PhraseObject:
    def __init__(phrase):
        phrase.measures = 0
        phrase.notes = 0
        phrase.duration = 0
        phrase.syllables = 0

class DataRecorder:
    tag, attrib, data = None, None, None

    def __init__(self):
        self.title, self.composer = None, None
        self.sectionObject = SectionObject()
        self.phraseObject = PhraseObject()
        self.sections, self.phrases = [], []
        #self.sectionPhraseCount, self.measureCount, self.noteCount, self.durationCount, self.syllableCount = 0, 0, 0, 0, 0
        #self.sectionData, self.sectionMeasures, self.sectionSyllables, self.sectionNotes, self.sectionDuration = [], [], [], [], []
        #self.phraseData, self.phraseMeasures, self.phraseSyllables, self.phraseNotes, self.phraseDuration = [], [], [], [], []
        self.completeCheck, self.lyricCheck, self.pitchCheck, self.puncCheck, self.capsCheck = False, False, False, False, False

    def start(self, tag, attrib):
        self.tag = tag
        self.attrib = attrib

    def end(self, tag):
        self.tag = None
        self.attrib = None

    def data(self, data):
        self.data = data
        if self.completeCheck == False:
            switchFunction = SwitchFunction(self.tag, self.attrib, self.data)
            switchFunction.FuncSwitch()
        
    def close(self):
        frottalaObject = FrottalaObject(self.title, self.composer, self.sections, self.phrases)
        corpusData.append(frottalaObject)

class SwitchFunction:
    def __init__(self, tag, attrib, data):
        self.tag = tag
        self.attrib = attrib
        self.data = data

    def Info(self):
        if self.data != ('Petrucci'):
            dataRecorder.title = self.data
        elif self.data == ('Petrucci'):
            dataRecorder.composer = self.data

    def MeasureCount(self):
        if dataRecorder.completeCheck == False:            
            if self.data == ('dashed'):
                dataRecorder.sectionObject.measures += 1
                dataRecorder.phraseObject.measures += 1
            elif self.data == ('light-heavy'):
                dataRecorder.sectionObject.measures += 1
                dataRecorder.phraseObject.measures += 1
                self.RecordSection()
                self.RecordPhrase()
                dataRecorder.completeCheck = True
            elif self.data != ('dashed') and self.data != ('light-heavy'):
                dataRecorder.sectionObject.measures += 1
                dataRecorder.phraseObject.measures += 1
                self.RecordSection()
                self.RecordPhrase()
    
    def LyricSwitch (self):
        dataRecorder.lyricCheck = True

    def SyllableCount(self):
        if dataRecorder.lyricCheck == True:
            self.CapsCheck()
            self.PuncSwitch()
            dataRecorder.sectionObject.syllables += 1
            dataRecorder.phraseObject.syllables += 1
            dataRecorder.lyricCheck = False

    def PitchSwitch (self):
        dataRecorder.pitchCheck = True

    def DurationCount (self):
        if dataRecorder.pitchCheck == True:
            dataRecorder.sectionObject.duration += int(self.data)
            dataRecorder.phraseObject.duration += int(self.data)
            dataRecorder.pitchCheck = False

    def PuncSwitch(self):
        punctuation = set(string.punctuation)
        if any(char in punctuation for char in self.data):
            dataRecorder.puncCheck = True            

    def CapsCheck(self):
        if self.data.islower() == False and dataRecorder.puncCheck == True:
            print(self.data)
            self.RecordPhrase()
        else:
            dataRecorder.capsCheck = False
            dataRecorder.puncCheck = False


    def FuncSwitch(self):
        switcher = {
            'credit-words': self.Info,
            'bar-style': self.MeasureCount,
            'lyric' : self.LyricSwitch,
            'text' : self.SyllableCount,
            'pitch' : self.PitchSwitch,
            'duration' : self.DurationCount

            }
        return switcher.get(self.tag, lambda: "Error: Switch Function - FuncSwitch")()

    def RecordSection (self):
        dataRecorder.sections.append(dataRecorder.sectionObject)
        dataRecorder.sectionObject = SectionObject()

    def RecordPhrase (self):
        dataRecorder.phrases.append(dataRecorder.phraseObject)
        dataRecorder.phraseObject = PhraseObject()
        dataRecorder.lyricCheck, dataRecorder.pitchCheck, dataRecorder.puncCheck, dataRecorder.capsCheck = False, False, False, False
    

def ProcessCorpus():
    print("Gathering Files")
    global root, corpusData, dataRecorder, corpCount
    corpusData = []

    for file in glob(r'E:/Documents/UNE/HUMS_301/XML Files/MusicXML\*.musicxml'):
        tree = etree.parse(file)
        root = tree.getroot()
        xmlString = etree.tostring(root, encoding="UTF-8", method='xml')
        dataRecorder = DataRecorder()
        parser = XMLParser(target = dataRecorder)
        parser.feed(xmlString)
        parser.close()

          
    # for frottala in somewhere longest data = column amount
    # put in excel using biggest values

    print('Corpus procssing compelete!')




ProcessCorpus()



