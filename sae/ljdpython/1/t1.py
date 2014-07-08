import web
urls=()
app=web.application(urls,globals())
db=web.database(port=3306,host="localhost",dbn="mysql",user="root",pw="zxc123",db="app_ljdpython")
d=db.select("bugs")
app.run()
