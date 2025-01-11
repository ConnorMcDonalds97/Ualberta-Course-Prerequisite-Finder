'''
    This python program takes in a url for an individual class from the Ualberta course catalog and will store 
    the paragraph that includes the information, specifically with the co/prerequisites
'''

import requests
from bs4 import BeautifulSoup
# from IndividualPara import isolateParagraph
from courseClass import Course
import GetPrereqCorereq

BASEURL = "https://apps.ualberta.ca/catalogue/course" 


def isolateParagraph(soup):
    '''
        looks through the html file and finds "containers"
        Returns the course name and its course description for parsing
    '''
    # Look for any errors and return "ERROR" if there's more than 1 error
    error = soup.find_all("h4", {"class": "alert-heading"})
    if len(error) > 0:
        return "ERROR"

    # soup.find_all returns a list of containers that include different parts of the website
    text = soup.find_all("div", {"class": "container"})
    
    # Tag contains the course number and the course description which contains information about prereq
    elementTag = text[3]
    
    courseNumber = elementTag.find("h1", {"class": "m-0"}).get_text().strip() # Find the course number as text
    courseDesc = elementTag.find_all("p")[1].get_text().strip()     # Finds the description of the course
    courseInfo = courseNumber + '\n' + courseDesc

    #print(f"{courseInfo}\n\n")

    return courseInfo


def nextURL(classCode: str) -> str:
    '''
        Takes a class code as input and returns the associated URL as a string
        ex: classCode = 'CMPUT 201'
        returns: "https://apps.ualberta.ca/catalogue/course/CMPUT/201" 
    '''
    codeList = classCode.split() #ie classCode "CMPUT 174"
    if (len(codeList) != 2):
        return 'INVALID'
    
    newURL = BASEURL + '/' + codeList[0] + '/' + codeList[1]

    # print(newURL)
    return newURL

def getContent(url):
    '''
        Takes a url as a string and scrapes the website
    '''
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    return soup

def convertCourseCode(courseCode):
    '''
        This function handles the logic to get from a course code to a prereqs list
    '''
    newUrl = nextURL(courseCode)    # gets the newURL to get the data for the courseCode

    if newUrl == 'INVALID': 
        # print("RETURINGING INVALID URL")  
        return "INVALID"
    
    soup = getContent(newUrl)
    paragraph = isolateParagraph(soup)
    if paragraph == "ERROR":
        return 'INVALID'
    
    prereqsList = GetPrereqCorereq.getPrereqs(paragraph)
    # print(f"prereqsList: {prereqsList}")
    return prereqsList
