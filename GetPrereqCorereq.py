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
    for idx in range(len(parent_text)):
        if parent_text[idx].isdigit():  #find the first number in the text, which is the course number
            parent_code = parent_text[:idx+3]
            return parent_code

def remove_punctuation(word):
    return re.sub(r'[^a-zA-Z0-9]', '', word)

def course_codes_list(prereq_string):
    '''
    Inputs: prereq_or (str) is a string. ie 
    "Prerequisites: one of CMPUT 101, 174, or 274; one of MATH 100, 114, 117, 134, 144, or 154; 
    and one of STAT 151, 161, 181, 235, 265, SCI 151, or MATH 181."

    Outputs: prereq_list (list) a 2d list. Example:
    [[CMPUT 101, CMPUT 192, CMPUT 274], 
    [MATH 100, MATH 114, MATH 117, MATH 134, MATH 144, MATH 154],
    [STAT 151, STAT 161, STAT 181, STAT 235, STAT 265, SCI 151, MATH 181]]
    '''
    prereq_list=[]
    prereq_or=prereq_string.split(";") #take our list of prereqs and separate them by the ";"
    print("BBBBBBBBBBBBBBBBBBBBBBBSSSSSS",prereq_or)
    coursename_stack=Stack() #have a stack of coursenames renewed for each group of sibling courses
    for siblings_line in prereq_or: 
        siblings_line=siblings_line.split()
        course_name=""
        for word in siblings_line:
            word=remove_punctuation(word)
           # print("HERE IS MYWORD", word)
            siblings=[]
            if word.isupper(): #do this--we can't simply say uppercase => course code; some courses are two words, ie "MA PH"
                print("AAAAAAAAAAAAAAAAAAAAAAAAA",word)
                if course_name:
                    course_name+=" "+word
                else:
                    course_name+=word
                print(course_name)
            if (word.isdigit()):
                coursename_stack.push(course_name)  
                print("COURSE NAME LLLLLLLLL",coursename_stack.peektop())
                print("THIS IS THE COURSENAME STACK",coursename_stack, course_name, word)
                #  every time we encounter a course code, push to stack. 
                #  That way, if we have courses with no course code, just peek to the stack
                course_name="" #clear the course code
                course_num=word #duh, because word is a digit.
                course_code = coursename_stack.peektop(), course_num #peek to the top of the stack!
                siblings.append(course_code)
        prereq_list.append(siblings)     
    return prereq_list       
        

def prereqs(parent_text):
    parent_text=parent_text.split()
    for i in range(len(parent_text)):
        if parent_text[i] == "Prerequisite:" or parent_text[i] == "Prerequisites:":
            prereq_idx = i  #index for the word "Prerequisite(s)"
            print(prereq_idx) #debug
            print(parent_text[prereq_idx]) #debug
    prereq_text_block=' '.join(parent_text[1+prereq_idx:])
    
    if "Corequesite" in prereq_text_block or "Corerequisites" in prereq_text_block: #if there are coreqs, get rid of them
        if "Corequesite" in prereq_text_block:
            coreq_idx=prereq_text_block.index("Corequesite")
        if "Corerequisites" in prereq_text_block:
            coreq_idx=prereq_text_block.index("Corerequisites")
        prereq_text_block=prereq_text_block[:coreq_idx]

    print("PREREQ TEXT BLOCK",prereq_text_block)
    
    prereq_list= course_codes_list(prereq_text_block)
    print(prereq_list)
              
coursetext= '''CMPUT 206 - Introduction to Digital Image Processing


View Available Classes



3 units (fi 6)(EITHER, 3-0-3)
An introduction to basic digital image processing theory, and the tools that make advanced image manipulation possible for ordinary users. Image processing is important in many applications: editing and processing photographs, special effects for movies, drawing animated characters starting with photographs, analyzing and enhancing remote imagery, and detecting suspects from surveillance cameras. Image processing building blocks and fundamental algorithms of image processing operations are introduced using Python libraries. 
Prerequisites: one of CMPUT 101, 174, or 274; one of MATH 100, 114, 117, 134, 144, or 154; and one of MA PH 151, 161, 181, 235, 265, SCI 151, or MATH 181. Corequesite: Blah blah blah 
'''

def main(coursetext):
        
    '''
    Inputs: parent_text (a huge block of text that includes the course name and description, type str)
    Outputs: two lists in a tuple
    '''
    code=course_code(coursetext)
    print(code)
    print(prereqs(coursetext))

main(coursetext)