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


class FrottalaObject:
    def __init__(self, title, composer, sections, phrases, cadences):
        self.title = title
        self.composer = composer
        self.sections = sections
        self.phrases = phrases
        self.cadences = cadences

class SectionObject:
    def __init__(self):
        self.phrases = 0
        self.measures = 0
        self.notes = 0
        self.syllables = 0
        self.cadenes = 0

class PhraseObject:
    def __init__(self):
        self.measures = 0
        self.notes = 0
        self.syllables = 0

class PartObject:
    def __init__(self):
        self.step = []
        self.octave = []
        self.duration = []
        self.compiled = []

class DataRecorder:
    xmlTag, xmlAttrib, xmlData = None, None, None

    def __init__(self):
        self.title, self.composer = None, None
        self.sectionObject = SectionObject()
        self.phraseObject = PhraseObject()
        self.partObjects = [None, None, None, None] 
        self.partTarget = 0
        self.sections, self.phrases, self.cadences = [], [], []
        self.currentMeasure, self.previousPhraseEnd, self.previousSectionEnd = 0, 0, 0
        self.lyricCheck, self.pitchCheck, self.puncCheck, self.capsCheck, self.restCheck = False, False, False, False, False

    def start(self, xmlTag, xmlAttrib):
        self.xmlTag = xmlTag
        self.xmlAttrib = xmlAttrib

    def end(self, xmlTag):
        self.xmlTag = None
        self.xmlAttrib = None

    def data(self, xmlData):
        self.xmlData = xmlData
        switchFunction = SwitchFunction(self.xmlTag, self.xmlAttrib, self.xmlData)
        switchFunction.FuncSwitch()
        
    def close(self):
        frottalaObject = FrottalaObject(self.title, self.composer, self.sections, self.phrases, self.cadences)
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

    def MeasureCounter(self):
        dataRecorder.currentMeasure = self.attrib.get('number', '0')

    def MeasureRecorder(self):
        if self.data == ('light-light', 'light-heavy'):
            dataRecorder.sectionObject.measures = (int(dataRecorder.currentMeasure) - int(dataRecorder.previousSectionEnd))
            dataRecorder.phraseObject.measures = (int(dataRecorder.currentMeasure) - int(dataRecorder.previousPhraseEnd))
            dataRecorder.previousSectionEnd, dataRecorder.previousPhraseEnd = dataRecorder.currentMeasure, dataRecorder.currentMeasure
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

    def PuncSwitch(self):
        punctuation = set(string.punctuation)
        if any(char in punctuation for char in self.data):
            dataRecorder.puncCheck = True

    def CapsCheck(self):
        if self.data.islower() == False and dataRecorder.puncCheck == True:
            dataRecorder.phraseObject.measures = (int(dataRecorder.currentMeasure) - int(dataRecorder.previousPhraseEnd))
            dataRecorder.previousPhraseEnd = dataRecorder.currentMeasure
            self.RecordPhrase()
        else:
            dataRecorder.capsCheck = False
            dataRecorder.puncCheck = False

    def PartSwitch(self):
        if str(self.attrib) == ("{'id': 'P1'}"):
            dataRecorder.partTarget = 0
            #print('Recording P1')
        elif str(self.attrib) == ("{'id': 'P2'}"):
            dataRecorder.partTarget = 1
            #print('Recording P2')
        elif str(self.attrib) == ("{'id': 'P3'}"):
            dataRecorder.partTarget = 2
            #print('Recording P3')
        elif str(self.attrib) == ("{'id': 'P4'}"):
            dataRecorder.partTarget = 3
            #print('Recording P4')
        dataRecorder.partObjects[dataRecorder.partTarget] = PartObject()

    def DurationCheck(self):
        rawValue = int(self.data)
        newValue = 1
        while rawValue > 64:
            newValue += 1
            rawValue -= 64
        dataRecorder.partObjects[dataRecorder.partTarget].duration.append(newValue)
        self.RestCheck()

    def RestCheck(self):
        if dataRecorder.restCheck == True:
            dataRecorder.partObjects[dataRecorder.partTarget].step.append('R')
            dataRecorder.partObjects[dataRecorder.partTarget].octave.append('R')
        else:
            dataRecorder.restCheck = True
    
    def StepCheck(self):
        dataRecorder.restCheck = False
        dataRecorder.partObjects[dataRecorder.partTarget].step.append(self.data)

    def OctaveCheck(self):
        dataRecorder.partObjects[dataRecorder.partTarget].octave.append(self.data)

    def FuncSwitch(self):
        switcher = {
            'credit-words': self.Info,
            'measure': self.MeasureCounter,
            'lyric' : self.LyricSwitch,
            'text' : self.SyllableCount,
            'pitch' : self.PitchSwitch,
            'part' : self.PartSwitch,
            'bar-style' : self.MeasureRecorder,
            'step' : self.StepCheck,
            'octave' : self.OctaveCheck,
            'duration' : self.DurationCheck,
            'rest' : self.RestCheck
            }
        return switcher.get(self.tag, lambda: "Error: Switch Function - FuncSwitch")()

    def RecordSection (self):
        #print('Section length = ', dataRecorder.sectionObject.measures)
        dataRecorder.sections.append(dataRecorder.sectionObject)
        dataRecorder.sectionObject = SectionObject()

    def RecordPhrase (self):
        #print('Phrase length = ', dataRecorder.phraseObject.measures)
        dataRecorder.phrases.append(dataRecorder.phraseObject)
        dataRecorder.sectionObject.phrases += 1
        dataRecorder.phraseObject = PhraseObject()
        dataRecorder.lyricCheck, dataRecorder.pitchCheck, dataRecorder.puncCheck, dataRecorder.capsCheck = False, False, False, False

class PartAnalyser:
    def __init__(self, partData):
        self.partData = partData
        self.partLists = []
        self.intervalLists = []

    def CompileLists(self):
        
        tarPart = 0
        partPitches = []
        if tarPart < 4:
            dataPosition = 0
            dataLength = len(self.partData[tarPart].step)
            while dataPosition < dataLength:
                step = str(self.partData[tarPart].step[dataPosition]).lower()
                octave = str(self.partData[tarPart].octave[dataPosition])
                duration = int(self.partData[tarPart].duration[dataPosition])
                finalNote = [step + octave]
                partPitches.extend(finalNote * duration)
                dataPosition += 1
            self.partLists.append(partPitches)
            print(len(partPitches))
            tarPart += 1
        else:
            tarPart = 0
        #self.MeasureIntervals()

    def MeasureIntervals(self):
        part1, part2, part3, part4 = self.partLists[0], self.partLists[1], self.partLists[2], self.partLists[3]
        print(part1, part2, part3, part4)
        
        dataPosition = 0
        dataLength = len(part1)

        while dataPosition < dataLength:
            if part1[dataPosition] != 'rR':
                p1 = pitch.Pitch(str(part1[dataPosition]))
            else:
                p1 = None
            if part2[dataPosition] != 'rR':
                p2 = pitch.Pitch(str(part2[dataPosition]))
            else:
                p2 = None
            if part3[dataPosition] != 'rR':
                p3 = pitch.Pitch(str(part3[dataPosition]))
            else:
                p3 = None
            if part4[dataPosition] != 'rR':
                p4 = pitch.Pitch(str(part4[dataPosition]))
            else:
                p4 = None
            #print(p1, p2, p3, p4)
            dataPosition += 1
    
def ProcessCorpus():
    print("Gathering Files")
    global dataRecorder

    for file in glob(r'E:/Documents/UNE/HUMS_301.2/Corpus/Corpus_XML\*.xml'):
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

class ChordAnalyser:
    def __init__(self):
        self.corpusChordList = []
        self.corpusLastFive = []
        self.corpusRootLists = []
        self.corpusIntList = []
        self.cadences = []

    def CollectChords(self):
        print('Collecting chords...')
        projectCorpus = corpus.corpora.LocalCorpus()
        projectCorpus.addPath('E:/Documents/UNE/HUMS_301.2/Corpus/Corpus_XML')
        count = 0
        for file in glob(r'E:/Documents/UNE/HUMS_301.2/Corpus/Corpus_XML\*.xml'):
            chordList = []
            currentFile = corpus.parse(file)
            target = currentFile.chordify()
            for chord in target.recurse().getElementsByClass('Chord'):
                chordList.append(chord)
            self.corpusChordList.append(chordList)
        print('Chords collected!')
        print(count)
        self.CompileLastFive()

    def CompileLastFive(self):
        print("Compiling 'Last Five' lists...")
        for chordList in self.corpusChordList:
            lastFive = []
            target = (len(chordList) - 5)
            while target < len(chordList):
                lastFive.append(chordList[target])
                target += 1
            #print(lastFive)
            self.corpusLastFive.append(lastFive)
        print('Lists Compiled!')
        self.AnalyseChordMotion()

    def AnalyseChordMotion(self):
        print('Analysing chord motion...')
        for chords in self.corpusLastFive:
            rList = []
            iList = []
            target = 0
            while target < 5:
                rList.append(chords[target].root())
                target += 1
            #print(rootList)
            self.corpusRootLists.append(rList)
            pTar1, pTar2 = 0, 1
            while pTar2 < 5:
                iStart = rList[pTar1]
                iFinish = rList[pTar2]
                iValue = interval.Interval(noteStart = iStart, noteEnd = iFinish)
                iList.append(iValue.simpleName)
                pTar1 += 1
                pTar2 += 1
            #print(iList)
            cadenceObject = CadenceObject(iList[0], iList[1], iList[2], iList[3])
            #print(cadenceObject.int1)
            self.cadences.append(cadenceObject)
        print('Motion analysed!')
        self.WriteMotionData()

    def WriteMotionData(self):
        print("Writing 'motionDataSet.csv'")
        targetFile, columns, writer, = None, None, None

        with open('motionDataSet.csv', 'w', newline = '') as targetFile:
            columns = ['Int 1', 'Int 2', 'Int 3', 'Int 4']
            writer = csv.DictWriter(targetFile, fieldnames = columns)

            writer.writeheader()

            for cadence in self.cadences:                
                writer.writerow({
                    'Int 1' : cadence.int1,
                    'Int 2' : cadence.int2,
                    'Int 3' : cadence.int3,
                    'Int 4' : cadence.int4
                })
        print('File complete!')
        self.CountIntervals()

    def CountIntervals(self):
        print('Calculating interval data...')
        int1List, int2List, int3List, int4List = [], [], [], []
        with open('motionDataSet.csv','r') as targetFile:
            lines = targetFile.readlines()
        for line in lines:
            data = line.split(',')
            int1List.append(data[0])
            int2List.append(data[1])
            int3List.append(data[2])
            int4List.append(data[3])
        count1, count2, count3, count4 = Counter(int1List), Counter(int2List), Counter(int3List), Counter(int4List)
        with open('IntCount_1.csv', 'w') as targetFile:  
            writer = csv.writer(targetFile)
            for key, value in count1.items():
               writer.writerow([key, value])
        with open('IntCount_2.csv', 'w') as targetFile:  
            writer = csv.writer(targetFile)
            for key, value in count2.items():
               writer.writerow([key, value])
        with open('IntCount_3.csv', 'w') as targetFile:  
            writer = csv.writer(targetFile)
            for key, value in count3.items():
               writer.writerow([key, value])
        with open('IntCount_4.csv', 'w') as targetFile:  
            writer = csv.writer(targetFile)
            for key, value in count4.items():
               writer.writerow([key, value])
        print('Interval data complete!')


class CadenceObject:
    def __init__(self, int1, int2, int3, int4):
        self.int1 = int1
        self.int2 = int2
        self.int3 = int3
        self.int4 = int4

global corpusData
corpusData = []
#ProcessCorpus()
chordAnalyser = ChordAnalyser()
chordAnalyser.CollectChords()
#WriteSectionData()
#WritePhraseData()

