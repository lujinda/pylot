import web
urls=(
        "/showtime.jpg","showtime"
        )

class showtime:
    def GET(self):
        return open("_taobao_t.jpg").read()

if __name__=="__main__":
    app=web.application(urls,globals())
    app.run()
