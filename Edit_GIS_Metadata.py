import xml.etree.ElementTree as ET
import os

def editXMLInfo(metadataPath, node, value):

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
    return [name for name in os.listdir(folder) if name.endswith(".xml")]



class GisMetaData(object):
    '''
        Use this class to perform edits and additions to GIS Metadata files 
    '''
    def __init__(self, metadataPath):
        ''' 
        '''
        self.metadataPath = metadataPath
        self._et = ET.ElementTree()
        self.root = self._et.parse(metadataPath)

    def add(self, newNode, aboveNode, value):
        ''' adds a node to the existing xml
        '''
        k = self.root.getiterator(newNode)
        if len(k) == 0:
            r = self.root.getiterator(aboveNode)[0]
            a = ET.SubElement(r, newNode)
            a.text = value
            self._et.write(self.metadataPath)

    def edit(self, node, value):
        ''' edit an existing node in the metadata file
        '''
        k = self.root.getiterator(node)

        if len(k) != 0:
            for r in k:
                r.text = value
                self._et.write(self.metadataPath)

    def list_metadata_files(self, folder):
        ''' List metadata(xml) files in a folder
        '''
        return [name for name in os.listdir(folder) if name.endswith(".xml")]