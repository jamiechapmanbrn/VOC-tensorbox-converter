from __future__ import print_function
from __future__ import division

import json
import xml.etree.ElementTree as ET

import os

out_file = 'tensorbox.json'

json_image = { 'image_path':'', 'rects':[] }
json_rect = { 'x1':0,'x2':0,'y1':0,'y2':0 }

def create_rect( x1,x2,y1,y2 ):
    return { 'x1':x1,'x2':x2,'y1':y1,'y2':y2 }

class image_dict:
    def __init__(self, image_path ):
        self.dict = { 'image_path':image_path, 'rects':[] }
        
    def add_rect(self, x1,x2,y1,y2 ):
        self.dict['rects'].append( create_rect(x1,x2,y1,y2) )
    
    def get_self(self):
        return self.dict
    
    

#example format we are converting to
format = '''<object-class> <x> <y> <width> <height>'''


#example formate we ar econverting from
example_input = \
'''<annotation>
  <folder>parking lot</folder>
  <filename>DJI_0065</filename>
  <path>/home/jamie/Downloads/parking lot/DJI_0065.JPG</path>
  <source>
    <database>Unknown</database>
  </source>
  <size>
    <width>4000</width>
    <height>3000</height>
    <depth>3</depth>
  </size>
  <segmented>0</segmented>
  <object>
    <name>car</name>
    <pose>Unspecified</pose>
    <truncated>0</truncated>
    <difficult>0</difficult>
    <bndbox>
      <xmin>108</xmin>
      <ymin>492</ymin>
      <xmax>241</xmax>
      <ymax>564</ymax>
    </bndbox>
  </object>'''


tag_dict = { 'car':'1' }


def intxmltag( the_tag, the_text):
    return int(the_tag.find(the_text).text)

def replace_ext( file_name, ext ):
    return os.path.splitext(file)[0] + ext


    
    
cwd = os.getcwd()

include_extensions = ['.jpg','.png']

files = [file for file in os.listdir( cwd ) if os.path.splitext(file)[1].lower() in include_extensions ]

image_list = []

for file in files:
    
    image_tag = image_dict(file)

    tree = ET.parse( os.path.splitext(file)[0] + '.xml'  )
    root = tree.getroot()

    size_tag = root.find('size')
    image_size = [ intxmltag( size_tag , 'width' ), intxmltag( size_tag ,'height') ]
    print(image_size)

    for tag in root.findall('object'):
        image_type = tag_dict[tag.find('name').text]
        bound_box = tag.find('bndbox')
        x1 = intxmltag(bound_box ,'xmin')
        x2 = intxmltag(bound_box ,'xmax')
        y1 = intxmltag(bound_box ,'ymin')
        y2 = intxmltag(bound_box ,'ymax')

        image_tag.add_rect( x1,x2,y1,y2 )
    image_list.append(image_tag.get_self())

with open(out_file, 'w') as write_file:
    write_file.write(json.dumps(image_list))