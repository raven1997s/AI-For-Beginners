from gedcom.parser import Parser
from gedcom.element.individual import IndividualElement
from gedcom.element.family import FamilyElement

g = Parser()
g.parse_file('data/tsars.ged')

d = g.get_element_dictionary()
[ (k,v.get_name()) for k,v in d.items() if isinstance(v,IndividualElement)]



d = g.get_element_dictionary()
[ (k,[x.get_value() for x in v.get_child_elements()]) for k,v in d.items() if isinstance(v,FamilyElement)]# print(family_elements)


gedcom_dict = g.get_element_dictionary()
individuals, marriages = {}, {}
def term2id(el):
    return "i" + el.get_pointer().replace('@', '').lower()

out = open("onto.ttl","a")

for k, v in gedcom_dict.items():
    if isinstance(v,IndividualElement):
        children, siblings = set(), set()
        idx = term2id(v)

        title = v.get_name()[0] + " " + v.get_name()[1]
        title = title.replace('"', '').replace('[', '').replace(']', '').replace('(', '').replace(')', '').strip()

        own_families = g.get_families(v, 'FAMS')
        for fam in own_families:
            children |= set(term2id(i) for i in g.get_family_members(fam, "CHIL"))

        parent_families = g.get_families(v, 'FAMC')
        if len(parent_families):
            for member in g.get_family_members(parent_families[0], "CHIL"): # NB adoptive families i.e len(parent_families)>1 are not considered (TODO?)
                if member.get_pointer() == v.get_pointer():
                    continue
                siblings.add(term2id(member))

        if idx in individuals:
            children |= individuals[idx].get('children', set())
            siblings |= individuals[idx].get('siblings', set())
        individuals[idx] = {'sex': v.get_gender().lower(), 'children': children, 'siblings': siblings, 'title': title}

    elif isinstance(v,FamilyElement):
        wife, husb, children = None, None, set()
        children = set(term2id(i) for i in g.get_family_members(v, "CHIL"))

        try:
            wife = g.get_family_members(v, "WIFE")[0]
            wife = term2id(wife)
            if wife in individuals: individuals[wife]['children'] |= children
            else: individuals[wife] = {'children': children}
        except IndexError: pass
        try:
            husb = g.get_family_members(v, "HUSB")[0]
            husb = term2id(husb)
            if husb in individuals: individuals[husb]['children'] |= children
            else: individuals[husb] = {'children': children}
        except IndexError: pass

        if wife and husb: marriages[wife + husb] = (term2id(v), wife, husb)

for idx, val in individuals.items():
    added_terms = ''
    if val['sex'] == 'f':
        parent_predicate, sibl_predicate = "isMotherOf", "isSisterOf"
    else:
        parent_predicate, sibl_predicate = "isFatherOf", "isBrotherOf"
    if len(val['children']):
        added_terms += " ;\n    fhkb:" + parent_predicate + " " + ", ".join(["fhkb:" + i for i in val['children']])
    if len(val['siblings']):
        added_terms += " ;\n    fhkb:" + sibl_predicate + " " + ", ".join(["fhkb:" + i for i in val['siblings']])
    out.write("fhkb:%s a owl:NamedIndividual, owl:Thing%s ;\n    rdfs:label \"%s\" .\n" % (idx, added_terms, val['title']))

for k, v in marriages.items():
    out.write("fhkb:%s a owl:NamedIndividual, owl:Thing ;\n    fhkb:hasFemalePartner fhkb:%s ;\n    fhkb:hasMalePartner fhkb:%s .\n" % v)

out.write("[] a owl:AllDifferent ;\n    owl:distinctMembers (")
for idx in individuals.keys():
    out.write("    fhkb:" + idx)
for k, v in marriages.items():
    out.write("    fhkb:" + v[0])
out.write("    ) .")
out.close()