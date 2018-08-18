from datetime import datetime
import datetime

class cycle:
	def get_cycle_start(self):
		return(self.cycle_start)

	def get_scheduled(self):            
		'''returns the four shifts scheduled in this cycle'''
		return(self.scheduled_shifts)

	def get_cycle(self):            
		''' returns the 16 shifts scheduled in this 8-day cycle '''
		return(self.cycle_shifts)

	def add_shift(self,ts,sched,shft):
		self.cycle[ts] = {}
		self.cycle[ts]['shift'] = shft
		self.cycle['scheduled'] = sched
		return

	def __init__(self,starttime,shifts):    
		''' Constructor for cycle class '''
		self.cycle = {}
		self.cycle_start = starttime
		ts = self.cycle_start
		self.add_shift(ts,True,shifts[ts])
		ts += datetime.timedelta(days=1)
		self.add_shift(ts,True,shifts[ts])
		ts += datetime.timedelta(days=1)
		ts += datetime.timedelta(hours=10)   # increment cycle start by 10 hours + 1 day
		self.add_shift(ts,True,shifts[ts])
		ts += datetime.timedelta(days=1)
		self.add_shift(ts,True,shifts[ts])
		ts = self.cycle_start
		for hrs in [10,24,14,24,10,14,10,14,10,14,10,14]:
			ts += datetime.timedelta(hours=hrs)
			self.add_shift(ts,False,shifts[ts])
		return

class shift:
	def get_hours(self):
		''' Returns number of hours in this shift '''
		return(self.hours)

	def get_day_shift(self):
		return(self.day_shift)

	def get_shift_crew(self):
		return(self.crew)

	def get_platoon(self):
		return(self.platoon)

	def __init__(self,ts,platoon,platoons):
		''' Constructor for shift class '''
		self.shift_start = ts               #start of shift
		self.platoon = platoon     	    #platoon scheduled
		if (ts.hour == 7):                  #If day shift:
			self.day_shift = True       #  Boolean day_shift is True
			self.hours = 10.0           #  Number of hours is 10
		else:                               #If night shift:
			self.day_shift = False      #  Boolean day_shift is False
			self.hours = 14.0           #  Number of hours is 14
		self.crew = shift_crew(platoons,platoon,ts)  #Crew list
		return

class shift_crew:
	def printx(self):
		for ffn in ['OF1','OF2','OF3','OF4','FF1','FF2','FF3','FF4','FF5']:
			print(ffn)
			print(type(self.crew[ffn]['FF']))
		return

	def get_crew(self):
		return(self.crew)

	def __init__(self,platoons,platoon,shift_start):
		''' Constructor for shift crew '''
		self.platoon = platoons[platoon]
		self.shift_start = shift_start
		self.crew = {}
		tsdat = shift_start.date()
		plt = self.platoon.get_ffs()
		for ffn in ['OF1','OF2','OF3','OF4','FF1','FF2','FF3','FF4','FF5']:
			self.crew[ffn] = {}
			self.crew[ffn]['FF'] = None
			for dat in plt[ffn].keys():
				if (dat <= tsdat):
					if (plt[ffn][dat]['end_date'] is None):
						self.crew[ffn]['FF'] = plt[ffn][dat]['ff']
					elif (plt[ffn][dat]['end_date'] >= tsdat):
						self.crew[ffn]['FF'] = plt[ffn][dat]['ff']
		return

class platoon:
	def get_ffs(self):
		return(self.ffs)

	def add_ff(self,pos,ff,start_date,end_date):
		if (pos not in self.ffs.keys()):
			self.ffs[pos] = {}
		self.ffs[pos][start_date] = {}
		self.ffs[pos][start_date]['ff'] = ff
		self.ffs[pos][start_date]['end_date'] = end_date
		return
		
	def __init__(self,platoon):
		''' Constructor for platoon class '''
		self.platoon_id = platoon
		self.ffs = {}

		return

class FF:
	def get_rank(self,date):
		current_rank = None
		for rank in self.ranks.keys():
			if ((ranks[rank]['fromdate']<=date) & (ranks[rank]['todate']>=date)):
				current_rank = rank
		return(current_rank)

	def set_rank(self,rank,fromdate,todate):
		ranks[rank] = {}
		ranks[rank]['fromdate'] = fromdate
		ranks[rank]['todate'] = todate
		return

	def get_name(self):
		name = self.lname + ', ' + self.fname
		return(name)

	def __init__(self,fname,lname,start_date,end_date):    
		''' Constructor for firefighter class '''
		self.fname = fname
		self.lname = lname
		self.full_name = lname + ', ' + fname
		if (start_date is None): self.start_date = datetime.date(2010,1,1)	
		else: self.start_date = None
		self.end_date = end_date
		self.ranks = {}
		self.names = {}
		



 





