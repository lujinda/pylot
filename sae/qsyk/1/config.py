#coding:utf8
import sae
import sae.const
import web
import os

urls=(
        '/',"index",
        )

app_root=os.path.dirname(__file__)
templates_root=os.path.join(app_root,'templates')
render=web.template.render(templates_root)

#db=web.database(port=int(sae.const.MYSQL_PORT), host=sae.const.MYSQL_HOST,dbn="mysql",
 #       user=sae.const.MYSQL_USER,pw=sae.const.MYSQL_PASS,
  #      db=sae.const.MYSQL_DB)
