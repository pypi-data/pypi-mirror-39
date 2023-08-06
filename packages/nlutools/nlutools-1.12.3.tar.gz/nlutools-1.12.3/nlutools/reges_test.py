import tools as nlu

print('测试分词')
#print(nlu.cut('这是一个能够输出名词短语的分词器，欢迎试用！',pos=True,cut_all=False,mode='fast'))
print(nlu.cut('这是一个能够输出名词短语的分词器，欢迎试用！'))
print('测试分词完成')

print('测试分句')
print(nlu.getSubSentences('我喜欢在春天去观赏桃花，在夏天去欣赏荷花，在秋天去观赏红叶，但更喜欢在冬天去欣赏雪景。',mode=1))
print('测试分句完成')
#print('测试下载词向量')
#nlu.getW2VFile('v1.0','~:')
#print('词向量下载完成')

print('测试句向量')
print(nlu.getSentenceVec(['主要负责机器学习算法的研究以及搭建神经网络、训练模型、编写代码，以及其他的一些工作','机器学习算法的研究以及搭建神经网络，训练模型']))
print('测试句向量完成')


print('测试情感分析')
print(nlu.predictEmotion(['这家公司很棒!','这家公司不咋地','这家公司还可以']))
print(nlu.predictEmotion(['这家公司很棒!','这家公司不咋地','这家公司还可以'],prob=True))
print('测试情感分析完成')


print('测试词向量')
print(nlu.getWordVec('深度学习'))
print(nlu.getWordVec(['深度学习']))
print(nlu.getMostSimiWords('深度学习',10))
print(nlu.getMostSimiWords(['深度学习','神经网络'],10))
print('测试词向量完成')
