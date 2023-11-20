# s203634 - Freja Holme Barkler 
# s203595 - Liva Friis Sommer
# Group 15

import numpy as np
import ifcopenshell
import ifcopenshell.util.element
import math as m

###### ------------ FINDS THE MODEL ------------ ######

from pathlib import Path

modelname = "LLYN-STRU"

try:
    dir_path = Path(__file__).parent
    model_url = Path.joinpath(dir_path, 'model', modelname).with_suffix('.ifc')
    model = ifcopenshell.open(model_url)
except OSError:
    try:
        import bpy
        model_url = Path.joinpath(Path(bpy.context.space_data.text.filepath).parent, 'model', modelname).with_suffix('.ifc')
        model = ifcopenshell.open(model_url)
        print(model_url)
    except OSError:
        print(f"ERROR: please check your model folder : {model_url} does not exist")


#General information
print("                                  ")
print("----------------------------------")
print("------ GENERAL INFORMATION -------")
print("----------------------------------")
print("                                  ")

print("This scripts relates data on the structural element of the model. The three element types taken into account is IfcBeams, IfcColumns, and IfcSlabs.\n")
print("The file type is", model.schema, "\n")


# Defines IFC elements and types
storey = model.by_type("IfCBuildingStorey")

    # Count all beams and types
all_beams = model.by_type("IfcBeam")
beam_types = model.by_type("IfcBeamType")

    # Count all columns and types
all_columns = model.by_type("IfcColumn")
column_types = model.by_type("IfcColumnType")

    # Count all slabs and types
all_slabs = model.by_type("IfcSlab")
slab_types = model.by_type("IfcSlabType")

# Computes a list of all materials
all_elements = all_beams + all_columns + all_slabs
all_types = beam_types + column_types + slab_types
all_materials = []
i = 0
for x in all_types:
    types_i = all_types[i]
    if ifcopenshell.util.element.get_material(types_i) == None:
       material = None   
    else:
        material = ifcopenshell.util.element.get_material(types_i)[0]
    all_materials.insert(i,material)
    i = i + 1

    # Computes a list without doublets
materials = []
[materials.append(x) for x in all_materials if x not in materials]

### Prints above information
print('The considered model has', len(storey), 'floors, and contains a total of', len(all_elements), 'structural element parts, distrubuted on beams, columns, and slabs. \nThese elements are assigned a total of', len(materials), 'material labels.\n')


print('\033[4m' + "The IfcMaterials which appear in the model:" + '\033[0m')
i = 0
for x in materials:
    print(materials[i])
    i = i + 1
print('\n')


print("More detailed informations follows on the storeys and considered structural elements.")




################################################################
################################################################STOREYS
################################################################
print("\n------------ STOREYS ---------------\n")

#Prints the amount of storeys in the model
print('\033[4m' + "The name of the floors occurring in the model:" + '\033[0m')


# Alle etager listes op og printes
floor_array = []
floor_number = []
i = 0
for LongName in storey:
    name = storey[i].LongName
    print('Floor',i, ":", storey[i].LongName)
    floor_array.append(name)
    floor_number.append(i)
    i=i+1
    if i == len(storey):
        break


################################################################
################################################################BEAMS
################################################################
print("\n------------ BEAMS ---------------\n")


# Counts all beams and prints them
print('There are', len(all_beams), 'beams in the model')

beam_names = []
beam_spans = []
beam_materials = []
beam_info = []
for i in range(len(all_beams)):
    type = ifcopenshell.util.element.get_type(all_beams[i])
    beam_names.append(type[2])
    
    material = ifcopenshell.util.element.get_material(type)[0]
    beam_materials.append(material)

    pset = ifcopenshell.util.element.get_psets(all_beams[i])
    pset_common = pset['Pset_BeamCommon']
    span = round(pset_common['Span'],2)
    beam_spans.append(span)
    

    info = (type [2], material, span)
    beam_info.append(info)
#If this is printed, a list of all 565 beams will occur


# A function that counts the occurrence of the same element in a list
def count_occurrence(a):
  k = {}
  for j in a:
    if j in k:
      k[j] +=1
    else:
      k[j] =1
  return k


# Counts the occurence of each beam type (name, material, and span)
beam_info_occurrence = count_occurrence(beam_info)
beam_name_occurrence = count_occurrence(beam_names)
beam_material_occurrence = count_occurrence(beam_materials)
beam_span_occurrence = count_occurrence(beam_spans)
print("\nWhen distinguishing between names, materials, and length of spans there are", len(beam_info_occurrence), "types of beams in the model.\nWhen only considering the name this number is", len(beam_name_occurrence), "while", len(beam_material_occurrence), "for materials, and", len(beam_span_occurrence), "for spans.\n")

beam_type_occurrences = []
beam_type_names = []
beam_type_materials = []
beam_type_spans = []
for x, y in beam_info_occurrence.items():
    beam_type_occurrences.append(y)
    beam_type_names.append(x[0])
    beam_type_materials.append(x[1])
    beam_type_spans.append(x[2])

print('\033[4m' + "The occurrence of each beam name:" + '\033[0m')
for x, y in beam_name_occurrence.items():
    print(y,':', x)

print('\n\033[4m' + "The occurrence of each material assigned to a beam:" + '\033[0m')
for x, y in beam_material_occurrence.items():
    print(y,':', x)

print('\n\033[4m' + "The minimum and maximum beam spans obtained:" + '\033[0m')
print("Minimum span: ", min(beam_spans))
print("Maximum span: ", max(beam_spans))

################################################################
################################################################COLUMNS
################################################################
print("\n------------ COLUMNS ---------------\n")


# Counts all columns and prints them
print('There are', len(all_columns), 'columns in the model')


# Creates a list of all columns in the model by their names
column_names = []
column_materials = []
column_info = []
for i in range(len(all_columns)):
    type = ifcopenshell.util.element.get_type(all_columns[i])
    column_names.append(type[2])
    
    material = ifcopenshell.util.element.get_material(type)[0]
    column_materials.append(material)
    
    info = (type [2], material)
    column_info.append(info)


#Counts the occurence of each column type (name, material, and span)
column_info_occurrence = count_occurrence(column_info)
column_name_occurrence = count_occurrence(column_names)
column_material_occurrence = count_occurrence(column_materials)
print("\nWhen distinguishing between names, materials, and length there are", len(column_info_occurrence), "types of columns in the model.\nWhen only considering the name this number is", len(column_name_occurrence), "while", len(column_material_occurrence), "for materials.\n")

column_type_occurrences = []
column_type_names = []
column_type_materials = []

for x, y in column_info_occurrence.items():
    column_type_occurrences.append(y)
    column_type_names.append(x[0])
    column_type_materials.append(x[1])

print('\033[4m' + "The occurrence of each column name:" + '\033[0m')
for x, y in column_name_occurrence.items():
    print(y,':', x)

print('\n\033[4m' + "The occurrence of each material assigned to a column:" + '\033[0m')
for x, y in column_material_occurrence.items():
    print(y,':', x)



################################################################
################################################################SLABS
################################################################
print("\n------------ SLABS ---------------\n")


# Counts all slabs and prints them
print('There are', len(all_slabs), 'slabs in the model')

# Creates a list of all slabs in the model by their names
slab_names = []
slab_materials = []
slab_info = []
for i in range(len(all_slabs)):
    type = ifcopenshell.util.element.get_type(all_slabs[i])
    slab_names.append(type[2])
    
    if ifcopenshell.util.element.get_material(type) == None:
       material = None   
    else:
        material = ifcopenshell.util.element.get_material(type)[0]       
    slab_materials.append(material)
    
    info = (type [2], material)
    slab_info.append(info)

#Counts the occurence of each slab type (name, material)
slab_info_occurrence = count_occurrence(slab_info)
slab_name_occurrence = count_occurrence(slab_names)
slab_material_occurrence = count_occurrence(slab_materials)
print("\nWhen distinguishing between names and materials there are", len(slab_info_occurrence), "types of slabs in the model.\nWhen only considering the name this number is", len(slab_name_occurrence), "while", len(slab_material_occurrence), "for materials.\n")

slab_type_occurrences = []
slab_type_names = []
slab_type_materials = []

for x, y in slab_info_occurrence.items():
    slab_type_occurrences.append(y)
    slab_type_names.append(x[0])
    slab_type_materials.append(x[1])

print('\033[4m' + "The occurrence of each slab name:" + '\033[0m')
for x, y in slab_name_occurrence.items():
    print(y,':', x)

print('\n\033[4m' + "The occurrence of each material assigned to a slab:" + '\033[0m')
for x, y in slab_material_occurrence.items():
    print(y,':', x)

###################### Export to excel #####################

import pandas as pd


scheme = model.schema

#Defining the data for excel
#Using DataFrame design
M = pd.DataFrame({'Model name':[modelname], 'File type':[scheme], 'Made by': ['s203634 & s203595'], 'Floors': len(storey), 'Beams':len(all_beams), 'Columns':len(all_columns), 'Slabs': len(all_slabs)})
Floors = pd.DataFrame({'Level':floor_number, 'Floor':floor_array})
B = pd.DataFrame({'Beam Types':beam_type_names, 'Occurrence':beam_type_occurrences, 'Material':beam_type_materials, 'Span':beam_type_spans})
C = pd.DataFrame({'Column Types':column_type_names, 'Occurrence':column_type_occurrences, 'Material':column_type_materials})
S = pd.DataFrame({'Slab Types':slab_type_names, 'Occurrence':slab_type_occurrences, 'Material':slab_type_materials})


# Choose the right path to where you want the excel file to end!!!
print('\nThe script will export data on the structural elements to an excel file. Please write the path that you wish the file to be exportet to in the code of the script.')
# Frejas file path
excel_file_path = '/Users/frejaholmebarkler/Desktop/Advanced BIM/Pyhton_Scripts_in_Blender/model_output.xlsx'

#Writer will write the excel file
writer = pd.ExcelWriter(excel_file_path)

#Puts the data into the excel file
M.to_excel(writer, sheet_name = 'Model info', index = False)
Floors.to_excel(writer, sheet_name = 'Floors', index = False)
B.to_excel(writer, sheet_name = 'Beams', index = False)
C.to_excel(writer, sheet_name = 'Columns', index = False)
S.to_excel(writer, sheet_name = 'Slabs', index = False)

#Saving the file
writer._save()


