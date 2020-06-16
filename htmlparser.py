#HTML PARSER PROGRAM
#AUTHOR ARKA
import sys

class htmlnode:
    def __init__(self):
        self.tagname = None
        self.parent = None
        self.id=None
        self.name = None
        self.classlist = []
        self.childlist = []
        self.attributelist = {}

    def getAttribute(self, key):
        if key in self.attributelist:
            return self.attributelist[key]
        else:
            return None
    def getId(self):
        return self.id
    def getClassList(self):
        return self.classlist
    def getParentNode(self):
        return self.parent
    def getChildren(self):
        return self.childlist
    def getTagName(self):
        return self.tagname
    def findElementById(self, identity):
        return searchElementById(self, identity)
    def findElementByTag(self, tagname):
        return searchElementByTag(self, tagname)
    def findElementByName(self, name):
        return searchElementByName(self, name)
    def findElementByClass(self, classname):
        return searchElementByClass(self, classname)
    def findElementsById(self, identity):
        elements=[]
        searchElementsById(self, elements, identity)
        return elements
    def findElementsByTag(self, tagname):
        elements=[]
        searchElementsByTag(self, elements, tagname)
        return elements
    def findElementsByClass(self, classname):
        elements=[]
        searchElementsByClass(self, elements, classname)
        return elements
    def findElementsByName(self, name):
        elements=[]
        searchElementsByName(self, elements, name)
        return elements


root = htmlnode()
root.tagname = "root"
garbagechars = ["\n", "\t", " "]
emptyelemlist= ["area", "base", "br", "col", "embed", "hr", "img", "input", "link",
                "meta", "param", "source", "track", "wbr", "!DOCTYPE"]
tagopen = False
ismarkup = True
isscript=False
tagstring=""
lasttagname=""
tagstack = []


### UTILITY FUNCTIONS
def searchElementById(node, identity):
    for child in node.childlist:
        if child.id == identity:
            return child
        else:
            n=searchElementById(child, identity)
            if n != None:
                return n
    return None

def searchElementByTag(node, tagname):
    for child in node.childlist:
        if child.tagname == tagname:
            return child
        else:
            n=searchElementByTag(child, tagname)
            if n != None:
                return n
    return None

def searchElementByName(node, name):
    for child in node.childlist:
        if child.name == name:
            return child
        else:
            n=searchElementByName(child, name)
            if n != None:
                return n
    return None

def searchElementByClass(node, classname):
    for child in node.childlist:
        for c in child.classlist:
            if classname == c:
                return child
        n=searchElementByClass(child, classname)
        if n != None:
            return n
    return None

def searchElementsById(node, elemlist, identity):
    if len(node.childlist) == 0:
        return
    for child in node.childlist:
        if child.id == identity:
            elemlist.append(child)
        searchElementsById(child, elemlist, identity)
    return

def searchElementsByTag(node, elemlist, tagname):
    if len(node.childlist) == 0:
        return
    for child in node.childlist:
        if child.tagname == tagname:
            elemlist.append(child)
        searchElementsByTag(child, elemlist, tagname)
    return

def searchElementsByClass(node, elemlist, classname):
    if len(node.childlist) == 0:
        return
    for child in node.childlist:
        for c in child.classlist:
            if classname == c:
                elemlist.append(child)
                break
        searchElementsByClass(child, elemlist, classname)
    return

def searchElementsByName(node, elemlist, name):
    if len(node.childlist) == 0:
        return
    for child in node.childlist:
        if child.name == name:
            elemlist.append(child)
        searchElementsByName(child, elemlist, name)
    return


### PARSE ATTRIBUTES
def parseAttribute(string):
    attrdict = {}
    iskey = True
    isval = False
    key=""
    value=""
    for i in range(len(string)):
        char = string[i]
        if iskey and char != " ":
            key += char
        if isval:
            value += char
        if char == "\"" and string[i-1] != "\\":
            if isval:
                value=value.strip("\"")
                attrdict[key] = value
                value=""
                key = ""
                isval = not isval
                iskey = not iskey
            else:
                isval = not isval
        if char == "=":
            key=key.strip("=")
            iskey = not iskey

    return attrdict


### PARSE HTML TAG
def parseTag(string):
    if len(string) == 0:
        return
    global root
    tagname=""
    attributestring=""
    attributelist=[]
    identity=""
    name=""
    classlist=[]

    if string[0] == "/":
        tagname=string[1:].strip()
    else:
        f=string.find(" ")
        if f == -1:
            tagname = string
        else:
            tagname = string[:f]
            attributestring=string[f:].strip().strip("/").strip()

    if len(attributestring) > 0:
        attributelist = parseAttribute(attributestring)

    if "id" in attributelist:
        identity=attributelist["id"]
        attributelist.pop("id")
    if "class" in attributelist:
        classstr=attributelist["class"]
        attributelist.pop("class")
        for classname in classstr.split(' '):
            if len(classname) > 0:
                classlist.append(classname)
    if "name" in attributelist:
        name=attributelist["name"]
        attributelist.pop("name")

    if string[-1] == "/":
        node = htmlnode()
        node.tagname = tagname
        node.parent = root
        node.attributelist = attributelist
        node.id=identity
        node.name=name
        node.classlist=classlist
        root.childlist.append(node)
    elif string[0] == "/":
        if tagname not in emptyelemlist:
            if tagstack[-1].tagname == tagname:
                root = root.parent
                tagstack.pop()
                #print("popping", p.tagname)
            else:
                print("error parsing html", "invalid markup", tagname, tagstack[-1].tagname)
    else:
        node = htmlnode()
        node.tagname = tagname
        node.parent = root
        node.attributelist = attributelist
        node.id=identity
        node.name=name
        node.classlist=classlist
        root.childlist.append(node)
        if tagname not in emptyelemlist:
            tagstack.append(node)
            root=node
            #print("pushing", node.tagname)
            
    return tagname


### SANITIZE HTML OF SCRIPTS
def sanitizeScript(htmlstring):
    start=0
    end=0
    while htmlstring.find("<script>") != -1:
        start = htmlstring.find("<script>")
        end = htmlstring.find("</script>", start + 8, len(htmlstring) - 1) + 9
        htmlstring = htmlstring[:start] + htmlstring[end:]
    #print(htmlstring)
    return htmlstring
		


### READ HTML MARKUP
def parseHTML(htmlstring):
    global tagopen, ismarkup, tagstring, lasttagname
    htmlstring=sanitizeScript(htmlstring)
    for i in range(len(htmlstring)):
        char = htmlstring[i]
        if char in garbagechars and not tagopen:
            continue
        if char=="<" and ismarkup:
            if htmlstring[i+1:i+4] == "!--":
                i = htmlstring.find('-->', i+4, len(htmlstring) - 1) + 3
                continue
            else:
                tagopen=True
                continue
        if char==">" and ismarkup:
            tagopen=False
            tagstring = tagstring.strip(" ")
            lasttagname=parseTag(tagstring)
            tagstring=""
            continue
        if char=="\"" and htmlstring[i-1] != "\\":
            ismarkup = not ismarkup
        if tagopen:
            tagstring += char

    if len(tagstack) != 0:
        print("error parsing html", "corrupted markup")
        return tagstack
        sys.exit()
    else:
        return root
