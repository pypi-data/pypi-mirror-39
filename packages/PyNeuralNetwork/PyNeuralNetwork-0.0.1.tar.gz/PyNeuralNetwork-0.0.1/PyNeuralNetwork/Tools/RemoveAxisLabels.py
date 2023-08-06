import numpy as np

def RemoveAxisLabels(ax,axis='x'):
	if axis == 'y':
		lbl = ax.get_yticklabels()
		ax.set_yticklabels(['']*np.size(lbl))
	else:
		lbl = ax.get_xticklabels()
		ax.set_xticklabels(['']*np.size(lbl))
