#!/usr/bin/env python
from daemonize import daemonize
import web
urls=(
        "/(.*)","index",
        )

class index():
    def GET(self,name=None):
        if not name:
            name="test"
        return ','.join(['hi',name])


if __name__=="__main__":
    from daemonize import daemonize
    daemonize(stdout="/tmp/stdout.log",
            stderr="/tmp/stderr.log")
    app=web.application(urls,globals())
    app.run()
