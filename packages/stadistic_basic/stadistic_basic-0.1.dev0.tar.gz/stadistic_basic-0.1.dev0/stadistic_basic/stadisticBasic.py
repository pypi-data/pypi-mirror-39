
class StaditicBasic():
	def sums(self, x): #ingresa datos de la poblacion
		cantidad = 0
		for i in x:
			cantidad = cantidad + i
		return cantidad
	def desviacion_estandar(self, y, z, n): # ingresa los datos de la poblacion mas la media y la el total de poblacion
		divicion = 0
		nn = n-1 
		h = [h-z for h in y ]
		f = [f**2 for f in h]
		for i in f:
			divicion = divicion + i
		rest = divicion/nn
		desv_estandar = rest**0.5
		return  desv_estandar 
			
	def nivel_significancia(self, x):
		if x == 90 or x == 10:
			s = 1 - 0.9
			y = round(s,2)
		elif x == 95 or x == 5:
			s = 1 - 0.95
			y = round(s,2)
		elif x == 99 or x == 1:
			s = 1 - 0.99
			y = round(s,2)
		return y
	def regla_decicion(self, x, y):
		talba_z_dos_colas=[1.65, 1.96, 2.58, 3.29]
		talba_z_una_cola = [1.28, 1.65, 2.33]
		if x == 2:
			if y == 0.1: j = talba_z_dos_colas[0]
			if y == 0.05: j = talba_z_dos_colas[1]
			if y == 0.01: j = talba_z_dos_colas[2]
			return j
		if x == 1:
			if y == 0.1: j = talba_z_una_cola[0]
			if y == 0.05: j = talba_z_una_cola[1]
			if y == 0.01: j = talba_z_una_cola[2]
			return j
		
	def validacion_conclucion(self,x,y,z):
		if x > y or x > z: return "se acepta la Ha y se rechaza la Ho"
		if x < y or x < z: return "se acepta la Ho y se rechaza la Ha"