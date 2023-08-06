
class HallarPorQorZ():
	def hallar_P(self,n,u):
		div = u/n
		return div
	def hallar_q(self,n,u):
		arriba = n-u 
		abajo = n
		div = arriba/abajo
		return div
	def hallar_z(self,p,PP,q,n):
		arriba = p-PP
		abajo = (p*q)/n
		abajo_Def = abajo**0.5
		respuesta = arriba/abajo_Def
		return respuesta