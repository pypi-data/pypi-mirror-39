
class CalculoZ():
	def calcular_z(self, n1, n2, x, y, ux, uy, ox, oy):
		arriba = (x-y)-(ux-uy)
		abajo = (((ox)**2/(n1))+((oy)**2/(n2)))**0.5
		z = arriba/abajo
		return z