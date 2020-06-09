#HTML PARSER PROGRAM
#AUTHOR: ARKA
import requests
URL = "https://arka816.github.io/portfolio/"
#r=requests.get(URL)
#script=r.content
script="""<html>
    <head>
        <meta charset='utf-8'>
        <title>Introduction</title>
        <link rel="stylesheet" type="text/css" href="proj1.css">
    </head>
    <body>
        <!-- code for header panel-->
        <div class="link">
                <h1 style="color: #48076b; >">Arkaprava Ghosh</h1>
                <span>&nbsp&nbsp&nbsp&nbsp</span>
                <span>
                        <a href="achievements.html">achievements</a>
                </span>
                <span>
                        <a href="academics.html">academics</a>
                </span>
                <span>
                        <a href="interests.html">interests</a>
                </span>
                <span>
                        <a href="contacts.html">contact me</a>
                </span>
        </div>
    </body>
</html>"""

class HTMLTreeNode:
    def __init__(self):
        self.tagName = None
        self.parent = None
        self.childList = None
        self.attributeList = None

def parse(script):
    script=script.decode('utf-8')
    i=0
    while(i<len(script)):
        
        
    
    
parse(script)