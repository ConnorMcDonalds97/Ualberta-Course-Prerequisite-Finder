import requests
from bs4 import BeautifulSoup

'''
like 99% sure this code is not used
'''


def isolateParagraph(soup):
    '''
        looks through the html file and finds "containers"
    '''
    
    # soup.find_all returns a list of containers that include different parts of the website
    text = soup.find_all("div", {"class": "container"})
    
    # Tag contains the course number and the course description which contains information about prereq
    elementTag = text[3]
    
    # Find the course number as text
    courseNumber = elementTag.find("h1", {"class": "m-0"}).get_text().strip()
    #print(courseNumber)
    
    # Finds the description of the course
    courseDesc = elementTag.find_all("p")[1].get_text().strip()
    #print(courseDesc)
    
    courseInfo = courseNumber + '\n' + courseDesc
    
    print(courseInfo)
    
    #print(elementTag)


def main():
    url = "https://apps.ualberta.ca/catalogue/course/cmput/201"

    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    isolateParagraph(soup)


if __name__ == '__main__':
    main()