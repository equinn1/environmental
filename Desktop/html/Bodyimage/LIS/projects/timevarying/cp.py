# -*- coding: utf-8 -*-
"""
Created on Thu Jun 16 09:47:26 2016

@author: gquinn
"""
import pickle
from cp_classes import *

subjects={}

for dis in ['BDD','MDD','OCD','SOC']:
    fname="data/STATE_"+dis+".txt"
    col=dis+'_STATE'

    fp = open(fname,'r')   #read state changes

    for line in fp:                              #loop through line by line
        if("SS:" in line):                            #first entry for this S
            wds = line.split()
            SS=wds[0].split(":")[1]                   #subject number
            initline=line

        
        if("ID" in line):                             #ID line
            wl=line.split("=")
            if(len(wl)>1):                            #skip if no ID
                ID=wl[1].strip()                          #save ID if there is one
                if(ID in subjects.keys()):            #ID already present?
                    newsub=subjects[ID]
                else:
                    newsub=subj(ID,SS)                #call subject constructor
                    subjects[ID]=newsub
                    subjects[ID].set_initline(dis,initline)
            
        if("Initial" in line):                        #save initial status
            init_state=line.split()[2].strip()
            subjects[ID].set_intake_state(init_state,dis)
            
        if("Max" in line):
            maxtime=int(line.split()[2])               #get max time
            subjects[ID].set_maxtime(maxtime,dis)      #save it in subject obj
            
            col_len=subjects[ID].get_cpo_len(col)
            if col_len==0:
                cpl=[subjects[ID].get_intake_state(dis)]*(maxtime+1)
                subjects[ID].set_cpo_col(cpl,col)
            else:
                subjects[ID].set_cpo_values(col,col_len,maxtime+1,to_state)

        if("STATE CHANGE" in line):
            wds=line.split()
            from_state=wds[3].strip()
            to_state=wds[5].strip()
            week=int(wds[8])
            cpo=subjects[ID].get_cpo()
            col_len=subjects[ID].get_cpo_len(col)
            if col_len==0:
                cpl=[subjects[ID].get_intake_state(dis)]*(week)
                subjects[ID].set_cpo_col(cpl,col)
            else:
                subjects[ID].set_cpo_values(col,col_len,week,from_state)
            

# set eligibility for study

dis='BDD'
#for key in subjects:
for key in subjects:   
 #   print(subjects[key].get_ID())
    maxtime=subjects[key].get_maxtime(dis)
    initline=subjects[key].get_initline(dis)
    subjects[key].set_instudy(False)
    if (maxtime >= 52):
        if ("scd102 1 scd104 2" in initline):
            subjects[key].set_instudy(True)
#    print(subjects[key].get_instudy())

#set atrisk indicators for each event of interest
            
def in_risk_set(key,current_state,state_col,risk_set_col):
    subjects[key].set_cpo_col(map(lambda z : z==current_state,\
    subjects[key].get_cpo_col(state_col)),risk_set_col)

def risk_set_union(key,col1,col2,newcol):
    rs1=subjects[key].get_cpo_col(col1)    #get first risk set column
    rs2=subjects[key].get_cpo_col(col2)    #get second risk set column
    rs3=[None]*len(rs1)
    for i in range(0,len(rs1)):
        rs3[i]=rs1[i] or rs2[i]
    subjects[key].set_cpo_col(rs3,newcol)  #save new risk set column
    
def epi_num(key,dis):
    state_col=dis+'_STATE'
    epi_col=dis+'_EPISODE'
    so=subjects[key].get_cpo_col(state_col)
    initial_state=subjects[key].get_intake_state(dis)
    epi=range(0,len(so))
    if initial_state=='IE_FC':
        epi[0]=1
    else:
        epi[0]=0
    for i in range(1,len(so)):
        epi[i]=epi[i-1]
        if so[i]=='IE_FC' and so[i-1]!='IE_FC':
            epi[i]=epi[i]+1
    subjects[key].set_cpo_col(epi,epi_col)
            
    

for key in subjects:
    
#BDD

# S in state IE_FC is elibigible for one stage remission and partial remission    
    in_risk_set(key,'IE_FC','BDD_STATE','RS_BDD_PARTREM') #BDD partrem 
    in_risk_set(key,'IE_FC','BDD_STATE','RS_BDD_1SREM') #BDD one stage rem
    
# S in IE_NFC is eligible for partial relapse, two stage remission   
    in_risk_set(key,'IE_NFC','BDD_STATE','RS_BDD_PARTREL') #BDD partrel
    in_risk_set(key,'IE_NFC','BDD_STATE','RS_BDD_2SREM')   #BDD two stage rem
    
# S in NIE_NP is eligible for full relapse, partial onset
    in_risk_set(key,'NIE_NP','BDD_STATE','RS_BDD_1SREL') #BDD one stage rel
    in_risk_set(key,'NIE_NP','BDD_STATE','RS_BDD_PARTONS') #BDD partial onset

# S in NIE_NFC is eligible for two stage relapse, partial improve
    in_risk_set(key,'NIE_NFC','BDD_STATE','RS_BDD_2SREL')  #BDD two stage rel
    in_risk_set(key,'NIE_NFC','BDD_STATE','RS_BDD_PARTIMP') #BDD partial improve

#S in NIE_NFC is eligible for two stage relapse, partial improve    
    in_risk_set(key,'NIE_NFC','BDD_STATE','RS_BDD_2SREL')  #BDD two stage rel
    in_risk_set(key,'NIE_NFC','BDD_STATE','RS_BDD_PARTIMP') #BDD partimp

#FULLREM risk set is union of one and two stage remission
    risk_set_union(key,'RS_BDD_1SREM','RS_BDD_2SREM','RS_BDD_FULLREM')  
    

#FULLREL risk set is union of one and two stage relapse
    risk_set_union(key,'RS_BDD_1SREL','RS_BDD_2SREL','RS_BDD_FULLREL')  

#compute episode number    
    epi_num(key,'BDD')  #episode number
    
#MDD    
    
# S in state IE_FC is elibigible for one stage remission and partial remission    
    in_risk_set(key,'IE_FC','MDD_STATE','RS_MDD_PARTREM') #BDD partrem 
    in_risk_set(key,'IE_FC','MDD_STATE','RS_MDD_1SREM') #BDD one stage rem
    
# S in IE_NFC is eligible for partial relapse, two stage remission   
    in_risk_set(key,'IE_NFC','MDD_STATE','RS_MDD_PARTREL') #BDD partrel
    in_risk_set(key,'IE_NFC','MDD_STATE','RS_MDD_2SREM')   #BDD two stage rem
    
# S in NIE_NP is eligible for full relapse, partial onset
    in_risk_set(key,'NIE_NP','MDD_STATE','RS_MDD_1SREL') #BDD one stage rel
    in_risk_set(key,'NIE_NP','MDD_STATE','RS_MDD_PARTONS') #BDD partial onset

# S in NIE_NFC is eligible for two stage relapse, partial improve
    in_risk_set(key,'NIE_NFC','MDD_STATE','RS_MDD_2SREL')  #BDD two stage rel
    in_risk_set(key,'NIE_NFC','MDD_STATE','RS_MDD_PARTIMP') #BDD partial improve

#S in NIE_NFC is eligible for two stage relapse, partial improve    
    in_risk_set(key,'NIE_NFC','MDD_STATE','RS_MDD_2SREL')  #BDD two stage rel
    in_risk_set(key,'NIE_NFC','MDD_STATE','RS_MDD_PARTIMP') #BDD partimp
    
#FULLREM risk set is union of one and two stage remission
    risk_set_union(key,'RS_MDD_1SREM','RS_MDD_2SREM','RS_MDD_FULLREM')  
    
#FULLREL risk set is union of one and two stage relapse
    risk_set_union(key,'RS_MDD_1SREL','RS_MDD_2SREL','RS_MDD_FULLREL')  

#compute episode number    
    epi_num(key,'MDD')  #episode number
    
dis='BDD'
for key in ['5CC']:
    print(key)
    cpo=subjects[key].get_cpo()
    print(cpo)           
    print(len(cpo['RS_BDD_PARTREM']))

def cp_risk_set(event_col,state_col,event_state,covar,cutoff_week):
    csvf=open(event_col+'.csv','w')
    csvf.write("ID,start,end,episode,flag\n")
    
    for key in subjects:
        if subjects[key].get_instudy():
            ID=subjects[key].get_ID()
            risk_set=subjects[key].get_cpo_col(event_col)
            state=subjects[key].get_cpo_col(state_col)
            episode_number=subjects[key].get_cpo_col(covar)
    
            print "%s %s" % (ID, event_col) 
        
            rs_start=0
            flag='censor'
            maxweek=min(len(risk_set),cutoff_week)
            for i in range(1,maxweek):
                epi=episode_number[i]
                if (risk_set[i]==True and risk_set[i-1]==False):
                    rs_start=i
                    flag='censor'
                elif (risk_set[i]==False and risk_set[i-1]==True):
                    rs_end=i
                    if state[i]==event_state:
                        flag='event'
                    print "        %s %s %s %s %s" % (ID, rs_start, rs_end, epi, flag)
                    csvf.write("%s,%s,%s,%s,%s\n" % (ID, rs_start, rs_end, epi,1))
                    rs_start=None
                elif i==maxweek-1:
                    if risk_set[i]:
                        rs_end=i
                        print "        %s %s %s %s %s" % (ID, rs_start, rs_end, epi, flag)
                        csvf.write("%s,%s,%s,%s,%s\n" % (ID, rs_start, rs_end, epi,2))
                elif episode_number[i] != episode_number[i-1]:
                    flag="covariate"
                    if risk_set[i]:
                        rs_end=i-1
                        last_epi=episode_number[i-1]
                        print "        %s %s %s %s %s" % (ID, rs_start, rs_end, last_epi, flag)
                        csvf.write("%s,%s,%s,%s,%s\n" % (ID, rs_start, rs_end, epi,3))
                
                        
cp_risk_set('RS_BDD_PARTREM','BDD_STATE','IE_NFC','BDD_EPISODE',208)           

#pf=open('bdd_state_python.obj','wb')      
#pickle.dump(subjects,pf,pickle.HIGHEST_PROTOCOL)