# -*- coding: utf-8 -*-
"""
Created on Sat Jun 18 07:40:18 2016

@author: gquinn
"""


class cpentry:
    def get_start(self):
        return self.start
    def set_start(self,start):
        self.start=start
        return
    def get_end(self):
        return self.end
    def set_end(self,end):
        self.end=end
        return
    def get_state(self):
        return self.state
    def set_state(self,state):
        self.state=state
        return
    def __init__(self,start,end,state):
        self.start=start
        self.end=end
        self.state=state
        return

class subj:
    def get_init(self):
        return self.init
    def set_init(self,init,dis):
        self.init[dis]=init
        return
    def get_cpentries(self):
        return self.cpentries
    def set_cpentries(self,cpentries):
        self.cpentries=cpentries
        return
    def get_ID(self):
        return self.ID
    def set_ID(self,ID):
        self.ID=ID
        return
    def get_maxwk(self):
        return self.maxwk
    def set_maxwk(self,maxwk):
        self.maxwk=maxwk
        return
    def __init__(self,ID,SS,scd102,scd104,scd106):
        self.ID=ID
        self.scd102=scd102
        self.scd104=scd104
        self.scd106=scd106
        self.SS=SS
        self.maxwk=None
        self.cpentries=[]
        return