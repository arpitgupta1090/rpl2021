from .models import parmtable


class Envariable(object):

	def __init__(self):
		self.sid = self.setVariables('sid')
		self.baseamount = int(self.setVariables('baseamount'))
		self.noofwindict = int(self.setVariables('noofwindict'))
		self.noofselectdict = int(self.setVariables('noofselectdict'))
		self.noofleaders = int(self.setVariables('noofleaders'))
		self.scorestatus = self.setVariables('scorestatus')
		self.select1status = self.setVariables('select1status')
		self.select2status = self.setVariables('select2status')
		self.s1point = self.setVariables('s1point')
		self.s2point = self.setVariables('s2point')
		self.s1desc = self.setVariables('s1desc')
		self.s2desc = self.setVariables('s2desc')
		self.sbit = self.setVariables('sbit')

	def setVariables(self, gvar):
	
		dict1 = {}
		all_parm = parmtable.objects.all()
		for parm in all_parm:
			dict1[parm.parm_key] = parm.parm_data
		return dict1.get(gvar)
