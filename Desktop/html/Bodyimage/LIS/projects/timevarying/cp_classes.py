# -*- coding: utf-8 -*-
"""
Created on Thu Jul 7 08:46:18 2016

@author: gquinn
"""

class subj:                                 #subject class
    def get_intake_states(self):               #get intake state 
        return self.intake_state
    def get_intake_state(self,dis):               #get intake state 
        return self.intake_state[dis]
    def set_intake_state(self,init,dis):      #set intake state
        self.intake_state[dis]=init
        return
    def get_cpo(self):                     #return cp entries dictionary
        return self.cpo 
    def get_cpo_len(self,col):              #return cp entries dictionary
        if col in self.cpo:
            col_len=len(self.cpo[col])
        else:
            col_len=0
        return col_len 
    def get_cpo_col(self,col):              #return cp entries
        return self.cpo[col]
    def set_cpo_col(self,cpo_obj,col):       #set cpentries
        self.cpo[col]=cpo_obj
        return
    def set_cpo_values(self,col,start,end,value):
        self.cpo[col][start:end]=[value]*(end-start)
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
    def get_maxtime(self,dis):                      #return max time
        return self.maxtime[dis]
    def set_maxtime(self,maxtime,dis):             #set max time
        self.maxtime[dis]=maxtime
        return
    def __init__(self,ID,SS):      #subject constructor
        self.ID=ID                          #subject ID
        self.initline={}                    #init line images
        self.SS=SS                          #SS number
        self.maxtime={}                     #max time for subject
        self.intake_state={}                #intake state dictionary
        self.instudy=None                   #flag for in study or not
        self.cpo={}                         #ragged array for data
        return