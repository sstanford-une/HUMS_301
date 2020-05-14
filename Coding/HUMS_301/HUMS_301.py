# Functions and Packages imported
import os
import string
import itertools
from music21 import *
from glob import glob
from lxml import *
from collections import Counter
from openpyxl import Workbook
import winsound
import ntpath

# Declaration of lists used in code
corpusTrees = []
corpusComposers = []
corpusTitles = []
corpusSyllables = []

syllableDictionary = []

# Declare the corpus used
projectCorpus = corpus.corpora.LocalCorpus()
projectCorpus.addPath('E:/Documents/UNE/HUMS_301/XML Files/MusicXML')

# Declare the spreadsheet where data will be recorded
workbook = Workbook()
sheet = workbook.active

# Collect corpus titles and place into list
def ProcessTitles():
    pieceTitle = ntpath.basename(file)
    corpusTitles.append(pieceTitle.replace('.musicxml', ''))

def ProcessSyllables():
    for syllable in root.iter('text'):
        corpusSyllables.append(syllable.text)

def CreateDictionary(inputList):
    return list(dict.fromkeys(inputList))

def CountMeasures():
    measures = 0
    for measure in root.iter('meaure'):
        print(measure.text)


def ProcessCorpus():
    print("Gathering Files")
    global file
    global root
    
    for file in glob(r'E:/Documents/UNE/HUMS_301/XML Files/MusicXML\*.musicxml'):
        tree = etree.parse(file)
        root = tree.getroot()

        ProcessTitles()
        ProcessSyllables()
        CountMeasures()

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
print(*corpusTitles, sep = ", ")
syllableDictionary = CreateDictionary(corpusSyllables)
print(*syllableDictionary, sep = ", ")

