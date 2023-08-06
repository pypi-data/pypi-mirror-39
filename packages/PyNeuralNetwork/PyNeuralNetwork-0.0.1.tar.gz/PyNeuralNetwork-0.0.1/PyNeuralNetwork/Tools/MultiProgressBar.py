import sys
import numpy as np
from ColorString import GetFGCode,GetEndFormat

class MultiProgressBar(object):
	def __init__(self,total0,total1,Prefix0='',Prefix1='',Suffix0='',Suffix1='',Percent0=True,Percent1=True,Fraction0=True,Fraction1=True,Length=50,CharDone='=',CharTodo=' ',PercColor=None,FracColor=None):
	
		self.total0 = total0
		self.total1 = total1

		lp0 = len(Prefix0)
		lp1 = len(Prefix1)
		
		mxlp = np.max([lp0,lp1])
		pad0 = ' '*(mxlp - lp0)
		pad1 = ' '*(mxlp - lp1)
		
		self.temp0 = Prefix0 + pad0 + '{:s}' + Suffix0
		self.temp1 = Prefix1 + pad1 + '{:s}' + Suffix0	

		self.Init = False
		self.Percent0 = Percent0
		self.Percent1 = Percent0
		self.Fraction0 = Fraction0
		self.Fraction1 = Fraction1
		
		self.CharDone = CharDone
		self.CharTodo = CharTodo
		self.Length = Length
		
		if PercColor is None:
			self.Pfmt = '{:6.2f}%'
		else:
			self.Pfmt = GetFGCode(PercColor) + '{:6.2f}%' + GetEndFormat()

		
		l0 = str(len(str(abs(self.total0))))
		l1 = str(len(str(abs(self.total1))))
		
		if FracColor is None:
			self.F0fmt = '({:'+l0+'d}/{:'+l0+'d})'
			self.F1fmt = '({:'+l1+'d}/{:'+l1+'d})'
		else:
			self.F0fmt = GetFGCode(FracColor) + '({:'+l0+'d}/{:'+l0+'d})' + GetEndFormat()
			self.F1fmt = GetFGCode(FracColor) + '({:'+l1+'d}/{:'+l1+'d})' + GetEndFormat()
		

		
		
	def UpdateBars(self,i0,i1,HeadStr=''):
		if not self.Init:
			#create space for bars
			sys.stdout.write("\n"*3)
			self.Init=True
			
			
		p0 = np.float32(i0)/self.total0
		p1 = np.float32(i1)/self.total1

		nChar0 = np.int32(np.round(p0*self.Length))
		nChar1 = np.int32(np.round(p1*self.Length))

		bar0 = ' [' + self.CharDone*nChar0 + self.CharTodo*(self.Length-nChar0) + '] '
		bar1 = ' [' + self.CharDone*nChar1 + self.CharTodo*(self.Length-nChar1) + '] '

		str0 = ''+bar0
		str1 = ''+bar1

		P0 = self.Pfmt.format(100*p0)
		P1 = self.Pfmt.format(100*p1)

		
		F0 = self.F0fmt.format(i0,self.total0)
		
		F1 = self.F0fmt.format(i1,self.total1)
		
		if self.Percent0:
			str0 += P0+' '
		if self.Fraction0:
			str0 += F0+' '
		
		if self.Percent1:
			str1 += P1+' '
		if self.Fraction0:
			str1 += F1+' '

		sys.stdout.write('\x1b[1000D')
		sys.stdout.write('\x1b[3A') #this should go up 3 lines
		
		print(HeadStr)	
		print(self.temp0.format(str0))	
		print(self.temp1.format(str1))	
