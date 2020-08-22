from more_itertools import ilen

from readmdict import MDX, MDD

mdxfile = "data/德汉全席大词典.mdx"  #  24M ilen(MDX(mdxfile).keys())
# items()/keys() 594796  headers
# mdx = MDX(mdxfile)  # 18.5 s
# mdx.header: b'Description': 词条数：70万  完美变元音 日期：2006.11.22日 Ansbach
[b'GeneratedByEngineVersion',
 b'RequiredEngineVersion',
 b'Encrypted',
 b'Encoding',
 b'Format',
 b'Compact',
 b'Compat',
 b'KeyCaseSensitive',
 b'Description',
 b'Title',
 b'DataSourceFormat',
 b'StyleSheet']
# keys, items

mdxfile = "data/德语自修词典.mdx"  # 31M
# mdx = MDX(mdxfile)  # 18s
# print(ilen(mdx) 664022
# mdx.header.get(b"Description").decode(): 词条数：77万  完美变元音 日期：2009.01.02日 Konstanz

# mdx(filename).items()
# In [219]: ilen(mdx.items())
# Out[219]: 594796

# mdx_dict = dict(MDX(mdxfile).items())  #  17.6 s [*...] 38.6 s/46s sys.getsizeof(mdx_dict): 5150400 => dict: 20971616/20971616

# ############# 新德汉词典 (mingqing007 - 2017.01.04).mdx
mdxfile = r"data/新德汉词典 (mingqing007 - 2017.01.04).mdx"  # 7.3M
mdx = MDX(mdxfile)  # 2.4s

mdx_dict = dict((key.decode(), val.decode()) for key, val in MDX(mdxfile).items())  # byte to str 10.8 s

from pyquery  import PyQuery as pq
from save_tempfile impotr save_tempfile

# tr > td > font > b
In [322]: pq(mdx_dict.get("sein"))("tr > td > font > b")
Out[322]: [<b>, <b>]  # .text() 'I.V.i.(s.) II.Pron.'

In [324]: pq(mdx_dict.get("Sein"))("tr > td > font > b").text()
Out[324]: 'n. -s, unz.'
# explantion text not structured, unusable

#  ###########  Oxford-Duden Concise De-En.mdx
mdxfile = r"data/Oxford-Duden Concise De-En.mdx"  # 7.3M
mdx = MDX(mdxfile)  # 2.4s

mdx_dict = dict((key.decode(), val.decode()) for key, val in MDX(mdxfile).items())