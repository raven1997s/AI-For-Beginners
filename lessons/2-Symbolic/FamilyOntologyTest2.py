import rdflib
from owlrl import DeductiveClosure, OWLRL_Extension

g = rdflib.Graph()
g.parse("onto.ttl", format="turtle")

print("Triplets found:%d" % len(g))

DeductiveClosure(OWLRL_Extension).expand(g)
print("Triplets after inference:%d" % len(g))


qres = g.query(
    """SELECT DISTINCT ?aname ?bname
       WHERE {
          ?a fhkb:isMotherOf ?b .
          ?a rdfs:label ?aname .
          ?b rdfs:label ?bname .
       }""")

for row in qres:
    print("%s is mother of %s" % row)