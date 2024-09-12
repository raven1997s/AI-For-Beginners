from pyknow import *

class Animals(KnowledgeEngine):
    @Rule(OR(
           AND(Fact('sharp teeth'),Fact('claws'),Fact('forward looking eyes')),
           Fact('eats meat')))
    def cornivor(self):
        self.declare(Fact('carnivor'))
        
    @Rule(OR(Fact('hair'),Fact('gives milk')))
    def mammal(self):
        self.declare(Fact('mammal'))

    @Rule(Fact('mammal'),
          OR(Fact('has hooves'),Fact('chews cud')))
    def hooves(self):
        self.declare('ungulate')
        
    @Rule(OR(Fact('feathers'),AND(Fact('flies'),Fact('lays eggs'))))
    def bird(self):
        self.declare('bird')
        
    @Rule(Fact('mammal'),Fact('carnivor'),
          Fact(color='red-brown'),
          Fact(pattern='dark spots'))
    def monkey(self):
        self.declare(Fact(animal='monkey'))

    @Rule(Fact('mammal'),Fact('carnivor'),
          Fact(color='red-brown'),
          Fact(pattern='dark stripes'))
    def tiger(self):
        self.declare(Fact(animal='tiger'))

    @Rule(Fact('ungulate'),
          Fact('long neck'),
          Fact('long legs'),
          Fact(pattern='dark spots'))
    def giraffe(self):
        self.declare(Fact(animal='giraffe'))

    @Rule(Fact('ungulate'),
          Fact(pattern='dark stripes'))
    def zebra(self):
        self.declare(Fact(animal='zebra'))

    @Rule(Fact('bird'),
          Fact('long neck'),
          Fact('cannot fly'),
          Fact(color='black and white'))
    def straus(self):
        self.declare(Fact(animal='ostrich'))

    @Rule(Fact('bird'),
          Fact('swims'),
          Fact('cannot fly'),
          Fact(color='black and white'))
    def pinguin(self):
        self.declare(Fact(animal='pinguin'))

    @Rule(Fact('bird'),
          Fact('flies well'))
    def albatros(self):
        self.declare(Fact(animal='albatross'))
        
    @Rule(Fact(animal=MATCH.a))
    def print_result(self,a):
          print('Animal is {}'.format(a))
                    
    def factz(self,l):
        for x in l:
            self.declare(x)

ex1 = Animals()
ex1.reset()
ex1.factz([
    Fact(color='red-brown'),
    Fact(pattern='dark stripes'),
    Fact('sharp teeth'),
    Fact('claws'),
    Fact('forward looking eyes'),
    Fact('gives milk')])
ex1.run()
ex1.facts