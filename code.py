import nltk
import requests
import operator
from lxml import html
from bs4 import BeautifulSoup

particules = ("de", "du", "von") #gros bout de scotch...
months = ("January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December")

def get_page(url):
    page = requests.get(url)
    return BeautifulSoup(page.content, "lxml")

class Customer():

    def __init__(self, surname, name):
        self.surname = surname
        self.name = name
        print ("New Customer named " + self.surname + " " + self.name)

class States_list():
    states = []

    def __init__(self):
        url = "https://en.wikipedia.org/wiki/List_of_sovereign_states"
        print (url)
        soup = get_page(url)
        table = soup.find('table', {'class' : 'sortable wikitable'})
        for span in table.findAll('span'):
            if ('id' in span.attrs):
                self.states.append(span.attrs['id'])
        url = "https://fr.wikipedia.org/wiki/Liste_des_pays_du_monde"
        print (url)
        soup = get_page(url)
        table = soup.find('table', {'class' : 'wikitable alternance'})
        for tr in table.findAll('tr'):
            for a in tr.findAll('a'):
                if ('title' in a.attrs):
                    self.states.append(a.attrs['title'][10:])
                    break
        print (self.states)

    def is_states(self, state):
        if (state in self.states):
            return True
        else:
            return False

def get_wiki(Customer):
    base_url = "https://en.wikipedia.org/wiki/"
    target = Customer.surname + "_" + Customer.name
    print (base_url + target)
    return base_url + target
    #Consolider l'input :name/surname avec les differentes possibilites
    #Anglais, francais, etc.. ?
    #gerer if no wiki page


def get_all_name(tagged):
    lst_name = []
    flag = False
    name = ""
    for token in tagged:
        if (flag == False and name != ""):
            lst_name.append(name)
            name = ""
        if ((token[1] == 'NNP' and len(token[0]) > 2 and not(token[0] in months)) or (token[0] in particules and flag == 1)):
            if (flag == True):
                name += " " + token[0]
            else:
                name = token [0]
            flag = True
        else:
            flag = False
    return lst_name

def is_in_lst(str, lst):
    n = 0
    for item in lst:
        if (str in item):
            n += 1
    return n

def get_occ(lst_name):
    dict = {}
    for name in lst_name:
        if name not in dict:
            dict[name] = is_in_lst(name, lst_name)
    sorted_dict = sorted(dict.items(), key=operator.itemgetter(1), reverse=True)
    return sorted_dict

def l_analyze(sentence):
    tokens = nltk.word_tokenize(sentence)
    tagged = nltk.pos_tag(tokens)
    occurences = get_occ(get_all_name(tagged))
    print (occurences[0:6])
    entities = nltk.chunk.ne_chunk(tagged)
    return entities

new = Customer("Emmanuel", "Macron")
States = States_list()
print(States.is_states('Australia'))
print(States.is_states('Australie'))
url_en = get_wiki(new)
soup = get_page(url_en)
str = soup.get_text()
sentence = """Google entreprise is in a good situation"""

sentence_3 = """Macron has notably advocated in favor of the free market and reducing the public-finances deficit.[73] He first publicly used the term "liberal" to describe himself in a 2015 interview with Le Monde. He added that he is "neither right nor left" and that he advocates "a collective solidarity".[74][75] During a visit to the Puy du Fou in Vendée with Philippe de Villiers in August 2016, he stated, "Honesty compels me to say that I am not a socialist."[76] He explained that he was part of the "left government" because he wanted "to serve the public interest" as any minister would.[77] In his book Revolution, published in November 2016, Macron presents himself as both a "leftist" and a "liberal ... if by liberalism one means trust in man."[78] With his party En Marche!, Macron's stated aim is to transcend the left–right divide in a manner similar to François Bayrou or Jacques Chaban-Delmas, asserting that "the real divide in our country ... is between progressives and conservatives". With the launch of his independent candidacy and his use of anti-establishment rhetoric, Macron has been labelled a "populist" by some observers, notably Manuel Valls, but Macron rejects this term."""

l_analyze(sentence_3)
l_analyze(str)
