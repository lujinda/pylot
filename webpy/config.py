#coding:utf8
import re,web,time
render=web.template.render('temp')
urls=(
		'/','index',
		'/login/?' ,'login',#login GET
		'/login/loginPost','loginPost',#POST
		'/logout','logout',#reset
		'/signup/?','signup',#GET
		'/signup/getAccount','getAccount',#POST
		'/messBoard','messBoard',#show message
		'/lmess','lmess',#leave a message
		'/frame/top.html','readTop',
		'/frame/main.html','readMain',
		'/frame/right.html','readRight',
#		'/.+','error404'#other path=not found
		)
web.config.debug=False
db_host='127.0.0.1'
db_dbn='mysql'
db_user='root'
db_pw='zxc123'
db_db='blog'
u_r=re.compile(r'\w{6,20}') #match username
p_r=re.compile(r"^[\x21-\x7e]{6.20}$")#match password ,\x21-\x7e is a match ascii's 33-126
e_r=re.compile(r'^([\w-]+)@(([\w-]+\.)+[a-zA-z]{2,4})$') #mathch email
db=web.database(db_host,dbn=db_dbn,user=db_user,pw=db_pw,db=db_db)	#set database
ERROR_404=u'hi,小盆友，迷路了吗，让我们回到首页好吗？'
ERROR_DB=u'唉，数据库出错了～'
def isEmpty(s):
	return s.replace(" ","") ==""
def authUser(user,pwd):
		return len(db.select('accounts',where='username=\'%s\' and password=\'%s\'' %(user,pwd)))
	
