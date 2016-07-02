# -*- coding: utf-8 -*-
"""
Created on Sat Jun 18 07:40:18 2016

@author: gquinn
"""
class cpobj:                      #counting process object class
    def cp_add(self,time,flag):                 #add a cp entry
        for i in range(0,len(self.start)):      #find insertion point
            if(self.start[i]<=time):            #start must be <= time
                if(self.end[i] >= time):        #end must be >= time
                    temp_end=self.end[i]        #copy current end time
                    temp_flag=self.flag[i]      #copy current flag
                    temp_cov=self.covariates[i].copy() #copy covariates
                    self.end[i]=time            #set end time=time
                    self.flag[i]=flag           #set flag=input flag
                    self.start.insert(i,time)   #new entry with start=time
                    self.end.insert(i,temp_end) #copy old end time
                    self.flag.insert(i,temp_flag) #copy old flag
                    self.covariates.insert(i,temp_cov) #copy old covariates
        return
    def get_covariates(self):                   #return covariates dictionary
        return self.covariates
        
    def set_covariates(self,start,end,key,value): #set covariates value
        instart=False                             #check if start time in list
        for i in range(0,len(self.start)):        #loop through start
            if(self.start[i]==start):             #set instart=True if match
                instart=True
        if(instart==False):                       #if it's not there
            self.cp_add(start,4)                  # add it
        inend=False                               #check if end time in list
        for i in range(0,len(self.end)):          #loop through end times
            if(self.end[i]==end):                 #set inend=true if match
                inend=True
        if(inend==False):                         #if it's not there
            self.cp_add(end,4)                    # add it
        for i in range(0,len(self.start)):        #now loop through cp entries
            if (self.start[i]<=start & self.end[i]>=end):  #if start/end match
                self.covariates[i][key]=value     #set covariates value
        return
        
    def print_cp(self):
        for i in range(0,len(self.start)):        #print cp entry
            print "%d %d %d" % (self.start[i], self.end[i], self.flag[i])
            print(self.covariates[i])
        return        
        
    def __init__(self,start,end):                 #cpobj constructor
        self.start=[]
        self.end=[]
        self.flag=[]
        self.covariates=[]
        self.start.insert(0,start)
        self.end.insert(0,end)
        self.flag.insert(0,2)
        self.covariates.insert(0,{})
        return

class scentry:           #state change entry class
    def get_start(self):                    #return start time  
        return self.start
    def set_start(self,start):              #set start time
        self.start=start
        return
    def get_end(self):                      #return end time
        return self.end
    def set_end(self,end):                  #set end time
        self.end=end
        return
    def get_state(self):                    #get state
        return self.state              
    def set_state(self,state):              #set state
        self.state=state
        return
    def __init__(self,start,end,state):     #cpentry constructor
        self.start=start
        self.end=end
        self.state=state
        return

class cpentry:           #counting process entry class
    def get_start(self):                    #return start time  
        return self.start
    def set_start(self,start):              #set start time
        self.start=start
        return
    def get_end(self):                      #return end time
        return self.end
    def set_end(self,end):                  #set end time
        self.end=end
        return
    def get_flag(self):                    #get state
        return self.flag              
    def set_state(self,flag):              #set state
        self.flag=flag
        return
    def __init__(self,start,end,flag):     #cpentry constructor
        self.start=start
        self.end=end
        self.flag=flag
        return

class cp:       #counting process class
    def get_cpentries(self):              #return cp entries
        return self.cpentries
    def set_cpentries(self,cpentries):       #set cpentries
        self.cpentrie=cpentries
        return
    def __init__(self,cpid):
        self.cpid=cpid
        self.cpentries=[]

class subj:                                 #subject class
    def get_intake_states(self):               #get intake state 
        return self.intake_state
    def get_intake_state(self,dis):               #get intake state 
        return self.intake_state[dis]
    def set_intake_state(self,init,dis):      #set intake state
        self.intake_state[dis]=init
        return
    def get_cpdict(self):                     #return cp entries dictionary
        return self.cpdict 
    def get_cpentries(self,dis):              #return cp entries
        return self.cpdict[dis]
    def set_cpentries(self,cpentries,evt):       #set cpentries
        self.cpdict[evt]=cpentries
    def get_scdict(self):                     #return cp entries dictionary
        return self.scdict 
    def get_scentries(self,dis):              #return cp entries
        return self.scdict[dis]
    def set_scentries(self,scentries,dis):       #set cpentries
        self.scdict[dis]=scentries
        return
    def get_ID(self):                         #return ID
        return self.ID
    def set_ID(self,ID):                      #set ID
        self.ID=ID
        return
    def set_instudy(self,val):
        self.instudy=val
        return
    def get_instudy(self):
        return self.instudy
    def get_initlines(self):                   #return initline dictionary
        return self.initline
    def get_initline(self,dis):                #return initline entry
        return self.initline[dis]
    def set_initline(self,dis,iline):         #return initline for disorder
        self.initline[dis]=iline
        return
    def get_maxtime(self):                      #return max time
        return self.maxtime
    def set_maxtime(self,maxtime):             #set max time
        self.maxtime=maxtime
        return
    def __init__(self,ID,SS):      #subject constructor
        self.ID=ID                          #subject ID
        self.initline={}                    #init line images
        self.SS=SS                          #SS number
        self.maxtime=None                   #max time for subject
        self.intake_state={}                #intake state dictionary
        self.scdict={}
        self.cpdict={}                      #cp entries dictionary
        self.instudy=None
        return