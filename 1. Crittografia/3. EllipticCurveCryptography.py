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
