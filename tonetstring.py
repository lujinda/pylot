def toHex(n):
    return hex(ord(n)).split('x',1)[1]

def toNetstring(s):
    s="%d:%s"%(len(s),s)
    print s+','
    newStr=[]
    for char in s:
        newStr.append(toHex(char))
    newStr.append(toHex(','))
    
    return "<%s>,"%(' '.join(newStr))

def main():
    sStr=raw_input("please input a string:")
    dStr=toNetstring(sStr)
    print dStr


if __name__=="__main__":
    main()

