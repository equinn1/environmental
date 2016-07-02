# -*- coding: utf-8 -*-
"""
Created on Thu Jun 16 09:47:26 2016

@author: gquinn
"""
import pickle
from counting_process_classes import *

subjects={}                                       #subject dictionary
cps={}                                            #counting process dictionary

for dis in ['BDD','MDD','OCD','SOC']:
    fname="data/STATE_"+dis+".txt"

    fp = open(fname,'r')   #read state changes

    for line in fp:                              #loop through line by line
        if("SS:" in line):                            #first entry for this S
            wds = line.split()
            SS=wds[0].split(":")[1]                   #subject number
            initline=line

        
        if("ID" in line):                             #ID line
            wl=line.split("=")
            if(len(wl)>1):                            #skip if no ID
                ID=wl[1]                          #save ID if there is one
                if(ID in subjects.keys()):            #ID already present?
                    newsub=subjects[ID]
                else:
                    newsub=subj(ID,SS)                #call subject constructor
                    subjects[ID]=newsub
                    subjects[ID].set_initline(dis,initline)
            
        if("Initial" in line):                        #save initial status
            init_state=line.split()[2]
            subjects[ID].set_intake_state(init_state,dis)
            scentries=[]
            newsc=scentry(0,None,init_state)
            scentries.append(newsc)
            subjects[ID].set_scentries(scentries,dis)
        
            
        if("Max" in line):
            maxtime=line.split()[2]
            subjects[ID].set_maxtime(maxtime)
            scentries=newsub.get_scentries(dis)
            lastone=len(scentries)-1
            lastcp=scentries[lastone]
            lastcp.set_end(maxtime)
            newsub.set_scentries(scentries,dis)

        if("STATE CHANGE" in line):
            wds=line.split()
            from_state=wds[3]
            to_state=wds[5]
            week=wds[8]
            newsc=scentry(week,None,to_state)
            scentries=newsub.get_scentries(dis)
            imax=len(scentries)-1
            sce = scentries[imax]
            sce.set_end(week)
            scentries.append(newsc)
            newsub.set_scentries(scentries,dis)

# set eligibility for study
dis='BDD'
for key in subjects:
    print(subjects[key].get_ID())
    maxtime=subjects[key].get_maxtime()
    initline=subjects[key].get_initline(dis)
    subjects[key].set_instudy(False)
    if (maxtime >= 52):
        if ("scd102 1 scd104 2" in initline):
            subjects[key].set_instudy(True)
    print(subjects[key].get_instudy())
    
print("Starting list")
for key in subjects:
    print(subjects[key].get_ID())
    scdict=subjects[key].get_scdict()
    for dis in scdict.keys():
        print(dis)
        scentries=scdict[dis]
        for i in range(0,len(scentries)):
            scentries[i].print_entry()
#        print(dis)

#BDD Partial remissions cp list
cpid="BDD PARTREM"
cps[cpid]=cp(cpid)
cpentries=cps[cpid].get_cpentries()

for key in subjects:
    if subjects[key].get_instudy()==True:  #select S in study
        S=S+1
        ID=subjects[key].get_ID()
        scentries=subjects[key].get_scentries('BDD')
        prevstate=None
        for i in range(0,len(scentries)):
            if (scentries[i].get_state()=='IE_FC'):
                cpstart=scentries[i].get_start()
 #           scentries[i].print_entry()
            if scentries[i].get_state()=='IE_NFC' :
                if prevstate=='IE_FC':
                    newcpe=cpentry(cpstart,scentries[i].get_start(),1,ID)
                    cps[cpid].append_cpentries(newcpe)
  #                  newcpe.print_entry()
                    cpstart=None
            prevstate=scentries[i].get_state()

print("S")
           
for cpid in cps:
    cpentries=cps[cpid].get_cpentries()
    for i in range(0,len(cpentries)):
        cpentries[i].print_entry()
#for key in subjects:            #build BDD partial remission events
#    if subjects[key].get_instudy()==True:
#        maxtime=subjects[key].get_maxtime()  #get max time
#        newcp=cpentry(0,maxtime,2)     #initial cp entry o to max censored
#        cps[cpid].append_cpentries(newcp)
#
#for key in cps:
#    cpentries=cps[key].get_cpentries()
#    for i in range(0,len(cpentries)):
#        cpentries[i].print_entry()
#print(cps["BDD PARTREM"])
#                                   #get state changes
#    scentries=scdict['BDD']   
        
        
            
#pf=open('bdd_state_python.obj','wb')      
#pickle.dump(subjects,pf,pickle.HIGHEST_PROTOCOL)