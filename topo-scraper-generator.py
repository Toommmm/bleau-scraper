import urllib2
import re
import jinja2
import codecs
from bs4 import BeautifulSoup

response = urllib2.urlopen("https://bleau.info/topos/topo1176.html" + "?locale=en")
soup = BeautifulSoup(response,"lxml")
print soup.title.string
print ''

# all html links on main page
#for link in soup.find_all('a'):
#      print(link.get('href'))

mydiv0 = soup.find_all("div", class_="topo_photo")
for div0 in mydiv0:
  topo = "http://www.bleau.info" + str(div0.find('a')['href'])
  print topo

counter = 0
boulder_info = [[0]*60 for i in range(6)]

mydivs = soup.find_all("div", class_="row lvar")
for div in mydivs:
  counter = counter + 1

  number = div.contents[1].get_text().strip()
  print 'Nr ', number

  boulder_info[0][counter] = unicode(number)

  temp = div.contents[3].get_text().strip().replace('\n',', ')
  info = [x.strip() for x in temp.split(',')]
  info = filter(None,info)
  if(not str(info[2][0]).isdigit()):
    info.insert(2,"")
  if(not str(info[3][0]).isupper()):
    info.insert(3,"")
  if(not str(info[4][0]).isupper()):
    info.insert(4,"")

  for i in range(len(info)):
    print i, info[i]

  boulder_info[1][counter] = unicode(info[0])
  boulder_info[2][counter] = unicode(info[1])
  boulder_info[3][counter] = unicode(info[3])
  boulder_info[4][counter] = unicode(info[5])

  boulder = "http://www.bleau.info" + str(div.find('a')['href'] + "?locale=en")
  response2 = urllib2.urlopen(boulder)
  soup2 = BeautifulSoup(response2,"lxml")

  mydiv2 = soup2.find_all("div", class_="bdesc")
  for div2 in mydiv2: 
    extra = div2.get_text().strip()
    print 'Info ',extra
    boulder_info[5][counter] = unicode(extra) 

#  mydiv3 = soup2.find_all("div", class_="bp_wrapper")
#  for div3 in mydiv3: 
#    photo = div3.find('a')['href']
#    if 'trace' in str(photo):
#      print photo
#    if 'gilles' in str(photo):
#      print photo

  print ''


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
TEMPLATE_FILE = "/home/tom/Documents/Topo/scraper/template.html"

# Read the template file using the environment object.
# This also constructs our Template object.
template = templateEnv.get_template( TEMPLATE_FILE )

# Specify any input variables to the template as a dictionary.
templateVars = { "title"  : "Test Example",
                 "numb"   : boulder_info[0],
                 "name"   : boulder_info[1],
                 "grad"   : boulder_info[2],
                 "open"   : boulder_info[3],
                 "type"   : boulder_info[4],
                 "info"   : boulder_info[5]}

# Finally, process the template to produce our final text.
outputText = template.render( templateVars )

htmlfile=codecs.open('boulders.html','w',encoding='utf-8')
htmlfile.write(outputText)
htmlfile.close()





