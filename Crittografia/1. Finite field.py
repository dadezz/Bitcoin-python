"""
Un campo finito è un campo algebrico in cui vi è un numero finito di elementi. In particolare, 
Le operazioni di moltiplicazione e addizione sono chiuse nel campo, ovvero sono definite in modo tale
da ritornare un numero appartenente al campo stesso (per esempio addizione modulare). 

Chiamo p l'ordine (la grandezza) del campo, che avrà quindi elementi {0, 1, 2, ... , p-1}
Ovviamente, l'ordine sarà sempre maggiore di un unità rispetto all'elemento più grande. 
I campi che interessano a noi sono i campi il cui ordine è un numero primo. (notare che un campo finito  
Ha sempre un ordine che è potenza di un primo). 
"""

class FieldElement:
	def __init__(self, num, prime):
		#controllo semplicemente che il numero appartenga al campo
		if num >= prime or num < 0: 
			error = 'Num {} not in field range 0 to {}'.format(
num, prime - 1)
			raise ValueError(error)
		self.num = num #elemento del campo
		self.prime = prime #prime è quindi l'ordine del campo

	def __repr__(self):
		#formattazione elementi del campo
		return 'FieldElement_{}({})'.format(self.prime, self.num)

	def __eq__(self, other):
		if other is None:
			return False
		return self.num == other.num and self.prime == other.prime

	def __ne__(self, other):
		if other is None:
			return True
		return self.num != other.num and self.prime != other.prime 
