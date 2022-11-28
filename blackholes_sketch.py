# Import javascript modules
from js import THREE, window, document, Object, console
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
    global renderer, scene, camera, controls,composer,layers
    
    #Set up the renderer
    renderer = THREE.WebGLRenderer.new()
    renderer.setPixelRatio( window.devicePixelRatio )
    renderer.setSize(window.innerWidth, window.innerHeight)
    document.body.appendChild(renderer.domElement)

    # Set up the scene
    scene = THREE.Scene.new()
    back_color = THREE.Color.new(0.1,0.1,0.1)
    scene.background = back_color
    camera = THREE.PerspectiveCamera.new(75, window.innerWidth/window.innerHeight, 0.1, 1000)
    camera.position.z = 70
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
    layers = {"current_iteration": 0,
              "maximum_iterations": 3}

    
    layers = Object.fromEntries(to_js(layers))
  
    
    my_axiom_system = system(layers.current_iteration, layers.maximum_iterations , "X")
    

    console.log(my_axiom_system)
    
      # Set up GUI
    gui = window.dat.GUI.new()
    param_folder = gui.addFolder('Parameters')
    param_folder.add(layers, "current_iteration" ,0,10,1)
    param_folder.add(layers, "maximum_iterations" ,0,10,1)
    param_folder.open()

    draw_system((my_axiom_system), THREE.Vector3.new(0,0,0))


    #-----------------------------------------------------------------------
    # USER INTERFACE
    # Set up Mouse orbit control
    controls = THREE.OrbitControls.new(camera, renderer.domElement)


    #-----------------------------------------------------------------------
    # RENDER + UPDATE THE SCENE AND GEOMETRIES
    render()
    
#-----------------------------------------------------------------------
# HELPER FUNCTIONS
# Define RULES in a function which takes one SYMBOL and applies rules generation
def generate(symbol):
    if symbol == "X":
        return "F[+X-X]"
    elif symbol == "F":
        return "F"
    elif symbol == "+":
        return "+"
    elif symbol == "-":
        return "-"
    elif symbol == "[":
        return "["
    elif symbol == "]":
        return "]"
# A recursive fundtion, which taken an AXIOM as an inout and runs the generate function for each symbol
            #global         #anzahl Layer       global
def system(current_iteration, max_iterations, axiom):
    current_iteration += 1
    new_axiom = ""
    for symbol in axiom:
        new_axiom += generate(symbol)
    if current_iteration >= max_iterations:
        return new_axiom #letztes Axiom
    else:
        return system(current_iteration, max_iterations, new_axiom)
                                                            # new axiom for the next layer
global scene
def draw_system(axiom, start_pt):
    move_vec = THREE.Vector3.new(0,10,0)
    dist = move_vec.y
    old_states = []
    old_move_vecs = []
    lines = []
    circle = []
    # generating multiple points 
    for symbol in axiom:
        if symbol == "F" or symbol == "X":
            old = THREE.Vector3.new(start_pt.x, start_pt.y, start_pt.z)
            new_pt = THREE.Vector3.new(start_pt.x, start_pt.y, start_pt.z)
            new_pt = new_pt.add(move_vec)
            line = []
            line.append(old)
            line.append(new_pt)
            lines.append(line)
            
            
            start_pt = new_pt
            # define the generated points as midpoints for circles
            global DrawCircle
            def DrawCircle(start_pt, dist,):
                curve = THREE.EllipseCurve.new(start_pt.x, start_pt.y,dist,dist)
          
                points = curve.getPoints(50)

                geometry = THREE.BufferGeometry.new().setFromPoints(points)
                
                material = THREE.LineBasicMaterial.new( THREE.Color.new(0x0000ff))
                ellipse = THREE.Line.new(geometry, material)
                
                # if radius is greater than the number, show the circles
                if dist > 0.5:
                    DrawCircle((start_pt),dist/1.1)
                    

                scene.add(ellipse)
                
            
         
            #outer Circle
            DrawCircle(start_pt, dist/1.2)
    
            circle = []
            circle.append(DrawCircle)
            
   
            
        elif symbol == "+": 
            move_vec.applyAxisAngle(THREE.Vector3.new(0,0,1), math.pi/4)
        
        elif symbol == "-":
            move_vec.applyAxisAngle(THREE.Vector3.new(0,0,1), -math.pi/2)
        
        elif symbol == "[":
            old_state = THREE.Vector3.new(start_pt.x, start_pt.y, start_pt.z)
            old_move_vec = THREE.Vector3.new(move_vec.x, move_vec.y, move_vec.z)
            old_states.append(old_state)
            old_move_vecs.append(old_move_vec)

        elif symbol == "]":
            start_pt = THREE.Vector3.new(old_states[-1].x, old_states[-1].y, old_states[-1].z)
            move_vec = THREE.Vector3.new(old_move_vecs[-1].x, old_move_vecs[-1].y, old_move_vecs[-1].z)
            old_states.pop(-1)
            old_move_vecs.pop(-1)

"""circle generation in sliders, doesn't work
def update_circles():


    if len(circle) != 0:
        if len(circle) != layers.maximum_iterations/3:
            for DrawCircle in circle: 
                scene.remove(DrawCircle)
                
                circle = []

            
            
            def generate(symbol):
                if symbol == "X":
                    return "F[+X-X]"
                elif symbol == "F":
                    return "F"
                elif symbol == "+":
                    return "+"
                elif symbol == "-":
                    return "-"
                elif symbol == "[":
                    return "["
                elif symbol == "]":
                    return "]"
            # A recursive fundtion, which taken an AXIOM as an inout and runs the generate function for each symbol
                        #global         #anzahl Layer       global
            def system(current_iteration, max_iterations, axiom):
                current_iteration += 1
                new_axiom = ""
                for symbol in axiom:
                    new_axiom += generate(symbol)
                if current_iteration >= max_iterations:
                    return new_axiom #letztes Axiom
                else:
                    return system(current_iteration, max_iterations, new_axiom)
                                                
            
    
            
            
            
            def draw_system(axiom, start_pt):
                move_vec = THREE.Vector3.new(0,10,0)
                dist = move_vec.y
                old_states = []
                old_move_vecs = []
                lines = []
                circle = []
                # generating multiple points 
                for symbol in axiom:
                    if symbol == "F" or symbol == "X":
                        old = THREE.Vector3.new(start_pt.x, start_pt.y, start_pt.z)
                        new_pt = THREE.Vector3.new(start_pt.x, start_pt.y, start_pt.z)
                        new_pt = new_pt.add(move_vec)
                        line = []
                        line.append(old)
                        line.append(new_pt)
                        lines.append(line)
                        
                        
                        start_pt = new_pt
                        # define the generated points as midpoints for circles
                        def DrawCircle(start_pt, dist,):
                            curve = THREE.EllipseCurve.new(start_pt.x, start_pt.y,dist,dist)
                    
                            points = curve.getPoints(50)

                            geometry = THREE.BufferGeometry.new().setFromPoints(points)
                            
                            material = THREE.LineBasicMaterial.new( THREE.Color.new(0x0000ff))
                            ellipse = THREE.Line.new(geometry, material)
                            
                            # if radius is greater than the number, show the circles
                            if dist > 0.5:
                                DrawCircle((start_pt),dist/1.1)
                                

                            scene.add(ellipse)
                            
                        
                    
                        #outer Circle
                        DrawCircle(start_pt, dist/1.2)
                        
                        circle = []
                        circle.append(DrawCircle)
                        print(circle)
                        
                    
                        
                    elif symbol == "+": 
                        move_vec.applyAxisAngle(THREE.Vector3.new(0,0,1), math.pi/4)
                    
                    elif symbol == "-":
                        move_vec.applyAxisAngle(THREE.Vector3.new(0,0,1), -math.pi/2)
                    
                    elif symbol == "[":
                        old_state = THREE.Vector3.new(start_pt.x, start_pt.y, start_pt.z)
                        old_move_vec = THREE.Vector3.new(move_vec.x, move_vec.y, move_vec.z)
                        old_states.append(old_state)
                        old_move_vecs.append(old_move_vec)

                    elif symbol == "]":
                        start_pt = THREE.Vector3.new(old_states[-1].x, old_states[-1].y, old_states[-1].z)
                        move_vec = THREE.Vector3.new(old_move_vecs[-1].x, old_move_vecs[-1].y, old_move_vecs[-1].z)
                        old_states.pop(-1)
                        old_move_vecs.pop(-1)
                        
                        
       """
            
                            
                            
                
                    



 
# Simple render and animate
def render(*args):
    window.requestAnimationFrame(create_proxy(render))
    controls.update()
    #update_circles()
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
    
    
    
    
    
    