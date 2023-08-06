from tnthai.swathclone.SC import SwathC
from tnthai.swathclone.SC import SwathDicTrie 
from tnthai.swathclone.SC import SwathSegmentAlgorithm 

def SafeSegment(text):
    segmenter = SwathC(SwathDicTrie, SwathSegmentAlgorithm)
    return segmenter.Segment(text,"Safe")

def UnsafeSegment(text):
    segmenter = SwathC(SwathDicTrie, SwathSegmentAlgorithm)
    return segmenter.Segment(text,"Unsafe")

def SmartSegment(text):
    segmenter = SwathC(SwathDicTrie, SwathSegmentAlgorithm)
    return segmenter.Segment(text,"Smart")

def SafeSegmentBounding(text):
    segmenter = SwathC(SwathDicTrie, SwathSegmentAlgorithm)
    return segmenter.Segment(text,"SafeBounding")