import MySQLdb
import chardet
db_host='www.db4free.net'
db_user='linuxpython'
db_pwd='zxc123'
db_name='linuxpython'
class Db():
	def __init__(self):
		try:
			self.db=MySQLdb.connect(db_host,db_user,db_pwd,db_name,charset="utf8")
		except Exception,e:
			print e
	def	checkPwd(self,user,pwd):
		pwd=hashlib.md5(pwd).hexdigest()
		cursor=self.db.cursor()
		sql="select * from accounts where username=\'%s\' and password=\'%s\'" %(user,pwd)
		return len(self.selectSql(sql))
	def selectSql(self,sql):
		cursor=self.db.cursor()
		cursor.execute(sql)
		return cursor.fetchall()

	def listNote(self,user):
		sql="select title,content from notes where username=\'%s\'" %(user)
		return self.selectSql(sql)

if __name__=='__main__':
	t=Db()
#	print t.
	t.listNote('admin')
