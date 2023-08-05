import codecs,jieba
from random import randint, sample
class van_m:
    def __init__(self,p2c,c2p):
        self.p2c = self.read_data(p2c)
        self.c2p = self.read_data(c2p)

    def read_data(self,filename):
        lines = codecs.open(filename,'r','utf8').readlines()
        lines = [i.replace('\n','').strip() for i in lines]
        lines = [i.split('<>') for i in lines]
        dict_out = dict()
        for idx,line in enumerate(lines):
            key = line[0]
            tmp = line[1].split(',')
            dict_out[key] = tmp[:]
        return dict_out

    def convert(self,sentence):
        seg_list = list(jieba.cut(sentence))
        out_list = []
        for i in seg_list:
            if i in self.p2c:
                out_list.append(sample(self.p2c[i],1)[0])
            else:
                out_list.append(i)
        return ''.join(out_list)
