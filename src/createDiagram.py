from courseClass import Course
import json

def dumpCourseToJSON(course_list, json_file):
    nodeDataArray = []
    linkDataArray = []

    # Fancy Colors
    color_i = 0

    # Make the map to apply topological sort
    course_map = {}
    for i_course in course_list:
        course_map[i_course.name] = i_course

    # Make a queue with the level attached
    course_queue = [[course_list[0].name, 0]]
    # Save nodes in cache
    course_viewed = set()

    for q_course in course_queue:
        # Check the cache
        if (q_course[0] in course_viewed):
            continue
        course_viewed.add(q_course[0])
        
        # Add to Array
        catalog_link = "https://apps.ualberta.ca/catalogue/course/" + q_course[0].replace(" ", "/")
        nodeDataArray.append({"key":q_course[0], "level":q_course[1], "catalog":catalog_link})
        
        # Get the course
        try:
            i_course = course_map[q_course[0]]
        except:
            i_course = Course(q_course[0], [])

        # Prereq
        if (i_course.prereqs == None or len(i_course.prereqs) == 0):
            continue

        # print(i_course.name, "prereqs", i_course.prereqs, type(i_course.prereqs))

        for colors in i_course.prereqs:
            if (type(colors) != list):
                continue
            for j_course in colors:
                # Add all connections to the link data file
                linkDataArray.append({"from":i_course.name, "to":j_course, "line_color":color_i})
                # Add to the queue
                course_queue.append([j_course, q_course[1] + 1])
            # Next color group (finished this or fucntionality)
            color_i = color_i + 1
    
    # Write the JSON file
    write_file = open(json_file, 'w')

    # print("final node data:", nodeDataArray)

    all_data = [nodeDataArray, linkDataArray]
    write_file.write(json.dumps(all_data))

    write_file.close()


def main():
    courses = []
    courses.append(Course("MATH 315", [["MATH 305"], ["MATH 303", "MATH 304"]]))
    courses.append(Course("MATH 305", []))
    courses.append(Course("MATH 304", [["MATH 100"]]))
    courses.append(Course("MATH 303", [["MATH 100"]]))
    courses.append(Course("MATH 100", []))

    dumpCourseToJSON(courses, "static/js/JSON/diagramData.json")

if __name__ == "__main__":
    main()