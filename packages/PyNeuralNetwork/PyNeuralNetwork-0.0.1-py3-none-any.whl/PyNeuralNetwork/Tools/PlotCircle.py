import numpy as np

def PlotCircle(fig,r,x0=0.0,y0=0.0,linewidth=1.0,linestyle='-',zorder=2,color=[0.0,0.0,0.0],fill=None):

	a=np.arange(361,dtype='float32')*np.pi/180.0
	x=r*np.sin(a)+x0
	y=r*np.cos(a)+y0
	if (fill is None) == False:
		fig.fill(x,y,color=fill,zorder=zorder)
	fig.plot(x,y,color=color,linestyle=linestyle,linewidth=linewidth,zorder=zorder)
	
