#coding:utf8
import fileinput
import re
def replacement(match):
    code=match.group(1)
    try:
        return str(eval(code,scope))
    except SyntaxError:
        exec code in scope
        return ''

file_pat=re.compile(r'\[(.+?)\]')
scope={}
lines=[]
for line in fileinput.input():
        lines.append(line)
text="".join(lines)
print file_pat.sub(replacement,text)
