import urllib
import urllib2
import re
import jinja2
import codecs
import pdfkit
from bs4 import BeautifulSoup
from operator import itemgetter

# Bois Rond Auberge
#response = urllib2.urlopen("https://bleau.info/topos/topo244.html" + "?locale=en")
# Mont Simonet 
#response = urllib2.urlopen("https://bleau.info/topos/topo247.html" + "?locale=en")
# Rocher de la Salamandre Est
#response = urllib2.urlopen("https://bleau.info/topos/topo1176.html" + "?locale=en")
# Apremont Bizons
#response = urllib2.urlopen("https://bleau.info/topos/topo254.html" + "?locale=en")
# Apremont Haut des Gorges
#response = urllib2.urlopen("https://bleau.info/topos/topo1169.html" + "?locale=en")
# Apremont Butte aux Peintres
response = urllib2.urlopen("https://bleau.info/topos/topo145.html" + "?locale=en")
# Apremont Sanglier
response = urllib2.urlopen("https://bleau.info/topos/topo267.html" + "?locale=en")
# Apremont Butte aux Dames (Sector Nord)
response = urllib2.urlopen("https://bleau.info/topos/topo1163.html" + "?locale=en")
# Apremont Haut des Gorges
#response = urllib2.urlopen("https://bleau.info/topos/topo1169.html" + "?locale=en")
# Apremont Portes du Desert
#response = urllib2.urlopen("https://bleau.info/topos/topo1170.html" + "?locale=en")
# Apremont Desert
#response = urllib2.urlopen("https://bleau.info/topos/topo1175.html" + "?locale=en")

# Open page and get area name
soup = BeautifulSoup(response,"lxml")
title = soup.title.string
area = title[0:title.find(" - ")]
print area

# Get info to reach the area
mydiv9 = soup.find_all("div", class_="col-md-6")
area_over = "http://www.bleau.info" + str(mydiv9[0].find('a')['href']) + "?locale=en"
response3 = urllib2.urlopen(area_over)
soup3 = BeautifulSoup(response3,"lxml")

mydiv8 = soup3.find_all("p")
area_info = mydiv8[0].get_text().strip()
print area_info

# Get the topos
topo_counter = 0
topo_list = [0]*10

mydiv0 = soup.find_all("div", class_="topo_photo")
for div0 in mydiv0:
  topo_list[topo_counter] = "http://www.bleau.info" + str(div0.find('a')['href'])
  print topo_list[topo_counter]
  urllib.urlretrieve(str(topo_list[topo_counter]), area.replace(" ","") + "-" + str(topo_counter) + ".jpg")
  topo_counter = topo_counter + 1

boulder_counter = 0
boulder_info = [[0]*200 for i in range(10)]

mydivs = soup.find_all("div", class_="row lvar")
for div in mydivs:

  number = div.contents[1].get_text().strip()
  print 'Nr ', number

  boulder_info[0][boulder_counter] = unicode(number)

# info
# 0 - Name
# 1 - Grade
# 2 - Grade (bis)
# 3 - Opener
# 4 - Opener (bis)
# 5 - Opener (bis)
# 6 - Type
# 7 - Type (bis)
# 8 - Type (bis)
# 9 - Type (bis)

# boulder_info
# 1 - Name
# 2 - Grades
# 3 - Openers
# 4 - Types
# 5 - Extra
# 6 - Ascents

  temp = div.contents[3].get_text().strip().replace('\n',', ')
  info = [x.strip() for x in temp.split(',')]
  info = filter(None,info)
  if(not str(info[2][0]).isdigit()):
    info.insert(2,"")
  if((not str(info[3][0]).isupper()) and \
     (str(info[3]).find('yann') < 0)):
    info.insert(3,"")
  if(4 < len(info) and not str(info[4][0]).isupper()):
    info.insert(4,"")
  if(5 < len(info) and not str(info[5][0]).isupper()):
    info.insert(5,"")

  for i in range(len(info)):
    print i, info[i]

  boulder_info[1][boulder_counter] = unicode(info[0])

  boulder_info[2][boulder_counter] = unicode(info[1])
  if (info[2] != ""): 
    boulder_info[2][boulder_counter] = boulder_info[2][boulder_counter] + "(" + unicode(info[2]) + ")"

  boulder_info[3][boulder_counter] = unicode(info[3])
  if (4 < len(info) and info[4] != ""): 
    boulder_info[3][boulder_counter] = boulder_info[3][boulder_counter] + ", " + unicode(info[4])
  if (5 < len(info) and info[5] != ""): 
    boulder_info[3][boulder_counter] = boulder_info[3][boulder_counter] + ", " + unicode(info[5])

  boulder_info[4][boulder_counter] = unicode(info[6])
  if (7 < len(info) and info[7] != ""): 
    boulder_info[4][boulder_counter] = boulder_info[4][boulder_counter] + ", " + unicode(info[7])
  if (8 < len(info) and info[8] != ""): 
    boulder_info[4][boulder_counter] = boulder_info[4][boulder_counter] + ", " + unicode(info[8])
  if (9 < len(info) and info[9] != ""): 
    boulder_info[4][boulder_counter] = boulder_info[4][boulder_counter] + ", " + unicode(info[9])

  boulder = "http://www.bleau.info" + str(div.find('a')['href'] + "?locale=en")
  response2 = urllib2.urlopen(boulder)
  soup2 = BeautifulSoup(response2,"lxml")

  mydiv2 = soup2.find_all("div", class_="bdesc")
  for div2 in mydiv2: 
    extra = div2.get_text().strip()
    print 'Info ',extra
    boulder_info[5][boulder_counter] = unicode(extra) 

#  mydiv3 = soup2.find_all("div", class_="bp_wrapper")
#  for div3 in mydiv3: 
#    photo = div3.find('a')['href']
#    if 'trace' in str(photo):
#      print photo
#    if 'gilles' in str(photo):
#      print photo

  repeats = 0
  mydiv4 = soup2.find_all("div", class_="bopins")
  for div4 in mydiv4: 
    ascents = div4.get_text().strip()
    if (unicode(ascents).find('ascents') > 0):
      repeats = ascents[unicode(ascents).find('(')+1:unicode(ascents).find(' total)')]
  print 'Ascents ', repeats
  boulder_info[6][boulder_counter] = int(repeats) 
 


# End of loop over boulders
  print ''
  boulder_counter = boulder_counter + 1

boulder_popu = zip(*sorted(zip(*boulder_info),key=itemgetter(6),reverse=True))


# In this case, we will load templates off the filesystem.
# This means we must construct a FileSystemLoader object.
# 
# The search path can be used to make finding templates by
#   relative paths much easier.  In this case, we are using
#   absolute paths and thus set it to the filesystem root.
templateLoader = jinja2.FileSystemLoader( searchpath="/" )

# An environment provides the data necessary to read and
#   parse our templates.  We pass in the loader object here.
templateEnv = jinja2.Environment( loader=templateLoader )

# This constant string specifies the template file we will use.
TEMPLATE_FILE = "/home/tom/Documents/Topo/bleauScraper/template.html"

# Read the template file using the environment object.
# This also constructs our Template object.
template = templateEnv.get_template( TEMPLATE_FILE )

# Specify any input variables to the template as a dictionary.
templateVars = { "title"  : area,
       "road"     : area_info,
       "list"     : topo_list[0:topo_counter],
       "numb"     : boulder_info[0][0:boulder_counter],
       "name"     : boulder_info[1][0:boulder_counter],
       "grad"     : boulder_info[2][0:boulder_counter],
       "open"     : boulder_info[3][0:boulder_counter],
       "type"     : boulder_info[4][0:boulder_counter],
       "info"     : boulder_info[5][0:boulder_counter],
       "reps"     : boulder_info[6][0:boulder_counter],
       "numb"     : boulder_info[0][0:boulder_counter],
       "numb_popu": boulder_popu[0][0:10],
       "name_popu": boulder_popu[1][0:10],
       "grad_popu": boulder_popu[2][0:10],
       "reps_popu": boulder_popu[6][0:10]}

# Finally, process the template to produce our final text.
outputText = template.render( templateVars )

htmlfile=codecs.open(area.replace(' ','')+'.html','w',encoding='utf-8')
htmlfile.write(outputText)
htmlfile.close()

