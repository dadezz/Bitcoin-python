"""
Uno strumento matematico che si può usare per chiudere l'addizione e la moltiplicazione
All'interno di un campo finito è l'aritmetica modulare.
La si trova alle elementari quando si imparano a fare le divisioni. Se la divisione non
Restituiva un numero intero, spuntava fuori il resto. Il resto è sempre un elemento del
Campo finito. Si pensi per esempio a un campo di ordine 60: una divisione per 60 può dare
Come resto esclusivamente un numero all'interno della lista di elementi {1,2,...,59}. Di
Conseguenza, l'aritmetica modulare è sempre chiusa nel campo.
"""

>>>a, b = 5, 3
>>>c = a%b		6=# il modulo si indica con %
>>>print(c)	# il risultato è 2, ovvero il resto della divisione

"""
Ecco quindi che si può definire l'addizione modulare. Senza astrazioni, la si può visualizzare con un orologio, 
Il cui elemento più grande è 24.
Se sono le 22, fra 3 ore che ore saranno? Non le 25, sarà l'1.
Notare che 1 è il resto della divisione di (22+3) per 24.
Formalmente, definiamo quindi l'addizione modulare come il resto della divisione dei due numeri sommati per il modulo.
"""
>>>mod = 24
>>>a, b = 22, 3
>>>c = (a+b)%mod
>>>print(c)	# il risultato è 1.

# Arriviamo quindi alla definizione del metodo per la classe Finitefield:

def __add__(self, other):
	#controllo che l'ordine del campo sia lo stesso, perché non posso sommare due
	#numeri con moduli diversi, non ha nessun significato matematico
	if self.prime != other.prime:
		raise TypeError('Cannot add two numbers in different fields')
	num = (self.num + other.num) % self.prime
	return self.__class__(num, self.prime)

def __sub__(self, other):
	#allo stesso modo definisco la sottrazione
	if self.prime != other.prime:
		raise TypeError('Cannot add two numbers in different fields')
	num = (self.num - other.num) % self.prime
	return self.__class__(num, self.prime)

"""
Moltiplicare significa sommare molte volte e elevare all'esponente significa moltiplicare molte volte.
Avendo quindi capito l'addizione modulare, non sarà difficile definire le altre due.
Supponiamo un campo di ordine 19:
8*17 = (8+8+8+8+8+8+8+8)%19 = 136%19 = 3
7^3  = (7*7*7)%19 = 343%19 = 1.
Può sembrare controintuitivo, ma le operazioni vanno definite in questo modo per far sì 
Che il risultato risulti sempre un elemento del campo.
"""
def __mul__(self, other):
	if self.prime != other.prime:
		raise TypeError('Cannot add two numbers in different fields')
	num = (self.num * other.num) % self.prime
	return self.__class__(num, self.prime)

def __pow__(self, exponent):
	num = (self.num ** exponent) % self.prime 
	return self.__class__(num, self.prime)
# l'elevazione a potenza si può rifare in modo più efficiente come pow(self.num, exponent, self.prime)

"""
Sfortunatamente, per la divisione le cose si complicano, non è così intuitiva. Nella matematica a cui siamo abituati,
La divisione è l'inversa della moltiplicazione. 5*8=56 implica che 56/8=7. Non si può dividere per 0
In un campo finito di ordine 19, sappiamo che 3*7=2 e xhe 9*5=7. Implicherebbe quindi 2/7=3 e 7/5=9. Decisamente controintuitivo
Pensare che delle frazioni abbiano come risultato elementi interi del campo.
Come calcolo 2/7 se non so a priori che 3*7=2? La risposta ci arriva dal piccolo teorema di Fermat, che non dimostro qui: (n^(p-1)%p=1, con p numero primo.
Dal momento che la divisione è l'inverso della moltiplicazione,
a/b = a*(1/b) = a*b^(-1). Possiamo ridurre la divisione a una moltiplicazione a patto di conoscere b^(-1), ed è qui che entra in gioco Fermat.
Sappiamo che b^(p-1)=1, perché p è primo. Da cui b^(-1) = b^(-1)*1 = b^(-1)*b^(p-1) = b^(p-2). Possiamo quindi calcolare l'inverso usando l'esponente.
Un esempio in un campo di ordine 19: 2/7 = 2*7
^(19–2) = 2*7
^17, = 465261027974414%19 = 3
"""

def __truediv__(self, other):
	if self.prime != other.prime:
		raise TypeError('Cannot add two numbers in different fields')
	num = (self.num * other.num ^ (self.prime - 2))%self.prime
	return self.__class__(num, self.prime)

"""
Ultima cosa da fare è sistemare gli esponenti negativi.
Ci viene incontro sempre il piccolo teorema di Fermat.
Siccome a^(p–1)=1, possiamo moltiplicare per a^(p-1) quante volte vogliamo.
Da cui a^-3 = a^-3*a^(p-1) = a^(p-4)
"""

# ridefinisco quindi il metodo __pow__
def __pow__(self, exponent):
	n = exponent % (self.prime - 1) 
	num = pow(self.num, n, self.prime)
	return self.__class__(num, self.prime)
