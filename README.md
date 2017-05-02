## Moodle Crawler for Humboldt University of Berlin
#### Testet with Moodle Version from November 2016

Download all Files from all courses from the choosen semester.

> Reference: [https://moodle.hu-berlin.de](https://moodle.hu-berlin.de)

---

### Requierment
 
 - **python3**
 
 - **HU Moodle Account**


---

### How to run:

**Download**

First of all you need to download the python file *.py


**open Terminal in Folder of Script**

~~~~
python3 moodle-crawler.py
~~~~
or
~~~~
python moodle-crawler.py
~~~~

~~~~
====================================
#    Humbold Universität Berlin    #
#          Moodle Crawler          #
====================================
Script to download all PDF Documents of all courses from the Moodle plattform

Login to proceed.
~~~~
**Enter Moodle-Username and Password**
~~~~

Benutzername: 
Passwort: 
~~~~
**Choose Semester to download**

*Note: If you select a semester with no courses, the script will download ALL courses without filtering by semester!*

~~~~
Available Semester: 
0  -  SoSe 2012
1  -  WiSe 2012/13
2  -  SoSe 2013
3  -  WiSe 2013/14
4  -  SoSe 2014
5  -  WiSe 2014/15
6  -  SoSe 2015
7  -  WiSe 2015/16
8  -  SoSe 2016
9  -  WiSe 2016/17
Choose Semester: 1
Successfully logged in.
==============================
~~~~


### How to stop:

If you want to stop the script, just hit

> Ctrl + C

or 

> Strg + C
