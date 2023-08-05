import van_model
from tqdm import tqdm
import codecs
test1 = '../data/chinese/xiaohuangji.conv'
p2c,c2p = '../data/p2c.happy','../data/c2p.happy'
model = van_model.van_m(p2c=p2c,c2p=c2p)
def convert(filename):
    outfile = codecs.open(filename+'.cy','w','utf8')
    lines = codecs.open(filename,'r','utf8').readlines()
    for line in tqdm(lines):
        out = model.convert(line)
        outfile.write(line)
        outfile.write(out)
convert(test1)
