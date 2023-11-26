# s203634 - Freja Holme Barkler 
# s203595 - Liva Friis Sommer
# Group 15


################################################################
################################################################ Imported packages
################################################################

import numpy as np
import ifcopenshell
import ifcopenshell.util.element
from pathlib import Path
import pandas as pd

################################################################
################################################################ Imports the IFC model
################################################################

# Searches for an IFC file with the name 'model'
modelname = 'model'

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
        print(f'ERROR: please check your model folder : {model_url} does not exist')


################################################################
################################################################ General information
################################################################

print("\n----------------------------------")
print("------ GENERAL INFORMATION -------")
print("----------------------------------\n")

print("This scripts relates data on the structural element of the model. The three element types taken into account is IfcBeams, IfcColumns, and IfcSlabs.\n")
print("The file type is", model.schema, "\n")


# Computes lists of all storeys and of all elements and types pertaining to the considered structural element

    # For storeys
storey = model.by_type("IfCBuildingStorey")

    # For beams
all_beams = model.by_type("IfcBeam")
beam_types = model.by_type("IfcBeamType")

    # For columns
all_columns = model.by_type("IfcColumn")
column_types = model.by_type("IfcColumnType")

    # For slabs
all_slabs = model.by_type("IfcSlab")
slab_types = model.by_type("IfcSlabType")

    # For all elements
all_elements = all_beams + all_columns + all_slabs
all_types = beam_types + column_types + slab_types



# Computes a list of all materials corresponding to the order of the list of all elements

all_materials = []
i = 0
for x in all_elements:
    if ifcopenshell.util.element.get_material(x) == None:
        material = None   
    else:
        material = ifcopenshell.util.element.get_material(x)[0]
    all_materials.insert(i,material)
    i = i + 1

    
    # Computes a material list without doublets

materials = []
[materials.append(x) for x in all_materials if x not in materials]


# Prints an overview of the highlights of the data computed above

print('The considered model has', len(storey), 'floors, and contains a total of', len(all_elements), 'structural element parts, distrubuted on beams, columns, and slabs. \nThese elements are assigned a total of', len(materials), 'material labels.\n')

print('\033[4m' + "The IfcMaterials which appear in the model:" + '\033[0m')
i = 0
for x in materials:
    print('   ',materials[i])
    i = i + 1

print("\nMore detailed informations follows on the storeys and considered structural elements.")


################################################################
################################################################ Storeys
################################################################

print("\n------------ STOREYS ---------------\n")


# Prints the name of each floor in the model

print('\033[4m' + "The name of the floors occurring in the model:" + '\033[0m')
floor_array = []
floor_number = []
i = 0
for LongName in storey:
    name = storey[i].LongName
    print('   Floor',i, ":", name)
    floor_array.append(name)
    floor_number.append(i)
    i=i+1
    if i == len(storey):
        break


################################################################
################################################################ Beams
################################################################

print("\n------------ BEAMS ---------------\n")


# Prints and computes the number of beams appearing in the model

print('There are', len(all_beams), 'beams in the model')


# Computes lists of considered data of the beams

beam_names = []
beam_spans = []
beam_materials = []
beam_info = []
for i in all_beams:
    type_i = ifcopenshell.util.element.get_type(i)
    
    # Name of beams
    beam_names.append(type_i[2])
    
    # Material of beams
    material = ifcopenshell.util.element.get_material(type_i)[0]
    beam_materials.append(material)
    
    # Span of beam
    pset = ifcopenshell.util.element.get_psets(i)
    pset_common = pset['Pset_BeamCommon']
    span = round(pset_common['Span'],2)
    beam_spans.append(span)
    
    # Combines above information to one list
    info = (type_i [2], material, span)
    beam_info.append(info)


# Computes a function counting the occurrence of each type of element

def count_occurrence(a):
  k = {}
  for j in a:
    if j in k:
      k[j] +=1
    else:
      k[j] =1
  return k


# Applies function to count the occurence of above considered data for each beam type

    # Occurance of names
beam_name_occurrence = count_occurrence(beam_names)
    # Occurance of materials
beam_material_occurrence = count_occurrence(beam_materials)
    # Occurance of span lengths
beam_span_occurrence = count_occurrence(beam_spans)
    # Occurance of all combined sets of information
beam_info_occurrence = count_occurrence(beam_info)


# Prints a summation of the occurance of beams and types in model

print("\nWhen distinguishing between names, materials, and length of spans there are", len(beam_info_occurrence), "types of beams in the model.\nWhen only considering the name this number is", len(beam_name_occurrence), "while", len(beam_material_occurrence), "for materials, and", len(beam_span_occurrence), "for spans.\n")


# Prints lists of the occurance of several data points relevant for the beam element

    # Occurance of names
print('\033[4m' + "The occurrence of each beam name:" + '\033[0m')
for x, y in beam_name_occurrence.items():
    print('   ',y,':', x)

    # Occurance of materials
print('\n\033[4m' + "The occurrence of each material assigned to a beam:" + '\033[0m')
for x, y in beam_material_occurrence.items():
    print('   ',y,':', x)

    # Maximum and minimum span lengths
print('\n\033[4m' + "The minimum and maximum beam spans obtained:" + '\033[0m')
print('   ',"Minimum span: ", min(beam_spans))
print('   ',"Maximum span: ", max(beam_spans))



################################################################
################################################################ Columns
################################################################

print("\n------------ COLUMNS ---------------\n")


# Prints and computes the number of columns appearing in the model
print('There are', len(all_columns), 'columns in the model')


# Computes lists of considered data of the beams

column_names = []
column_materials = []
column_info = []
for i in all_columns:
    type_i = ifcopenshell.util.element.get_type(i)
    
    # Name of columns
    column_names.append(type_i[2])
    
    # Material of columns
    material = ifcopenshell.util.element.get_material(type_i)[0]
    column_materials.append(material)
    
    # Combines above information to one list
    info = (type_i [2], material)
    column_info.append(info)


# Applies function to count the occurence of above considered data for each beam type

    # Occurance of names
column_name_occurrence = count_occurrence(column_names)
    # Occurance of materials
column_material_occurrence = count_occurrence(column_materials)
    # Occurance of all combined sets of information
column_info_occurrence = count_occurrence(column_info)


# Prints a summation of the occurance of columns and types in model

print("\nWhen distinguishing between names, materials, and length there are", len(column_info_occurrence), "types of columns in the model.\nWhen only considering the name this number is", len(column_name_occurrence), "while", len(column_material_occurrence), "for materials.\n")


# Prints lists of the occurance of several data points relevant for the beam element

    # Occurance of names
print('\033[4m' + "The occurrence of each column name:" + '\033[0m')
for x, y in column_name_occurrence.items():
    print('   ',y,':', x)

    # Occurance of materials
print('\n\033[4m' + "The occurrence of each material assigned to a column:" + '\033[0m')
for x, y in column_material_occurrence.items():
    print('   ',y,':', x)


################################################################
################################################################ Slabs
################################################################

print("\n------------ SLABS ---------------\n")


# Prints and computes the number of slabs appearing in the model
print('There are', len(all_slabs), 'slabs in the model')


# Computes lists of considered data of the beams

slab_names = []
slab_materials = []
slab_info = []
for i in all_slabs:
    type_i = ifcopenshell.util.element.get_type(i)
    
    # Name of slabs
    slab_names.append(type_i[2])
    
    # Material of slabs
    if ifcopenshell.util.element.get_material(type_i) == None:
       material = None   
    else:
        material = ifcopenshell.util.element.get_material(type_i)[0]       
    slab_materials.append(material)
    
    # Combines above information to one list
    info = (type_i [2], material)
    slab_info.append(info)


#Counts the occurence of each slab type (name, material)

slab_info_occurrence = count_occurrence(slab_info)
slab_name_occurrence = count_occurrence(slab_names)
slab_material_occurrence = count_occurrence(slab_materials)


# Prints a summation of the occurance of columns and types in model

print("\nWhen distinguishing between names and materials there are", len(slab_info_occurrence), "types of slabs in the model.\nWhen only considering the name this number is", len(slab_name_occurrence), "while", len(slab_material_occurrence), "for materials.\n")


# Prints lists of the occurance of several data points relevant for the beam element

    # Occurance of names
print('\033[4m' + "The occurrence of each slab name:" + '\033[0m')
for x, y in slab_name_occurrence.items():
    print('   ',y,':', x)

    # Occurance of materials
print('\n\033[4m' + "The occurrence of each material assigned to a slab:" + '\033[0m')
for x, y in slab_material_occurrence.items():
    print('   ',y,':', x)


################################################################
################################################################ Assign material properties - user input
################################################################

# Prints introducing note to user program
print('\nIn the following we will be considering the structural related parameters of the materials.\nYou are given two options:\n  1. To assign the material parameters yourself for a list of ', len(materials),' materials.\n  2. To choose already programmed values for a selected few materials.') 


# Creates a dictonary for each material parameter.
dict_densities = {}
dict_emodulus = {}
dict_gmodulus = {}
dict_poissons = {}
dict_fy = {}
dict_fu = {}
dict_fck = {}
dict_fctm = {}


# Begins userinput program to assign material specific properties

# Computes a while loop ensuring the a valid user input
i = 0
while i == 0:
    i = input('Please type the number of the option you choose:')
    
    # Option 1: User assign material parameters
    if i == '1':

        # Runs through all materialtypes
        for x in materials:
            
            # Assigns an empty string for each parameter in case no other value is given
            rho = ''
            E = ''
            G = ''
            v = ''
            fy = ''
            fu = ''
            fck = ''
            fctm = ''
             
            m = 0
            while m == 0:
                
                # Controls if the actual material is pre-defined - and in that case assigns to the specific script for this material.
                if x == None:
                    m = '5'
                elif 'stål' in str.lower(x):
                    m = '1'
                elif 'beton' in str.lower(x):
                    m = '2'
                elif 'isolering' in str.lower(x):
                    m = '3'
                    
                # Ask for user input if material is not pre-defined
                else:
                    m = input ('Please assign a material from the list below to the the ifcmaterial of "' + x + '". \n  1. Steel \n  2. Concrete \n  3. Insulation \n  4. Other \n  5. Unkown \nType the number of the belonging material:')
                
                
                # Script for steel
                if m == '1':
                    print('\nThe ifcmaterial "', x, '" have been assigned to steel. \nIt is assumed to be of the type construction steel, which is why a number of characteristic material parameters are assigned in advance.')
                    
                    # Material specific values for steel
                    rho = 7850
                    E = 0.21e6
                    v = 0.3
                    G = round(E / (2*(1+v)),2)
                    
                    # Computes yield stress & tensile stress depended on two user inputs
                    print('.........................\nThe strenght of,', x, ' is depended on the assigned strenght class and the nominal thickness of the element.')
                    
                        # userinput: thickness
                    print('\nThe thickness must not exceed 80 mm and must be given in [mm], however in relation to the strength class we differ the options listed below,\n  1. <=40 [mm] \n  2.  >40 [mm]')
                    t = 0
                    while t == 0:
                        t = input('\nPlease enter the number that alligns with the thickness you wish to use in the calculations:')
                        if t == '1' or t == '2':
                            None
                        else:
                            # Error message for unvalid input
                            print('Error: The input was either not numeric or above 80 mm. Please try again')
                            t = 0
                    
                    
                        # userinput: strength class
                    print('\nThe streght classes considered are in agreement with the standard of "EN 10025-2" and listed below.\n  1. S235\n  2. S275\n  3. S355\n  4. S450')
                    c = 0
                    while c == 0:
                        c = input('\nPlease enter the number of the strenght class you wish to use in the calculations:')
                        
                        # Assigns strength properties depended on the user inputs
                        
                        # S235
                        if c == '1':  
                            if t == '1':
                                fy = 235
                                fu = 360
                            elif t == '2':
                                fy = 215
                                fu = 360
                        # S275
                        elif c == '2':
                            if t == '1':
                                fy = 275
                                fu = 430
                            elif t == '2':
                                fy = 255
                                fu = 410
                        # S355
                        elif c == '3':
                            if t == '3':
                                fy = 355
                                fu = 510
                            elif t == '4':
                                fy = 335
                                fu = 470
                                
                        # S450
                        elif c == '4':
                            if t == '5':
                                fy = 440
                                fu = 550
                            elif t == '6':
                                fy = 410
                                fu = 550
                                
                        else:
                            # Error message for unvalid input
                            print("Error: Please choose a number from the list")
                            c = 0
                                    
                # Script for concrete
                elif m == '2':
                    
                    print('.........................\nThe ifcmaterial "', x, '" have been assigned to concrete. \nThe density of concrete is depended on its composition and use. Roughly speaking, three categories have been established and listed below each with its own assumed density.\n  1. Light weighted concrete \n  2. Traditional concrete \n  3. Heavy concrete ')
                    
                    # userinput: Concrete type
                    rho = 0
                    while rho == 0:
                        rho = input('Please enter the number of the category you wish to use in the calculations, or type a density yourself in the range of 600 to 6000 kg/m3:')
                        
                        if rho == '1':
                            rho = 1200
                        elif rho == '2':
                            rho = 2400
                        elif rho == '3':
                            rho = 4800
                        elif rho.isnumeric() == True:
                            rho = int(rho)
                            if rho < 600 or rho > 6000:
                               print('Error: The input was not realistic. Please try again')
                               rho = 0         
                        else:
                            print('Error: The input was not numeric. Please try again')
                            rho = 0

                    # userinput: Strength class
                    print('\nThe strenght of is depended on the assigned strenght class.')
                    print('\nA list of selected strength classes is seen below.\n  1. C12\n  2. C20\n  3. C30\n  4. C40\n  5. C50\n  6. C60\n  7. C80\n')
                    c = 0
                    while c == 0:
                        c = input('\nPlease enter the number of the strenght class you wish to use in the calculations:')
                        
                        # Assigns strength properties depended on the user inputs
                        
                        # C12
                        if c == '1':
                            fck = 12
                            fctm = 1.6
                        # C20
                        elif c == '2':
                            fck = 20
                            fctm = 2.2
                        # C30
                        elif c == '3':
                            fck = 30
                            fctm = 2.9
                        # C40
                        elif c == '4':
                            fck = 40
                            fctm = 3.5
                        # C50
                        elif c == '5':
                            fck = 50
                            fctm = 4.1
                        # C60
                        elif c == '6':
                            fck = 60
                            fctm = 4.4
                        # C80
                        elif c == '7':
                            fck = 80
                            fctm = 4.8
            
                        else:
                            # Error message for unvalid input
                            print("Error: Please choose a number from the list")
                            c = 0
                        

                # Script for insulation 
                elif m == '3':
                    print('........................\nThe ifcmaterial "', x, '" have been assigned to insulation.\nThe density is depended on the type of insulation. Three categories have been established and listed below each with its own assumed density.\n  1. Light weighted insulation \n  2. Medium weighted insulation \n  3. Heavy weighted insulation ')
                    
                    # Assigns density depended on user input
                    
                    rho = 0
                    while rho == 0:
                        rho = input('Please enter the number of the category you wish to use in the calculations, or type a density yourself in the range of 10 to 300 kg/m3:')
                        
                        if rho == '1':
                            rho = 30
                        elif rho == '2':
                            rho = 100
                        elif rho == '3':
                            rho = 300
                        elif rho.isnumeric() == True:
                            rho = int(rho)
                            if rho < 10 or rho > 300:
                               print('Error: The input was not realistic. Please try again')
                               rho = 0         
                        else:
                            # Error message for unvalid input
                            print('Error: The input was not numeric. Please try again')
                            rho = 0
                    

                elif m == '4':
                    print('.........................\nThe ifcmaterial "', x, '" have been assigned to another material than the listed.')

                    rho = 0
                    while rho == 0:
                        rho = input('Please type the density of "' + x + '":')
                        if rho.isnumeric() == True:
                            rho = int(rho)
                        else:
                            # Error message for unvalid input
                            print('Error: The input was not numeric. Please try again')
                            rho = 0
                
                elif m == '5':
                    print('.........................\nThe material ',x,' is unknown. No properties will be assigned')
                    
                    
                else:
                    # Error message for unvalid input
                    print('Error: Please choose a number from the list')
                    m = 0
            
            dict_densities[x] = rho
            dict_emodulus[x] = E
            dict_gmodulus[x] = G
            dict_poissons[x] = v
            dict_fy[x] = fy
            dict_fu[x] = fu
            dict_fck[x] = fck
            dict_fctm[x] = fctm
          
            
    # Option 2: Pre-assigned material parameters
    elif i == '2':

        # Runs through the list of materials
        for x in materials:
            rho = ''
            E = ''
            G = ''
            v = ''
            fy = ''
            fu = ''
            fck = ''
            fctm = ''
            
            # Assign material specific values to the materials of which the name is detected in the IFCname
            if x == None:
                None
                    
            elif 'stål' in str.lower(x):
                rho = 7850
                E = 0.21e6
                v = 0.3
                G = round(E / (2*(1+v)),2)           
                fy = 255
                fu = 410
                                
            elif 'beton' in str.lower(x):
                rho = 2400
                fck = 40
                fctm = 3.5
                
            elif 'isolering' in str.lower(x):
                rho = 100
                
            
            dict_densities[x] = rho
            dict_emodulus[x] = E
            dict_gmodulus[x] = G
            dict_poissons[x] = v
            dict_fy[x] = fy
            dict_fu[x] = fu
            dict_fck[x] = fck
            dict_fctm[x] = fctm        

    else:
        # Error message for unvalid input
        print('Error: Please type a number from the list')
        i = 0

        

################################################################
################################################################ Modyfies propertyset
################################################################

# Runs thorugh all elements and modifies propertyset of each
i = 0
for element in all_elements:

    property_values = []
    material = all_materials[i]
    
    # Creates property value set for the materials of which a material parameter is assigned.
    
    # Density
    value = dict_densities[material]
    if type(value) == int or type(value) == float:
        #Computes an additional property set and loads it in the existing set of propertysets.  
        a = model.createIfcPropertySingleValue("Density", "Description of My Own Property", model.create_entity("IfcReal", value), None)
        property_values.append(a)
    else:
        # If no density value is assigned the density is defined as a nontype
        a = model.createIfcPropertySingleValue("Density", "Description of My Own Property", model.create_entity("IfcText", value), None)
        property_values.append(a)
        
        
    # Modulus of elasticity  
    value = dict_emodulus[material]    
    if type(value) == int or type(value) == float:
        #Computes an additional property set and loads it in the existing set of propertysets.  
        a = model.createIfcPropertySingleValue("Modulus of elasticity", "Description of My Own Property", model.create_entity("IfcReal", value), None)
        property_values.append(a)
    
    
    # Shear modulus
    value = dict_gmodulus[material]
    if type(value) == int or type(value) == float:
        #Computes an additional property set and loads it in the existing set of propertysets.  
        a = model.createIfcPropertySingleValue("Shear modulus", "Description of My Own Property", model.create_entity("IfcReal", value), None)
        property_values.append(a)
   
   
    # Poissons ratio
    value = dict_poissons[material]
    if type(value) == int or type(value) == float:
        #Computes an additional property set and loads it in the existing set of propertysets.  
        a = model.createIfcPropertySingleValue("Poisson's ratio", "Description of My Own Property", model.create_entity("IfcReal", value), None)
        property_values.append(a)
   
     
    # Yield stress
    value = dict_fy[material]
    if type(value) == int or type(value) == float:
        #Computes an additional property set and loads it in the existing set of propertysets.  
        a = model.createIfcPropertySingleValue("Yield stress", "Description of My Own Property", model.create_entity("IfcReal", value), None)
        property_values.append(a)
   
    
    # Tensile stress
    value = dict_fu[material]
    if type(value) == int or type(value) == float:
        #Computes an additional property set and loads it in the existing set of propertysets.  
        a = model.createIfcPropertySingleValue("Tensile stress", "Description of My Own Property", model.create_entity("IfcReal", value), None)
        property_values.append(a)
    
    
    # Compressive stress    
    value = dict_fck[material]
    if type(value) == int or type(value) == float:
        #Computes an additional property set and loads it in the existing set of propertysets.  
        a = model.createIfcPropertySingleValue("Compressive stress", "Description of My Own Property", model.create_entity("IfcReal", value), None)
        property_values.append(a)
    
    
    # Mean tensile stress
    value = dict_fctm[material]
    if type(value) == int or type(value) == float:
        #Computes an additional property set and loads it in the existing set of propertysets.  
        a = model.createIfcPropertySingleValue("Tensile stress", "Description of My Own Property", model.create_entity("IfcReal", value), None)
        property_values.append(a)
    
    
    # Creates propertyset of material values and load in the list of property values defined above 
    property_set = model.createIfcPropertySet(element.GlobalId, element.OwnerHistory, "Pset_MaterialValues", None, property_values)
    model.createIfcRelDefinesByProperties(element.GlobalId, element.OwnerHistory, None, None, [element], property_set)
       
    i = i + 1


################################################################
################################################################ Calculate mass of elements and generates info for the excel sheet
################################################################


# The following loop goes through eah storey and collets its amount of strutural elements
# and their volumes and newly assigned density in order to calulate the weight of these structural elements at each storey
# The volumes of the storeys are listed in the following order: 
# [EK_Kælder, ES_Stue, E1_1. Sal, E2_2. Sal, E3_3. Sal, E4_4. Sal]

print('\nPlease have patient, while the geometry and loads are being programed. This will take a few seconds.')

beam_geometry = []
mass_beams = []
countbeams = []
column_geometry = []
mass_columns = []
countcolumns = []
slab_geometry = []
mass_slabs = []
countslabs = []


# Runs through the elements at each floor level and calculates the total volume and mass of each group of elements 

i = 0

for x in storey:
    
    # Defines the considered floor level
    st = storey[i].LongName


    # Computes a loop for each of the element groups that sums up the number of elements and total mass at the consindered floor level    
    
    # Beams
    
    p = 0
    M = 0
    c = 0

    for x in all_beams:

        # Locates the storey of the element
        container = ifcopenshell.util.element.get_container(x)
        loc = container.Name
        
        
        # Check if the storey of the element matches the current considered floor
        if st == loc:          
                        
            # Defines propertysets of element
            qpset = ifcopenshell.util.element.get_psets(x)['Qto_BeamBaseQuantities']
            vpset = ifcopenshell.util.element.get_psets(x)['Pset_MaterialValues']
        
        
            # Computes mass of element
            if type(vpset['Density']) == int or type(vpset['Density']) == float:
                Mass = round(qpset['NetVolume'] * vpset['Density'],2)
            else:
                # If no density is assigned the mass is noted as 'not defined'
                Mass = 'Not defined'
                
   
            # Computes a list containg geometry and mass related information and append to list
            b_geo = [loc, beam_names[p], beam_materials[p], qpset['Length'], qpset['CrossSectionArea'], qpset['NetVolume'],vpset['Density'],Mass]
            beam_geometry.append(b_geo)            
          
           
            if type(Mass) == int or type(Mass) == float:
                # Sum up mass for elements at floor
                M = M+Mass
                c = c+1
    
        p=p+1
    
    # The data is collected and added to the list
    countbeams.append(c)
    mass_beams.append(M)
    
    
    
    # Columns - corresponding to beams
    
    p = 0
    M = 0
    c = 0
    
    for x in all_columns:
        container = ifcopenshell.util.element.get_container(x)
        loc = container.Name
        
        if st == loc:
                    
            qpset = ifcopenshell.util.element.get_psets(x)['Qto_ColumnBaseQuantities']
            vpset = ifcopenshell.util.element.get_psets(x)['Pset_MaterialValues']
        
            if type(vpset['Density']) == int or type(vpset['Density']) == float:
                Mass = round(qpset['NetVolume'] * vpset['Density'],2)
            else:
                Mass = 'Not defined'
        
            b_geo = [loc, column_names[p], column_materials[p], qpset['Length'], qpset['CrossSectionArea'], qpset['NetVolume'],vpset['Density'],Mass]
            column_geometry.append(b_geo)
        

            if type(Mass) == int or type(Mass) == float:
                M = M+Mass
                c = c+1
        p=p+1
        
    countcolumns.append(c)
    mass_columns.append(M)
    
    
    
    # Slabs - corresponding to #beams
    
    p = 0
    M = 0
    c = 0
    
    for x in all_slabs:

        container = ifcopenshell.util.element.get_container(x)
        loc = container.Name

        if st == loc:
                        
            qpset = ifcopenshell.util.element.get_psets(x)['Qto_SlabBaseQuantities']
            vpset = ifcopenshell.util.element.get_psets(x)['Pset_MaterialValues']
        
            if type(vpset['Density']) == int or type(vpset['Density']) == float:
                Mass = round(qpset['NetVolume'] * vpset['Density'],2)
            else:
                Mass = 'Not defined'
            
            b_geo = [loc, slab_names[p], slab_materials[p], qpset['Width'], qpset['Length'], qpset['NetArea'], qpset['NetVolume'],vpset['Density'],Mass]
            slab_geometry.append(b_geo)
        

            if type(Mass) == int or type(Mass) == float:
                M = M+Mass
                c = c+1
        p=p+1
    
    countslabs.append(c)
    mass_slabs.append(M)

    i=i+1
    

################################################################
################################################################ Exports to excel
################################################################

print('\nThe script will export data on the structural elements to an excel file, which will be saved in same location as the workbook.\nMoreover, the script saves a modified ifcmodel with the newly assigned propertysets.\n')


# Defines the data for excel. Uses DataFrame design

beam_geometry = list(map(list, zip(*beam_geometry)))
column_geometry = list(map(list, zip(*column_geometry)))
slab_geometry = list(map(list, zip(*slab_geometry)))


# Defines it in a list for an overview of the number and mass per floor level.
dataset = []
i = 0
for x in floor_array:
    data = [floor_array[i], countbeams[i], mass_beams[i], countcolumns[i], mass_columns[i], countslabs[i], mass_slabs[i]]
    dataset.append(data)
    i=i+1

# Transform the arrangement of the data to columns
dataset = list(map(list, zip(*dataset)))


# Computes the sheets for the excel file and defines the name and belonging data for each columns

B = pd.DataFrame({'Location':beam_geometry[0], 'Type':beam_geometry[1], 'Material':beam_geometry[2], 'Length [mm]':beam_geometry[3], 'CrossSectionArea [m^2]':beam_geometry[4], 'Volume [m^3]':beam_geometry[5], 'Density [kg/m^3]':beam_geometry[6], 'Mass [kg]':beam_geometry[7]})
C = pd.DataFrame({'Location':column_geometry[0], 'Type':column_geometry[1], 'Material':column_geometry[2], 'Length [mm]':column_geometry[3], 'CrossSectionArea [m^2]':column_geometry[4], 'Volume [m^3]':column_geometry[5], 'Density [kg/m^3]':column_geometry[6], 'Mass [kg]':column_geometry[7]})
S = pd.DataFrame({'Location':slab_geometry[0], 'Type':slab_geometry[1], 'Material':slab_geometry[2], 'Width [mm]':slab_geometry[3], 'Length [mm]':slab_geometry[4], 'Area [m^2]':slab_geometry[5], 'Volume [m^3]':slab_geometry[6], 'Density [kg/m^3]':slab_geometry[7], 'Mass [kg]':slab_geometry[8]})
D = pd.DataFrame({'ETAGE': dataset[0], 'Number of beams': dataset[1], 'Mass of beams [kg]': dataset[2], 'Number of columns': dataset[3], 'Mass of colums [kg]': dataset[4], 'Number of slabs': dataset[5], 'Mass of slabs [kg]': dataset[6], 'Total self-weight [kg]': ''})


# Defines path for excel file. Is saved at the same location of the workbook
excel_file_path = Path.joinpath(Path(bpy.context.space_data.text.filepath).parent, 'output').with_suffix('.xlsx')


# Writes the excel file in give path
writer = pd.ExcelWriter(excel_file_path)

B.to_excel(writer, sheet_name = 'Beams', index = False)
C.to_excel(writer, sheet_name = 'Columns', index = False)
S.to_excel(writer, sheet_name = 'Slabs', index = False)
D.to_excel(writer, sheet_name = 'Self-weight at storeys', index = False)


# Saves the file
writer._save()


################################################################
################################################################ Export ifc file
################################################################

# File path for new ifc model
model_file_path = Path.joinpath(Path(bpy.context.space_data.text.filepath).parent, 'model', 'my_ifcfile').with_suffix('.ifc')

# Saves the modified model 
model.write(model_file_path)

print('\nThe path of the excel file is,\n',excel_file_path, '\nThe path of the modified ifc model is,\n',model_file_path)


