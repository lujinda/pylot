import qiniu.conf
import os
qiniu.conf.ACCESS_KEY="BbDU4MoFrx2YaF6tqBFmnKHFuDlq1EO-mm2ldlBm"
qiniu.conf.SECRET_KEY="WWdwgm4oRmOh_L9yKbyWplcUFaIGAZXk8e_UOtDs"

import qiniu.rs

policy=qiniu.rs.PutPolicy("ljdpython")
uptoken=policy.token()

import qiniu.io

localfile="/home/ljd/py/t.py"
filename=os.path.basename(localfile)

ret,err=qiniu.io.put_file(uptoken,filename,localfile)
if err:
    qiniu.rs.Client().delete("ljdpython",filename)
