'''
This baby program should grow into the program to sort courses into the tree of prereqs/coreqs. 
FOR NOW, all this code does is take ONE course and find its prereqs and coreqs.
For one course code,
2D array: 1 array for prereqs, 1 array for coreqs

EXAMPLE TEXT:
"
CMPUT 206 - Introduction to Digital Image Processing


View Available Classes



3 units (fi 6)(EITHER, 3-0-3)
An introduction to basic digital image processing theory, and the tools that make advanced image manipulation possible for ordinary users. Image processing is important in many applications: editing and processing photographs, special effects for movies, drawing animated characters starting with photographs, analyzing and enhancing remote imagery, and detecting suspects from surveillance cameras. Image processing building blocks and fundamental algorithms of image processing operations are introduced using Python libraries. Prerequisites: one of CMPUT 101, 174, or 274; one of MATH 100, 114, 117, 134, 144, or 154; and one of STAT 151, 161, 181, 235, 265, SCI 151, or MATH 181.
"

Return a tuple with three items:
(COURSE_CODE, list of prereqs, list of coreqs)
'''
import re

class Stack:
    def __init__(self):
        self.items = []
    
    def push(self, item):
        self.items.append(item)
    
    def pop(self):  
        if self.isEmpty():
            raise Exception("Cannot pop from an empty stack.")
        return self.items.pop()
    
    def peektop(self): 
        if self.isEmpty():
            raise Exception("Cannot peek into an empty stack.")
        return self.items[len(self.items)-1] 
    
    def isEmpty(self):
        return self.items == []
    
    def size(self):
        return len(self.items)
    
    def show(self):
        print(self.items)
    
    def peek_through(self):
        currently=[]
        for i in self.items:
            currently.append(i)
        return currently    
    
    def __str__(self):
        stackAsString = ''
        for item in self.items:
            stackAsString += str(item) + ' '
        return stackAsString
    
    def clear(self):
        if not self.isEmpty():
            self.items.clear()


def course_code(parent_text):
    #parent_text=parent_course.split()
    #get the course code
    parent_text = parent_text.replace(" ", "_")
    # print("PARENT TEXT:", parent_text)
    for idx in range(len(parent_text)):
        if parent_text[idx].isdigit():  #find the first number in the text, which is the course number
            parent_code = parent_text[:idx-1] + " " + parent_text[idx:idx+3]
            return parent_code

def remove_punctuation(word):
    if "." in word:
        end=True
    else:
        end=False
    return (re.sub(r'[^a-zA-Z0-9]', '', word), end)

def course_codes_list(prereq_string): 
    '''
    This code only runs if the word "Prereq" etc is in the string.

    Inputs: prereq_string (str) is a string. ie 
    "Prerequisites: one of CMPUT 101, 174, or 274; one of MATH 100, 114, 117, 134, 144, or 154; 
    and one of STAT 151, 161, 181, 235, 265, SCI 151, or MATH 181."

    Outputs: prereq_list (list) a 2d list. Example:
    [[CMPUT 101, CMPUT 192, CMPUT 274], 
    [MATH 100, MATH 114, MATH 117, MATH 134, MATH 144, MATH 154],
    [STAT 151, STAT 161, STAT 181, STAT 235, STAT 265, SCI 151, MATH 181]]
    '''
    prereq_list = []
    prereq_string = prereq_string.replace("and",";")
    prereq_or = prereq_string.split(";") #take our list of prereqs and separate them by the ";"
    coursename_stack = Stack() #have a stack of coursenames renewed for each group of sibling courses
    for siblings_line in prereq_or:
        siblings = []
        siblings_line = siblings_line.split()
        course_name = ""
        for word in siblings_line:
            word, end_flag=remove_punctuation(word)
            if end_flag:
                end_index=prereq_string.index(".")

            if word.isupper(): #do this--we can't simply say uppercase => course code; some courses are two words, ie "MA PH"
                if course_name:
                    course_name += "_"+word
                else:
                    course_name += word

            if (word.isdigit()):
                #  every time we encounter a course code, push to stack. 
                #  That way, if we have courses with no course code, just peek to the stack
                if (course_name):
                    coursename_stack.push(course_name)
                course_name = "" #clear the course code
                course_num = word #duh, because word is a digit.
                course_code = ""
                try:
                    course_code = coursename_stack.peektop() + " " + course_num #peek to the top of the stack!
                except:
                    pass
                if course_code:
                    siblings.append(course_code)
            
            if end_flag:
                if not siblings:
                    siblings=prereq_string[:end_index]
                prereq_list.append(siblings)
                return prereq_list
                
        if siblings:
             prereq_list.append(siblings)
    return prereq_list       
        

''' generates the prerequisite list
    input: parent_text (block text that holds the course description)
    output: prereq_list (2D list of all prerequisite classes)
'''
def prereqs(parent_text: str):
    prereqBlockList = ['Prerequisite:', 'Prerequisites:', 'Prerequisite', 'Prerequisites']
    parent_text=parent_text.split()
    prereq_idx=0
    for i in range(len(parent_text)):
        if parent_text[i] in prereqBlockList:
            prereq_idx = i  #index for the word "Prerequisite(s)"
    if not prereq_idx:
        return None
    prereq_text_block=' '.join(parent_text[1+prereq_idx:])
    
    if "Corequesite" in prereq_text_block or "Corerequisites" in prereq_text_block: #if there are coreqs, get rid of them
        if "Corequesite" in prereq_text_block:
            coreq_idx=prereq_text_block.index("Corequesite")
        if "Corerequisites" in prereq_text_block:
            coreq_idx=prereq_text_block.index("Corerequisites")
        prereq_text_block=prereq_text_block[:coreq_idx]
    
    prereq_list= course_codes_list(prereq_text_block)
    return(prereq_list)

def getPrereqs(coursetext):
        
    '''
    Inputs: parent_text (a huge block of text that includes the course name and description, type str)
    Outputs: a string, two lists in a tuple
    '''
    code = course_code(coursetext)
    prereqlist = (prereqs(coursetext))
    # print("THE PREREQLIST", code, prereqlist)
    return code, prereqlist


ex1= '''CMPUT 204 - Algorithms I
3 units (fi 6)(EITHER, 3-1S-0)
Faculty of Science

The first of two courses on algorithm design and analysis, with emphasis on fundamentals of searching,
sorting, and graph algorithms. Examples include divide and conquer, dynamic programming, greedy methods, backtracking, and local search methods, together with analysis techniques to estimate program efficiency. 
Prerequisites: CMPUT 175 or 275, and CMPUT 272; and one of MATH 100, 114, 117, 134, 144, or 154.'''
ex2='''CMPUT 206 - Introduction to Digital Image Processing
3 units (fi 6)(EITHER, 3-0-3)
Faculty of Science

An introduction to basic digital image processing theory, and the tools that make advanced 
image manipulation possible for ordinary users. 
Image processing is important in many applications: editing and processing photographs, special effects for movies, drawing animated characters starting with photographs, analyzing and enhancing remote imagery, and detecting suspects from surveillance cameras. 
Image processing building blocks and fundamental algorithms of image processing operations are introduced using Python libraries. 
Prerequisites: one of CMPUT 101, 174, or 274; one of MATH 100, 114, 117, 134, 144, or 154; and one of STAT 151, 161, 181, 235, 265, SCI 151, or MATH 181.'''
ex3='''CMPUT 275 - Introduction to Tangible Computing II
3 units (fi 6)(EITHER, 0-6L-0)
Faculty of Science

This is part 2 of a 2 sequence intensive introduction to Computing Science. Part 2 expands to add object-oriented programming, with C++, and more complex algorithms and data structures such as shortest paths in graphs; divide and conquer and dynamic programming; client-server style computing; and recursion. Prerequisite: CMPUT 274. Note: this course is taught in studio-style, where lectures and labs are blended into 3 hour sessions, twice a week. Enrollment is limited by the capacity of the combined lecture/lab facilities. Credit cannot be obtained for CMPUT 275 if one already has credit for any of CMPUT 174, 175, or 201, except with permission of the Department.'''
ex4='''OLIVIA 101 - skdbfksdbna nasjwjsnx ewud'''

ex5='''CMPUT 201 - Practical Programming Methodology
3 units (fi 6)(EITHER, 3-0-3)
Faculty of Science

Introduction to the principles, methods, tools, and practices of the professional programmer. The lectures focus on the fundamental principles of software engineering based on abstract data types and their implementations. The laboratories offer an intensive apprenticeship to the aspiring software developer. Students use C and software development tools of the Unix environment. Prerequisite: CMPUT 175. Credit cannot be obtained for CMPUT 201 if credit has been obtained for CMPUT 275, except with permission of the Department.'''

ex5='''CMPUT 174 - Introduction to the Foundations of Computation I
3 units (fi 6)(EITHER, 3-0-3)
Faculty of Science

CMPUT 174 and 175 use a problem-driven approach to introduce the fundamental ideas of Computing Science. 
Emphasis is on the underlying process behind the solution, independent of programming language or style. Basic notions of state, control flow, data structures, recursion, modularization, and testing are introduced through solving simple problems in a variety of domains such as text analysis, map navigation, game search, simulation, and cryptography. Students learn to program by reading and modifying existing programs as well as writing new ones. No prior programming experience is necessary. 
Prerequisite: Math 30, 30-1, or 30-2. See Note (1) above. Credit cannot be obtained for CMPUT 174 if credit has already been obtained for CMPUT 274, 275, or ENCMP 100, except with permission of the Department.'''
