#coding:utf8
def lines(f):
    for line in f:
        yield line
    yield '\n'

def blocks(f):
    block=[]
    for line in lines(f):# 如果没有上面的yield '\n'，则到了文件最后的时候，不会任何返回，则最后一块，将无法返回了。所以需要yield '\n' 在文件末.
        if line.strip():
            block.append(line)
        elif block:
            yield "".join(block).strip()
            block=[]

