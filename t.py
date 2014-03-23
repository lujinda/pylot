#coding:utf8
import fileinput,re
def replacement(match):
    code=match.group(1)
    try:
        return str(eval(code,scope)) # 如果code是'y+x'　则会在scope中查找有无y和x
    except SyntaxError:
        exec code in scope #　把code存入scope字典命令空间中，如'y=10'(字符串)　这样的话，在eval中计算时，假如第一个参数中带有变量，则会在scope字典命令空间中进行查找.
        return ''
    
filed_pat=re.compile(r'\[(.+?)\]')

scope={}
lines=[]
for line in fileinput.input():
    lines.append(line)
text="".join(lines)
print filed_pat.sub(replacement,text)
    

