import urllib2
import re
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
boulder_info = [[0]*6 for i in range(60)]

mydivs = soup.find_all("div", class_="row lvar")
for div in mydivs:
  counter = counter + 1

  number = div.contents[1].get_text().strip()
  print 'Nr ', number

  boulder_info[counter][0] = unicode(number)

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

  boulder_info[counter][1] = unicode(info[0])
  boulder_info[counter][2] = unicode(info[1])
  boulder_info[counter][3] = unicode(info[3])
  boulder_info[counter][4] = unicode(info[5])

  boulder = "http://www.bleau.info" + str(div.find('a')['href'] + "?locale=en")
  response2 = urllib2.urlopen(boulder)
  soup2 = BeautifulSoup(response2,"lxml")

  mydiv2 = soup2.find_all("div", class_="bdesc")
  for div2 in mydiv2: 
    extra = div2.get_text().strip()
    print 'Info ',extra
    boulder_info[counter][5] = unicode(extra) 

#  mydiv3 = soup2.find_all("div", class_="bp_wrapper")
#  for div3 in mydiv3: 
#    photo = div3.find('a')['href']
#    if 'trace' in str(photo):
#      print photo
#    if 'gilles' in str(photo):
#      print photo

  print ''

print boulder_info[10]





