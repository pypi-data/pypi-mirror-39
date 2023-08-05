import codecs,jieba
from tqdm import tqdm
from .vanish_model_dir import van_model

class Model:
    def __init__(self):
        self.use_replace_model(p2c='./data/p2c_happy.py',c2p='./data/c2p_happy.py')
    def use_replace_model(self,p2c,c2p):
        self.model = van_model.van_m(p2c=p2c,c2p=c2p)
    def convert(self,sentence):
        return self.model.convert(sentence)

model = Model()
print(model.convert('我是个杀手，我没有感情。'))