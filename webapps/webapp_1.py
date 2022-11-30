# Import javascript modules
from js import THREE, window, document, Object
# Import pyscript / pyodide modules
from pyodide.ffi import create_proxy, to_js
# Import python module
import math


#-----------------------------------------------------------------------
# USE THIS FUNCTION TO WRITE THE MAIN PROGRAM
def main():
    #-----------------------------------------------------------------------
    # VISUAL SETUP
    # Declare the variables
    global renderer, scene, camera, controls,composer
    
    #Set up the renderer
    renderer = THREE.WebGLRenderer.new()
    renderer.setPixelRatio( window.devicePixelRatio )
    renderer.setSize(window.innerWidth, window.innerHeight)
    document.body.appendChild(renderer.domElement)

    # Set up the scene
    scene = THREE.Scene.new()
    back_color = THREE.Color.new(0.1,0.1,0.1)
    scene.background = back_color
    camera = THREE.OrthographicCamera.new(window.innerWidth / - 8, window.innerWidth / 8, window.innerHeight / 8, window.innerHeight / - 8, 1, 1000)
    camera.position.z = 100
    
    scene.add(camera)

    # Graphic Post Processing
    global composer
    post_process()

    # Set up responsive window
    resize_proxy = create_proxy(on_window_resize)
    window.addEventListener('resize', resize_proxy) 
    #-----------------------------------------------------------------------
    # YOUR DESIGN / GEOMETRY GENERATION
    # Geometry Creation
    #Declare parameters
 
######################
    global length , width, total, geometry, Hexa , shape, HexaSettings, Hexas, Hexa_lines
    
    Hexas = []
    Hexa_lines = []
     
    length = 2.5*1
    width = 1.5*1
    total = 3*1

    
    HexaSettings = {
        "steps": 1,
        "depth": length,
        "distance": length*4,
        "distanceToX": 2*length,
        "distanceToY": 2*width ,
        
        "bevelEnabled": False,
        "bevelThickness": 1,
        "bevelSize": 1,
        "bevelOffset": 1.3,
        "bevelSegments": 1,
        "Horizontal":10,
        "Vertical": 10,
        "Depth_z": 3
    }

    HexaSettings = Object.fromEntries(to_js(HexaSettings))
    
    
    # create material
    global material, line_material, line_color
    color = THREE.Color.new("rgb(169,115,8)")
    material = THREE.MeshBasicMaterial.new()
    material.transparent = False
    material.opacity = 0.5
    material.color = color
    
    line_material = THREE.LineBasicMaterial.new()
    line_material.color = THREE.Color.new("rgb(0,0,0)")
    
    
    
        
    
    
    ##############

    
  # Set up GUI
    gui = window.dat.GUI.new()
    param_folder = gui.addFolder('Parameters')
    
    param_folder.add(HexaSettings, 'Horizontal', 1,15,1)
    param_folder.add(HexaSettings, 'Vertical', 1,15,1)
    param_folder.add(HexaSettings, 'Depth_z', 1,10,1)
    param_folder.add(HexaSettings, 'depth', -10,20)
    param_folder.add(HexaSettings, 'distance', 1,20,1)
    param_folder.add(HexaSettings, 'bevelOffset', 1,3,0.01)
    

    param_folder.open()
    


    
###############
  
    

    # generating Hexagons using loop
    
    
    global x,y,z, ax, cz
    x=0
    y=0
    z=0
    ax = 1
    by = 1
    cz = 1
   

    for w in range(1,HexaSettings.Horizontal): 
        for v in range(HexaSettings.Depth_z):
            for i in range(HexaSettings.Vertical):  
                
                shape = THREE.Shape.new()
                shape.moveTo( 0,0 )
                shape.lineTo( -width, length)
                shape.lineTo( width, length )
                shape.lineTo( total, 0 )

                shape.lineTo( width, -length)
                shape.lineTo( -width, -length )
                shape.lineTo( -total, 0 )
                shape.lineTo( -width, length)
                shape.lineTo( 0, 0 )
                
                
               
                
                geometry = THREE.ExtrudeGeometry.new( shape, HexaSettings )
               
               
                
                
                if w % 2 == 0 and i % 2 == 0 :
                    
                    
                                    
                    shape = THREE.Shape.new()
                    shape.moveTo( 0,0 )
                    shape.lineTo( -width/HexaSettings.bevelOffset, length/HexaSettings.bevelOffset)
                    shape.lineTo( width/HexaSettings.bevelOffset, length/HexaSettings.bevelOffset )
                    shape.lineTo( total/HexaSettings.bevelOffset, 0 )

                    shape.lineTo( width/HexaSettings.bevelOffset, -length/HexaSettings.bevelOffset)
                    shape.lineTo( -width/HexaSettings.bevelOffset, -length/HexaSettings.bevelOffset)
                    shape.lineTo( -total/HexaSettings.bevelOffset, 0 )
                    shape.lineTo( -width/HexaSettings.bevelOffset, length/HexaSettings.bevelOffset)
                    shape.lineTo( 0, 0 )
                    
                    
                    geometry = THREE.ExtrudeGeometry.new( shape, HexaSettings )
                    
                    geometry.scale(ax, by, cz)
                    HexaSettings.bevelOffset*i
                    
                    
                    geometry.translate(x,2*HexaSettings.distanceToY*i+y,
                                   z*v)
                    color_2 = THREE.Color.new("rgb(280,200,40)")
                    material_2 = THREE.MeshBasicMaterial.new()
                    material_2.transparent = False
                    material_2.opacity = 0.5
                    material_2.color = color_2
                    
                    Hexa = THREE.Mesh.new( geometry, material_2 ) 
                    
                    
                    Hexas.append(Hexa)
                    scene.add( Hexa )
                    
                    edges = THREE.EdgesGeometry.new( Hexa.geometry )
                    line = THREE.LineSegments.new( edges, line_material)
                    Hexa_lines.append(line)
                    scene.add( line )

                    
                    
                    
                else:
                    geometry.translate(x,2*HexaSettings.distanceToY*i+y,z*v)
                    
                   
                    

                    Hexa = THREE.Mesh.new( geometry, material ) 
                    #lines = THREE.LineSegments.new(wireframe)
                    #Hexa_lines.append(lines)
                    Hexas.append(Hexa)
                    scene.add( Hexa )
                    #scene.add( Hexa_lines )
                
                    edges = THREE.EdgesGeometry.new( Hexa.geometry )
                    line = THREE.LineSegments.new( edges, line_material)
                    Hexa_lines.append(line)
                    scene.add( line )

                

                    
                
            z = HexaSettings.distance
           
            
    

     
         
            
        x = HexaSettings.distanceToX*w
        y= HexaSettings.distanceToY * w
        
        cz = (HexaSettings.depth /HexaSettings.depth)/2
        
      
        
        

 


    
    



   
    #------------------------------
    # -----------------------------------------
    # USER INTERFACE
    # Set up Mouse orbit control
    controls = THREE.OrbitControls.new(camera, renderer.domElement)

    ##################
   
    
    
    
    #-----------------------------------------------------------------------
    # RENDER + UPDATE THE SCENE AND GEOMETRIES
    render()
    
#-----------------------------------------------------------------------
# HELPER FUNCTIONS
#update the cubes


def update_Hexas():
    global Hexas, Hexa_lines, material, line_material
    
    if len(Hexas) != 0:
        if len(Hexas) != HexaSettings.Horizontal:
            for Hexa in Hexas: 
                scene.remove(Hexa)
            for lines in Hexa_lines: 
                scene.remove(lines)
                
        if len(Hexas) != HexaSettings.Vertical:
            for Hexa in Hexas: 
                scene.remove(Hexa)
            for lines in Hexa_lines: 
                scene.remove(lines)
                
        if len(Hexas) != HexaSettings.Depth_z:
            for Hexa in Hexas: 
                scene.remove(Hexa)
            for lines in Hexa_lines: 
                scene.remove(lines)
                
                
                Hexas = []
                Hexa_lines = []
                

            
           
        
            global x,y,z,  ax, cz
            x=0
            y=0
            z=0
            ax = 1
            by = 1
            cz = 1
        

            for w in range(1,HexaSettings.Horizontal): 
                for v in range(HexaSettings.Depth_z):
                    for i in range(HexaSettings.Vertical):  
                        
                        shape = THREE.Shape.new()
                        shape.moveTo( 0,0 )
                        shape.lineTo( -width, length)
                        shape.lineTo( width, length )
                        shape.lineTo( total, 0 )

                        shape.lineTo( width, -length)
                        shape.lineTo( -width, -length )
                        shape.lineTo( -total, 0 )
                        shape.lineTo( -width, length)
                        shape.lineTo( 0, 0 )
                        
                        
                    
                        
                        geometry = THREE.ExtrudeGeometry.new( shape, HexaSettings )
                        
                    
                        
                        if w % 2 == 0 and i % 2 == 0 :
                            
                            
                                            
                            shape = THREE.Shape.new()
                            shape.moveTo( 0,0 )
                            shape.lineTo( -width/HexaSettings.bevelOffset, length/HexaSettings.bevelOffset)
                            shape.lineTo( width/HexaSettings.bevelOffset, length/HexaSettings.bevelOffset )
                            shape.lineTo( total/HexaSettings.bevelOffset, 0 )

                            shape.lineTo( width/HexaSettings.bevelOffset, -length/HexaSettings.bevelOffset)
                            shape.lineTo( -width/HexaSettings.bevelOffset, -length/HexaSettings.bevelOffset)
                            shape.lineTo( -total/HexaSettings.bevelOffset, 0 )
                            shape.lineTo( -width/HexaSettings.bevelOffset, length/HexaSettings.bevelOffset)
                            shape.lineTo( 0, 0 )
                            
                            
                            geometry = THREE.ExtrudeGeometry.new( shape, HexaSettings )
                            
                            geometry.scale(ax, by, cz)
                            HexaSettings.bevelOffset*i
                            
                            
                            geometry.translate(x,2*HexaSettings.distanceToY*i+y,
                                        z*v)
                            color_2 = THREE.Color.new("rgb(280,200,40)")
                            material_2 = THREE.MeshBasicMaterial.new()
                            material_2.transparent = False
                            material_2.opacity = 0.5
                            material_2.color = color_2
                            
                            Hexa = THREE.Mesh.new( geometry, material_2 ) 
                            
                            
                            Hexas.append(Hexa)
                            scene.add( Hexa )
                            
                            edges = THREE.EdgesGeometry.new( Hexa.geometry )
                            line = THREE.LineSegments.new( edges, line_material)
                            Hexa_lines.append(line)
                            scene.add( line )
                                
                            
                            
                        else:
                            geometry.translate(x,2*HexaSettings.distanceToY*i+y,z*v)
                            
                            
                            

                            Hexa = THREE.Mesh.new( geometry, material ) 
                            #lines = THREE.LineSegments.new(wireframe)
                            #Hexa_lines.append(lines)
                            Hexas.append(Hexa)
                            scene.add( Hexa )
                            #scene.add( Hexa_lines )
                            
                            edges = THREE.EdgesGeometry.new( Hexa.geometry )
                            line = THREE.LineSegments.new( edges, line_material)
                            Hexa_lines.append(line)
                            scene.add( line )

                        

                            
                        
                    z = HexaSettings.distance
                   
                    
            

            
                
                    
                x = HexaSettings.distanceToX*w
                y= HexaSettings.distanceToY * w
                
                cz = (HexaSettings.depth /HexaSettings.depth)/2
                
            
       
                    
                
            

               
        else: 
            for i in range(len(Hexas)):
                Hexa = Hexas[i]
                line = Hexa_lines[i]
           


                x=0
                y=0
                z=0
                ax = 1
                by = 1
                cz = 1
            

                for w in range(1,HexaSettings.Horizontal): 
                    for v in range(HexaSettings.Depth_z):
                        for i in range(HexaSettings.Vertical):  
                            
                            shape = THREE.Shape.new()
                            shape.moveTo( 0,0 )
                            shape.lineTo( -width, length)
                            shape.lineTo( width, length )
                            shape.lineTo( total, 0 )

                            shape.lineTo( width, -length)
                            shape.lineTo( -width, -length )
                            shape.lineTo( -total, 0 )
                            shape.lineTo( -width, length)
                            shape.lineTo( 0, 0 )
                            
                            
                        
                            
                            geometry = THREE.ExtrudeGeometry.new( shape, HexaSettings )

                   
                            edges = THREE.EdgesGeometry.new( Hexa.geometry )
                            line = THREE.LineSegments.new( edges, line_material)
                            Hexa_lines.append(line)
                            scene.add( line )
                            
                            
                            
                            if w % 2 == 0 and i % 2 == 0 :
                                
                                
                                                
                                shape = THREE.Shape.new()
                                shape.moveTo( 0,0 )
                                shape.lineTo( -width/HexaSettings.bevelOffset, length/HexaSettings.bevelOffset)
                                shape.lineTo( width/HexaSettings.bevelOffset, length/HexaSettings.bevelOffset )
                                shape.lineTo( total/HexaSettings.bevelOffset, 0 )

                                shape.lineTo( width/HexaSettings.bevelOffset, -length/HexaSettings.bevelOffset)
                                shape.lineTo( -width/HexaSettings.bevelOffset, -length/HexaSettings.bevelOffset)
                                shape.lineTo( -total/HexaSettings.bevelOffset, 0 )
                                shape.lineTo( -width/HexaSettings.bevelOffset, length/HexaSettings.bevelOffset)
                                shape.lineTo( 0, 0 )
                                
                                
                                geometry = THREE.ExtrudeGeometry.new( shape, HexaSettings )
                                
                                geometry.scale(ax, by, cz)
                                HexaSettings.bevelOffset*i
                                
                                
                                geometry.translate(x,2*HexaSettings.distanceToY*i+y,
                                            z*v)
                                color_2 = THREE.Color.new("rgb(280,200,40)")
                                material_2 = THREE.MeshBasicMaterial.new()
                                material_2.transparent = False
                                material_2.opacity = 0.5
                                material_2.color = color_2
                                
                                Hexa = THREE.Mesh.new( geometry, material_2 ) 
                                
                                
                                Hexas.append(Hexa)
                                scene.add( Hexa )
                                
                                edges = THREE.EdgesGeometry.new( Hexa.geometry )
                                line = THREE.LineSegments.new( edges, line_material)
                                Hexa_lines.append(line)
                                scene.add( line )
                                            
                                    
                                
                                
                            else:
                                geometry.translate(x,2*HexaSettings.distanceToY*i+y,z*v)
                                
                                

                                Hexa = THREE.Mesh.new( geometry, material ) 
                         
                                Hexas.append(Hexa)
                                scene.add( Hexa )
                           
                                
                             
                    

                            
                
                            Hexa.geom = geometry
                            
                            edges = THREE.EdgesGeometry.new(Hexa.geom)
                            line.geom = edges
                
            




    
# Simple render and animate

    
def render(*args):
    window.requestAnimationFrame(create_proxy(render))
    update_Hexas()
    controls.update()
    composer.render()

# Graphical post-processing
def post_process():
    render_pass = THREE.RenderPass.new(scene, camera)
    render_pass.clearColor = THREE.Color.new(0,0,0)
    render_pass.ClearAlpha = 0
    fxaa_pass = THREE.ShaderPass.new(THREE.FXAAShader)

    pixelRatio = window.devicePixelRatio

    fxaa_pass.material.uniforms.resolution.value.x = 1 / ( window.innerWidth * pixelRatio )
    fxaa_pass.material.uniforms.resolution.value.y = 1 / ( window.innerHeight * pixelRatio )
   
    global composer
    composer = THREE.EffectComposer.new(renderer)
    composer.addPass(render_pass)
    composer.addPass(fxaa_pass)

# Adjust display when window size changes
def on_window_resize(event):

    event.preventDefault()

    global renderer
    global camera
    
    camera.aspect = window.innerWidth / window.innerHeight
    camera.updateProjectionMatrix()

    renderer.setSize( window.innerWidth, window.innerHeight )

    #post processing after resize
    post_process()
#-----------------------------------------------------------------------
#RUN THE MAIN PROGRAM
if __name__=='__main__':
    main()
    
    
    
