"""
IMPORTANZA DI UN k UNICO

è di fondamentale importanza che k sia unico per ogni firma, non deve mai essere riutilizzato. Infatti, se venisse riutilizzato, verrebbe rivelata la chiave privata.
Ecco come:

siano privKey la chiave privata e z1, z2 i due messaggi su cui usiamo lo stesso k.

k*G = (r,y)
s1 = (z1+r*privKey)/k, s2 = (z2+r*privKey)/k
s1/s2 = (z1+r*privKey)/(z2+r*privKey)
s1(z2+r*privKey) = s2(z1+r*privKey)
s1*z2+s1*r*privKey = s2*z1+s2*r*privKey
s1*r*privKey–s2*r*privKey = s2*z1–s1*z2
privKey = (s2*z1–s1*z2)/(r*s1–r*s2)

Se qualcuno vedesse entrambe le firme, potrebbe trovare la nostra chiave privata. Per esempio, nel 2010 l'hack della PlayStation 3 fu dovuto proprio a una negligenza 
sul riutilizzo di k.
Per evitare tutto ciò, si può usare uno standard per generare k in modo deterministico, che usa la chiave privata e il messaggio z per creare un unico, determinato k
ogni volta. La specifica si trova in https://datatracker.ietf.org/doc/html/rfc6979, e le modifiche al codice sono queste:
"""
  class PrivateKey:
    #...
    def sign(self, z):
      k = self.deterministic_k(z)     #Usiamo un k deterministico invece che random. Tutto il resto nella firma rimane uguale
      r = (k * G).x.num
      k_inv = pow(k, N - 2, N)
      s = (z + r * self.secret) * k_inv % N
      if s > N / 2:
        s = N - s
      return Signature(r, s)
    
    def deterministic_k(self, z):
      k = b'\x00' * 32
      v = b'\x01' * 32
      if z > N:
        z -= N
      z_bytes = z.to_bytes(32, 'big')
      secret_bytes = self.secret.to_bytes(32, 'big')
      s256 = hashlib.sha256
      k = hmac.new(k, v + b'\x00' + secret_bytes + z_bytes, s256).digest()
      v = hmac.new(k, v, s256).digest()
      k = hmac.new(k, v + b'\x01' + secret_bytes + z_bytes, s256).digest()
      v = hmac.new(k, v, s256).digest()
      while True:
        v = hmac.new(k, v, s256).digest()
        candidate = int.from_bytes(v, 'big')
        if candidate >= 1 and candidate < N:
          return candidate                            #questo algoritmo restituisce un valido candidato per k
        k = hmac.new(k, v + b'\x00', s256).digest()
        v = hmac.new(k, v, s256).digest()

"""
Determinato in questo modo, k sarà unico con altissima probabilità, questo perché sha256 non ha collisioni note ed è "collision-resistant". 
Un altro aspetto positivo è che la firma per un dato messaggio z con la stessa chiave privata sarà sempre la stessa, cosa molto utile in testing e debugging
"""
