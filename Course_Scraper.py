import requests
from bs4 import BeautifulSoup
import re

URL = "https://catalog.gatech.edu/coursesaz/"
page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")
majors = str(soup.find_all("a"))
majors = re.findall('\(([^)]+)\)', majors)

course_list = []

for major in majors:
    major = major.lower()
    print(f"Starting {major}...")
    URL = f"https://catalog.gatech.edu/coursesaz/{major}"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    courses = soup.find_all("p", class_="courseblocktitle")
    for element in courses:
        course_credit_hours = int(re.search(r'(\d+)\D+$', element.text).group(1))
        course_name = element.text[0:element.text.find('.')].replace(u'\xa0', u' ')
        if re.search(r'\d{4}$', course_name) != None and course_credit_hours <= 4:
            temp_string = course_name + " " + str(course_credit_hours)
            #print(temp_string)
            course_list.append(temp_string)

course_file = open("course_list.txt", "w")
course_file.write(str(course_list))
course_file.close()
