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
import csv
import winsound
import ntpath
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import pandas as pandas



class FrottalaObject:
    def __init__(self, title, composer, sections, phrases):
        self.title = title
        self.composer = composer
        self.sections = sections
        self.phrases = phrases

        #print(self.title, "by", self.composer, "has been recorded.")

class SectionObject:
    def __init__(self):
        self.phrases = 0
        self.measures = 0
        self.notes = 0
        self.duration = 0
        self.syllables = 0

class PhraseObject:
    def __init__(self):
        self.measures = 0
        self.notes = 0
        self.duration = 0
        self.syllables = 0

class DataRecorder:
    xmlTag, xmlAttrib, xmlData = None, None, None

    def __init__(self):
        self.title, self.composer = None, None
        self.sectionObject = SectionObject()
        self.phraseObject = PhraseObject()
        self.sections, self.phrases = [], []
        self.completeCheck, self.lyricCheck, self.pitchCheck, self.puncCheck, self.capsCheck = False, False, False, False, False

    def start(self, xmlTag, xmlAttrib):
        self.xmlTag = xmlTag
        self.xmlAttrib = xmlAttrib

    def end(self, xmlTag):
        self.xmlTag = None
        self.xmlAttrib = None

    def data(self, xmlData):
        self.xmlData = xmlData
        if self.completeCheck == False:
            switchFunction = SwitchFunction(self.xmlTag, self.xmlAttrib, self.xmlData)
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
            #print(self.data)
            dataRecorder.title = self.data
        elif self.data == ('Petrucci'):
            dataRecorder.composer = self.data

    def MeasureCount(self):           
        if self.data == ('dashed'):
            dataRecorder.sectionObject.measures += 1
            dataRecorder.phraseObject.measures += 1
        elif self.data == ('light-light'):
            dataRecorder.sectionObject.measures += 1
            dataRecorder.phraseObject.measures += 1
            self.RecordSection()
            self.RecordPhrase()
        elif self.data == ('light-heavy'):
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
            dataRecorder.sectionObject.notes += 1
            dataRecorder.phraseObject.notes += 1
            dataRecorder.pitchCheck = False

    def PuncSwitch(self):
        punctuation = set(string.punctuation)
        if any(char in punctuation for char in self.data):
            dataRecorder.puncCheck = True

    def CapsCheck(self):
        if self.data.islower() == False and dataRecorder.puncCheck == True:
            # print(self.data)
            self.RecordPhrase()
        else:
            dataRecorder.capsCheck = False
            dataRecorder.puncCheck = False

    def CompleteSwitch(self):
        if str(self.attrib) == ("{'id': 'P1'}"):
            #print(self.attrib, "YES!")
            dataRecorder.completeCheck = False
        elif str(self.attrib) != ("{'id': 'P1'}"):
            dataRecorder.completeCheck = True
            #print(self.attrib, "NOPE!!")


    def FuncSwitch(self):
        switcher = {
            'credit-words': self.Info,
            'bar-style': self.MeasureCount,
            'lyric' : self.LyricSwitch,
            'text' : self.SyllableCount,
            'pitch' : self.PitchSwitch,
            'duration' : self.DurationCount,
            'part' : self.CompleteSwitch

            }
        return switcher.get(self.tag, lambda: "Error: Switch Function - FuncSwitch")()

    def RecordSection (self):
        dataRecorder.sections.append(dataRecorder.sectionObject)
        dataRecorder.sectionObject = SectionObject()

    def RecordPhrase (self):
        dataRecorder.phrases.append(dataRecorder.phraseObject)
        dataRecorder.sectionObject.phrases += 1
        dataRecorder.phraseObject = PhraseObject()
        dataRecorder.lyricCheck, dataRecorder.pitchCheck, dataRecorder.puncCheck, dataRecorder.capsCheck = False, False, False, False
    
def ProcessCorpus():
    print("Gathering Files")
    global dataRecorder

    for file in glob(r'E:/Documents/UNE/HUMS_301/MusicXML\*.musicxml'):
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

def SectionScatterPlot():
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    data, phrase = None, None
    frottala, sections, phrases, measures, notes, duration, syllables = [], [], [], [], [], [], []
    d = 0
    for data in corpusData:
        s = 0
        for phrase in corpusData[d].sections:
            frottala.append(d + 1)
            sections.append(s + 1)
            phrases.append(corpusData[d].sections[s].phrases)
            measures.append(corpusData[d].sections[s].measures)
            notes.append(corpusData[d].sections[s].notes)
            duration.append(corpusData[d].sections[s].duration)
            syllables.append(corpusData[d].sections[s].syllables)
            s += 1
        d += 1

    #print(x)
    #ax.scatter(frottala, sections, phrases, c='b', marker='o')
    ax.scatter(phrases, frottala, syllables, c='g', marker='o')
    #ax.scatter(frottala, sections, notes, c='y', marker='o')
    #ax.scatter(frottala, sections, duration, c='c', marker='o')
    #ax.scatter(frottala, sections, syllables, c='m', marker='o')

    ax.set_xlabel('phrases')
    ax.set_ylabel('frottala')
    ax.set_zlabel('syllables')

    plt.show()


def WriteSectionData():
    targetFile, columns, writer, frottala = None, None, None, None
    num, dec = 0, 0

    with open('sectionDataSet.csv', 'w', newline = '') as targetFile:
        columns = ['Frottala', 'Section', 'Phrases', 'Measures', 'Notes', 'Duration', 'Syllables']
        writer = csv.DictWriter(targetFile, fieldnames = columns)

        writer.writeheader()

        for frottala in corpusData:
            num += 1
            for value in frottala.sections:
                dec += 1
                writer.writerow({
                    'Frottala' : num,
                    'Section' : dec,
                    'Phrases' : value.phrases,
                    'Measures' : value.measures,
                    'Notes' : value.notes,
                    'Duration' : value.duration,
                    'Syllables' : value.syllables
                })
            dec = 0

def WritePhraseData():
    targetFile, columns, writer, frottala = None, None, None, None
    num, dec = 0, 0

    with open('phraseDataSet.csv', 'w', newline = '') as targetFile:
        columns = ['Frottala', 'Phrase', 'Measures', 'Notes', 'Duration', 'Syllables']
        writer = csv.DictWriter(targetFile, fieldnames = columns)

        writer.writeheader()

        for frottala in corpusData:
            num += 1
            for value in frottala.phrases:
                dec += 1
                writer.writerow({
                    'Frottala' : num,
                    'Phrase' : dec,
                    'Measures' : value.measures,
                    'Notes' : value.notes,
                    'Duration' : value.duration,
                    'Syllables' : value.syllables
                })
            dec = 0






global corpusData
corpusData = []
ProcessCorpus()
SectionScatterPlot()
#WriteSectionData()
#WritePhraseData()

