#using NLTK to extract the names of the prosecutors and the defendants
#Trial 1

import nltk
from nameparser.parser import HumanName

def humannames(text):
    tokens = nltk.tokenize.word_tokenize(text)
    pos = nltk.pos_tag(tokens)
    sentiment = nltk.ne_chunk(pos, binary = False)
    list_of_person = []
    person = []
    name = ""
    for subtree in sentiment.subtrees(filter=lambda t: t.label() == 'PERSON'):
        for leaf in subtree.leaves():
            person.append(leaf[0])
        if len(person) > 1:
            for p in person:
                name += p + ' '
            if name[:-1] not in list_of_person:
                list_of_person.append(name[:-1])
            name = ''
        person = []

    return (list_of_person)

with open("pressReleases.csv") as f:
    text = f.read() + '\n'

names = humannames(text)
for name in names:
    print(name)
    last_first = HumanName(name).last + ', ' + HumanName(name).first
    print(last_first)
