class Ask():
    def __init__(self,choices=['y','n']):
        self.choices = choices
    def ask(self):
        if max([len(x) for x in self.choices])>1:
            for i,x in enumerate(self.choices):
                print("{0}. {1}".format(i,x),flush=True)
            x = int(input())
            return self.choices[x]
        else:
            print("/".join(self.choices),flush=True)
            return input()

class Content():
    def __init__(self,x):
        self.x=x
        
class If(Content):
    pass

class AND(Content):
    pass

class OR(Content):
    pass

rules = {
    'default': Ask(['y','n']),
    'color' : Ask(['red-brown','black and white','other']),
    'pattern' : Ask(['dark stripes','dark spots']),
    'mammal': If(OR(['hair','gives milk'])),
    'carnivor': If(OR([AND(['sharp teeth','claws','forward-looking eyes']),'eats meat'])),
    'ungulate': If(['mammal',OR(['has hooves','chews cud'])]),
    'bird': If(OR(['feathers',AND(['flies','lies eggs'])])),
    'animal:monkey' : If(['mammal','carnivor','color:red-brown','pattern:dark spots']),
    'animal:tiger' : If(['mammal','carnivor','color:red-brown','pattern:dark stripes']),
    'animal:giraffe' : If(['ungulate','long neck','long legs','pattern:dark spots']),
    'animal:zebra' : If(['ungulate','pattern:dark stripes']),
    'animal:ostrich' : If(['bird','long nech','color:black and white','cannot fly']),
    'animal:pinguin' : If(['bird','swims','color:black and white','cannot fly']),
    'animal:albatross' : If(['bird','flies well'])
}


class KnowledgeBase():
    def __init__(self,rules):
        self.rules = rules
        self.memory = {}
        
    def get(self,name):
        if ':' in name:
            k,v = name.split(':')
            vv = self.get(k)
            return 'y' if v==vv else 'n'
        if name in self.memory.keys():
            return self.memory[name]
        for fld in self.rules.keys():
            if fld==name or fld.startswith(name+":"):
                # print(" + proving {}".format(fld))
                value = 'y' if fld==name else fld.split(':')[1]
                res = self.eval(self.rules[fld],field=name)
                if res!='y' and res!='n' and value=='y':
                    self.memory[name] = res
                    return res
                if res=='y':
                    self.memory[name] = value
                    return value
        # field is not found, using default
        res = self.eval(self.rules['default'],field=name)
        self.memory[name]=res
        return res
                
    def eval(self,expr,field=None):
        # print(" + eval {}".format(expr))
        if isinstance(expr,Ask):
            print(field)
            return expr.ask()
        elif isinstance(expr,If):
            return self.eval(expr.x)
        elif isinstance(expr,AND) or isinstance(expr,list):
            expr = expr.x if isinstance(expr,AND) else expr
            for x in expr:
                if self.eval(x)=='n':
                    return 'n'
            return 'y'
        elif isinstance(expr,OR):
            for x in expr.x:
                if self.eval(x)=='y':
                    return 'y'
            return 'n'
        elif isinstance(expr,str):
            return self.get(expr)
        else:
            print("Unknown expr: {}".format(expr))

kb = KnowledgeBase(rules)
kb.get('animal')