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
for x in all_elements:
    element_i = all_elements[i]
    if ifcopenshell.util.element.get_material(element_i) == None:
       material = None   
    else:
        material = ifcopenshell.util.element.get_material(element_i)[0]
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
    print('   ',materials[i])
    i = i + 1


print("\nMore detailed informations follows on the storeys and considered structural elements.")


################################################################
################################################################STOREYS
################################################################
print("\n------------ STOREYS ---------------\n")

#Prints the nymber of storeys in the model
print('\033[4m' + "The name of the floors occurring in the model:" + '\033[0m')


# Alle etager listes op og printes
floor_array = []
floor_number = []
i = 0
for LongName in storey:
    name = storey[i].LongName
    print('   Floor',i, ":", storey[i].LongName)
    floor_array.append(name)
    floor_number.append(i)
    i=i+1
    if i == len(storey):
        break


################################################################
################################################################ BEAMS
################################################################
print("\n------------ BEAMS ---------------\n")


# Counts all beams and prints them
print('There are', len(all_beams), 'beams in the model')

beam_names = []
beam_spans = []
beam_materials = []
beam_info = []
for i in all_beams:
    type_i = ifcopenshell.util.element.get_type(i)
    beam_names.append(type_i[2])
    
    material = ifcopenshell.util.element.get_material(type_i)[0]
    beam_materials.append(material)

    pset = ifcopenshell.util.element.get_psets(i)
    pset_common = pset['Pset_BeamCommon']
    span = round(pset_common['Span'],2)
    beam_spans.append(span)
    

    info = (type_i [2], material, span)
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
    print('   ',y,':', x)

print('\n\033[4m' + "The occurrence of each material assigned to a beam:" + '\033[0m')
for x, y in beam_material_occurrence.items():
    print('   ',y,':', x)

print('\n\033[4m' + "The minimum and maximum beam spans obtained:" + '\033[0m')
print('   ',"Minimum span: ", min(beam_spans))
print('   ',"Maximum span: ", max(beam_spans))



################################################################
################################################################ COLUMNS
################################################################
print("\n------------ COLUMNS ---------------\n")


# Counts all columns and prints them
print('There are', len(all_columns), 'columns in the model')


# Creates a list of all columns in the model by their names
column_names = []
column_materials = []
column_info = []
for i in all_columns:
    type_i = ifcopenshell.util.element.get_type(i)
    column_names.append(type_i[2])
    
    material = ifcopenshell.util.element.get_material(type_i)[0]
    column_materials.append(material)
    
    info = (type_i [2], material)
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
    print('   ',y,':', x)

print('\n\033[4m' + "The occurrence of each material assigned to a column:" + '\033[0m')
for x, y in column_material_occurrence.items():
    print('   ',y,':', x)


################################################################
################################################################ SLABS
################################################################
print("\n------------ SLABS ---------------\n")


# Counts all slabs and prints them
print('There are', len(all_slabs), 'slabs in the model')

# Creates a list of all slabs in the model by their names
slab_names = []
slab_materials = []
slab_info = []
for i in all_slabs:
    type_i = ifcopenshell.util.element.get_type(i)
    slab_names.append(type_i[2])
    
    if ifcopenshell.util.element.get_material(type_i) == None:
       material = None   
    else:
        material = ifcopenshell.util.element.get_material(type_i)[0]       
    slab_materials.append(material)
    
    info = (type_i [2], material)
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
    print('   ',y,':', x)

print('\n\033[4m' + "The occurrence of each material assigned to a slab:" + '\033[0m')
for x, y in slab_material_occurrence.items():
    print('   ',y,':', x)


###########################################################
########################################################### Assign densities
###########################################################


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

# Loop for given options
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
                
                # Controls if the actual material is pre-defined
                if x == None:
                    m = '5'
                elif 'stål' in str.lower(x):
                    m = '1'
                elif 'beton' in str.lower(x):
                    m = '2'
                elif 'isolering' in str.lower(x):
                    m = '3'
                # User input if material is not pre-defined
                else:
                    m = input ('Please assign a material from the list below to the the ifcmaterial of "' + x + '". \n  1. Steel \n  2. Concrete \n  3. Insulation \n  4. Other \n  5. Unkown \nType the number of the belonging material:')
                
                # Steel
                if m == '1':
                    print('\nThe ifcmaterial "', x, '" have been assigned to steel. \nIt is assumed to be of the type construction steel, which is why a number of characteristic material parameters are assigned in advance.')
                    
                    # Material values 
                    rho = 7850
                    E = 0.21e6
                    v = 0.3
                    G = round(E / (2*(1+v)),2)
                    
                    # Yield stress & tensile stress
                    print('.........................\nThe strenght of,', x, ' is depended on the assigned strenght class and the nominal thickness of the element.')
                    
                        # userinput: thickness
                    t = 0
                    
                    print('\nThe thickness must not exceed 80 mm and must be given in [mm], however in relation to the strength class we differ the options listed below,\n  1. <=40 [mm] \n  2.  >40 [mm]')
                        
                    while t == 0:
                        t = input('\nPlease enter the number that alligns with the thickness you wish to use in the calculations:')
                        if t == '1' or t == '2':
                            None
                        else:
                            print('Error: The input was either not numeric or above 80 mm. Please try again')
                            t = 0
                    
                    print('\nThe streght classes considered are in agreement with the standard of "EN 10025-2" and listed below.\n  1. S235\n  2. S275\n  3. S355\n  4. S450')
                        # userinput: strength class
                    c = 0
                    while c == 0:
                        
                        c = input('\nPlease enter the number of the strenght class you wish to use in the calculations:')
                        
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
                            print("Error: Please choose a number from the list")
                            c = 0
                                    
                # Concrete
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
                        
                        # user inputs
                        c = input('\nPlease enter the number of the strenght class you wish to use in the calculations:')
                        
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
                            print("Error: Please choose a number from the list")
                            c = 0
                        

                # Insulation 
                elif m == '3':
                    print('........................\nThe ifcmaterial "', x, '" have been assigned to insulation.\nThe density is depended on the type of insulation. Three categories have been established and listed below each with its own assumed density.\n  1. Light weighted insulation \n  2. Medium weighted insulation \n  3. Heavy weighted insulation ')
                    
                    # userinput: Insulation type
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
                            print('Error: The input was not numeric. Please try again')
                            rho = 0
                
                elif m == '5':
                    print('.........................\nThe material ',x,' is unknown. No properties will be assigned')
                    
                    
                else:
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

        for x in materials:
            rho = ''
            E = ''
            G = ''
            v = ''
            fy = ''
            fu = ''
            fck = ''
            fctm = ''
            
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
        print('Error: Please type a number from the list')
        i = 0

        

# Assign the largest density value to none defined materials
#int_densities = []
#for i in range(len(materials)):
#    if materials[i] != None:
#        int_densities.append(densities[i])
#for i in range(len(materials)):
#    if densities[i] == "not defined":
#        densities[i] = max(int_densities)

#print("\nFor elements of which the material is assigned 'None' the density is with respect the structure, conservatively assigned the largest density appearing in the model. The final list of densities assigned to the materials are the following,")

#dict_densities = {}
#for i in range(len(densities)):
#    dict_densities[materials[i]] = densities[i]

#print('   ',materials[i], ':', densities[i],'\n')




###########################################################
########################################################### Modyfies propertyset
###########################################################

# Modifies propertyset 
i = 0
for element in all_elements:
    # Finds the index in the list of materials corresponding to the material of the i element
    #material_index = materials.index(all_materials[i])
    # Assign the density corresponding to the material index to
    #density_value = densities[material_index]
    property_values = []
    material = all_materials[i]
    
    
    # Creates property value set for materials of which a material parameter is assigned.
    value = dict_densities[material]
    if type(value) == int or type(value) == float:
        #Computes an additional property set and loads it in the existing set of propertysets.  
        a = model.createIfcPropertySingleValue("Density", "Description of My Own Property", model.create_entity("IfcReal", value), None)
        property_values.append(a)
    else:
        a = model.createIfcPropertySingleValue("Density", "Description of My Own Property", model.create_entity("IfcText", value), None)
        property_values.append(a)
        
    value = dict_emodulus[material]    
    if type(value) == int or type(value) == float:
        #Computes an additional property set and loads it in the existing set of propertysets.  
        a = model.createIfcPropertySingleValue("Modulus of elasticity", "Description of My Own Property", model.create_entity("IfcReal", value), None)
        property_values.append(a)
    
    value = dict_gmodulus[material]
    if type(value) == int or type(value) == float:
        #Computes an additional property set and loads it in the existing set of propertysets.  
        a = model.createIfcPropertySingleValue("Shear modulus", "Description of My Own Property", model.create_entity("IfcReal", value), None)
        property_values.append(a)
   
    value = dict_poissons[material]
    if type(value) == int or type(value) == float:
        #Computes an additional property set and loads it in the existing set of propertysets.  
        a = model.createIfcPropertySingleValue("Poisson's ratio", "Description of My Own Property", model.create_entity("IfcReal", value), None)
        property_values.append(a)
     
    value = dict_fy[material]
    if type(value) == int or type(value) == float:
        #Computes an additional property set and loads it in the existing set of propertysets.  
        a = model.createIfcPropertySingleValue("Yield stress", "Description of My Own Property", model.create_entity("IfcReal", value), None)
        property_values.append(a)
     
    value = dict_fu[material]
    if type(value) == int or type(value) == float:
        #Computes an additional property set and loads it in the existing set of propertysets.  
        a = model.createIfcPropertySingleValue("Tensile stress", "Description of My Own Property", model.create_entity("IfcReal", value), None)
        property_values.append(a)
        
    value = dict_fck[material]
    if type(value) == int or type(value) == float:
        #Computes an additional property set and loads it in the existing set of propertysets.  
        a = model.createIfcPropertySingleValue("Compressive stress", "Description of My Own Property", model.create_entity("IfcReal", value), None)
        property_values.append(a)
    
    value = dict_fctm[material]
    if type(value) == int or type(value) == float:
        #Computes an additional property set and loads it in the existing set of propertysets.  
        a = model.createIfcPropertySingleValue("Tensile stress", "Description of My Own Property", model.create_entity("IfcReal", value), None)
        property_values.append(a)
    
     
    #print(property_values)   
    property_set = model.createIfcPropertySet(element.GlobalId, element.OwnerHistory, "Pset_MaterialValues", None, property_values)
    model.createIfcRelDefinesByProperties(element.GlobalId, element.OwnerHistory, None, None, [element], property_set)
       
       
    #print(ifcopenshell.util.element.get_psets(element)['Pset_MaterialValues'])
    i = i + 1

#print(ifcopenshell.util.element.get_psets(all_beams[3])['Pset_MaterialValues'])

################################################################
################################################################ Creation of structed lists with Load related properties (geometry, density, mass) for each structural element
################################################################ info for the excel sheet
################################################################
# The following loop goes through eah storey and collets its amount of strutural elements
# and their volumes and newly assigned density in order to calulate the weight of these structural elements at each storey
# The volumes of the storeys are listed in the following order: 
# [EK_Kælder, ES_Stue, E1_1. Sal, E2_2. Sal, E3_3. Sal, E4_4. Sal]

print('\nPlease have patient, while the geometry and loads are being programed. This might take a while.')

mass_beams = []
countbeams = []
mass_columns = []
countcolumns = []
mass_slabs = []
countslabs = []

# First, a loop goes through one storey at a time:
i = 0
for x in storey:
    #defines the name of the story that we're at
    st = storey[i].LongName

    ########################## BEAM ##########################
    # Next, a loop that counts the amount of beams at storey[i]
    # The loop also adds the total mass of beams at storey[i] to a list
    p = 0
    M = 0
    c = 0
    # Creates a list containing all_beams and then appending material and geometry to each beam
    beam_geometry = []
    for x in all_beams:
        # Finds element[p]
        element = all_beams[p]
        # Finds the storey name, that element[p] is located at
        container = ifcopenshell.util.element.get_container(element)
        loc = container.Name
        
        # Propertysets of element
        qpset = ifcopenshell.util.element.get_psets(element)['Qto_BeamBaseQuantities']
        vpset = ifcopenshell.util.element.get_psets(element)['Pset_MaterialValues']
        
        if type(vpset['Density']) == int or type(vpset['Density']) == float:
            Mass = round(qpset['NetVolume'] * vpset['Density'],2)
        else:
            Mass = 'Not defined'
        
        # Computes a list containg geometry and mass related information and append to list
        b_geo = [loc, beam_names[p], beam_materials[p], qpset['Length'], qpset['CrossSectionArea'], qpset['NetVolume'],vpset['Density'],Mass]
        beam_geometry.append(b_geo)
            
        # If element[p] is located at the same storey as storey[i], we'll add it to the list
        if st == loc:
            if type(Mass) == int or type(Mass) == float:
                M = M+Mass
                c = c+1
        p=p+1
    
    # Hereby, the data is collected and added to the list before it goes to the next storey
    countbeams.append(c)
    mass_beams.append(M)
    
    
    ########################## COLUMN ##########################
    # This is the same loop as before, just with columns
    p = 0
    M = 0
    c = 0
    column_geometry = []
    for x in all_columns:
        element = all_columns[p]
        container = ifcopenshell.util.element.get_container(element)
        loc = container.Name
        
        qpset = ifcopenshell.util.element.get_psets(element)['Qto_ColumnBaseQuantities']
        vpset = ifcopenshell.util.element.get_psets(element)['Pset_MaterialValues']
        
        if type(vpset['Density']) == int or type(vpset['Density']) == float:
            Mass = round(qpset['NetVolume'] * vpset['Density'],2)
        else:
            Mass = 'Not defined'
        
        # Computes a list containg geometry and mass related information and append to list
        b_geo = [loc, column_names[p], column_materials[p], qpset['Length'], qpset['CrossSectionArea'], qpset['NetVolume'],vpset['Density'],Mass]
        column_geometry.append(b_geo)
        
        
        if st == loc:
            if type(Mass) == int or type(Mass) == float:
                M = M+Mass
                c = c+1
        p=p+1
        
    countcolumns.append(c)
    mass_columns.append(M)
    
    ########################## SLAB ##########################  
    # This is the same loop as before, just with slabs
    p = 0
    M = 0
    c = 0
    # Creates a list containing all_slabs and then appending material and geometry to each slab
    slab_geometry = []
    for x in all_slabs:
        element = all_slabs[p]
        container = ifcopenshell.util.element.get_container(element)
        loc = container.Name
        
        # gets the slab quantities
        qpset = ifcopenshell.util.element.get_psets(element)['Qto_SlabBaseQuantities']
        vpset = ifcopenshell.util.element.get_psets(element)['Pset_MaterialValues']
        
        if type(vpset['Density']) == int or type(vpset['Density']) == float:
            Mass = round(qpset['NetVolume'] * vpset['Density'],2)
        else:
            Mass = 'Not defined'
            
        # Computes a list containg geometry and mass related information and append to list
        b_geo = [loc, slab_names[p], slab_materials[p], qpset['Width'], qpset['Length'], qpset['NetArea'], qpset['NetVolume'],vpset['Density'],Mass]
        slab_geometry.append(b_geo)
        
        
        if st == loc:
            if type(Mass) == int or type(Mass) == float:
                M = M+Mass
                c = c+1
        p=p+1
    
    countslabs.append(c)
    mass_slabs.append(M)

    i=i+1
    
################################################################
################################################################ Export to excel
################################################################


print('\nThe waiting time is over! \nThe script will export data on the structural elements to an excel file, which will be saved in same location as the workbook.\nMoreover, the script saves a modified ifcmodel with the newly assigned propertysets.\n')

import numpy as np
import pandas as pd

scheme = model.schema

#Defining the data for excel
#Using DataFrame design

beam_geometry = list(map(list, zip(*beam_geometry)))
column_geometry = list(map(list, zip(*column_geometry)))
slab_geometry = list(map(list, zip(*slab_geometry)))


dataset = []
i = 0
for x in floor_array:
    data = [floor_array[i], countbeams[i], mass_beams[i], countcolumns[i], mass_columns[i], countslabs[i], mass_slabs[i]]
    dataset.append(data)
    i=i+1

dataset = list(map(list, zip(*dataset)))

B = pd.DataFrame({'Location':beam_geometry[0], 'Type':beam_geometry[1], 'Material':beam_geometry[2], 'Length [mm]':beam_geometry[3], 'CrossSectionArea [m^2]':beam_geometry[4], 'Volume [m^3]':beam_geometry[5], 'Density [kg/m^3]':beam_geometry[6], 'Mass [kg]':beam_geometry[7]})
C = pd.DataFrame({'Location':column_geometry[0], 'Type':column_geometry[1], 'Material':column_geometry[2], 'Length [mm]':column_geometry[3], 'CrossSectionArea [m^2]':column_geometry[4], 'Volume [m^3]':column_geometry[5], 'Density [kg/m^3]':column_geometry[6], 'Mass [kg]':column_geometry[7]})
S = pd.DataFrame({'Location':slab_geometry[0], 'Type':slab_geometry[1], 'Material':slab_geometry[2], 'Width [mm]':slab_geometry[3], 'Length [mm]':slab_geometry[4], 'Area [m^2]':slab_geometry[5], 'Volume [m^3]':slab_geometry[6], 'Density [kg/m^3]':slab_geometry[7], 'Mass [kg]':slab_geometry[8]})
D = pd.DataFrame({'ETAGE': dataset[0], 'Beams': dataset[1], 'Mass of beams [kg]': dataset[2], 'Columns': dataset[3], 'Mass of colums [kg]': dataset[4], 'Slabs': dataset[5], 'Mass of slabs [kg]': dataset[6], 'Total self-weight [kg]': ''})



#Saves the exel file at the same location of the workbook
excel_file_path = Path.joinpath(Path(bpy.context.space_data.text.filepath).parent, 'output').with_suffix('.xlsx')

#Writer will write the excel file
writer = pd.ExcelWriter(excel_file_path)


B.to_excel(writer, sheet_name = 'Beams', index = False)
C.to_excel(writer, sheet_name = 'Columns', index = False)
S.to_excel(writer, sheet_name = 'Slabs', index = False)
D.to_excel(writer, sheet_name = 'Self-weight at storeys', index = False)

#Saving the file
writer._save()

# File path for mew ifc model
model_file_path = Path.joinpath(Path(bpy.context.space_data.text.filepath).parent, 'model', 'my_ifcfile').with_suffix('.ifc')

# Saves the modified model 
model.write(model_file_path)

print('\nThe path of the excel file is,\n',excel_file_path, '\nThe path of the modified ifc model is,\n',model_file_path)


