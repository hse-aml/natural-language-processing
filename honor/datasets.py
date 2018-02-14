# Copyright 2015 Conchylicultor. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

import ast
import os
import random
import re
from time import time

import nltk
from tqdm import tqdm

"""
Load the cornell movie dialog corpus.

Available from here:
http://www.cs.cornell.edu/~cristian/Cornell_Movie-Dialogs_Corpus.html

"""

class CornellData:
    """

    """

    def __init__(self, dirName):
        """
        Args:
            dirName (string): directory where to load the corpus
        """
        self.lines = {}
        self.conversations = []

        MOVIE_LINES_FIELDS = ["lineID","characterID","movieID","character","text"]
        MOVIE_CONVERSATIONS_FIELDS = ["character1ID","character2ID","movieID","utteranceIDs"]

        self.lines = self.loadLines(os.path.join(dirName, "movie_lines.txt"), MOVIE_LINES_FIELDS)
        self.conversations = self.loadConversations(os.path.join(dirName, "movie_conversations.txt"), MOVIE_CONVERSATIONS_FIELDS)

        # TODO: Cleaner program (merge copy-paste) !!

    def loadLines(self, fileName, fields):
        """
        Args:
            fileName (str): file to load
            field (set<str>): fields to extract
        Return:
            dict<dict<str>>: the extracted fields for each line
        """
        lines = {}

        with open(fileName, 'r', encoding='iso-8859-1') as f:  # TODO: Solve Iso encoding pb !
            for line in f:
                values = line.split(" +++$+++ ")

                # Extract fields
                lineObj = {}
                for i, field in enumerate(fields):
                    lineObj[field] = values[i]

                lines[lineObj['lineID']] = lineObj

        return lines

    def loadConversations(self, fileName, fields):
        """
        Args:
            fileName (str): file to load
            field (set<str>): fields to extract
        Return:
            list<dict<str>>: the extracted fields for each line
        """
        conversations = []

        with open(fileName, 'r', encoding='iso-8859-1') as f:  # TODO: Solve Iso encoding pb !
            for line in f:
                values = line.split(" +++$+++ ")

                # Extract fields
                convObj = {}
                for i, field in enumerate(fields):
                    convObj[field] = values[i]

                # Convert string to list (convObj["utteranceIDs"] == "['L598485', 'L598486', ...]")
                lineIds = ast.literal_eval(convObj["utteranceIDs"])

                # Reassemble lines
                convObj["lines"] = []
                for lineId in lineIds:
                    convObj["lines"].append(self.lines[lineId])

                conversations.append(convObj)

        return conversations

    def getConversations(self):
        return self.conversations


# Based on code from https://github.com/AlJohri/OpenSubtitles
# by Al Johri <al.johri@gmail.com>

import xml.etree.ElementTree as ET
import datetime
import os
import sys
import json
import re
import pprint

from gzip import GzipFile

"""
Load the opensubtitles dialog corpus.
"""

class OpensubsData:
    """
    """

    def __init__(self, dirName):
        """
        Args:
            dirName (string): directory where to load the corpus
        """

        # Hack this to filter on subset of Opensubtitles
        # dirName = "%s/en/Action" % dirName

        print("Loading OpenSubtitles conversations in %s." % dirName)
        self.conversations = []
        self.tag_re = re.compile(r'(<!--.*?-->|<[^>]*>)')
        self.conversations = self.loadConversations(dirName)

    def loadConversations(self, dirName):
        """
        Args:
            dirName (str): folder to load
        Return:
            array(question, answer): the extracted QA pairs
        """
        conversations = []
        dirList = self.filesInDir(dirName)
        for filepath in tqdm(dirList, "OpenSubtitles data files"):
            if filepath.endswith('gz'):
                try:
                    doc = self.getXML(filepath)
                    conversations.extend(self.genList(doc))
                except ValueError:
                    tqdm.write("Skipping file %s with errors." % filepath)
                except:
                    print("Unexpected error:", sys.exc_info()[0])
                    raise
        return conversations

    def getConversations(self):
        return self.conversations

    def genList(self, tree):
        root = tree.getroot()

        timeFormat = '%H:%M:%S'
        maxDelta = datetime.timedelta(seconds=1)

        startTime = datetime.datetime.min
        strbuf = ''
        sentList = []

        for child in root:
            for elem in child:
                if elem.tag == 'time':
                    elemID = elem.attrib['id']
                    elemVal = elem.attrib['value'][:-4]
                    if elemID[-1] == 'S':
                        startTime = datetime.datetime.strptime(elemVal, timeFormat)
                    else:
                        sentList.append((strbuf.strip(), startTime, datetime.datetime.strptime(elemVal, timeFormat)))
                        strbuf = ''
                else:
                    try:
                        strbuf = strbuf + " " + elem.text
                    except:
                        pass

        conversations = []
        for idx in range(0, len(sentList) - 1):
            cur = sentList[idx]
            nxt = sentList[idx + 1]
            if nxt[1] - cur[2] <= maxDelta and cur and nxt:
                tmp = {}
                tmp["lines"] = []
                tmp["lines"].append(self.getLine(cur[0]))
                tmp["lines"].append(self.getLine(nxt[0]))
                if self.filter(tmp):
                    conversations.append(tmp)

        return conversations

    def getLine(self, sentence):
        line = {}
        line["text"] = self.tag_re.sub('', sentence).replace('\\\'','\'').strip().lower()
        return line

    def filter(self, lines):
        # Use the followint to customize filtering of QA pairs
        #
        # startwords = ("what", "how", "when", "why", "where", "do", "did", "is", "are", "can", "could", "would", "will")
        # question = lines["lines"][0]["text"]
        # if not question.endswith('?'):
        #     return False
        # if not question.split(' ')[0] in startwords:
        #     return False
        #
        return True

    def getXML(self, filepath):
        fext = os.path.splitext(filepath)[1]
        if fext == '.gz':
            tmp = GzipFile(filename=filepath)
            return ET.parse(tmp)
        else:
            return ET.parse(filepath)

    def filesInDir(self, dirname):
        result = []
        for dirpath, dirs, files in os.walk(dirname):
            for filename in files:
                fname = os.path.join(dirpath, filename)
                result.append(fname)
        return result


def extractText(line, fast_preprocessing=True):
    if fast_preprocessing:
        GOOD_SYMBOLS_RE = re.compile('[^0-9a-z ]')
        REPLACE_BY_SPACE_RE = re.compile('[/(){}\[\]\|@,;#+_]')
        REPLACE_SEVERAL_SPACES = re.compile('\s+')

        line = line.lower()
        line = REPLACE_BY_SPACE_RE.sub(' ', line)
        line = GOOD_SYMBOLS_RE.sub('', line)
        line = REPLACE_SEVERAL_SPACES.sub(' ', line)
        return line.strip()
    else:
        return nltk.word_tokenize(line)


def splitConversations(conversations, max_len=20, fast_preprocessing=True):
    data = []
    for i, conversation in enumerate(tqdm(conversations)):
        lines = conversation['lines']
        for i in range(len(lines) - 1):
            request = extractText(lines[i]['text'])
            reply = extractText(lines[i + 1]['text'])
            if 0 < len(request) <= max_len and 0 < len(reply) <= max_len:
                data += [(request, reply)]
    return data


def readCornellData(path, max_len=20, fast_preprocessing=True):
    dataset = CornellData(path)
    conversations = dataset.getConversations()
    return splitConversations(conversations, max_len=max_len, fast_preprocessing=fast_preprocessing)


def readOpensubsData(path, max_len=20, fast_preprocessing=True):
    dataset = OpensubsData(path)
    conversations = dataset.getConversations()
    return splitConversations(conversations, max_len=max_len, fast_preprocessing=fast_preprocessing)
