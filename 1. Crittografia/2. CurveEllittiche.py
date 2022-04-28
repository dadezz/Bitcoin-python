"""
Le curve ellittiche hanno una forma del tipo y^2 = x^3 + ax + b.
Il grafico risulta simmetrico rispetto all'asse delle x. La si può visualizzare tramite un
Qualsiasi software di creazione grafici, comunque ci si può immaginare una cubica sulle ordinate
Positive e il suo simmetrico su quelle negative, con gli angoli "smussati".
Specificamente, ma lo si vedrà bene nel capitolo successivo, la curva ellittica
Usata per il bitcoin ha equazione y^2 = x^3 + 7, ovvero a=0 e b=7 nell'eqazione canonica.
Per i nostri fini, non siamo interessati alla curva in sé, ma ai singoli punti a essa appartenenti.
Definiamo quindi la classe "point", che identifica uno specifico punto e le sue coordinate.
Usiamo le variabili a, b per identificare i parametri della equazione canonica.
"""

class Point:
	def __init__(self, x, y, a, b):
		self.a = a
		self.b = b
		self.x = x
		self.y = y
		if self.y**2 != self.x**3 + a * x + b: 

			#controllo che il punto appartenga alla curva, 
			#ovvero ne soddisfi l'equazione
			raise ValueError('({}, {}) is not on the curve'.format(x, y))
	def __eq__(self, other):
		#due punti sono uguali se e solo se sono uguali le coordinate e
		#appartengono alla stessa curva. 
		return self.x == other.x and self.y == other.y \
			and self.a == other.a and self.b == other.b
	def __ne__(self, other):
		#alle stesse condizioni se i punti son diversi
		return self.x != other.x and self.y != other.y \
			and self.a != other.a and self.b != other.b 
