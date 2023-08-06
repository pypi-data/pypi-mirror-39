#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import AbstractWordSegment as AWS
import os, sys
import datrie
import string
#import cProfile
#import Timecount
import json

sys.setrecursionlimit(1000000)

class SwathDicTrie(AWS.PrototypeGramTrie):
    def __init__(self, ):
        #Initialize GramTrie
        self.Trie = datrie.Trie.load(os.path.dirname(os.path.abspath(__file__))+'/my.trie')

#SegmentAlgorithm class
class SwathSegmentAlgorithm(AWS.PrototypeSegmentAlgorithm):
    def __init__(self, ):
        self.globalResult = list()
        self.result = list()
        self.failSegmentRemainText = []
        
    def Segmenting(self, InputString, GramTrie):
        Mode = "Safe"
        self.inputWord = InputString.decode('utf-8')
        
        #call recursive Segment_safe to find only first result
        self.Segment_safe(InputString.decode('utf-8'), GramTrie)
        #clone result from temp
        result = list(self.globalResult)
        #empty blacklist
        self.failSegmentRemainText = []
        #if no result in safe
        if len(result) == 0:
            Mode = "Unsafe"
            #do unsafe segment
            self.Segment_unsafe(InputString.decode('utf-8'), GramTrie)
            #clone result from temp
            result = list(self.globalResult)
        
        '''Mode = "Unsafe"
        #do unsafe segment
        self.Segment_unsafe(InputString.decode('utf-8'), GramTrie)
        #clone result from temp
        result = list(self.globalResult)
        '''
        #clear global Temp result
        self.globalResult = list()
        
        return result, Mode
    
    def Segment_safe(self, remainText, trie):
        #if remainText in cache fail so not trying segment
        if remainText in self.failSegmentRemainText:
            return False
        #To get only first result
        if len(self.globalResult) > 0:
            return
        
        #this always be true
        assert ("".join(self.result) + remainText) == self.inputWord
        
        if len(remainText) > 0:
            FirstChar = remainText[0]
            if self.isLeadingChar(FirstChar):
                Prefixes = trie.prefixes(remainText)
                resultOrCount = False
                
                for i in range(len(Prefixes)-1,-1,-1):
                    selectedPrefix = Prefixes[i]
                    self.result.append(selectedPrefix)
                    suffixRemainText = remainText[len(selectedPrefix):]
                    prefixResult = self.Segment_safe(suffixRemainText, trie)
                    self.result.pop()
                    resultOrCount = resultOrCount or prefixResult
                
                if resultOrCount == False:
                    self.failSegmentRemainText.append(remainText)
                
            else:
                if FirstChar in string.ascii_letters+string.digits+string.printable:
                    # is leading with punctuation
                    if FirstChar in string.punctuation:
                        j = 0
                        while remainText[j] in string.punctuation:
                            j+=1
                            if len(remainText) == j:
                                break
                        self.result.append(remainText[:j])
                        self.Segment_safe(remainText[j:], trie)
                        self.result.pop()
                        
                    
                    # is whitespace
                    if FirstChar in string.whitespace:
                        j = 0
                        while remainText[j] in string.whitespace:
                            j+=1
                            if len(remainText) == j:
                                break
                        self.result.append(remainText[:j])
                        self.Segment_safe(remainText[j:], trie)
                        self.result.pop()
                        
                    # is digit
                    if FirstChar in string.digits:
                        j = 0
                        while remainText[j] in string.digits:
                            j+=1
                            if len(remainText) == j:
                                break
                        self.result.append(remainText[:j])
                        self.Segment_safe(remainText[j:], trie)
                        self.result.pop()
                        
                    # is english char
                    if FirstChar in string.ascii_letters:
                        j = 0
                        while remainText[j] in string.ascii_letters:
                            j+=1
                            if len(remainText) == j:
                                break
                        self.result.append(remainText[:j])
                        self.Segment_safe(remainText[j:], trie)
                        self.result.pop()
                else:
                    #in case other langauge , skip letter by letter
                    self.result.append(remainText[0])
                    self.Segment_safe(remainText[1:], trie)
                    self.result.pop()
        else:
            #all remainText consume so. get the segmenting result
            self.globalResult.append(list(self.result))
       
    def Segment_unsafe(self, remainText, trie):
        #To get only first result
        if len(self.globalResult) > 0:
            return
    
        #this always be true
        assert ("".join(self.result) + remainText) == self.inputWord
        
        if len(remainText) > 0:
            FirstChar = remainText[0]
            if self.isLeadingChar(FirstChar):
                Prefixes = trie.prefixes(remainText)
                for i in range(len(Prefixes)-1,-1,-1):
                    self.result.append(Prefixes[i])
                    self.Segment_unsafe(remainText[len(Prefixes[i]):], trie)
                    self.result.pop()
                j=0
                unsafePrefixes=""
                while j<len(remainText):
                    Prefixes = trie.prefixes(remainText[j:])
                    j=j+1
                    if len(Prefixes)>0 :
                        unsafePrefixes=remainText[:j-1]
                        break
                    else:
                        unsafePrefixes=remainText[:j]
                    if j==len(remainText):
                        unsafePrefixes = remainText
                        break
                    if not self.isLeadingChar(remainText[j]):
                        unsafePrefixes = remainText[:j]
                        break
                self.result.append(unsafePrefixes)
                self.Segment_unsafe(remainText[len(unsafePrefixes):], trie)
                self.result.pop()
            else:
                if FirstChar in string.ascii_letters+string.digits+string.printable:
                    # is leading with punctuation
                    if FirstChar in string.punctuation:
                        j = 0
                        while remainText[j] in string.punctuation:
                            j+=1
                            if len(remainText) == j:
                                break
                        self.result.append(remainText[:j])
                        self.Segment_unsafe(remainText[j:], trie)
                        self.result.pop()
                        
                    
                    # is whitespace
                    if FirstChar in string.whitespace:
                        j = 0
                        while remainText[j] in string.whitespace:
                            j+=1
                            if len(remainText) == j:
                                break
                        self.result.append(remainText[:j])
                        self.Segment_unsafe(remainText[j:], trie)
                        self.result.pop()
                        
                    # is digit
                    if FirstChar in string.digits:
                        j = 0
                        while remainText[j] in string.digits:
                            j+=1
                            if len(remainText) == j:
                                break
                        self.result.append(remainText[:j])
                        self.Segment_unsafe(remainText[j:], trie)
                        self.result.pop()
                        
                    # is english char
                    if FirstChar in string.ascii_letters:
                        j = 0
                        while remainText[j] in string.ascii_letters:
                            j+=1
                            if len(remainText) == j:
                                break
                        self.result.append(remainText[:j])
                        self.Segment_unsafe(remainText[j:], trie)
                        self.result.pop()
                else:
                    self.result.append(remainText[0])
                    self.Segment_unsafe(remainText[1:], trie)
                    self.result.pop()
        else :
            self.globalResult.append(list(self.result))
                    
    def isLeadingChar(self, ch):
        #0E4E 0e4F 0e5a 0e5b
        thai_unicode_char = u'กขฃคฅฆงจฉชซฌญฎฏฐฑฒณดตถทธนบปผฝพฟภมยรฤลฦวศษสหฬอฮฯะ ัาำ ิ ี ึ ื ุ ู ฺ ฿เแโใไๅๆ ็ ่ ้ ๊ ๋ ์ ํ ๐๑๒๓๔๕๖๗๘๙' + u"\u0e4e\u0e4f\u0e5a\u0e5b"
        return ch in thai_unicode_char.replace(" ","")
        #return ch in u'กขฃคฅฆงจฉชซฌญฎฏฐฑฒณดตถทธนบปผฝพฟภมยรลวศศษสหฬอฮะึาิูแุีเัโไใ ่ ้ ๊ ๋ ำ็ฤ์ฦํฯืๆ ฺ '.replace(" ","")
        #return ord(ch) >= ord('ก'.decode('utf-8')) and  ord(ch) <= ord('ฮ'.decode('utf-8'))

    
#Putting altogether GramTrie and SegmentAlgorithm to function as Segmentation
class SwathClone(AWS.PrototypeGramSegment):
    def __init__(self, GramTrieClass, SegmentAlgorithmClass):
        self.GramTrie = GramTrieClass()
        self.SegmentAlgorithm = SegmentAlgorithmClass()
        #also assert if trying to create other type of class
        assert isinstance(self.GramTrie, AWS.AbstractGramTrie)
        assert isinstance(self.SegmentAlgorithm, AWS.AbstractSegmentAlgorithm)
    
    def Segment(self, toBeSegmentInput):
        #Call SegmentAlgorithm to segment by passing GramTrie
        result, Mode = self.SegmentAlgorithm.Segmenting(toBeSegmentInput, self.GramTrie.Trie)
        return result, Mode

if __name__ == '__main__':
    #example of calling WordSegment
    WordSegment = SwathClone(SwathDicTrie,SwathSegmentAlgorithm)
   
    #text = sys.argv[1]
    f = open("./src/tnthai/swathclone/tests/rawpdftext","r")

    text = "".join(f.readlines())

    result, mode = WordSegment.Segment(text)
    jsonResult = {}
    jsonResult["Result"] = mode
    Solutions = []
    for segs in result:
        res = []
        for seg in segs:
            res.append(seg)
        Solutions.append(res)
    jsonResult["Solutions"]=Solutions
    
    print json.dumps(jsonResult)
    
