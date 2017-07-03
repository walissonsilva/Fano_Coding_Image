import sys
import os

#input a file 
if len(sys.argv) == 0:
    print sys.argv
    print "no file input"
else:
    fi = open("Arquivos/IMG.txt","rb")
    infile = bytearray(fi.read())                     #turn input into arrays of bytes
    size = len(infile)                 #size of the bytes array
    #print "before encoding the size of the file is", size
    #print infile
    
    #calculate the probability of each byte
    freq = [0] * 256                    #initiate the list of probability
    num = ""
    for b in infile:
        if (b == 32):
            b = int(num)
            freq[b] += 1
            num = ""
        else:
            num += chr(b)
        
    #creat a list of lists containing the information
    tuplist = []
    for i in range(256):
        tuplist.append([i, freq[i], ''])
        
    #sort the freq by probability from most to least
    stuplist = sorted(tuplist, key = lambda tup: tup[1], reverse = True)
    #delete all the elements with possibility zero
    indzero = 256
    for i in range(len(stuplist)):
        if stuplist[i][1] == 0:
            indzero = i
            break
        
    #shannon-fano-encode the bytelist
    def finddivide(flist):                       #find the divide position
        diflist = []
        for k in range(len(flist)):
            sumA = 0
            sumB = 0
            for i in range(k):
                sumA += flist[i][1]           #first sum
            for i in range(k, len(flist)):
                sumB += flist[i][1]           #second sum
            dif = abs(sumA - sumB)              #difference
            diflist.append((k, dif))            #creat a diflist
        sdiflist = sorted(diflist, key = lambda dif: dif[1])
        return sdiflist[0][0]                    #wall is the dividing line
    
    def sfencoder(list, d):
        if len(list) == 2:                         #return condition for recursive call
            list[0][2] += '0'
            list[1][2] += '1'
            return True
        if len(list) == 1:
            if d == 'l':    list[0][2] += '0'
            elif d == 'r':  list[0][2] == '1'
            else: print "illegal parameter"
            return True
        divpos = finddivide(list)                  #get the divide postion
        for i in range(divpos):
            list[i][2] += '0'
        for i in range(divpos, len(list)):
            list[i][2] += '1'
        sfencoder(list[:divpos],'l')
        sfencoder(list[divpos:],'r')                    #recursive call
        return list
    
    #map of encoding
    encodedlist = sfencoder(stuplist[:indzero],'l')
    #creat a dictionary for the encoding
    sfdic = {}
    for i in range(len(encodedlist)):
        sfdic[encodedlist[i][0]] = encodedlist[i][2]
    #print sfdic
    arquivo = open('Arquivos/encoded.txt', 'w')
    for chave in sfdic.keys():
        linha = str(int(chave)) +  ":" + sfdic[chave] + "\n"
        arquivo.write(linha)
        print int(chave), ":", sfdic[chave]
    
    #encode the input file
    newfile = ""
    num = ''
    for bite in infile:
        if (bite == 32):
            bite = int(num)
            newfile += sfdic[bite] 
            num = ''
        else:
            num += chr(bite)
    #divide the string into substrings of 8 elements
    listofbytes = []
    for i in range(len(newfile)/8):
        listofbytes.append(newfile[(i*8):(i*8+8)])
    lstlen = len(listofbytes[len(listofbytes)-1])
    #append the last element to 8 bits
    if lstlen != 8:
        for i in range(8-lstlen):
            listofbytes[len(listofbytes)-1].append('0')
    #convert the 8-element string into numbers
    dcmlst = []
    for strbyte in listofbytes:
        strbyte = bytearray(strbyte)
        u = 0
        for i in range(8):
            u += (strbyte[i]-48)*2**(7-i) 
        dcmlst.append(u)
    flst = bytearray(dcmlst)
    #print infile
    #print flst
#print "\nafter the compression the size of the file is",len(flst)