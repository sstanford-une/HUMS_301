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


global currentTag, currentAttrib, currentData
global titleData, composerData


class FrottalaObject:
    def __init__(frot, title, composer, text, measures, sections, phrases):
        frot.title = title
        frot.composer = composer
        frot.text = text
        frot.measures = measures
        frot.sections = sections
        frot.phrases = phrases

        print(frot.title, " by ", frot.composer, " has been recorded.")

    # return super().__init__(*args, **kwargs)


class DataRecorder:
    title = None
    composer = None
    tag = None
    attrib = None
    data = None
    def start(self, tag, attrib):
        self.tag = tag
        self.attrib = attrib

    def end(self, tag):
        self.tag = None
        self.attrib = None

    def data(self, data):
        self.data = data
        switchFunction = SwitchFunction(self.tag, self.attrib, self.data)
        switchFunction.FuncSwitch()
        
        #SwitchFunction.dataFunction()
        #if self.currentTag == 'credit-words':
         #   if data != ('Petrucci'):
          #      self.title = data
           # elif data == ('Petrucci'):
            #    self.composer = data

    def close(self):
        print(self.title, 'was composed by', self.composer)


class SwitchFunction:
    def __init__(self, tag, attrib, data):
        self.tag = tag
        self.attrib = attrib
        self.data = data

    def Info(self):
        if self.data != ('Petrucci'):
            DataRecorder.title = self.data
        elif self.data == ('Petrucci'):
            DataRecorder.composer = self.data

    def FuncSwitch(self):
        switcher = {
            'credit-words': self.Info
            }
        return switcher.get(self.tag, lambda: "Error: Switch Function - FuncSwitch")()

class SectionRecorder:
    def __init__(section, measureCount, syllableCount, noteCount, phraseCount, barline):
        section.measureCount = measureCount
        section.syllableCount = syllableCount
        section.noteCount = noteCount


# Declaration of lists used in code
corpusSyllables = []
frotSyllables = []
dataLibrary = []
syllableDictionary = []

# Declare the corpus used
projectCorpus = corpus.corpora.LocalCorpus()
projectCorpus.addPath('E:/Documents/UNE/HUMS_301/XML Files/MusicXML')

# Declare the spreadsheet where data will be recorded
# workbook = Workbook()
# sheet = workbook.active

# Collect corpus titles and place into list
def ProcessTitle():
    filename = ntpath.basename(file)
    frotTitle = pieceTitle.replace('.musicxml', '')

def ProcessComposer():
    for composer in root.iter('creator'):
        frotComposer = composer.text


def ProcessSyllables():
    for syllable in root.iter('text'):
        corpusSyllables.append(syllable.text)
        frotSyllables.append(syllable.text)


def CreateDictionary(inputList):
    return list(dict.fromkeys(inputList))

# def RecordSection():

def CountMeasures():
    measureCount = 0
    sectionMeasureCount = 0

    frotMeasureData = [0]
    frotSectionData = []
    for measure in root.iter('measure'):
        if int(measure.get('number')) > measureCount:
            measureCount = int(measure.get('number'))
    frotMeasureData.append(frotBarCount)

    for barline in root.iter('bar-style'):
        sectionData = []
        if barline.text == 'dashed':
            measureCount += 1
        elif barline.text != 'dashed' and barline.text != 'light-heavy':
            sectionData = [sectionBarCount, barline.text]
            frotSectionData.append(sectionData)
        elif barline.text == 'light-heavy':
            sectionData = [sectionBarCount, barline.text]
            frotSectionData.append(sectionData)
            break
    
        section = SectionRecorder()

    frotData.append(frotMeasureData)
    


def ProcessCorpus():
    print("Gathering Files")
    global root, frotData, frotTitle, frotComposer, frotMeasures, frotPhrases
    
    for file in glob(r'E:/Documents/UNE/HUMS_301/XML Files/MusicXML\*.musicxml'):
        tree = etree.parse(file)
        root = tree.getroot()
        xmlString = etree.tostring(root, encoding="UTF-8", method='xml')
        # frotData[name, composer, measures]
        frotData = []
        frottalaData = DataRecorder()
        parser = XMLParser(target = frottalaData)
        parser.feed(xmlString)
        parser.close()
        #ProcessTitle()
        #ProcessComposer()
        #CountMeasures()
        #ProcessSyllables()
        #dataLibrary.append(frotData)

    print('Corpus procssing compelete!')

def ProgressReport():
	global progress
	progress += 1
	print("Files Processed: ", progress, "/62")

def ProgressReset():
	global progress
	progress = 0

# Initate functions in sequence
ProcessCorpus()
# print(*corpusTitles, sep = ", ")
syllableDictionary = CreateDictionary(corpusSyllables)
# print(*syllableDictionary, sep = ", ")
print(len(dataLibrary))
# print(len(frotData[0][2][1]))
#x = FrottalaObject('Poop', [1, 2, 3])

