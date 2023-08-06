import requests
import json
import ast

#does this user have a differnt download url?
# def download(name,location,token):
#     url="https://studiobitonti.appspot.com/storage/download?name=%s&t=%s" % (name,token)
#     print(url)
#     #write content
#     with open(url, 'wb') as f:
#         f.write(r.content)

def cylindricalProjection(target,resolution,height,output,center,range,startDir,rotateAxis,token):
    """
    The cylindrical projection function wraps a cylindrical mesh around the input mesh. It can used to shrink wrap the mesh and create a new cleaner and refined mesh. The target and resolution can basic inputs required, whereas advance inputs include defining a center, and axis for the projection. This projection is made using a cylindrical base.

    Target: (string) The uploaded .Obj target to be projected on.
    Resolution: (int) Is the number cells in U and V direction.
    Height:(float)  Height of cylinder to be projected.
    File Name:(string)  Name of the resultant file for the surface lattice.
    """
    url ="https://studiobitonti.appspot.com/cylindricalProjection"
    payload = {"target":target,"center":center,"resolution":resolution,"range":range,"rotateAxis":rotateAxis,"start_dir":startDir,"height":height,"filename":output,"t":token}
    print(json.dumps(payload))
    r = requests.post(url,json=payload)
    return r.text

def sphericalProjection(target,center,resolution,range,rotateAxis,output,token):
    """
    The spherical projection function works by wraps a given mesh with a sphere either partially or whole in order to create a clean base surface from the input. The target and resolution can basic inputs required, whereas advance inputs include defining a center, and axis for the projection. This projection is made using a spherical base.

    Target:(String) The uploaded .Obj target to be projected on.
    Resolution: (int) Is the number cells in U and V direction.
    File Name:(string)  Name of the resultant file for the surface lattice.
    """
    url ="https://studiobitonti.appspot.com/sphericalProjection"
    payload = {"target":target,"center":center,"resolution":resolution,"range":range,"rotateAxis":rotateAxis,"filename":output,"t":token}
    print(json.dumps(payload))
    r = requests.post(url,json=payload)
    return r.text

def planarProjection(target,center,direction,size,resolution,output,token):
    """
    The plane projection function wraps a given mesh input by projecting a place on to it from the specified direction. This function can be used to patch holes, create a new draped mesh over multiple objects, etc. The required inputs include the target file name, center of the object, direction of projection, size of the plane and its resolution.

    Target:(String) The uploaded .Obj target to be projected on.
    Center:(array) 3D coordinate of projection center, by default [0,0,0].
    Direction:(vector) 3D vector defining, the direction where projection starts, by default [1,0,0].
    Size:(2D vector)  Is the [U,V] input defining the size of the projected plane.
    Resolution:(int) Is the number cells in U and V direction.
    File Name:(string)  Name of the resultant file for the surface lattice.
    """
    url ="https://studiobitonti.appspot.com/planeProjection"
    payload = {"target":target,"center":center,"direction": direction,"size":size,"resolution":resolution,"filename":output,"t":token}
    print(json.dumps(payload))
    r = requests.post(url,json=payload)
    return r.text

def boolean(input1,input2,output,operation,token): #operations are Union, Interset and Difference
    """
    This is the Doc stings located at the top of the file.

    Input1:(string) Name of first .obj component file uploaded to storage.
    Input2:(string) Name of second .obj component file uploaded to storage.
    Output:(string) Result file name for the boolean operation in .obj format.
    Operation:(string) Choose one from union,difference and intersection.
    """
    url ="https://studiobitonti.appspot.com/boolean"
    payload = {"input1":input1,"input2":input2,"operation":operation,"output":output,"t":token}
    print(json.dumps(payload))
    r = requests.post(url,json=payload)
    return r.text

def convexHull(a,token):
    """
    The convex hull function creates a boundary around the outermost laying points. It is used to get a sense of size of the point cloud field.
    Input is an array
    """
    url ="https://studiobitonti.appspot.com/convexHull"
    payload = {"points":a,"t":token}
    print(json.dumps(payload))
    r = requests.post(url,json=payload)
    return r.text

def voronoi(a,token):
    """
    The voronoi function creates partitions based on distance between the input points.
    Input is an array
    """
    url ="https://studiobitonti.appspot.com/voronoi"
    payload = {"points":a,"t":token}
    print(json.dumps(payload))
    r = requests.post(url,json=payload)
    return r.text

def delaunay(a,token):
    """
    The delaunay triangulation function creates triangular connections in 2D and 3D. The input is a point cloud array in any dimensions.
    Input is an array
    """
    url ="https://studiobitonti.appspot.com/delaunay"
    payload = {"points":a,"t":token}
    print(json.dumps(payload))
    r = requests.post(url,json=payload)
    return r.text

def blend(compA,compB,value,output,token):
    """
    The blend function takes two mesh objects with same topology and different vertices locations, then output a blended geometry given a value between 0 and 1.

    compA:(string)  name of component A obj file uploaded to storage
    compB:(String)  name of component B obj file uploaded to storage
    filename:(string) target output file name
    value:(float)  float between 0 and 1, the blend position between compA and compB
    """
    url ="https://studiobitonti.appspot.com/blend"
    payload = {"compA":compA,"compB":compB,"value":value,"filename":output,"t":token}
    print(json.dumps(payload))
    r = requests.post(url,json=payload)
    return r.text

#not working Li will check backend
def meshSplit(target,output,token):
    """
    The split mesh function breaks down the given mesh input into its component mesh parts.

    Target:(string)  Name of input .obj/.stl file uploaded to storage
    Filename:(string) Target output file name
    """
    url ="https://studiobitonti.appspot.com/meshSplit"
    payload = {"target":target,"filename":output,"t":token}
    print(json.dumps(payload))
    r = requests.post(url,json=payload)
    return r.text

def meshReduce(target,output,portion,token):
    """
    Reduce the number of faces of a mesh.

    target:(string) the name of the mesh you want to reduce
    output:(string) the name of the new mesh after reduction.
    portion:(float) the percentage you wish to reduce the mesh.
    """
    url ="https://studiobitonti.appspot.com/meshreduction"
    payload = {"target":target,"portion":portion,"filename":output,"t":token}
    print(json.dumps(payload))
    r = requests.post(url,json=payload)
    return r.text

def genLatticeUnit(case,chamfer,centerChamfer,bendIn,cBendIn,connectPt,output,token):
    """
    Case:(float) Is an integer value between 0 - 7,  defining different type of lattice units.
    Chamfer:(float) Is a float value between 0 to 0.5 defining the angle of chamfer of the corners.
    Center Chamfer:(float) Is a float value between 0 to 0.5 defining the angle of chamfer from the center.
    Bendln:(float) Is a float value between 0 and 1, defining angle bend of the lines.
    cBendln:(float)  Is a float value between 0 and 1,defining the central bend of the lines.
    Connect Pt:(float)  Is a float value between 0 and 1, defining the connection points.
    """
    url = "https://studiobitonti.appspot.com/latticeUnit"
    payload = {"case":case,"chamfer":chamfer,"centerChamfer":centerChamfer,"bendIn":bendIn,"cBendIn":cBendIn,"connectPt":connectPt,"filename":output,"t":token}
    print(json.dumps(payload))
    r = requests.post(url,json=payload)
    return r.text


def parseComponents(a):
    bodyMain=""
    for i in range(len(a)):
        body="{\"component\":\"%s\",\"attractor\":{\"point\":%s,\"range\":%s}}" % (a[i][0],a[i][1],a[i][2])
        if(i>0):
            bodyMain+=","+body
        else:
            bodyMain+=body
    final="\"blendTargets\":["+bodyMain+"]}"
    return final

def marchingCube(lines,resolution,memberThickness,filename,token):
    """
    The marching cubes function is used to create a mesh from the given line input. Is it used to create a thickness that can be defined by the user, as well as the resolution.

    Lines:(string) Is the uploaded .obj file containing lines to be meshed by Marching Cubes algorithm.
    Resolution:(int)  Is the integer value between from 64 to 600, defining the resolution of the meshing operation. Lower value gives a more coarse result, whereas a higher value gives out a more refined result.
    Member Thickness:(float)  Is a float value defining the radius of the line members being meshed.
    Filename:(string) Name of the resultant file of the meshed object.
    """
    url = "https://studiobitonti.appspot.com/marchingCube"
    payload = {"lines":lines,"resolution":resolution,"memberThickness":memberThickness,"filename":filename,"t":token}
    print(json.dumps(payload))
    r = requests.post(url,json=payload)
    return r.text

class volumeLattice:
    """
    This is for lattices that conform to volumes but do not change the shape of the lattice units.
    """
    def __init__(self): #set global variables
        #URL is always this.
        #self.url = "https://studiobitonti.appspot.com/stochasticLattice"
        self.url = "https://studiobitonti.appspot.com/volumeLattice"
        self.urlStochastic = "https://studiobitonti.appspot.com/stochasticLattice"
        #variables that need to be set by the user.
        self.poreSize=0.1
        self.volume=""
        self.output=""
        self.component="unit_1.obj"
        self.componentSize=1
        #attactors will be formated as an 2D array "["unit_0.obj", [0,0,0], 20], ["unit_1.obj", [4,36,22], 20]]"
        #default values are files included in sample repo.
        self.attractorSet=[["unit_0.obj", [0,0,0], 20], ["unit_1.obj", [4,36,22], 20]]

#functions for seting key variables
    #input an array with all the attractor information. [["unit_0.obj", [0,0,0], 20], ["unit_1.obj", [4,36,22], 20]]
    def setAttractor(self,a): #attractors are optional (blended lattices only)
        self.attractorSet=a
    #(string) Set the file name for the exported lattice structure
    def setOutput(self,output):#file name that you want to save out
        self.output=output
    #(String) set the volume you want to fill with the lattice
    def setVolume(self,volume):#base surface
        self.volume=volume
    #(float) For stochastic lattices only. This will be the miniumum pore size for the stochastic lasttice.
    def setPoreSize(self,pore):#pore size for stochastic Lattice
        self.poreSize=pore
    #(float) This is the size of the lattice grid. For one unit.
    def setComponentSize(self,cellHeight):#size of componet in a static or graded grid
        self.componentSize=cellHeight

#lattice generation functions

    def stochasticLatticeStatic(self,token):
        """
        The stochastic lattice function creates a randomly seeded lattice structure inside a given volume. The density can be controlled using the pore size.
        """
        payload = {"volume":self.volume,"poreSize":self.poreSize,"filename":self.output,"t":token}
        print(json.dumps(payload))
        #make post request
        r = requests.post(self.urlStochastic,json=payload)
        print(r.text)
        return r.text

    def volumeLatticeStatic(self,token):
        """
        The volume lattice function generates arrays of a given lattice structure across a volume in a parametric fashion. The input parameters take in a base component of the volume and a module to be arrayed. Other parameters like component size help define the size of the module which is arrayed.
        """
        payload = {"component":self.component,"volume":self.volume,"componentSize":self.componentSize,"filename":self.output,"t":token}
        print(json.dumps(payload))
        #make post request
        r = requests.post(self.url,json=payload)
        print(r.text)
        return r.text

    def volumeLatticeAttractor(self,token):
        """
        The volume lattice function generates arrays of a given lattice structure across a volume in a parametric fashion.
        This function is much like volumeLatticeStatic with the difference that it can also use an array of attractors to make blended structures.
        """
        #get attractor information
        att=parseComponents(self.attractorSet)
        payload = "{\"component\":\"%s\",\"volume\":\"%s\",\"componentSize\":%s,\"filename\": \"%s\",\"t\":\"%s\",%s" % (self.component,self.volume,self.componentSize,self.output,token,att)
        print(payload)
        #convert paylod to dictionary
        dict=ast.literal_eval(payload)
        #make post request
        r = requests.post(self.url,json=dict)
        print(r.text)
        return r.text

class surfaceLattice:
    """
    This class is for lattice that form their shapes to surfaces
    """
    def __init__(self): #set global variables
        """
        Initialize
        """
        #URL is always this.
        self.url = "https://studiobitonti.appspot.com/surfaceLattice"
        #Always True
        self.autoScale="true"
        self.ESIPLON=1
        self.bin="true"
        #variables that need to be set by the user.
        self.output = ""
        self.cellHeight=1
        #attactors will be formated as an 2D array [["unit_0.obj", [0,0,0], 20], ["unit_1.obj", [4,36,22], 20]]"
        #default values are files included in sample repo.
        self.attractorSet=[["unit_0.obj", [0,0,0], 20], ["unit_1.obj", [4,36,22], 20]]
        self.component="unit_1.obj"
        self.base="Base_Surface.obj"
        self.ceil="Ciel_CompB.obj"

#functions for seting key variables
    #pass in an array of attractors [["unit_0.obj", [0,0,0], 20], ["unit_1.obj", [4,36,22], 20]]
    def setAttractor(self,a): #attractors are optional (blended lattices only)
        self.attractorSet=a
    #(float) Set the bin value.
    def setBin(self,bin):
        self.bin=bin
    #(float) Epsilon is used to determin tolerances that define when two lattice cells are considered touching.
    def setEspilon(self,espilon):
        self.ESIPLON=espilon
    #(string) this is the name of the file that the function will output after it is computed.
    def setOutput(self,output):#file name that you want to save out
        self.output=output
    #(string) Define the base surface to populat lattices on. This will be a mesh with all 4 sided faces.
    def setSurface(self,base):#base surface
        self.base=base
    #(string) Define the second surface. Lattice units can be populated between two surfaces of differnt shape with the same topology.
    def setTopSurface(self,ceil):#Top surface
        self.ceil=ceil
    #(float) If you do not define a top surface you will need to define a constant height to offset the lattice units.
    def setCellHeight(self,cellHeight):#if no top surface is defined set a cell height. Else it will be set to 1
        self.cellHeight=cellHeight
    #(string) This is the primary component with out attractors.
    def setComponent(self,component):
        self.component=component

#lattice generation functions

    def twoSurfaceAttractors(self,token):#Lattice between two surfaces with attractors for blended lattice
        """
        Populte multiple lattice units between wo surfaces.
        The distribution of those units is defined by the distance from a set of attractors.
        The height is defined by the cell height variable.
        """
        #get attractor information
        att=parseComponents(self.attractorSet)
        payload = "{\"component\":\"%s\",\"base\":\"%s\",\"cellHeight\":%s,\"filename\": \"%s\",\"t\":\"%s\",%s" % (self.component,self.base,self.cellHeight,self.output,token,att)
        print(payload)
        #convert paylod to dictionary
        dict=ast.literal_eval(payload)
        #make post request
        r = requests.post(self.url,json=dict)
        print(r.text)
        return r.text

    def oneSurfaceLatticeAttractors(self,token):#Lattice on one surface with a constant offset with attractors for blended lattice
        """
        Populte multiple lattice units on top of one surface.
        The distribution of those units is defined by the distance from a set of attractors.
        The height is defined by the cell height variable.
        """
        #get attractor information
        att=parseComponents(self.attractorSet)
        payload = "{\"component\":\"%s\",\"base\":\"%s\",\"cellHeight\":%s,\"filename\": \"%s\",\"t\":\"%s\",%s" % (self.component,self.base,self.cellHeight,self.output,token,att)
        print(payload)
        #convert paylod to dictionary
        dict=ast.literal_eval(payload)
        #make post request
        r = requests.post(self.url,json=dict)
        print(r.text)
        return r.text

    def surfaceLatticeStatic(self,token): #Lattice on one surface with a constant offset
        """
        Populte a lattice unit ontop of one surface. The height is defined by the cell height variable.
        """
        payload = {"component":self.component,"base":self.base,"cellHeight":self.cellHeight,"filename":self.output,"t":token}
        print(json.dumps(payload))
        #make post request
        r = requests.post(self.url,json=payload)
        print(r.text)
        return r.text

    def twoSurfaceLatticeStatic(self,token):#Lattice structure between two surfaces
        """
        Populate lattice units between a top and bottom surface.
        """
        payload = {"component":self.component,"base":self.base,"cellHeight":self.cellHeight,"filename":self.output,"t":token,"ceil":self.ceil,"autoScale":self.autoScale,"ESIPLON":self.ESIPLON,"bin":self.bin}
        print(json.dumps(payload))
        #make post request
        r = requests.post(self.url,json=payload)
        print(r.text)
        return r.text

class conformalVolume:
    """
    This object of for lattices that conform their shape to volumes.
    """
    def __init__(self): #set global variables
        """
        Initialize
        """
        #URL is always this.
        self.urlGrid = "https://studiobitonti.appspot.com/conformalGrid"
        self.urlPopulate = "https://studiobitonti.appspot.com/boxMorph"
        #variables that need to be set by the user.
        self.u=65
        self.v=18
        self.w=3
        self.unitize="true"
        self.export="Board_Lattice.obj"
        self.component="box2.obj"
        self.surfaces="Skate.json"#This will be a JSON file with the surface points organized
        self.gridOutput="Skate_Grid.json"#grid output will be JSON format
        self.boxes=""
        #attactors will be formated as an 2D array "["unit_0.obj", [0,0,0], 20], ["unit_1.obj", [4,36,22], 20]]"
        #default values are files included in sample repo.
        self.attractorSet=[["unit_0.obj", [0,0,0], 20], ["unit_1.obj", [4,36,22], 20]]

#functions for seting key variables
    def setAttractor(self,a): #attractors are optional (blended lattices only)
        self.attractorSet=a
    def setUVW(self,u,v,w):
        """
        U: Input the number of grid cells in u direction.
        V: Input number of grid cells in v direction.
        W: Input number of grid cells in w direction.
        """
        self.u=u
        self.v=v
        self.w=w
    #(boolean) The input of true or false,defines whether to redivide the surface in unitized way.
    def setUnitize(self,unitize):
        self.unitize=unitize
    #(string) Component: Is the uploaded .Obj component to be arrayed.
    def setComponent(self,unitize):
        self.unitize=unitize
    #(string) Name of the uploaded .json file of surface grid representations.
    def setSurfaces(self,surfaces):
        self.surfaces=surfaces
    #(string) Name of the .json file for export.
    def setGridOutput(self,gridOutput):#file name that you want to save out
        self.gridOutput=gridOutput

#Generate conformalGrid
    def genGrid(self,token):
        """
        The conformal grid function generates a grid structure inside a given mesh input. The U,V,W are variables for the number of the grid cells.

        U: Input the number of grid cells in u direction.
        V: Input number of grid cells in v direction.
        W: Input number of grid cells in w direction.
        Surface: Name of the uploaded .json file of surface grid representations.
        Filename: Name of the resultant file for the lattice unit.
        """
        url ="https://studiobitonti.appspot.com/meshreduction"
        payload = {"u":self.u,"v":self.v,"w":self.w,"unitize":self.unitize,"surfaces":self.surfaces,"filename":self.gridOutput,"t":token}
        self.boxes=self.gridOutput
        print(json.dumps(payload))
        r = requests.post(self.urlGrid,json=payload)
        return r.text

#Populate conformal lattice
    def populateLattice(self,token):#Lattice on one surface with a constant offset with attractors for blended lattice
        """
        The Populate modulus function populates a given component into a conformal grid structure. It fill the boxes of the conformal grid into the component defined in the input.

        Component: Is the uploaded .Obj component to be arrayed.
        Boxes: Is the name of uploaded box scaffold json name.
        File Name:  Name of the resultant file for the surface lattice.
        """
        #get attractor information
        att=parseComponents(self.attractorSet)
        payload = "{\"boxes\":\"%s\",\"component\":\"%s\",\"filename\": \"%s\",\"t\":\"%s\",%s" % (self.boxes,self.component,self.export,token,att)
        print(payload)
        #convert paylod to dictionary
        dict=ast.literal_eval(payload)
        #make post request
        r = requests.post(self.urlPopulate,json=dict)
        print(r.text)
        return r.text
