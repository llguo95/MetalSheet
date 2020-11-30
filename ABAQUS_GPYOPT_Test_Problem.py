# -*- coding: mbcs -*-
from part import *
from material import *
from section import *
from assembly import *
from step import *
from interaction import *
from load import *
from mesh import *
from optimization import *
from job import *
from sketch import *
from visualization import *
from connectorBehavior import *

folder_path = os.getcwd()

Rtxtpath = "{}/Rvalue.txt".format(folder_path)
htxtpath = "{}/hvalue.txt".format(folder_path)

R=float(open(Rtxtpath, "r").read().strip())
h=float(open(htxtpath, "r").read().strip())
# 0.1<h<0.3
# 0.1<R<0.2
# pi*R*R+0.8*h>0.25
# minimize output

mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=200.0)
mdb.models['Model-1'].sketches['__profile__'].rectangle(point1=(0.0, 0.0), 
    point2=(1.0, 1.0)) 
mdb.models['Model-1'].sketches['__profile__'].rectangle(point1=(0.1, 0.1), 
    point2=(0.9, 0.1+h))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(
    0.3, 0.7), point1=(0.3, 0.7+R))
mdb.models['Model-1'].Part(dimensionality=THREE_D, name='Base_Model', type=
    DEFORMABLE_BODY)
mdb.models['Model-1'].parts['Base_Model'].BaseShell(sketch=
    mdb.models['Model-1'].sketches['__profile__'])
del mdb.models['Model-1'].sketches['__profile__']
mdb.models['Model-1'].Material(name='Steel')
mdb.models['Model-1'].materials['Steel'].Elastic(table=((200000000000.0, 0.3), 
    ))
mdb.models['Model-1'].HomogeneousShellSection(idealization=NO_IDEALIZATION, 
    integrationRule=SIMPSON, material='Steel', name='Sec_2mm_thick', 
    nodalThicknessField='', numIntPts=5, poissonDefinition=DEFAULT, 
    preIntegrate=OFF, temperature=GRADIENT, thickness=0.002, thicknessField='', 
    thicknessModulus=None, thicknessType=UNIFORM, useDensity=OFF)
mdb.models['Model-1'].parts['Base_Model'].Set(faces=
    mdb.models['Model-1'].parts['Base_Model'].faces.getSequenceFromMask((
    '[#1 ]', ), ), name='Set_Whole_Volume')
mdb.models['Model-1'].parts['Base_Model'].SectionAssignment(offset=0.0, 
    offsetField='', offsetType=MIDDLE_SURFACE, region=
    mdb.models['Model-1'].parts['Base_Model'].sets['Set_Whole_Volume'], 
    sectionName='Sec_2mm_thick', thicknessAssignment=FROM_SECTION)
mdb.models['Model-1'].rootAssembly.DatumCsysByDefault(CARTESIAN)
mdb.models['Model-1'].rootAssembly.Instance(dependent=ON, name='Base_Model-1', 
    part=mdb.models['Model-1'].parts['Base_Model'])
mdb.models['Model-1'].StaticStep(name='Step_Static_Aanalysis', previous=
    'Initial')
mdb.models['Model-1'].rootAssembly.Set(edges=
    mdb.models['Model-1'].rootAssembly.instances['Base_Model-1'].edges.getSequenceFromMask(
    ('[#120 ]', ), ), name='Set-1')
mdb.models['Model-1'].EncastreBC(createStepName='Step_Static_Aanalysis', 
    localCsys=None, name='Boundary_Condition', region=
    mdb.models['Model-1'].rootAssembly.sets['Set-1'])
mdb.models['Model-1'].rootAssembly.Set(name='Tip', vertices=
    mdb.models['Model-1'].rootAssembly.instances['Base_Model-1'].vertices.getSequenceFromMask(
    ('[#80 ]', ), ))
mdb.models['Model-1'].ConcentratedForce(cf3=1.0, createStepName=
    'Step_Static_Aanalysis', distributionType=UNIFORM, field='', localCsys=None
    , name='Tip_Force', region=mdb.models['Model-1'].rootAssembly.sets['Tip'])
mdb.models['Model-1'].parts['Base_Model'].seedPart(deviationFactor=0.1, 
    minSizeFactor=0.1, size=0.05)
mdb.models['Model-1'].parts['Base_Model'].generateMesh()
mdb.models['Model-1'].rootAssembly.regenerate()
mdb.Job(atTime=None, contactPrint=OFF, description='', echoPrint=OFF, 
    explicitPrecision=SINGLE, getMemoryFromAnalysis=True, historyPrint=OFF, 
    memory=90, memoryUnits=PERCENTAGE, model='Model-1', modelPrint=OFF, 
    multiprocessingMode=DEFAULT, name='Job_Simulation', nodalOutputPrecision=
    SINGLE, numCpus=1, numGPUs=0, queue=None, resultsFormat=ODB, scratch='', 
    type=ANALYSIS, userSubroutine='', waitHours=0, waitMinutes=0)
mdb.models.changeKey(fromName='Model-1', toName='Test_Model')
del mdb.jobs['Job_Simulation']
mdb.Job(atTime=None, contactPrint=OFF, description='', echoPrint=OFF, 
    explicitPrecision=SINGLE, getMemoryFromAnalysis=True, historyPrint=OFF, 
    memory=90, memoryUnits=PERCENTAGE, model='Test_Model', modelPrint=OFF, 
    multiprocessingMode=DEFAULT, name='Job_Simulation', nodalOutputPrecision=
    SINGLE, numCpus=1, numGPUs=0, queue=None, resultsFormat=ODB, scratch='', 
    type=ANALYSIS, userSubroutine='', waitHours=0, waitMinutes=0)
mdb.jobs['Job_Simulation'].submit(consistencyChecking=OFF)


from odbAccess import *
odb = openOdb(path='Job_Simulation.odb')
step1 = odb.steps['Step_Static_Aanalysis']
frame1 = step1.frames[-1]
disps1 = frame1.fieldOutputs['U']
nodes = odb.rootAssembly.nodeSets['TIP']
disp1_at_nodes = disps1.getSubset(region=nodes)
outputFile = open('Displacement_of_tip.txt','w')

for dispVal in disp1_at_nodes.values:
    outputFile.write('%18.11E  ' % (dispVal.data[2]))
    
outputFile.close()



# Save by dongil on 2020_03_23-17.53.49; build 2018 2017_11_07-18.21.41 127140
# Save by dongil on 2020_03_23-17.53.51; build 2018 2017_11_07-18.21.41 127140

