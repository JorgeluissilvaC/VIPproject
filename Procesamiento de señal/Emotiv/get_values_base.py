dic1 = {'AF3':{'quality':1,'value':2},
	'AF4':{'quality':1,'value':2},
	'F3':{'quality':1,'value':2},
	'F4':{'quality':1,'value':2},
	'F7':{'quality':1,'value':2},
	'F8':{'quality':1,'value':2},
	'FC5':{'quality':1,'value':2},
	'FC6':{'quality':1,'value':2},
	'01':{'quality':1,'value':2},
	'02':{'quality':1,'value':2},
	'P7':{'quality':1,'value':2},
	'P8':{'quality':1,'value':2},
	'T7':{'quality':1,'value':2},
	'T8':{'quality':1,'value':2},
	'Unknown':{'quality':1,'value':2},
	'X':{'quality':1,'value':2},
	'Y':{'quality':1,'value':2},
	'Y':{'quality':1,'value':2},
	}
dic2= {'AF3':{'quality':1,'value':3},
	'AF4':{'quality':1,'value':3},
	'F3':{'quality':1,'value':23},
	'F4':{'quality':1,'value':23},
	'F7':{'quality':1,'value':23},
	'F8':{'quality':1,'value':23},
	'FC5':{'quality':1,'value':32},
	'FC6':{'quality':1,'value':23},
	'01':{'quality':1,'value':23},
	'02':{'quality':1,'value':23},
	'P7':{'quality':1,'value':23},
	'P8':{'quality':1,'value':23},
	'T7':{'quality':1,'value':23},
	'T8':{'quality':1,'value':23},
	'Unknown':{'quality':1,'value':23},
	'X':{'quality':1,'value':23},
	'Y':{'quality':1,'value':23},
	'Y':{'quality':1,'value':23},
	}

ldic =[]
ldic.append(dic1)
ldic.append(dic2)
dicx = ldic[0].copy()
for key,value in dicx.iteritems():
	dicx[key] = []
for i in ldic:
	for key, value in i.iteritems():
		value = i[key]['value']
		quality = i[key]['quality']
		dicx[key].append((quality,value))
		pass

print dicx
