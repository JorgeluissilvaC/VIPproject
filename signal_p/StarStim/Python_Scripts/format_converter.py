listol = [[0, 1, 2, 3, 4, 5, 6, 7],
	[7, 6, 5, 4, 3, 2, 1, 0],
	[0, -1, -2, -3, -4, -5, -6, -7],
	[-7, -6, -5, -4, -3, -2, -1, 0]]
dic = {}
for n in range(0,len(listol)):
	dic['e'+str(n+1)] = []
	for lista in listol:
		dic['e'+str(n+1)].append(lista[n])

print(dic) 

