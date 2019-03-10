import numpy as np
import os
total=10942
path='C://Users//ChenKx//Desktop//TSVD//resultnew//resultnew'
#path='C://Users//ChenKx//Desktop//TSVD//resultcodee//resultcodee.txt'
TPRprint=[]
FPRprint=[]
namematch=os.listdir(path)
for file in namematch:
    #print file
    filetemp=open(path+'//'+file)
    filetempline=filetemp.readlines()
    target=filetempline[0]
    TPRprinttemp=[1]*2000
    FPRprinttemp=[1]*2000
    targetbinaryname = (str(target.strip('\n')).split(':')[1]).split('_')[0]
    targetfunctionname = (str(target.strip('\n')).split(':')[2])
    #print targetbinaryname,targetfunctionname
    #print key
    startline=1
    TPRcount = 0
    FPRcount = 0
    number=0
    truenumber=0
    kkkk=0
    #print len(filetempline)
    for linee in range(len(filetempline)):
        #print filetempline[linee]=="#####"
        #print filetempline[linee].find('null:null#')
        if linee==0:
            continue
        if filetempline[linee].find('null:null#')==0:
            break
        if (linee)==startline:
            #print filetempline[linee]

            key = int(str(filetempline[linee]).split(' ')[0].split(':')[1])
            mmm=int(str(filetempline[linee]).split(' ')[3].split(':')[1])
            startline = startline + key + 1
            if TPRcount>mmm:
                TPRcount=mmm-1;
            #print key, mmm,startline
            #print 'TPR: ', float(TPRcount) / float(mmm)
            #print  'FPR: ', float(truenumber-TPRcount) / (total - mmm)
            TPRprinttemp[kkkk]=(float(TPRcount) / float(mmm))
            FPRprinttemp[kkkk]=(float(key-TPRcount)) / (total - mmm)
            kkkk=kkkk+1
            TPRcount = 0
            FPRcount = 0
            truenumber=0
            continue
        else :
            testname=filetempline[linee].split('#')
            #print startline
           # print testfunctioname
            #print TPRcount, FPRcount
            #test=filetempline[linee].split('#')
            #print len(test)
            truenumber=truenumber+len(testname)
            if (len(testname)-1)==1:
                testbinaryname = (str(testname[0]).split(':')[0]).split('_')[0]
                testfunctionname=(str(testname[0]).split(':')[1])
                issame = False
                testfunctionnamelist = testfunctionname.split('_')
                if testbinaryname==targetbinaryname:
                    if testfunctionname==targetfunctionname:
                        TPRcount=TPRcount+1
                    else:
                        FPRcount=FPRcount+1
                   # for ii in testfunctionnamelist:
                        #print ii
                     #   if targetfunctionname.find(str(ii))!=-1:
                        #    issame=True
                          #  break
                    if issame:
                        TPRcount = TPRcount + 1
                    else:
                        FPRcount = FPRcount + 1
                #else:
                #    FPRcount=FPRcount+1
            else:
                testlist=[]
                for testi in range(len(testname)-1):
                    testbinaryname=(str(testname[testi]).split(':')[0]).split('_')[0]
                   # print testbinaryname
                    if testbinaryname==targetbinaryname:
                        testlist.append(testi)
                #print testlist
                #if (len(testlist))>key:

                if len(testlist)!=0:
                    for testi in range(len(testlist)):
                       # testbinaryname=(str(test[testi]).split(':')[0]).split('_')[0]
                        testfunctionname = ((str(testname[testlist[testi]]).split(':')[1]))
                        issame=False
                        testfunctionnamelist=testfunctionname.split('_')
                        #for ii in testfunctionnamelist:
                        #    #print ii
                         #   if targetfunctionname.find(str(ii))!=-1:
                        #        issame=True
                         #       break
                        if testfunctionname==targetfunctionname:
                            issame=True
                        #print testfunctionname
                        #lentar=len(targetfunctionname)
                        #issame=False
                        #for i in range(lentar):
                            #temp=targetfunctionname[i:i+6]

                            #if testfunctionname.find(temp)!=-1:
                                    #issame=True
                                    #break
                        if issame:
                            TPRcount=TPRcount+1
                        else:
                            FPRcount=FPRcount+1

    TPRprint.append(TPRprinttemp)
    FPRprint.append(FPRprinttemp)
#print len(TPRprint[0])
#print FPRprint
temp=[]


for j in range(len(TPRprint[0])):
    tprtempsum = 0
    for i in range(len(TPRprint)):
        #print 'tpr:',TPRprint[i][j]
        tprtempsum=tprtempsum+TPRprint[i][j]
   # print 'tprsum:',tprtempsum
    temp.append(float(tprtempsum)/1000)
fprtempsum=0
tempp=[]
for j in range(len(FPRprint[0])):
    fprtempsum = 0
    for i in range(len(FPRprint)):
        fprtempsum=fprtempsum+FPRprint[i][j]
   # print fprtempsum
    tempp.append(float(fprtempsum)/1000)
print temp
print tempp
#print np.sum(FPRprint,axis=0)
            #print TPRcount,FPRcount


    #print number







