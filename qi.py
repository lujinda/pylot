import qiniu.conf
import os
qiniu.conf.ACCESS_KEY="BbDU4MoFrx2YaF6tqBFmnKHFuDlq1EO-mm2ldlBm"
qiniu.conf.SECRET_KEY="WWdwgm4oRmOh_L9yKbyWplcUFaIGAZXk8e_UOtDs"

import qiniu.rs

policy=qiniu.rs.PutPolicy("imgdata")
uptoken=policy.token()

import qiniu.io

localfile="/home/ljd/py/t.py"
import matplotlib.pyplot as plt
import cStringIO
s=cStringIO.StringIO()
plt.xticks(range(1,30))
plt.savefig(s)

ret,err=qiniu.io.put(uptoken,'a.png',s)
if err:
    qiniu.rs.Client().delete("ljdpython",filename)
