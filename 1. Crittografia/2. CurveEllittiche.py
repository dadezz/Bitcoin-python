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

"""
Ciò che ci serve di questa curva sono le operazioni. In particolare, c'è una cosa chiamata addizione di punti.
Dati due punti appartenenti alla curva, questa operazione ne restituisce un terzo, sempre appartenente alla curva.
Si chiama addizione perché per molti versi richiama l'addizione canonica, per esempio gode della proprietà commutativa.
Definiamo l'addizione nel seguente modo.
Ogni curva può essere intersecata da una retta qualsiasi in uno o tre punti. Solo in due casi particolari i punti
Di intersezione sono due: retta verticale o retta tangente in un punto.
Si può quindi definire l'addizione sfruttando il fatto che la retta si interseca una o tre volte con la curva ellittica
(torneremo ai casi particolari in un secondo momento).
Due punti definiscono una linea. Quindi, dal momento che la linea in questione intersecherà la curva una terza volta,
la proiezione simmetrica rispetto all'asse delle x di questo terzo punto sarà il risultato della nostra addizione.
Per cui, per ogni due punti P1 = (x1, y1) e P2 = (x2, y2), troviamo P1 + P2 in questo modo:
1. Troviamo il terzo punto di intersezione disegnando la retta congiungente i due punti
2. Riflettiamo il punto così trovato rispetto all'asse x (ne troviamo il simmetrico).

L'operazione così definita gode di alcune proprietà matematiche che di norma associamo all'addizione:
1. Esiste l'identità, il valore neutro, per cui I + A = A
2. È commutativa
3. È associativa
4. Esiste l'opposto, per cui A + (-A) = I.
Si noti che i due punti A e -A devono essere verticalmente allineati (caso speciale visto in precedenza).
La proprietà commutativa è ovvia, perché la retta interseca 3 volte la curva a prescindere dall'ordine con cui si prendono i punti.
La proprietà associativa non è invece ovvia ed è la ragione per cui si guarda il simmetrico (non dimostro).
Separo il codice per l'addizione in quattro casi:
1. Punti allineati verticalmente
2. Due punti diversi
3. Due punti coincidenti
4. retta verticale tangente in un solo punto
Vediamo la formula per fare l'addizione in caso di punti diversi. 
Chiamo s il coefficiente angolare (da "slope"). s = (y2-y1)/(x2-x1). 
Con s, possiamo calcolare x3 = s^2-x1-x2. Trovato x3, possiamo calcolare y3 = s(x1-x3)-y1. 
(y3 è il simmetrico rispetto alle ascisse). 
Nel caso di punti coincidenti (retta tangente alla curva), procediamo in modo similare. s = (3*x1^2+a)/2*y1; x3 = s^2-2*x1; y3 = s*(x1-x3)-y1. 
Vediamo ora la formula per il caso 4. Accade se e solo se P1 e P2 hanno la stessa ascissa e ordinata pari a zero. 
In questo caso, il denominatore del coefficiente angolare risuta 0, ma sappiamo che il risultato è l'identità. 
"""

# L'identità (punto all'infinito) sarà nella forma (None, None, a, b)
# Per prima cosa bisogna aggiustare __init__ per evitare che controlli che l'identità appartenga alla curva.
	def __init__(self, x, y, a, b):
		self.a = a
		self.b = b
		self.x = x
		self.y = y
		if self.x is None and self.y is None: 
			return
		if self.y**2 != self.x**3 + a * x + b:
			raise ValueError('({}, {}) is not on the curve'.format(x, y))

# Per seconda cosa ridefiniamo l'operatore __add__
	def __add__(self, other): 
		if self.a != other.a or self.b != other.b: #al solito, controllo che i punti siano validi
			raise TypeError('Points {}, {} are not on the same curve'.format
				(self, other))
		if self.x is None:	#se self.x è "None", significa che self è l'identità, quindi restituisce other
			return other	
		elif other.x is None:	#idem, a parti invertite. 
			return self
		elif self.x == other.x and self.y != other.y:	#se i due punti sono allineati verticalmente, restituisce l'identità 
			return self.__class__(None, None, self.a, self.b)
		elif self.x != other.x:		# caso più comune: due punti non coincidenti
			s = (other.y - self.y)/(other.x - self.x)
			x3 = s^2 - self.x - other.x
			y3 = s*(self.x - x3) - self.y
			return self.__class__(x3, y3, self.a, self.b)
		elif self == other:		#retta tangente alla curva
			s = (3 * self.x**2 + self.a) / (2 * self.y)
			x3 = s**2 - 2 * self.x
			y3 = s * (self.x - x3) - self.y
			return self.__class__(x3, y3, self.a, self. b)
		else:		#ultimo caso
			return self.__class__(None, None, self.a, self.b)
