import individualURLFinder as iFinder
from courseClass import Course

COURSELIST = []
COURSENAMELIST = []


def createLayer(givenT):
    '''
    This is a function that will recursively find all of the prerequisite courses as given 
    by givenT
    '''
    if givenT == 'INVALID':
        print("givenT: ", givenT)

    courseName = givenT[0] #original course
    prereqs = givenT[1] #the prereqs for the original course

    if givenT[1] == None:
        course = Course(courseName, prereqs)
        COURSELIST.append(course)
        COURSENAMELIST.append(courseName)
        return
    
    if courseName in COURSENAMELIST:
        print(f"Already in the CNL: {courseName}")
        return
    

    course = Course(courseName, prereqs)
    COURSELIST.append(course)
    COURSENAMELIST.append(courseName)
    
    for i in range(len(course.prereqs)):    # looping through all ANDs
        # print("course prereqs",course.prereqs[i], "course prereqs length ",len(course.prereqs[i]))
        
        if (isinstance((course.prereqs[i]), str) ):
            pass
        elif len(course.prereqs[i]) > 1: #  more than one course is a prereq
            for j in range(len(course.prereqs[i])):    # looping through all ORs
                courseCode = course.prereqs[i][j]

                if courseCode not in COURSENAMELIST:
                    prereqsList = iFinder.convertCourseCode(courseCode) # converts the coursecode into the prereqs list of that course
                    if prereqsList!='INVALID':
                        createLayer(prereqsList)
        elif len(course.prereqs[i]) == 1: # only one course is a prereq
            courseCode = course.prereqs[0][0]

            if courseCode not in COURSENAMELIST:
                prereqsList = iFinder.convertCourseCode(courseCode)
                if prereqsList != 'INVALID':
                    createLayer(prereqsList)
                else:
                    return
            
        elif len(course.prereqs[i]) == 0:
            return
        else:
            print("THIS SHOULD NEVER HAPPEN")


def userInput(name):
    COURSELIST.clear()
    COURSENAMELIST.clear()
    
    name = name.strip()

    # Replace the space with underscore
    name = name.replace(" ", "_")
    for char_i in range(len(name)):
        if (name[char_i].isdigit()):
            name = name[:char_i-1] + " " + name[char_i:char_i+3]
            break

    print("THE NAME: ", name)
    prereqsList = iFinder.convertCourseCode(name)
    createLayer(prereqsList)
    
    # for i in COURSELIST:
        # print(i.name)
        
    return COURSELIST

# def main():

#     userInput = 'MATH 315'
    

#     prereqsList = iFinder.convertCourseCode(userInput)
#     createLayer(prereqsList)
    
    
#     for i in COURSELIST:
#         print(i.name)
#     print(COURSENAMELIST)
    
    
# if __name__ == '__main__':
#     main()