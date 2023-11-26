## **41943 A4: OpenBIM Champion**

#### *Group 15: (s203634 & s203595)*

*Please check out our guided tutorial of how to use our tool: "HowToRun.pdf" or watch the tutorial video through the link: https://www.youtube.com/watch?v=vmxP8bfCp9U*

**The goal of our tool** is to support the user to verify the structural load capacity. 

This tool is thereby intended for structural engineers, and requires a structural analysis, why we are particularly interested in structural components which are load bearing. 

To this knowledge on loads cases and structural integrity have been used.

- In the script IFC concepts of extracting informations related to structural components have been used, as well as concepts of loading models, using user-input, updating the propertysets of the ifc-model, and exporting information to excel files. 

#### **Use cases**

The input data for the use case is an IFC model. 

The tool requires, that geometry assigned to the structural elements have been loaded into the IFC model beforehand (see HowToRun tutorial).

The use case is to calculate the self-weight of the structural construction, in order to verify the building for load capacity. 

The tool extracts information of the structural elements in the model, and with user inputs it imports new properysets of material parameters. Moreover, it calculates the self weight of the elements.

The process section is to add information regarding the load capacity of the structural elements, and thereby check the different load cases for capacity. Also, other load cases than just self-load, such as imposed loads, seismic load and snow loads etc. 

Other uses cases waiting for our use case to be completed could be use cases determining the price of the building, or shop lists. 

#### **IDM diagram**

The idea of the use case is shown in the diagram below. The highlighted green boxes are the ones which are developed in the tool so far. 
The purpose of this diagram is to show the goal of the tool, while focusing on a more narrow area. 

<img src="https://github.com/frejahbarkler/41934_GR15_A3/blob/main/BPMN.svg">

#### **Input**

The input data for the model is chosen to be a user input throught the terminal. The input values are related to the materials and elements. 

The process section here, is to add even more input data regarding the strength of the elements and design parameters, in order to check if the construction can be verified. 

#### **Output**

The output data is an excel sheet named *my_output* and an ifc file named *my_ifcfile*. The excel file will include an overview of all the structural elements, and thereby the self load of each component. The sheet will also include a list containing the structural elements located on each floor, and the weight of these. The ifc file includes an corresponding ifc model with updated propertysets for the structural materials.



#### **Value of the tool**

The societal value of the tool is to make it easier for the structural engineers to get an overview of the structure of an architectural model. Also, to check the structure for load capacity. The tool will speed up the process for the structural engineer, to get an overview before going into deeper and more detailed calculations. 

The business value of the model is to provide indicative calculations, which will benefit e.g. quick estimates on costs of materials.
