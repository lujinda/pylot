from twisted.internet import defer

def cancel_outer(d):
    print "outer cancel callback."

def cancel_inner(d):
    print "inner cancel callback."

def first_outer_callback(res):
    print "first outer callback,returning inner deferred"
    inner_d.callback("res")
    return inner_d

def second_outer_callback(res):
    print "second outer callback got:",res

def outer_errback(err):
    print "out errback got:",err

def inner_callback(res):
    print "inner callback"

outer_d=defer.Deferred(cancel_outer)
inner_d=defer.Deferred(cancel_inner)
inner_d.addCallback(inner_callback)

outer_d.addCallback(first_outer_callback)
outer_d.addCallback(second_outer_callback)
outer_d.addErrback(outer_errback)

outer_d.callback("result")

#print "canceling outer deferred"
outer_d.cancel()

print "done"

outer_d.cancel()
