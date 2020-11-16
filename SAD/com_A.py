import numpy as np
import math

#with open('dat.txt' , 'r') as file:
#con = file.read().split('\n')
#del con[-1]
#
#for i in con:
#    count += 1
#    arr.append(i.split(','))

out = []
address = []

with open('code.txt' , 'r') as file:
    con = file.read().split('\n')
    
    if not(con[-1]):
        del con[-1]
    
    for i in con:
        out.append(i.split('\t'))
        
def twosCom_decBin(dec, digit):
    if dec>=0:
            bin1 = bin(dec).split("0b")[1]
            while len(bin1)<digit :
                    bin1 = '0'+bin1
            return bin1
    else:
            bin1 = -1*dec
            return bin(dec-pow(2,digit)).split("0b")[1]

label = []
code = []
first = []
second = []
third = []
line = len(out)

for i in range (len(out)):
    for j in range (len(out[i])):
        if(j == 0):
            label.append(out[i][j])
        elif(j == 1):
            code.append(out[i][j])
        elif(j == 2):
            first.append(out[i][j])
        elif(j == 3):
            second.append(out[i][j])
        else:
            third.append(out[i][j])
            
labelin = dict()
addr = dict()
value = dict()

for i in range (line):
    if(label[i] != ''):
        labelin.update({label[i] : f'address[{i}]'})
    else:
        labelin.update({f'{int(i)}': f'address[{i}]'})


for i in range (line):
    if(code[i] == '.fill'):
        try:
            addr.update({f'address[{i}]': int(first[i])})
        except:
            index = 0
            for j in range (line):
                if(first[i] == label[j]):
                    index = int(j)
            
            addr.update({f'address[{i}]': index})

print(second)

for i in range (line):
    if(code[i] == 'lw'):
        if(not(third[i].isdecimal())):
#            print(addr.get(labelin.get(third[i])))
            op = 2 << 22
            addr.update({f'address[{i}]': op
            + (int(first[i]) << 19)
            + (int(second[i]) << 16)
            + int(addr.get(labelin.get(third[i])))
            })
        else:
            op = 2 << 22
            addr.update({f'address[{i}]': op
            + (int(first[i]) << 19)
            + (int(second[i]) << 16)
            + int(third[i])
            })
            
    elif(code[i] == 'add'):
        if(third[i].isdecimal()):
            op = 0 << 22
            addr.update({f'address[{i}]': op
            + (int(first[i]) << 19)
            + (int(second[i]) << 16)
            + (int(third[i]))
            })
        else:
            op = 0 << 22
            addr.update({f'address[{i}]': op
            + (int(first[i]) << 19)
            + (int(second[i]) << 16)
            + (int(addr.get(labelin.get(third[i]))))
            })
            
    elif(code[i] == 'nand'):
        if(third[i].isdecimal()):
            op = 1 << 22
            addr.update({f'address[{i}]': op
            + (int(first[i]) << 19)
            + (int(second[i]) << 16)
            + (int(third[i]))
            })
        else:
            op = 1 << 22
            addr.update({f'address[{i}]': op
            + (int(first[i]) << 19)
            + (int(second[i]) << 16)
            + (int(addr.get(labelin.get(third[i]))))
            })
            
    elif(code[i] == 'beq'):
        if(third[i].isdecimal()):
            op = 4 << 22
            addr.update({f'address[{i}]': op
            + (int(first[i]) << 19)
            + (int(second[i]) << 16)
            + (int(third[i]))
            })
        else:
            go = third[i]
            for g in range (len(label)):
                if(label[g] == go):
                    go = g
            go = int(go)
            save = go + 1 + i
            go = i - save
            converted = twosCom_decBin(go , 16)
            op = 4 << 22
            addr.update({f'address[{i}]': op
            + (int(first[i]) << 19)
            + (int(second[i]) << 16)
            + (int(converted,2))
            })
            
    elif(code[i] == 'noop'):
        op = 7 << 22
        addr.update({f'address[{i}]': op})
        
    elif(code[i] == 'halt'):
        op = 6 << 22
        addr.update({f'address[{i}]':op})
        
    elif(code[i] == 'jalr'):
        op = 5 << 22
        addr.update({f'address[{i}]':op
        + (int(first[i]) << 19)
        + (int(second[i]) << 16)
        })
       
for i in range (line):
    if(isinstance(addr.get(f'address[{i}]') , str)):
        print(12)
    
            
for i in range (line):
#    print(addr.get(f'address[{i}]'))
    print(f'address[{i}] : ' , addr.get(f'address[{i}]'))

with open('machine_code.txt' , 'w') as file:
    for i in range (line):
        con = file.write('%s\n' % (addr.get(f'address[{i}]')))


#for i in range (line):
#    if(code[i] == 'lw'):
#        op = 2 << 22
#        if(third[i].isnumeric()):
#            addr.update({f'addr{i}': op + (int(first[i]) << 19) + (int(second[i]) << 16) + (int(third[i]))})
#        else:
#            if(third[i] != ''):
#                addr.update({f'addr{i}': op +
#                (int(first[i]) << 19) +
#                (int(second[i]) << 16) +
#                (addr.get(labelin.get(third[i])))})
##    elif(code[i] == 'beq'):
##        op = 4 << 22
##        if(third[i].isnumeric()):
##            addr.update({f'addr{i}': op + (int(first[i]) << 19) + (int(second[i]) << 16) + (int(third[i]))})
##        else:
##            if(third[i] != ''):
##                addr.update({f'addr{i}': op +
##                (int(first[i]) << 19) +
##                (int(second[i]) << 16) +
##                (addr.get(labelin.get(third[i])))})
#    elif(code[i] == 'add'):
#        op = 0 << 22
#        addr.update({f'addr{i}': op + (int(first[i]) << 19) + (int(second[i]) << 16) + (int(third[i]))})
