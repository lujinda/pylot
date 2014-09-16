from twisted.internet import reactor
from twisted.enterprise import adbapi
import threading

dbpool=adbapi.ConnectionPool("sqlite3","temp.db",check_same_thread=False)



print threading.currentThread().getName()
def printResults(results):
    for elt in results:
        print elt[0]

def _insertName(transaction,name):
    print threading.currentThread().getName()
    transaction.execute("INSERT INTO contacts VALUES(?,?)",name)

def getName(name):
    return dbpool.runQuery("SELECT phone FROM contacts WHERE name = ?",
            (name,))

def insertName(name):
    return dbpool.runInteraction(_insertName,name)

def finish(_):
    dbpool.close()
    reactor.stop()

def made_error(_):
    print threading.currentThread().getName()
    print _


d=insertName(("lujindasd","120"))
d.addErrback(made_error)
d.addCallback(lambda x:getName("lujinda"))
d.addCallback(printResults)
d.addCallback(finish)

reactor.run()

