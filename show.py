#coding:utf8
from calendar import monthrange
from datetime import date
today=date.today()
month=today.month
year=today.year
days=monthrange(year,month)[1]

import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
zfont=FontProperties(fname="/data/h.ttf")

plt.figure(figsize=(12,8))
xmess=u"%s年%s月"%(year,month)
plt.xlabel(xmess,fontproperties=zfont)
plt.ylabel(u"故障数",fontproperties=zfont)
plt.title(xmess+u'\n'+u'故障统计图',fontproperties=zfont)
plt.xticks(range(1,days+1))
plt.grid(True)
plt.savefig("t.png")

