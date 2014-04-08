import sys,DNS

def hierquery(qstring,qtype):
    reqobj=DNS.Request()
    try:
        answerobj=reqobj.req(name = qstring,qtype = qtype)
        answers=[x['data'] for x in answerobj.answers if x['type'] == qtype]
    except DNS.Base.DNSError:
        answers= []
    if len(answers):
        return answers
    else:
        remainder=qstring.split(".",1)
        if len(remainder) == 1:
            return None
        else:
            return hierquery(remainder[1],qtype)
        
def findnameservers(hostname):
    return hierquery(hostname,DNS.Type.NS)

def getrecordsfromnameserver(qstring,qtype,nslist):
    for ns in nslist:
        reqobj=DNS.Request(server = ns)
        try:
            answers = reqobj.req(name = qstring,qtype = qtype).answers
            if len(answers):
                return answers
        except DNS.Base.DNSError:
            pass
    return []

def nslookup(qstring,qtype,verbose=1):
    nslist=findnameservers(qstring)
    if nslist == None:
        raise RuntimeError,"Could not find namserver to use."
    if verbose:
        print "Using namservers:",", ".join(nslist)
    return getrecordsfromnameserver(qstring,qtype,nslist)

if __name__ == "__main__":
    query=sys.argv[1]
    DNS.DiscoverNameServers()
    answers=nslookup(query,DNS.Type.ANY)
    if not len(answers):
        print "Not found."
    for item in answers:
        print "%-5s %s"%(item["typename"],item["data"])
