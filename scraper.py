# file scraper.py

# import own classes
import boulder as fb
import creator as cr

# import external stuff
import os
import sys
import requests

from urllib.request import urlopen 
from urllib.request import urlretrieve 

from bs4 import BeautifulSoup
from operator import itemgetter

def scrape_area(location,url):
#    s = requests.Session()
#
#    user_session = {'user_session[username]': '',
#                    'user_session[password]': ''}
#
#    r = s.post('https://bleau.info/user_session', data=user_session)
#
#    print(r.text)
#
#    r = s.get(url + "?locale=en")

#    print(r.content)

#    response1 = urlopen('https://bleau.info/profile')
#    print(response1)

    # Open correct page: the topo page
    response1 = urlopen(url + "?locale=en")
    
    # Open page and get area name
    soup = BeautifulSoup(response1,"lxml")
    soupTitle = soup.title.string
    soupName = soupTitle[0:soupTitle.find(" - ")]

    if "Fond des Gorges" in soupName:
        soupName += " Sector {}".format(soupTitle[-1:])
    if "Cuvier Nord" in soupName and "TMF" in soupTitle:
        soupName += " Sector TMP"
    if "Franchard Isatis" in soupName and "Fond" in soupTitle:
        soupName += " Fond"
    if "Long Boyau" in soupName and "Cosmos" in soupTitle:
        soupName += " Sector Cosmos"
    
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
    print()
    print("How to get there: \n" + area.getInfo())
    print()

    # Make a list of all topo images
    mydiv0 = soup.findAll("div", class_="topo_photo")
    for div0 in mydiv0:
        soupUrl = "http://www.bleau.info" + str(div0.find('a')['href'])
        area.addTopo(soupUrl)

        filename = area.getName().replace(" ","") + "-" + str(area.getToponumber()) + ".jpg"
        fullfilename = os.path.join(location, filename)

        urlretrieve(str(soupUrl),fullfilename)
    
    # Loop over all boulders in the topo
    boulder_counter = 0
    
    mydivs = soup.findAll("div", class_="row lvar")
    for div in mydivs:
    
        number = div.contents[1].get_text().strip()

#        print(div.contents[1])

        name = div.contents[3].find('a').contents[0]
        try: 
            openers = div.contents[3].find('em').contents[0]
        except:
            openers = 'n/a'
        try: 
            style = div.contents[3].find('span',{'class':'btype'}).contents[0]
        except: 
            style = 'n/a'
        grade = div.contents[3].contents[2].strip()
        
        tempboulder = fb.Boulder()
        tempboulder.setName(name)
        tempboulder.setNumb(number)
        tempboulder.setOpener(openers)
        tempboulder.setGrade(grade)
        tempboulder.setStyle(style)
    
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
      
        print(tempboulder.getNumb() , tempboulder.getName(), tempboulder.getGrade(), tempboulder.getAscents())
        area.addBoulder(tempboulder)
    
    # End loop over all boulders in the topo
    print()
    print("Boulders found: ",area.getBouldernumber())
    
    # Sort according to popularity
    print()
    print("The most popular boulders are")
    popular = sorted(area.boulder_list, key=itemgetter("ascents"), reverse=True)
    for item in popular[:10]:
        print(item.name, item.grade, item.ascents)

    return area

def main(url):
    location = os.getcwd() + '/topos/' 

    if url == 'all':
        with open('areas.txt', 'rU') as f:
            for line in f:
                name, url = line.split(": ")

                area = scrape_area(location,url.strip()) 
                cr.create_topo(location,area)
    else:
        area = scrape_area(location,url) 
        cr.create_topo(location,area)

if __name__ == '__main__':

    url = sys.argv[1]  
    
    main(url)
