"""
Abbiamo già creato un sacco di classi, tra cui PrivateKey, S256Point e Signature. C'è ora bisogno di cominciare a pensare a un modo per trasmettere questi
oggetti a altri computer nel network. è qui che entra in gioco la cosiddetta serializzazione, Ci serve comunicare o storare un S256Point o una firma o una
chiave privata, e vorremmo farlo in modo efficiente.

Uncompressed SEC Format
comincieremo dalla classe S256Point, che è quella relativa alla chiave pubblica. Ricordiamo che quest'ultima non è altro che una coordinata nella forma (x,y).
Come possiamo serializzare questo dato? Beh, esiste già uno standard per serializzare le chiavi pubbliche ECDSA, chiamato "Standards for Efficient 
Cryptography (SEC)" e, come suggerisce il nome, ha costi minimali in termini di risorse. Ci sono due tipi di formato SEC: compressed e uncompressed.
Vedremo per primo quest'ultimo.
Così è come l'uncompressed SEC format per un dato punto P=(x,y) è generato:
1. Inizia con il byte di prefisso, che è 0x04
2. Dopodiché viene attaccata la coordinata x come un intero big-endian
3. Infine allo stesso modo biene attaccata la coordinata x

Programmare la serializzazione nel formato SEC uncompressed è abbastanza diretto. La parte un attimo più complicata è la conversione di un numero di 256bit
in uno di 32byte, big-endian. Questo il codice:
"""

class S256Point(Point):
  #...
  def sec(self):
  #returns the binary version of the SEC format
    return b'\x04' + self.x.num.to_bytes(32, 'big') + self.y.num.to_bytes(32, 'big')    
    #to_bytes è un metodo di python3 per convertire un numero in byte. il primo argomento è la quantità di byte, la seconda specifica il tipo di "endian".
    
"""
Compressed SEC format
Ricordiamo che per ogni coordinata x, ci sono al massimo 2 coordinate y a essa relative, a causa del termine y^2 nell'equazione della curva ellittica, questo
sia nel campo R che in un campo finito. Se conosciamo x, la coordinata y deve essere y o p-y. Dal momento che p è un numero primo maggiore di 2, p è per
forza dispari. Di conseguenza, se y è pari, (p-y) è dispari, e viceversa. Questo è qualcosa che possiamo usare a nostro vantaggio per accorciare 
l'uncompressed SEC format
