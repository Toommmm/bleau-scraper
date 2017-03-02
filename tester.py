# file scraper.py

# import own classes
import boulder as fb

# import external stuff
import urllib 
import urllib2

from operator import itemgetter

from bs4 import BeautifulSoup

print "Hello"

cuvier = fb.Area("Bas Cuvier")
print cuvier.getName()

carnage = fb.Boulder()
#carnage.setName("Le Carnage")
carnage.name="Le Carnage"
print carnage.name

carnage.setGrade("7b+")
carnage.setGrade("7b")
print carnage.getGrade()

carnage.setOpener("Jan")
carnage.setOpener("Wolf")
print carnage.getOpener()

carnage.setStyle("Classic")
carnage.setStyle("Chipped")
print carnage.getStyle()

cuvier.addBoulder(carnage)
#cuvier.getBoulderlist()

nohands = fb.Boulder()
cuvier.addBoulder(nohands)
#cuvier.getBoulderlist()

print nohands["name"]
nohands["name"]="lala"
print nohands["name"]
print nohands.name
print nohands.getName()

nohands["style"].append("crimp")
nohands["style"].append("wall")
nohands.setStyle("classic")
print nohands["style"]

nohands["grade"].append("5c")
nohands.setGrade("6a")
print nohands["grade"]

nohands["test"]= 5
print nohands["test"]

cuvier.getBoulderlist()

print cuvier.boulder_list[0].name

newlist = sorted(cuvier.boulder_list, key=itemgetter("grade"), reverse=True)
for item in newlist:
	print item.grade
