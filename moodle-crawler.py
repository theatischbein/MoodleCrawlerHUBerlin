# ************************************************* #
#                                                   #
#       Script by Jonny Tischbein                   #
#       Email: jonny_tischbein@systemli.org         #
#       27.11.2016                                  #
#                                                   #
# **************************************************#

import urllib
import urllib.parse
import urllib.request
import getpass
import sys
import requests
import os

def showIntro():
	print('====================================')
	print('#    Humbold Universität Berlin    #')
	print('#          Moodle Crawler          #')
	print('====================================')
	print('Script to download all PDF Documents of all courses from the Moodle plattform')
	print('\nLogin to proceed.')
	return

def findingCourse(s, courses):
	start = 0
	find = r.find("/course/view.php?id=", start)

	while(find != -1):
		course = "https://moodle.hu-berlin.de%s" % str(r)[find:find+25]
		course_id = r[find+20:find+25]
		if course not in courses:
			# filter moodle help sites
			if '40916' not in course and '40917' not in course:
				if isCourseVisible(r, find, course_id):
					courses.append(course)
		start = find+25
		find = r.find("/course/view.php?id=", start)

def isCourseVisible(r, find, course_id):
	pattern_div = '<div id="coc-course-%s' % course_id
	pattern = ' coc-hidden'

	start_div = r.rfind(pattern_div, 0, find)
	if(start_div != -1):
		if(r.find(pattern, start_div, find) == -1):
			#print(course_id, "is visible")
			return True
		else:
			#print("Course %s not visible" %course_id)
			return False


def gettingFiles(s, files, sections):
	for course in courses:

		files = []

		r1 = s.get(course)
		r1 = r1.text

		start = 0
		find = r1.find("/mod/resource/view.php?id=", start)

		while(find != -1):
			file = "https://moodle.hu-berlin.de%s" %r1[find:find+33]
			if file not in files:
				#filter "Schreiben des Prsäidenten"
				if "1221387" not in file:
					files.append([])
					files[-1].append(file)
					files[-1].append(findingSection(r1, find))
			start = find+33
			find = r1.find("/mod/resource/view.php?id=", start)
		
		title_start = r1.find(">Kurs: ")+1
		title_end = r1.find("</title>")
		title = r1[title_start:title_end]

		print(title)
		
		title = title.replace("/", "_")
		path = "%s/%s" %(semester[int(choosen_semester)][0].replace("/", "_"), title[6:])

		os.makedirs(path,exist_ok=True)

		
		downloadFiles(s, path, files)

def findingSection(r1, find):
	pattern = '<span class="hidden sectionname">'
	Section_start = r1.rfind(pattern, 0, find)
	if(Section_start != -1):
		Section_end = r1.find("</", Section_start+len(pattern))
		Section_name = r1[Section_start+len(pattern):Section_end]

		if(Section_name not in sections):
			sections.append(Section_name)
		return Section_name


def downloadFiles(s, title, files):
	lastfile = ""

	for file in files:
		if not file:
			continue

		pdf_content = s.get(file[0], stream=True, allow_redirects=True)
		total_length = pdf_content.headers.get('content-length')

		file_name = pdf_content.headers.get('Content-Disposition')
		if not file_name:
			pdf_end = pdf_content.text.find(".pdf")
			if(pdf_end != -1):
				pdf_start = pdf_content.text.rfind('="', 0, pdf_end)
				if(pdf_start != -1):
					file_url = pdf_content.text[pdf_start+2:pdf_end+4]

					#download again
					pdf_content = ""
					pdf_content = s.get(file_url, stream=True, allow_redirects=True)
					total_length = pdf_content.headers.get('content-length')
					file_name = pdf_content.headers.get('Content-Disposition')


		if not file_name:
			print("Error: Again no Filename", pdf_content.headers)
			continue

		file_name_start = file_name.find("filename=")
		file_name = file_name[file_name_start+10:-1]

		if (file_name == lastfile):
			continue

		print("\n", file_name)
		lastfile = file_name

		subdir = "%s%s%s" % (title, "/", file[1])
		os.makedirs(subdir,exist_ok=True)

		path = "%s%s%s" % (subdir, "/", file_name)

		pdf_file = open(path, 'wb')
		if(pdf_content.status_code != 404):
			dl = 0
			total_length = int(total_length)
			for data in pdf_content.iter_content(chunk_size=4096):
			    dl += len(data)
			    pdf_file.write(data)
			    done = int(50 * dl / total_length)
			    sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50-done)) )    
			    sys.stdout.flush()
			print("")
		else:
			print("not found")


showIntro()
loginurl = 'https://moodle.hu-berlin.de/login/index.php';

my_username = input('Benutzername: ')

my_password = getpass.getpass('Passwort: ')

semester = [['SoSe 2012','2012-1'], ['WiSe 2012/13','2012-2'],['SoSe 2013','2013-1'], ['WiSe 2013/14','2013-2'],['SoSe 2014','2014-1'], ['WiSe 2014/15','2014-2'],['SoSe 2015','2015-1'], ['WiSe 2015/16','2015-2'],['SoSe 2016','2016-1'], ['WiSe 2016/17','2016-2']]
print('Available Semester: ')
i = 0
for s in semester:
	print(i, " - ", s[0])
	i+=1
choosen_semester = input('Choose Semester: ')

dashboard = 'https://moodle.hu-berlin.de/my/?coc-term=%s' %semester[int(choosen_semester)][1]

s = requests.Session()
s.post(loginurl, {'id' : 'login', 'username' : my_username, 'password' : my_password}, allow_redirects=True)
r = s.get(dashboard)
r = r.text

# Checking for Login
if r.find('body  id="page-my-index"') == -1:
	print("Error: your are not logged in")
	exit()
else:
	print("Successfully logged in.\n==============================\n")

	#=====================================
	# finding courses
	#=====================================
	courses = []
	findingCourse(s, courses)

	#=====================================
	# access courses and download files
	#==================

	# files[0] - link, files[1] - section
	files = [[]]
	sections = []
	gettingFiles(s, files, sections)



		
