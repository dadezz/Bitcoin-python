"""
I due capitoli precedenti han trattato la matematica fondamentale riguardante i campi finiti e le curve ellittiche. Unendo i due concetti, arriviamo adesso
al succo del discorso, arrivando a comprendere la crittografia a curva ellittica. Specificatamente, impareremo le primitive necessarie per firmare e
verificare un messaggio, che è ciò che è alla base di ciò che fa il Bitcoin.
Nel capitolo 2 abbiamo visto la curva ellittica all'interno dei numeri reali. Anch'essi sono un campo, con tutte le caratteristiche del FiniteField, esclusa
la finitezza (ci sono infiniti elementi).
Visualizzare una curva in R è facile, ma come appare in un campo finito? proviamo a vedere secp256k1 (l'equazione di Bitcoin) in F(103). Possiamo verificare
facilmente che il punto (17, 64) appartiene alla curva, calcolando e confrontando entrambi i lati dell'equazione:
y^2 = 64^2 % 103 = 79
x^3 + 7 = (17^3 + 7) % 103 = 79 //
Il grafico dell'equazione in un campo finito ha un aspetto competamente diverso, un insieme di punti in disordine, nulla a che fare con una "curva", cosa che
non stupisce, essendo i punti discreti e non continui. L'unico pattern riconoscibile è la simmetria (dovuta al termine y^2) rispetto a la linea parallela
all'asse x a metà dell'asse y (non rispetto all'asse x perché non ci sono numeri negativi).
è strabiliante il fatto che possiamo usare la stessa equazione per la somma dei punti con l'addizione, sottrazione, moltiplicazione, divisione ed elevamento
a potenza come li abbiamo definiti per il campo finito, e continua tutto a funzionare. Potrebbe sembrare sorprendente, ma questo tipo di regolarità sono 
tipiche della matematica astratta.
Siccome abbiamo definito un punto sulla curva ellittica e le operazioni nel campo finito, possiamo combinare le due classi per creare dei punti appartenenti
alla curva ellittica su un campo finito perché venga fuori questo risultato:

>> import FieldElement, Point
>> a = FieldElement(num=0, prime=223)
>> b = FieldElement(num=7, prime=223)
>> x = FieldElement(num=192, prime=223)
>> y = FieldElement(num=105, prime=223)
>> p1 = Point(x, y, a, b)
>> print(p1)
>> Point(192,105)_0_7 FieldElement(223)

a, b sono i coefficienti dell'equazione secp256k1 (0 e 7), x e y sono le coordinate del punto, prime è l'ordine del campo.
Quando inizializziamo "point", useremo la parte di codice dettata dal metodo __init__ della classe Point.
le operazioni matematiche sono i metodi __add__, __mul__ etc da noi definiti nella classe finite field, e non gli equivalenti classici.
"""

# è utile creare un test per vedere se stiamo procedendo nel modo corretto

class ECCTest(TestCase):
    def test_on_curve(self):
        prime = 223        # definisco l'ordine del campo
        a = FieldElement(0, prime)        # definisco i due coefficienti dell'equazione
        b = FieldElement(7, prime)
        valid_points = ((192, 105), (17, 56), (1, 193))       # coppie di coordinate valide
        invalid_points = ((200, 119), (42, 99))
        for x_raw, y_raw in valid_points:
            x = FieldElement(x_raw, prime)
            y = FieldElement(y_raw, prime)
            Point(x, y, a, b)       # passo gli oggetti della classe FieldElement alla classe Point. questo 
                                    # farà sì che le operazioni matematiche usate saranno quelle definite da noi
        for x_raw, y_raw in invalid_points:
            x = FieldElement(x_raw, prime)
            y = FieldElement(y_raw, prime)
            with self.assertRaises(ValueError):
                Point(x,y,a,b)        #idem come sopra, ma gestisco l'errore

"""
Nel momento in cui lo si va a eseguire, ritornerà un risultato positivo.
>>> from helper import run
>>> run(ECCTest('test_on_curve'))
.
----------------------------------------------------------------------
Ran 1 test in 0.001s
OK

Per fare la somma di punti, possiamo usare la stessa equazione nel campo finito (inclusa la retta y=mx+b). La somma dei punti non funziona solo in R, ma
anche nel campo finito perché è la curva ellittica stessa che esiste e funziona in entrambi i campi. In particolare, quando x1 ≠ x2 P:
1 = (x1,y1), P2 = (x3,y3), P3 = (x3,y3)
P1 + P2 = P3
s = (y3 – y1)/(x3 – x1)
x3 = s^2 – x1 – x3
y3 = s(x1 – x3) – y1
e,quando P1 = P2:
P1 = (x1,y1), P3 = (x3,y3)
P1 + P1 = P3
s = (3*x1^2 + a)/(2y1)
x3 = s^2 – 2*x1
y3 = s(x1 – x3) – y1

Come si programma, nella pratica, la somma di punti? dal momento che abbiamo già definito i metodi __add__ , __sub__ , __mul__ , __truediv__ , __pow__ ,
__eq__ e __ne__ in nella classe FieldElement, ci basta inzializzare Point con gli oggetti di FieldElement, e l'operazione funzionerà in automatico.
>>> prime = 223
>>> a = FieldElement(num=0, prime=prime)
>>> b = FieldElement(num=7, prime=prime)
>>> x1 = FieldElement(num=192, prime=prime)
>>> y1 = FieldElement(num=105, prime=prime)
>>> x2 = FieldElement(num=17, prime=prime)
>>> y2 = FieldElement(num=56, prime=prime)
>>> p1 = Point(x1, y1, a, b)
>>> p2 = Point(x2, y2, a, b)
>>> print(p1+p2)
Point(170,142)_0_7 FieldElement(223)
Possiamo anche estendere il programmino di test per far sì che esegua anche le somme 
"""

def test_add(self):
    prime = 223       # Ordine del campo
    a = FieldElement(0, prime)        # coefficienti dell'equazione
    b = FieldElement(7, prime)
    additions = (
      # lista di coordinate nel formato (x1, y1, x2, y2, x3, y3)
      # servono per fare il test successivamente
      (192, 105, 17, 56, 170, 142),
      (47, 71, 117, 141, 60, 139),
      (143, 98, 76, 66, 47, 71),
      )
    for x1_raw, y1_raw, x2_raw, y2_raw, x3_raw, y3_raw in additions:
        x1 = FieldElement(x1_raw, prime)
        y1 = FieldElement(y1_raw, prime)
        p1 = Point(x1, y1, a, b)        # creo l'oggetto punto dalle coordinate di "additions"
        x2 = FieldElement(x2_raw, prime)
        y2 = FieldElement(y2_raw, prime)
        p2 = Point(x2, y2, a, b)        # creo il secondo punto
        x3 = FieldElement(x3_raw, prime)
        y3 = FieldElement(y3_raw, prime)
        p3 = Point(x3, y3, a, b)        # il terzo è quello che dovrebbe essere il risultato
        self.assertEqual(p1 + p2, p3)   # controllo l'uguaglianza (NB: le coordinate le ho scelte io a priori)

"""
Ovviamente,un punto si può sommare a sé stesso,e poi di nuovo il risultato sommarlo al punto iniziale quante volte si vuole. Si definisce cosi il prodotto per uno scalare.
Caratteristica peculiare è la difficoltà nel predire la posizione del punto risultante senza effettivamente calcolarne le somme. 
Se la moltiplicazione è semplice da fare,non lo è la divisione, ed è questa caratteristica che è la base effettiva della crittografia a curva ellittica (d'ora in poi
Chiamerò questa caratteristica "discrete log problem" o DLP). Un'altra  proprietà è che a un certo multiplo del punto si arriva ad avere il punto all'infinito come risultato.
Per ogni punto G c'è quindi un set di multipli {G, 2G, 3G, ..., nG}, con nG=0. Questo set è chiamato gruppo finito ciclico. È interessante dal
Punto di vista matematico perché si comporta bene con le proprietà della somma: aG + bG = (a + b)G.
unendo queste caratteristiche matematiche al DLP, si arriva alla crittografia.
Moltiplicare per uno scalare significa sommare lo stesso punto a sé stesso n volte. I risultati di questa operazione in un campo finito sono particolarmente randomici, e 
questa caratteristica è ciò che rende la moltiplicazione un'operazione asimmetrica: è facile da calcolare in una direzione ma non in quella inversa (divisione). L'unico modo per
venirne. All'interno del gruppo ciclico finito, l'operazione (somma di punti) gode di alcune imporantissime proprietà: identià, associazione, commmutazione, inversibilità, chiusura.
Vediamo quindi come programmare la moltiplicazione per uno scalare:
"""

#in python, il metodo __rmul__ sovrascrive l'operatore moltiplicazione.

class Point:
    # ...
    def __rmul__(self, coefficient):
        # il prodotto è un'iterazione di somme, quindi basta imporre che inizialmente sia = 0
        product = self.__class__(None, None, self.a, self.b):
        # e poi sommare allo 0 il punto in questione (self) n volte (coefficient)
        # ogni iterazione del ciclo fa questo: sommare un'ulteriore volta il numero a sé stesso
            for _ in range(coefficient):
                product += self
            return product

# questo metodo va bene per coefficienti piccoli, ma quando questi diventano più grandi risulta impossibile calcolare il tutto in un tempo accettabile.
# usiamo quindi la tecnica dell'espansione binaria:

# class Point:
    def __rmul__ (self, coefficient):
        coef = coefficient
        current = self 
        # current rappresenta il punto che è al bit corrente. la prima iterazione nel loop rappresenta
        # 1*self, la seconda sarà 2*self, la terza 4*self, la quarta 8*self e così via le potenze di due.
        # viene raddoppiato il punto a ogni iterazione (in binario i coefficienti sono 1, 10, 100, 1000...)
        result = self.__class__(None, None, self.a, self.b)         # come nel metodo precedente, si parte dallo 0
        while coef:
            if coef & 1:        # vediamo se il bit più a destra è un 1. in tal caso, sommiamo il valore del bit corrente
                result += current
            current += current      # dobbiamo raddoppiare il punto finché non superiamo la grandezza massima del coefficiente
            coef >>=1       # spostiamo il coeefficiente di un bit a destra
        return result 

    """
    DEFINIRE LA CURVA DI BITCOIN
    i numeri primi finora usati sono troppo piccoli per evitare un attacco brute force.
    Una curva ellittica per la crittografia a chiave pubblica è definita a partire da questi parametri:
    1. si specificano i coefficienti a e b dell'equazione
    2. si definisce l'ordine (il prime) del campo finito
    3. si specificano le coordinate x,y del punto G generatore
    4. si specifica l'ordine del gruppo generato da G, n.
    
    I parametri della curva secp256k1 sono:
    1. a = 0, b = 7
    2. p = 2^256 - 2^32 - 977
    3. x(G) = 0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798, y(G) = 0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8
    4. n = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141.
    
    oltre a essere una curva relativamente semplice, è da notare che l'ordine del campo finito è estremamente vicino a 2^256, 
   la maggior parte dei numeri inferiori a 2^256 è nel campo finito e di conseguenza ogni numero nella curva ha le coordinate x e y esprimibili ognuna in 256 bits. Siccome anche
   n è molto vicino a 2^256, anche qualsiasi multiplo scalare dei punti è esprimibile in 256 bit. Terzo, 2^256 è un numero enorme, ma ogni numero inferiore può essere memorizzato
   in 32 bytes, rendendoci di fatto abbastanza facile rappresentare le chiavi private.
   """

# possiamo verificare con python che il punto G appartenga alla curva:
gx = 0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798
gy = 0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8
p = 2**256 - 2**32 - 977
print(gy**2 % p == (gx**3 + 7) % p)
# >>> True

# possiamo verificare anche che il punto G generi un campo ciclico di ordine n:
import FieldElement, Point
n = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141
x = FieldElement(gx, p)
y = FieldElement(gy, p)
seven = FieldElement(7, p)
zero = FieldElement(0, p)
G = Point(x, y, zero, seven)
print(n*G)
# >>> Point(infinity).

# Siccome sappiamo la curva con cui lavoreremo, possiamo creare una subclass per usare esclusivamente i parametri di secp256k1

P = 2**256 - 2**32 - 977
class S256Field(FieldElement):
    
    # facciamo una sottoclasse in modo da non dover specificare P ogni volta.
    def __init__(self, num, prime=None):
        super().__init__(num=num, prime=P)
    
    # vogliamo rappresentare il numero sempre con 64 caratteri, vedendo anche gli zeri iniziali
    def __repr__(self):
        return '{:x}'.format(self.num).zfill(64)

# Allo stesso modo, possiamo definire la sottoclasse che definisce i punti della curva

A, B = 0, 7
class S256Point(Point):
    
    def __init__(self, x, y, a=None, b=None):       # None significa che non serve che venga inserito (perché assegnato successivamente nella sottoclasse)
        a, b = S256Field(A), S256Field(B)
    if type(x) == int:
        super().__init__(x=S256Field(x), y=S256Field(y), a=a, b=b)
    else:       # nel caso inizializzassimo il punto all'infinito
        super().__init__(x=x, y=y, a=a, b=b)

"""
Abbiamo ora un modo più facile per inizializzare un punto della curva secp256k1, senza dover secificare ogni volta i valori di a e b.
Possiamo anche definire __rmul__ in modo un po' più efficiente, dal momento che conosciamo l'ordine del gruppo, n.
(usiamo N maiuscolo come convenzione per definire una costante e non una variabile)
"""
N = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141
class S256Point(Point):
    def __rmul__(self, coefficient):
        coef = coefficient % N      # possiamo passare al modulo n perché nG = 0
        return super().__rmul__(coef)
    
# Possiamo quindi adesso definire in modo diretto il punto G:
G = S256Point(0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798, 
             0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8)

"""
Abbiamo ora tutto ciò che serve per fare le operazioni di crittografia a chiave pubblica. L'operazione chiave che ci serve è P = eG, che è asimmetrico: possiamo
facilmente calcolare P se conosciamo e e G, ma non abbiamo modo di ricavare e.
Generalmente, chiamiamo e la chiave privata e P la chiave pubblica. Da notare che la chiave privata è un singolo numero di 256 bit, mentre la chiave pubblica è una coppia
di coordinate (x, y) in cui entrambe sono numeri di 256bit.

FIRMA E VERIFICA
Vogliamo provare che siamo in possesso del numero segreto "e" (la chiave privata), senza mostrarla in chiaro. Lo facciamo inserendo un target nel calcolo e raggiungendo successivamente
quel target. Un esempio per capire cosa si intende: per dimostrare di avere una buona mira, non bisogna tirare una palla e poi dire che il target che avevamo era il punto che è andata
a colpire, bisogna invece prima annunciare qual'è il nostro target, il nostro bersaglio, e solo successivamente dimostrare di essere in grado di colpirlo.
L'algoritmo che permette di "annunciare" il target è detto signature algorithm. Nel nostro caso si chiama Elliptic Curve Digital Signature Algorithm, in breve ECDSA. vediamo come funziona:
Nel nostro caso, il segreto da mantenere è "e", che soddisfa eG=P (P è la chiave pubblica, e è la chiave privata). Il nostro target è un numero casuale di 256bit, che chiamiamo k.
Facciamo quindi kG=R. Adesso è R il target che stiamo puntando. Ci interessa solo la coordinata x di R, che chiamiamo r. (La r sta per random).
a questo punto, la seguente equazione è equivalente al DLP: uG+vP=kG, dove k è stato scelto randomicamente, u,v≠0 possono essere scelti da chi firma e G,P sono conosciuti. 
Ciò è dovuto al fatto che uG+vP=kG implica vP=(k-u)G. 
Siccome è diverso da 0, possiamo dividere per v: P=((k-u)/v)G. 
Se conosciamo e, ovvero la chiave privata, abbiamo:eG=((k-u)/v)G, da cui e=(k-u)/v.
Ciò significa che qualsiasi coppia (u,v) che soddisfa la precedente equazione è sufficiente. Se cnon conoscessimo e, dovremmo giocare con la coppia (u,v) finché e=(k-u)/v. Se potessimo 
risolverlo on qualsiasi combinazione di u e v, avremmo risolto P=eG solo conoscendo P e G, in altre parole avremmo rotto il DLP. Ed è questo il punto. Per fornire (u,v) corrette, l'unico
modo che abbiamo è conoscere il segreto e. 

Tornando all'esempio precedente, ciò di cui non abbiamo discusso è come incorporare nel lancio della palla il target a cui puntiamo. In termini di firma e verifica, l'obiettivo è detto
signature hash. Un hash è una funzione deterministica che, a partire da un qualsiasi set arbitrario di dati, restituisce un altro dato (univoco) di misura fissa. Questo dato restituito
è l'impronta digitale del messaggio, e nell'algoritmo di firma viene incorporata questa impronta, non il messaggio iniziale. Se il mio obbiettivo fosse un uomo, potrei usare le sue impronte
digitali al posto suo, perché tanto la corrispondenza è univoca. L'impronta rimane sempre la stessa ed è unica per ogni persona. Ugualmente, l'hash di un set di dati è sempre lo stesso ed 
è univocamente determinato. 
Indichiamo l'hash con la lettera z, e lo possiamo incorporare nell'equazione in questo modo: u=z/s, v=r/s.
Possiamo calcolare s:
uG + vP = R = kG
uG + veG = kG
u + ve = k
z/s + re/s = k
(z + re)/s = k
s = (z + re)/k
Questa è la base del signature algorithm, e la verifica è diretta:
uG + vP = (z/s)G + (re/s)G = ((z + re)/s)G = ((z + re)/((z + re)/k))G = kG = (r,y)

Dalla teoria alla pratica:

In pratica, io ho la coppia di chiavi pubblica e privata (prvK e PubK), l'hash del messaggio (z). Scelgo quindi un secondo numero da mantenere segreto (k). 
Da questo numero posso calcolare r, che è la coordinata x del punto che si ottiene moltiplicando il generatore (G) per il numero segreto k. 
La firma s = (z + r*prvK)/k ha quindi due elmenti, k e prvK, che sono privati e non si possono direttamente ricavare, mentre sono pubblici r, s, z e pubK (che ricordiamo
essere la chiave privata moltiplicata per il generatore G).
La verifica è di facile effettuazione. Mi ricavo il punto R' a partire dalla firma ricevuta: R' = (z*G + r*PubK)/s. Chiamo, analogamente a prima, r' la coordinata x di questo punto.
Non mi resta quindi controllare che r' == r (che ricordiamo essere pubblico). Se la condizione si verifica, ecco che ho la prova che l'utente che mi ha fornito la firma possiede
a tutti gli effetti la chiave privata, senza che questa sia mai stata effettivamente esposta.

Riassumendo, questi gli step:
1. Conosciamo z, l'hash del messaggio. Ci vengono dati (r, s) come firma. Conosciamo inoltre la chiave pubblica P.
2. Calcoliamo u = z/s, v = r/s
3. Calcoliamo uG + vP = R
4. Se la coordinata x di R è uguale a r, la firma è valida.
Questo perché, dal momento che r è usato nell'operazione di verifica (che calcola r stesso), l'unico modo per conoscerlo prima di ricavarlo è essere in possesso della chiave privata.

"""

#VERIFICA DI UNA FIRMA

z = 0xbc62d4b80d9e36da29c16c5d4d9f11731f36052c72401a76c23c0fb5a9b74423  #hash 
r = 0x37206a0610995c58074999cb9767b87af4c4978db68c06e8e6e81d282047a7c6  #coordinata x di R
s = 0x8ca63759c1157ebeaec0d03cecca119fc9a75bf8e6d0fa65c841c8e2738cdaec  #firma
px = 0x04519fac3d910ca7e7138f7013706f619fa8f033e6ec6e09370ea38cee6a7574 #coord della pubKey
py = 0x82b51eab8c27c66e26c858a079bcdf4f1ada34cec420cafc7eac1a42216fb6c4
P = S256Point(px, py)       #chiave pubblica
s_inv = pow(s, N-2, N)      #1/s nel FiniteField, usando il piccolo teorema di Fermat
u = z * s_inv % N           #u = z/s
v = r * s_inv % N           #v = r/s
r1 = (u*G + v*point).x.num  #uG + vP = (r,y). ci serve verificare la coordinata x
#>>> print(r1 == r)
#>>> True se la verifica è riuscita, False altrimenti.

# Formalizziamo quanto fatto sopra abbiamo già la classe S256Point, creiamo la classe Signature che contiene i valori r e s:

    class Signature:
        def __init__(self, r, s):   #i due elementi costituenti la firma
            self.r = r
            self.s = s
        
        def __repr__(self):
            return 'Signature({:x},{:x})'.format(self.r, self.s) #rappresentazione della firma
            
#Possiamo ora scrivere il metodo che verifica la firma
   
    class S256Point(Point):
        #...
        def verify(self, z, sig):
            s_inv = pow(sig.s, N - 2, N)    #come prima, piccolo teorema di Fermat
            u = z * s_inv % N               #u = z/s
            v = sig.r * s_inv % N           #v = r/s
            total = u * G + v * self        #uG + vP = (r,y). ci serve verificare la coordinata x
            return total.x.num == sig.r     #verifico

"""        
FIRMA
A questo punto, avendo capito come funziona la verifica, l'algoritmo di firma è abbastanza ovvio. L'unica cosa che manca è scegliere quale k usare. Random è la scelta migliore
Si procede in questo modo:
1. Ci viene fornito z e conosciamo la chiave privata tale che eG=P
2. Scegliamo un k random
3. Calcoliamo r=kG ed estrapoliamo r 
4. Calcoliamo  Calculate s = (z + re)/k
5. Fatto. La firma è (r, s)

Si noti che la pubkey P deve essere trasmessa a chiunque voglia verificare la firma, che deve anche conoscere z. Vedremo più avanti che z è computata e che P e inviata insieme alla firma
Possiamo a questo punto creare la firma, ci serviamo di alcune primitive che abbiamo (S25Point, G, N, hash256)
"""
e = int.from_bytes(hash256(b'my secret'), 'big')    #è un esempio di "brain wallet", la chiave è un segreto che si tiene a mente
z = int.from_bytes(hash256(b'my message'), 'big')   #hash del messaggio
k = 1234567890                                      #per semplicità, usiamo un k fissato. Ricordiamo che va scelto randomicamente.
r = (k*G).x.num                                     #kG = (r,y), e prendiamo la coordinata x
k_inv = pow(k, N-2, N)
s = (z+r*e) * k_inv % N                             #s = (z + re)/k
point = e*G                                         #la chiave pubblica deve essere conosciuta da chi verifica

#FORMALIZZIAMO IL TUTTO

    class PrivateKey:                               #contiene la nostra coppia di chiavi
        def __init__(self, secret):
            self.secret = secret
            self.point = secret * G
            
        def hex(self):
            return '{:x}'.format(self.secret).zfill(64) #rappresentato come numero esadecimale di 64 cifre (eventualmente coi dovuti 0 davanti)
        
        #creiamo il metodo per la firma:
        def sign(self, z):
            k = randint(0,N)                            #IMPORTANTE!!! NON USARE LA LIBRERIA RANDOM, MA UNA FONTE DI ENTROPIA VERA. Usiamo qui randint a puro scopo didattico
            r = (k*G).x.num
            k_inv = pow(k, N-2, N)
            s = (z + r*self.secret) * k_inv % N         #s = (z + re)/k
            if s > N/2:                                 #per ragioni di malleabilità, utilizzando un s basso otterremo nodi per inoltrare le nostre transazioni.
                s = N - s
            return Signature(r, s)                      #L'oggetto firma l'abbiamo definito in precedenza

# Si rimanda a ../CorollarioK la spiegazione sull'importanza (e derivazione) di un k randomico e unico
