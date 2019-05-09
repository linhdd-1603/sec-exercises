from socket import socket

dic = {'1': ['  #', '  #', '  #', '  #', '  #'],
       '2': ['###', '  #', '###', '#  ', '###'],
       '3': ['###', '  #', '###', '  #', '###'],
       '4': ['# #', '# #', '###', '  #', '  #'],
       '5': ['###', '#  ', '###', '  #', '###'],
       '6': ['###', '#  ', '###', '# #', '###'],
       '7': ['###', '  #', '  #', '  #', '  #'],
       '8': ['###', '# #', '###', '# #', '###'],
       '9': ['###', '# #', '###', '  #', '###'],
       '0': ['###', '# #', '# #', '# #', '###'],
       '+': ['   ', ' # ', '###', ' # ', '   '],
       '-': ['   ', '   ', '###', '   ', '   '],
       '*': ['   ', '# #', ' # ', '# #', '   '],
       '/': ['   ', '  #', ' # ', '#  ', '   ']}


def parseString(input):
    print input
    lines = str(input).split("\n")
    result = ''
    leng = len(lines[0]) / 5
    for m in range(0, leng):
        temp = []
        for n in range(0, 5):
            temp.append(lines[n][m * 5:m * 5 + 3])
        for key in dic:
            if (dic[key] == temp):
                result += key
    return result


sock = socket()
sock.connect(('188.166.218.1', 2016))
while True:
    data = sock.recv(10240)
    print data
    data = sock.recv(10240)
    # print(data)
    result = parseString(data)
    print result
    a = eval(result)
    print a
    sock.send((str(a) + "\n").encode())
# print eval('75*30-53-11*57-93-46+15*93*85*42+22-20*64*16/59')

