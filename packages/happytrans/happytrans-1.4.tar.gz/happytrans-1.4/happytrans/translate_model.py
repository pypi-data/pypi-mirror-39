import codecs,jieba
from tqdm import tqdm
from .vanish_model_dir import van_model
import sys,os,platform,site
class Model:
    def __init__(self):
        #self.use_replace_model(p2c='data/p2c.happy',c2p='data/c2p.happy')
        #path = 'lib\site-packages\happytrans\data' if platform.system()=='Windows' else 'lib/site-packages/happytrans/data';path=os.path.join(sys.prefix,path)
        path = os.path.join(site.getsitepackages()[-1],'happytrans','data')
        self.use_replace_model(p2c=os.path.join(path,'p2c.happy'),
               c2p=os.path.join(path,'c2p.happy'))
    def use_replace_model(self,p2c,c2p):
        self.model = van_model.van_m(p2c=p2c,c2p=c2p)
    def convert(self,sentence):
        return self.model.convert(sentence)

model = Model()
print(model.convert('我是个杀手，我没有感情'))