def sum_digit1(number):
    number=filter(lambda x:x.isdigit(),number)
    Sum=reduce(lambda x,y:int(x)+int(y),number)
    return '+'.join(number) + ' = ' +str(Sum)

def sum_digit2(number):
    number=[int(x) for x in number if x.isdigit()]
    return '%s = %d' %('+'.join(map(str,number)),sum(number))
number=raw_input('please input a number:')
print sum_digit1(number)
print sum_digit2(number)
