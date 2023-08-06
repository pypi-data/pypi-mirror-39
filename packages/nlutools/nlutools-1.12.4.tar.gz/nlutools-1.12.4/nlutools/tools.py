from rpc_client import *
from config import *
from utils import *

import subprocess

# Segment
def cut(sentence,pos=True,cut_all=False,mode='fast'):
    try:
        if mode in ['fast','accurate'] and pos in [True,False] and cut_all in [True,False]:
            data={'text':sentence,'mode':mode,'pos':pos,'cut_all':cut_all}
            return doTask(mapConf['cut'],'segmentor',data)
        else:
            raiseException('Advise:check parameters,make sure value of mode is fast or default , value of pos is true,false or default as well')
    except Exception as e:
            raiseException('%s exception \nplease contact supportor %s for this exception ! \n%s'%('segmentor',supportConf['cut'],e))

# Word2Vector
def getW2VFile(version_key,localpath):
    try:
        if not version_key or not version_key.strip():
            cat = subprocess.Popen(['hadoop', 'fs', '-cat', mapConf['w2v_hdfs_version_file']], stdout=subprocess.PIPE)
            for line in cat.stdout:
                version_key=bytes.decode(line).strip()
                break;
        if version_key and version_key.strip():
            try:
                subprocess.call(['hadoop','fs','-get',mapConf['w2v_hdfs_dir']+version_key.lower(),localpath])
            except Exception as e:
                raiseException('%s exception \nplease contact supportor %s for this exception ! \n%s'%('w2v',supportConf['w2v'],e))
    except Exception as e:
        if 'command not found' in str(e):
            raise Exception('Advise: please install hadoop client before use getW2VFile')

def getWordVec(word):
    try:
        if isinstance(word,str):
            word = [word]
        data = {'words':word}
        return doTask(mapConf['w2v'],'w2v',data)
    except Exception as e:
        raiseException('%s exception \nplease contact supportor %s for this exception ! \n%s'%('w2v',supportConf['w2v'],e))

def getMostSimiWords(word,topn=10):
    try:
        data = {'words':word,'topn':topn}
        return doTask(mapConf['w2v'],'w2v',data)
    except Exception as e:
        raiseException('%s exception \nplease contact supportor %s for this exception ! \n%s'%('w2v',supportConf['w2v'],e))

def getCharacterVec(character):
    pass

# Sentence2Vector
def getSentenceVec(sentences):
    try:
        if isinstance(sentences,list):
            data = {'senlist':sentences}
            return doTask(mapConf['s2v'],'sentencevec',data)
        return None
    except Exception as e:
        raiseException('%s exception \nplease contact supportor %s for this exception ! \n%s'%('s2v',supportConf['s2v'],e))
    
# LanguageModel

# EmotionParser
def predictEmotion(sentences, prob=False):
    try:
        if sentences:
            data = {'text':sentences,'prob':prob}
            return doTask(mapConf['emotion'],'sentiment',data)
        return None
    except Exception as e:
        raiseException('%s exception \nplease contact supportor %s for this exception ! \n%s'%('emotion',supportConf['emotion'],e))

# SentenceSpliter
def getSubSentences(sentence,mode=0):
    try:
        if mode == 0 or mode == 1:
            data={'sentence':sentence,'mode':mode}
            return doTask(mapConf['sentence_spliter'],'sentence_spliter',data)
        else:
            raiseException('Advise: make sure value of mode is 0 or 1')
    except Exception as e:
        raiseException('%s exception \nplease contact supportor %s for this exception ! \n%s'%('sentence',supportConf['sentence'],e))

#EntityParser

#SentenceTypeParser




