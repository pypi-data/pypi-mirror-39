from .rpc_client import *
from .config import *
from .utils import *

import subprocess

# Segment
def cut(sentence,mode='fast',pos=True,cut_all=False):
    try:
        if mode in ['fast','accurate'] and pos in [True,False] and cut_all in [True,False]:
            data={'text':sentence,'mode':mode,'pos':pos,'cut_all':cut_all}
            return doTask(mapConf['cut'],'segmentor',data)
        else:
            printException('make sure value of mode is  \'fast\',\'accurate\' or empty, value of pos is \'true\',\'false\' or empty as well.')
            return None
    except Exception as e:
            printException(e)
            return None

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
                printException(e)
    except Exception as e:
        if 'command not found' in str(e):
            printException('please install hadoop client before use getW2VFile')

def getWordVec(word):
    pass

def getCharacterVec(character):
    pass

# Sentence2Vector
def getSentenceVec(sentence):
    pass

# LanguageModel

# EmotionParser

# SentenceSpliter
def getSubSentences(sentence,mode=0):
    try:
        if mode == 0 or mode == 1:
            data={'sentence':sentence,'mode':mode}
            return doTask(mapConf['sentence_spliter'],'sentence_spliter',data)
        else:
            printException('make sure value of mode is 0 or 1')
    except Exception as e:
        print(e)
        return None


#EntityParser

#SentenceTypeParser




