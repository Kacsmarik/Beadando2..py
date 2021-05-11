import csv
import re

f=[]


with open('contacts.csv','r',encoding='UTF-8')as file:
    reader=csv.DictReader(file,delimiter=';')
    next(reader)
    for row in reader:

        f.append(row)


nevbe=re.compile(u'[a-zA-ZäáéöóőüűÁÄÖÜ]+', flags=re.UNICODE)
cim=re.compile(u'\d{4,4}[a-zA-ZäáéöóőüűÁÓÖÜ, ]+.+[0-9]{1,2}.', flags=re.UNICODE)
telefonszam=re.compile(u'\d{,2}\s\d{6,7}', flags=re.UNICODE)
emailcim=re.compile(u'[a-zA-ZäáéöóőüűÁÓÖÜ!#$&+-.]+\w+@[a-zäáéöóőüű]+.[a-zäáéöóőüű]+', flags=re.UNICODE)

ellernorzes= lambda  row,pattern, kriterium: row[kriterium]==' '.join(pattern.findall(row[kriterium]))


def ell(row):
    ch1=ellernorzes(row,nevbe,'NAME')
    ch2=ellernorzes(row,cim,'ADDRESS')
    ch3=ellernorzes(row,telefonszam,'PHONE')
    ch4=ellernorzes(row,emailcim,'EMAIL')

    return ch1&ch2&ch3&ch4

with open('contacts_good.csv','w',encoding='UTF-8',newline='')as goodFile:
    jofajl=csv.DictWriter(goodFile,delimiter=';',fieldnames=reader.fieldnames)
    jofajl.writeheader()
    for row in f:
        if ell(row):
            print(row)
            jofajl.writerow(row)


with open('contacts_bad.csv','w',encoding='UTF-8',newline='')as badFile:
    rosszfajl=csv.DictWriter(badFile,delimiter=';', fieldnames=['NAME','ADDRESS','PHONE','EMAIL','INDEX'])
    rosszfajl.writeheader()
    count=0
    for row in f:
        if ell(row)==False:
            count+=1
            row ['INDEX']=count
            rosszfajl.writerow(row)

