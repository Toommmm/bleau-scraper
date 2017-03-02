# file scraper.py

# import own classes
import boulder as fb

# import external stuff
from urllib.request import urlopen 
from urllib.request import urlretrieve 

from bs4 import BeautifulSoup
from operator import itemgetter

# Open correct page: the topo page
response1 = urlopen("https://bleau.info/topos/topo218.html" + "?locale=en")

# Open page and get area name
soup = BeautifulSoup(response1,"lxml")
soupTitle = soup.title.string
soupName = soupTitle[0:soupTitle.find(" - ")]

# Make new area 
area = fb.Area(soupName)
print("Scraping " + area.getName())

# Get info to reach the area, this can be found on the parent page: the area page
mydiv9 = soup.findAll("div", class_="col-md-6")
area_over = "http://www.bleau.info" + str(mydiv9[0].find('a')['href']) + "?locale=en"
response3 = urlopen(area_over)
soup3 = BeautifulSoup(response3,"lxml")

# Get the info 
mydiv8 = soup3.findAll("p")
soupInfo = mydiv8[0].get_text().strip()
area.setInfo(soupInfo)
print("How to get there: \n" + area.getInfo())

# Make a list of all topo images
mydiv0 = soup.findAll("div", class_="topo_photo")
for div0 in mydiv0:
  soupUrl = "http://www.bleau.info" + str(div0.find('a')['href'])
  area.addTopo(soupUrl)
  urlretrieve(str(soupUrl), area.getName().replace(" ","") + "-" + str(area.getToponumber()) + ".jpg")


# Loop over all boulders in the topo
boulder_counter = 0

mydivs = soup.findAll("div", class_="row lvar")
for div in mydivs:

  number = div.contents[1].get_text().strip()

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
  info = list(filter(None,info))
  if(not str(info[2][0]).isdigit()):
    info.insert(2,"")
  if((not str(info[3][0]).isupper()) and \
     (str(info[3]).find('yann') < 0)):
    info.insert(3,"")
  if(4 < len(info) and not str(info[4][0]).isupper()):
    info.insert(4,"")
  if(5 < len(info) and not str(info[5][0]).isupper()):
    info.insert(5,"")

  tempboulder = fb.Boulder()
  tempboulder.setName(info[0])
  tempboulder.setNumb(number)

#  print tempboulder.getNumb() , tempboulder.getName()

  tempboulder.setGrade(info[1])
  if (info[2] != ""): 
    tempboulder.setGrade(info[2])

  tempboulder.setOpener(info[3])
  if (4 < len(info) and info[4] != ""): 
    tempboulder.setOpener(info[4])
  if (5 < len(info) and info[5] != ""): 
    tempboulder.setOpener(info[5])

  tempboulder.setStyle(info[6])
  if (7 < len(info) and info[7] != ""): 
    tempboulder.setStyle(info[7])
  if (8 < len(info) and info[8] != ""): 
    tempboulder.setStyle(info[8])
  if (9 < len(info) and info[9] != ""): 
    tempboulder.setStyle(info[9])

# Get info on how to climb the boulder, this can be found on the boulder page
  boulder = "http://www.bleau.info" + str(div.find('a')['href'] + "?locale=en")
  response2 = urlopen(boulder)
  soup2 = BeautifulSoup(response2,"lxml")

  mydiv2 = soup2.findAll("div", class_="bdesc")
  for div2 in mydiv2: 
    extra = div2.get_text().strip()
    tempboulder.setInfo(str(extra))

# Get the number of repeats of the boulder
  repeats = 0

  mydiv4 = soup2.findAll("div", class_="bopins")
  for div4 in mydiv4: 
    ascents = div4.get_text().strip()
    if (str(ascents).find('ascents') > 0):
      repeats = int(ascents[str(ascents).find('(')+1:str(ascents).find(' total)')])
  tempboulder.setAscents(repeats)
  
#  print temoboulder.getInfo()
#  print tempboulder.getOpener()
#  print tempboulder.getGrade()
#  print tempboulder.getAscents()

  print(tempboulder.getNumb() , tempboulder.getName(), tempboulder.getGrade(), tempboulder.getAscents())
  area.addBoulder(tempboulder)

# End loop over all boulders in the topo
print(area.getBouldernumber())

# Sort according to popularity
print()
print("The most popular boulders are")
popular = sorted(area.boulder_list, key=itemgetter("ascents"), reverse=True)
for item in popular[:10]:
	print(item.name, item.grade, item.ascents)
