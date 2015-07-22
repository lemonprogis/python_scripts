def editXMLInfo(metadataPath, node, value):
    import xml.etree.ElementTree as ET

    #get xml file set up
    xml1 = ET.ElementTree()
    xml1.parse(metadataPath)
    root = xml1.getroot()

    #make sure node already exists
    k = root.getiterator(node)

    if len(k) != 0:
        for r in k:
            #edit node value
            r.text = value
            #save metadata file
            xml1.write(metadataPath)

def addXMLInfo(metadataPath, newNode, aboveNode, value):
    import xml.etree.ElementTree as ET

    #get xml file set up
    xml1 = ET.ElementTree()
    xml1.parse(metadataPath)
    root = xml1.getroot()

    #see if the node already exists
    k = root.getiterator(newNode)
    #if not, it needs to be added
    if len(k) == 0:
        #adds new sub element to first node named like aboveNode
        r = root.getiterator(aboveNode)[0]
        #create new node
        a = ET.SubElement(r, newNode)
        #set node value
        a.text = value
        #save metadata file
        xml1.write(metadataPath)
        
def listmetadatafiles(folder):
    import os
    mList = []
    list = os.listdir(folder)
    for names in list:
        if names.endswith(".xml"):
            mList.append(names)
    return mList
