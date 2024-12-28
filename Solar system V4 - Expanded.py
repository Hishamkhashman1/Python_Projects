from math import cos,sin,pi
import os
import random
from vpython import box, button, canvas, local_light, ring, rotate, scene, sphere, vector, color, rate, wtext, label, textures

# constants and scale
AU=1.496e11 # Astronomical unit is 149.6 million kms
scale=1e-10 # Scale of the model
Vizualization_scale=8.5 #adjustable additional scale factor for better visualization
Orbital_speed={
'Mercury': 47.87,
'Venus': 35.02,
'Earth': 29.78,
'Mars': 24.077,
'Jupiter': 13.07,
'Saturn': 9.69,
'Uranus': 6.81,
'Neptune': 5.43,

}

Orbital_periods={
'Mercury': 88.0,
'Venus': 224.7,
'Earth': 365.3,
'Mars': 687.0,
'Jupiter': 4331,
'Saturn': 10747,
'Uranus': 30589,
'Neptune': 59800,


# Moon of Earth orbital period
'Moon': 27.3,

# Prominent asteroids in the Asteroid Belt
'Ceres': 1680.5,
'Pallas': 1686.0,
'Juno': 1592.0,
'Vesta': 1325.0,
}



# Planet radii in kilometers (real values)
planet_radii = {
'Mercury': 2439.7,
'Venus': 6051.8,
'Earth': 6371.0,
'Mars': 3389.5,
'Jupiter': 69911,
'Saturn': 58232,
'Uranus': 25362,
'Neptune': 24622,

# Moon of Earth radius
'Moon': 1737.1,

# Moons of Mars radii
'Phobos': 11.1,
'Deimos': 6.2,


# Moons of Jupiter radii
'Io': 1821.6,
'Europa': 1560.8,
'Ganymede': 2634.1,
'Callisto': 2410.3,

# Moons of Saturn radii
'Mimas': 198.8,
'Enceladus': 252.1,
'Tethys': 533.1,
'Dione': 561.4,
'Rhea': 763.8,
'Titan': 2575.5,
'Iapetus': 734.5,

# Moons of Uranus radii
'Miranda': 235.8,
'Ariel': 578.9,
'Umbriel': 584.7,
'Titania': 788.9,
'Oberon': 761.4,

# Moons of Neptune radii
'Triton': 1353.4,
'Proteus': 210.3,
'Nereid': 170.0,

# Prominent Asteroids in the Asteroid Belt
'Ceres': 469.73,
'Pallas': 256.23,
'Juno': 258.23,
'Vesta': 262.7,



# Sun radius in kilometers (real value)

'Sun': 696340,
}

# Planet distances from the Sun in kilometers (real values)
planet_distances = {
'Mercury': 57910000,
'Venus': 108200000,
'Earth': 149600000,
'Mars': 227940000,
'Jupiter': 778330000,
'Saturn': 1429400000,
'Uranus': 2870990000,
'Neptune': 4497100000,

# Moon of Earth distance from the Earth
'Moon': 384400,

# Moons of Mars distances from Mars
'Phobos': 9377,
'Deimos': 23460,

# Moons of Jupiter distances from Jupiter
'Io': 421800,
'Europa': 671100,
'Ganymede': 1070000,
'Callisto': 1883000,

# Moons of Saturn distances from Saturn
'Mimas': 185520,
'Enceladus': 238020,
'Tethys': 294660,
'Dione': 377400,
'Rhea': 527040,
'Titan': 1221870,
'Iapetus': 3560820,

# Moons of Uranus distances from Uranus
'Miranda': 129390,
'Ariel': 191020,
'Umbriel': 266300,
'Titania': 435910,
'Oberon': 583520,

# Moons of Neptune distances from Neptune
'Triton': 354800,
'Proteus': 117647,
'Nereid': 551340,

# Prominent Asteroids in the Asteroid Belt
'Ceres': 413700000,
'Pallas': 414000000,
'Juno': 414000000,
'Vesta': 414000000,



# Sun distance from the sun
'Sun': 0,
}

# Scaling Planet's radii

scaled_planet_radii = {planet: radius*scale*Vizualization_scale for planet, radius in planet_radii.items()}

# Scaling Planet's distances
scaled_planet_distances = {planet: distance*scale/Vizualization_scale for planet, distance in planet_distances.items()}

# Constants for the asteroid belt
min_distance = scaled_planet_distances['Mars']
max_distance= scaled_planet_distances['Jupiter']



# Create the Sun

sun = sphere(pos=vector(0,0,0), radius=scaled_planet_radii['Sun'], color=color.yellow, emmisive=True)



# Add a light source at the Sun's position
sun_light = local_light(pos=sun.pos, color=color.white)  # Add this line to create a light source at the Sun's position

# Create Mercury
mercury = sphere(pos=vector(scaled_planet_distances['Mercury'],0,0), radius=scaled_planet_radii['Mercury'], color=color.gray(0.5), make_trail=True,trail_radius=scaled_planet_radii['Mercury']*0.2,texture=textures.rock)
mercury_label = label(pos=mercury.pos, text=f"Mercury\nType: Planet\nSpeed: {Orbital_speed['Mercury']} km/s\nDistance: {planet_distances['Mercury']} km\nOrbital Period: {Orbital_periods['Mercury']} days", xoffset=20, yoffset=20, space=30, height=10, border=4, font='sans')
# Create Venus
venus = sphere(pos=vector(scaled_planet_distances['Venus'],0,0), radius=scaled_planet_radii['Venus'], color=color.orange, make_trail=True,trail_radius=scaled_planet_radii['Venus']*0.2,texture=textures.rock)
venus_label = label(pos=venus.pos, text=f"Venus\nType: Planet\nSpeed: {Orbital_speed['Venus']} km/s\nDistance: {planet_distances['Venus']} km\nOrbital Period: {Orbital_periods['Venus']} days", xoffset=20, yoffset=20, space=30, height=10, border=4, font='sans')

# Create Earth

earth = sphere(pos=vector(scaled_planet_distances['Earth'],0,0), radius=scaled_planet_radii['Earth'], color=color.blue, make_trail=True,trail_radius=scaled_planet_radii['Earth']*0.2,texture=textures.rock,shininess=0.6, emissive=False)
earth_label = label(pos=earth.pos, text=f"Earth\nType: Planet\nSpeed: {Orbital_speed['Earth']} km/s\nDistance: {planet_distances['Earth']} km\nOrbital Period: {Orbital_periods['Earth']} days", xoffset=20, yoffset=20, space=30, height=10, border=4, font='sans')
def follow_earth():
    scene.camera.pos = earth.pos + vector(0, 0.5, 2)
    scene.camera.axis = earth.pos - scene.camera.pos
    scene.camera.fov = 0.2
    scene.up = vector(0, 0, 1)

# Insert a button to follow Earth
button(text='Follow Earth', bind=follow_earth)




# Create the Moon of Earth
moon=sphere(pos=vector(scaled_planet_distances['Earth']+planet_distances['Moon']*scale,0,0), radius=scaled_planet_radii['Moon'], color=color.white, make_trail=True,trail_radius=scaled_planet_radii['Moon']*0.1,texture=textures.rough)
# Create Mars
mars = sphere(pos=vector(scaled_planet_distances['Mars'],0,0), radius=scaled_planet_radii['Mars'], color=color.red, make_trail=True,trail_radius=scaled_planet_radii['Mars']*0.2,texture=textures.rough)
mars_label = label(pos=mars.pos, text=f"Mars\nType: Planet\nSpeed: {Orbital_speed['Mars']} km/s\nDistance: {planet_distances['Mars']} km\nOrbital Period: {Orbital_periods['Mars']} days", xoffset=20, yoffset=20, space=30, height=10, border=4, font='sans')
phobos = sphere(pos=vector(scaled_planet_distances['Mars']+planet_distances['Phobos']*scale,0,0), radius=scaled_planet_radii['Phobos'], color=color.gray(0.5), make_trail=True,trail_radius=scaled_planet_radii['Phobos']*0.1)
deimos = sphere(pos=vector(scaled_planet_distances['Mars']+planet_distances['Deimos']*scale,0,0), radius=scaled_planet_radii['Deimos'], color=color.gray(0.5), make_trail=True,trail_radius=scaled_planet_radii['Deimos']*0.1)

# Create Jupiter
jupiter = sphere(pos=vector(scaled_planet_distances['Jupiter'],0,0), radius=scaled_planet_radii['Jupiter'], color=color.orange, make_trail=True,trail_radius=scaled_planet_radii['Jupiter']*0.2)
jupiter_label = label(pos=jupiter.pos, text=f"Jupiter\nType: Planet\nSpeed: {Orbital_speed['Jupiter']} km/s\nDistance: {planet_distances['Jupiter']} km\nOrbital Period: {Orbital_periods['Jupiter']} days", xoffset=20, yoffset=20, space=30, height=10, border=4, font='sans')    
io=sphere(pos=vector(scaled_planet_distances['Jupiter']+planet_distances['Io']*scale,0,0), radius=scaled_planet_radii['Io'], color=color.gray(0.5), make_trail=True,trail_radius=scaled_planet_radii['Io']*0.1)
europa=sphere(pos=vector(scaled_planet_distances['Jupiter']+planet_distances['Europa']*scale,0,0), radius=scaled_planet_radii['Europa'], color=color.gray(0.5), make_trail=True,trail_radius=scaled_planet_radii['Europa']*0.1)
ganymede=sphere(pos=vector(scaled_planet_distances['Jupiter']+planet_distances['Ganymede']*scale,0,0), radius=scaled_planet_radii['Ganymede'], color=color.gray(0.5), make_trail=True,trail_radius=scaled_planet_radii['Ganymede']*0.1)
callisto=sphere(pos=vector(scaled_planet_distances['Jupiter']+planet_distances['Callisto']*scale,0,0), radius=scaled_planet_radii['Callisto'], color=color.gray(0.5), make_trail=True,trail_radius=scaled_planet_radii['Callisto']*0.1)

# Create Saturn
saturn = sphere(pos=vector(scaled_planet_distances['Saturn'],0,0), radius=scaled_planet_radii['Saturn'], color=color.yellow, make_trail=True,trail_radius=scaled_planet_radii['Saturn']*0.2)
saturn_ring = ring(pos=vector(scaled_planet_distances['Saturn'],0,0), axis=vector(0,0,1), radius=scaled_planet_radii['Saturn']*2, thickness=scaled_planet_radii['Saturn']*0.2, color=color.white)
saturn_label = label(pos=saturn.pos, text=f"Saturn\nType: Planet\nSpeed: {Orbital_speed['Saturn']} km/s\nDistance: {planet_distances['Saturn']} km\nOrbital Period: {Orbital_periods['Saturn']} days", xoffset=20, yoffset=20, space=30, height=10, border=4, font='sans')
mimas=sphere(pos=vector(scaled_planet_distances['Saturn']+planet_distances['Mimas']*scale,0,0), radius=scaled_planet_radii['Mimas'], color=color.gray(0.5), make_trail=True,trail_radius=scaled_planet_radii['Mimas']*0.1)
enceladus=sphere(pos=vector(scaled_planet_distances['Saturn']+planet_distances['Enceladus']*scale,0,0), radius=scaled_planet_radii['Enceladus'], color=color.gray(0.5), make_trail=True,trail_radius=scaled_planet_radii['Enceladus']*0.1)
tethys=sphere(pos=vector(scaled_planet_distances['Saturn']+planet_distances['Tethys']*scale,0,0), radius=scaled_planet_radii['Tethys'], color=color.gray(0.5), make_trail=True,trail_radius=scaled_planet_radii['Tethys']*0.1)
dione=sphere(pos=vector(scaled_planet_distances['Saturn']+planet_distances['Dione']*scale,0,0), radius=scaled_planet_radii['Dione'], color=color.gray(0.5), make_trail=True,trail_radius=scaled_planet_radii['Dione']*0.1)
rhea=sphere(pos=vector(scaled_planet_distances['Saturn']+planet_distances['Rhea']*scale,0,0), radius=scaled_planet_radii['Rhea'], color=color.gray(0.5), make_trail=True,trail_radius=scaled_planet_radii['Rhea']*0.1)
titan=sphere(pos=vector(scaled_planet_distances['Saturn']+planet_distances['Titan']*scale,0,0), radius=scaled_planet_radii['Titan'], color=color.gray(0.5), make_trail=True,trail_radius=scaled_planet_radii['Titan']*0.1)
iapetus=sphere(pos=vector(scaled_planet_distances['Saturn']+planet_distances['Iapetus']*scale,0,0), radius=scaled_planet_radii['Iapetus'], color=color.gray(0.5), make_trail=True,trail_radius=scaled_planet_radii['Iapetus']*0.1)

# Create Uranus
uranus = sphere(pos=vector(scaled_planet_distances['Uranus'],0,0), radius=scaled_planet_radii['Uranus'], color=color.cyan, make_trail=True,trail_radius=scaled_planet_radii['Uranus']*0.2)
uranus_ring = ring(pos=vector(scaled_planet_distances['Uranus'],0,0), axis=vector(0,0,1), radius=scaled_planet_radii['Uranus']*1.8, thickness=scaled_planet_radii['Uranus']*0.1, color=color.gray(0.5))
uranus_label = label(pos=uranus.pos, text=f"Uranus\nType: Planet\nSpeed: {Orbital_speed['Uranus']} km/s\nDistance: {planet_distances['Uranus']} km\nOrbital Period: {Orbital_periods['Uranus']} days", xoffset=20, yoffset=20, space=30, height=10, border=4, font='sans')
miranda=sphere(pos=vector(scaled_planet_distances['Uranus']+planet_distances['Miranda']*scale,0,0), radius=scaled_planet_radii['Miranda'], color=color.gray(0.5), make_trail=True,trail_radius=scaled_planet_radii['Miranda']*0.1)
ariel=sphere(pos=vector(scaled_planet_distances['Uranus']+planet_distances['Ariel']*scale,0,0), radius=scaled_planet_radii['Ariel'], color=color.gray(0.5), make_trail=True,trail_radius=scaled_planet_radii['Ariel']*0.1)
umbriel=sphere(pos=vector(scaled_planet_distances['Uranus']+planet_distances['Umbriel']*scale,0,0), radius=scaled_planet_radii['Umbriel'], color=color.gray(0.5), make_trail=True,trail_radius=scaled_planet_radii['Umbriel']*0.1)
titania=sphere(pos=vector(scaled_planet_distances['Uranus']+planet_distances['Titania']*scale,0,0), radius=scaled_planet_radii['Titania'], color=color.gray(0.5), make_trail=True,trail_radius=scaled_planet_radii['Titania']*0.1)
oberon=sphere(pos=vector(scaled_planet_distances['Uranus']+planet_distances['Oberon']*scale,0,0), radius=scaled_planet_radii['Oberon'], color=color.gray(0.5), make_trail=True,trail_radius=scaled_planet_radii['Oberon']*0.1)

# Create Neptune
neptune = sphere(pos=vector(scaled_planet_distances['Neptune'],0,0), radius=scaled_planet_radii['Neptune'], color=color.blue, make_trail=True,trail_radius=scaled_planet_radii['Neptune']*0.2)
neptune_ring = ring(pos=vector(scaled_planet_distances['Neptune'],0,0), axis=vector(0,0,1), radius=scaled_planet_radii['Neptune']*1.5, thickness=scaled_planet_radii['Neptune']*0.1, color=color.gray(0.5))
neptune_label = label(pos=neptune.pos, text=f"Neptune\nType: Planet\nSpeed: {Orbital_speed['Neptune']} km/s\nDistance: {planet_distances['Neptune']} km\nOrbital Period: {Orbital_periods['Neptune']} days", xoffset=20, yoffset=20, space=30, height=10, border=4, font='sans')
triton=sphere(pos=vector(scaled_planet_distances['Neptune']+planet_distances['Triton']*scale,0,0), radius=scaled_planet_radii['Triton'], color=color.gray(0.5), make_trail=True,trail_radius=scaled_planet_radii['Triton']*0.1)
proteus=sphere(pos=vector(scaled_planet_distances['Neptune']+planet_distances['Proteus']*scale,0,0), radius=scaled_planet_radii['Proteus'], color=color.gray(0.5), make_trail=True,trail_radius=scaled_planet_radii['Proteus']*0.1)
nereid=sphere(pos=vector(scaled_planet_distances['Neptune']+planet_distances['Nereid']*scale,0,0), radius=scaled_planet_radii['Nereid'], color=color.gray(0.5), make_trail=True,trail_radius=scaled_planet_radii['Nereid']*0.1)

# Create Prominent Asteroids in the Asteroid Belt
ceres=sphere(pos=vector(scaled_planet_distances['Ceres'],0,0), radius=scaled_planet_radii['Ceres'], color=color.gray(0.5), make_trail=True,trail_radius=scaled_planet_radii['Ceres']*0.5)
ceres_label = label(pos=ceres.pos, text=f"Ceres\nType: Asteroid\nDistance: {planet_distances['Ceres']} km", xoffset=20, yoffset=20, space=30, height=10, border=4, font='sans')
pallas=sphere(pos=vector(scaled_planet_distances['Pallas'],0,0), radius=scaled_planet_radii['Pallas'], color=color.gray(0.5), make_trail=True,trail_radius=scaled_planet_radii['Pallas']*0.5)
pallas_label = label(pos=pallas.pos, text=f"Pallas\nType: Asteroid\nDistance: {planet_distances['Pallas']} km", xoffset=20, yoffset=20, space=30, height=10, border=4, font='sans')
juno=sphere(pos=vector(scaled_planet_distances['Juno'],0,0), radius=scaled_planet_radii['Juno'], color=color.gray(0.5), make_trail=True,trail_radius=scaled_planet_radii['Juno']*0.5)
juno_label = label(pos=juno.pos, text=f"Juno\nType: Asteroid\nDistance: {planet_distances['Juno']} km", xoffset=20, yoffset=20, space=30, height=10, border=4, font='sans')
vesta=sphere(pos=vector(scaled_planet_distances['Vesta'],0,0), radius=scaled_planet_radii['Vesta'], color=color.gray(0.5), make_trail=True,trail_radius=scaled_planet_radii['Vesta']*0.5)
vesta_label = label(pos=vesta.pos, text=f"Vesta\nType: Asteroid\nDistance: {planet_distances['Vesta']} km", xoffset=20, yoffset=20, space=30, height=10, border=4, font='sans')



# Set Initial camera position
initial_camera_pos = vector(scaled_planet_distances['Earth'] * 1, scaled_planet_distances['Earth'] * 1, scaled_planet_distances['Earth'] * 1)
initial_camera_axis = vector(-scaled_planet_distances['Earth']*1, -scaled_planet_distances['Earth']*1, -scaled_planet_distances['Earth']*1)
scene.camera.pos = initial_camera_pos
scene.camera.axis = initial_camera_axis
scene.up = vector(0, 1, 0)  # Set the up direction

# Create the asteroid Belt
def create_asteroid_belt():
        asteroids=[]
        for i in range(500):
                distance=random.uniform(min_distance,max_distance)
                print(distance) #for debugging
                angle=random.uniform(0,2*pi)
                print(angle) #for debugging
                x=distance*cos(angle)
                print(x) #for debugging
                y=distance*sin(angle)
                print(y) #for debugging
                z=random.uniform(-0.0001,0.0001)
                print(z) #for debugging
                min_radius=1
                max_radius=500
                asteroid=sphere(pos=vector(x,y,z),radius=random.uniform(min_radius,max_radius)*scale*Vizualization_scale,color=color.gray(0.5),make_trail=True,trail_radius=2000*scale*Vizualization_scale*0.01,trail_type='curve',trail_fade=30)
                asteroids.append(asteroid)
        return asteroids    
asteroids=create_asteroid_belt()




# Zooming and panning
zoom_factor = 0.1
pan_speed = 0.0001
tilt_angle = 0.0001

# Function to handle keydown events
def handle_keydown(event):
    key = event.key
    direction = scene.center - scene.camera.pos
    direction = direction.norm()
    # Zoom in and out
    if key == 'w':  # Zoom in
        scene.camera.pos += direction * (1 / zoom_factor)
    elif key == 's':  # Zoom out
        scene.camera.pos -= direction * zoom_factor
    # Panning    
    elif key == 'left':  # Pan left
        scene.camera.pos += vector(-pan_speed, 0, 0)
        scene.center += vector(-pan_speed, 0, 0)
    elif key == 'right':  # Pan right
        scene.camera.pos += vector(pan_speed, 0, 0)
        scene.center += vector(pan_speed, 0, 0)
    elif key == 'up':  # Pan up
        scene.camera.pos += vector(0, pan_speed, 0)
        scene.center += vector(0, pan_speed, 0)
    elif key == 'down':  # Pan down
        scene.camera.pos += vector(0, -pan_speed, 0)
        scene.center += vector(0, -pan_speed, 0)
     # Tilting
    elif key == 'q':  # Tilt up
        scene.camera.axis = scene.camera.axis.rotate(angle=tilt_angle, axis=scene.camera.axis.cross(scene.up))
    elif key == 'e':  # Tilt down
        scene.camera.axis = scene.camera.axis.rotate(angle=-tilt_angle, axis=scene.camera.axis.cross(scene.up))
    # Reset camera
    elif key == 'r':  # Reset camera
        scene.camera.pos = initial_camera_pos
        scene.camera.axis = initial_camera_axis
        following = False  # Stop following Earth

# Bind the keydown event to the handle_keydown function
scene.bind('keydown', handle_keydown)

# Animation loop
t=0
while True:
    rate(50)
    t += 0.01
    earth.pos = vector(scaled_planet_distances['Earth']*cos(2*pi/Orbital_periods['Earth']*t), scaled_planet_distances['Earth']*sin(2*pi/Orbital_periods['Earth']*t), 0)
    mercury.pos = vector(scaled_planet_distances['Mercury']*cos(2*pi/Orbital_periods['Mercury']*t), scaled_planet_distances['Mercury']*sin(2*pi/Orbital_periods['Mercury']*t), 0)
    venus.pos = vector(scaled_planet_distances['Venus']*cos(2*pi/Orbital_periods['Venus']*t), scaled_planet_distances['Venus']*sin(2*pi/Orbital_periods['Venus']*t), 0)
    mars.pos = vector(scaled_planet_distances['Mars']*cos(2*pi/Orbital_periods['Mars']*t), scaled_planet_distances['Mars']*sin(2*pi/Orbital_periods['Mars']*t), 0)
    jupiter.pos = vector(scaled_planet_distances['Jupiter']*cos(2*pi/Orbital_periods['Jupiter']*t), scaled_planet_distances['Jupiter']*sin(2*pi/Orbital_periods['Jupiter']*t), 0)
    saturn.pos = vector(scaled_planet_distances['Saturn']*cos(2*pi/Orbital_periods['Saturn']*t), scaled_planet_distances['Saturn']*sin(2*pi/Orbital_periods['Saturn']*t), 0)
    saturn_ring.pos = saturn.pos
    uranus.pos = vector(scaled_planet_distances['Uranus']*cos(2*pi/Orbital_periods['Uranus']*t), scaled_planet_distances['Uranus']*sin(2*pi/Orbital_periods['Uranus']*t), 0)
    uranus_ring.pos = uranus.pos
    neptune.pos = vector(scaled_planet_distances['Neptune']*cos(2*pi/Orbital_periods['Neptune']*t), scaled_planet_distances['Neptune']*sin(2*pi/Orbital_periods['Neptune']*t), 0)
    neptune_ring.pos = neptune.pos
    moon.pos =earth.pos + vector((planet_distances['Moon']*scale)*cos(2*pi/Orbital_periods['Moon']*t), (planet_distances['Moon']*scale)*sin(2*pi/Orbital_periods['Moon']*t), 0)
    # Moons animations
    phobos.pos = mars.pos + vector((planet_distances['Phobos']*scale)*cos(2*pi/Orbital_periods['Mars']*t), (planet_distances['Phobos']*scale)*sin(2*pi/Orbital_periods['Mars']*t), 0)
    deimos.pos = mars.pos + vector((planet_distances['Deimos']*scale)*cos(2*pi/Orbital_periods['Mars']*t), (planet_distances['Deimos']*scale)*sin(2*pi/Orbital_periods['Mars']*t), 0)
    io.pos = jupiter.pos + vector((planet_distances['Io']*scale)*cos(2*pi/Orbital_periods['Jupiter']*t), (planet_distances['Io']*scale)*sin(2*pi/Orbital_periods['Jupiter']*t), 0)
    europa.pos = jupiter.pos + vector((planet_distances['Europa']*scale)*cos(2*pi/Orbital_periods['Jupiter']*t), (planet_distances['Europa']*scale)*sin(2*pi/Orbital_periods['Jupiter']*t), 0)
    ganymede.pos = jupiter.pos + vector((planet_distances['Ganymede']*scale)*cos(2*pi/Orbital_periods['Jupiter']*t), (planet_distances['Ganymede']*scale)*sin(2*pi/Orbital_periods['Jupiter']*t), 0)
    callisto.pos = jupiter.pos + vector((planet_distances['Callisto']*scale)*cos(2*pi/Orbital_periods['Jupiter']*t), (planet_distances['Callisto']*scale)*sin(2*pi/Orbital_periods['Jupiter']*t), 0)
    mimas.pos = saturn.pos + vector((planet_distances['Mimas']*scale)*cos(2*pi/Orbital_periods['Saturn']*t), (planet_distances['Mimas']*scale)*sin(2*pi/Orbital_periods['Saturn']*t), 0)
    enceladus.pos = saturn.pos + vector((planet_distances['Enceladus']*scale)*cos(2*pi/Orbital_periods['Saturn']*t), (planet_distances['Enceladus']*scale)*sin(2*pi/Orbital_periods['Saturn']*t), 0)
    tethys.pos = saturn.pos + vector((planet_distances['Tethys']*scale)*cos(2*pi/Orbital_periods['Saturn']*t), (planet_distances['Tethys']*scale)*sin(2*pi/Orbital_periods['Saturn']*t), 0)
    dione.pos = saturn.pos + vector((planet_distances['Dione']*scale)*cos(2*pi/Orbital_periods['Saturn']*t), (planet_distances['Dione']*scale)*sin(2*pi/Orbital_periods['Saturn']*t), 0)
    rhea.pos = saturn.pos + vector((planet_distances['Rhea']*scale)*cos(2*pi/Orbital_periods['Saturn']*t), (planet_distances['Rhea']*scale)*sin(2*pi/Orbital_periods['Saturn']*t), 0)
    titan.pos = saturn.pos + vector((planet_distances['Titan']*scale)*cos(2*pi/Orbital_periods['Saturn']*t), (planet_distances['Titan']*scale)*sin(2*pi/Orbital_periods['Saturn']*t), 0)
    iapetus.pos= saturn.pos + vector((planet_distances['Iapetus']*scale)*cos(2*pi/Orbital_periods['Saturn']*t), (planet_distances['Iapetus']*scale)*sin(2*pi/Orbital_periods['Saturn']*t), 0)
    miranda.pos = uranus.pos + vector((planet_distances['Miranda']*scale)*cos(2*pi/Orbital_periods['Uranus']*t), (planet_distances['Miranda']*scale)*sin(2*pi/Orbital_periods['Uranus']*t), 0)
    ariel.pos = uranus.pos + vector((planet_distances['Ariel']*scale)*cos(2*pi/Orbital_periods['Uranus']*t), (planet_distances['Ariel']*scale)*sin(2*pi/Orbital_periods['Uranus']*t), 0)
    umbriel.pos = uranus.pos + vector((planet_distances['Umbriel']*scale)*cos(2*pi/Orbital_periods['Uranus']*t), (planet_distances['Umbriel']*scale)*sin(2*pi/Orbital_periods['Uranus']*t), 0)
    titania.pos = uranus.pos + vector((planet_distances['Titania']*scale)*cos(2*pi/Orbital_periods['Uranus']*t), (planet_distances['Titania']*scale)*sin(2*pi/Orbital_periods['Uranus']*t), 0)
    oberon.pos = uranus.pos + vector((planet_distances['Oberon']*scale)*cos(2*pi/Orbital_periods['Uranus']*t), (planet_distances['Oberon']*scale)*sin(2*pi/Orbital_periods['Uranus']*t), 0)
    triton.pos = neptune.pos + vector((planet_distances['Triton']*scale)*cos(2*pi/Orbital_periods['Neptune']*t), (planet_distances['Triton']*scale)*sin(2*pi/Orbital_periods['Neptune']*t), 0)
    proteus.pos = neptune.pos + vector((planet_distances['Proteus']*scale)*cos(2*pi/Orbital_periods['Neptune']*t), (planet_distances['Proteus']*scale)*sin(2*pi/Orbital_periods['Neptune']*t), 0)
    nereid.pos= neptune.pos + vector((planet_distances['Nereid']*scale)*cos(2*pi/Orbital_periods['Neptune']*t), (planet_distances['Nereid']*scale)*sin(2*pi/Orbital_periods['Neptune']*t), 0)

    # Prominent Asteroids in the Asteroid Belt animations
    ceres.pos = vector(scaled_planet_distances['Ceres']*cos(2*pi/Orbital_periods['Ceres']*t), scaled_planet_distances['Ceres']*sin(2*pi/Orbital_periods['Ceres']*t), 0)
    pallas.pos = vector(scaled_planet_distances['Pallas']*cos(2*pi/Orbital_periods['Pallas']*t), scaled_planet_distances['Pallas']*sin(2*pi/Orbital_periods['Pallas']*t), 0)
    juno.pos = vector(scaled_planet_distances['Juno']*cos(2*pi/Orbital_periods['Juno']*t), scaled_planet_distances['Juno']*sin(2*pi/Orbital_periods['Juno']*t), 0)
    vesta.pos = vector(scaled_planet_distances['Vesta']*cos(2*pi/Orbital_periods['Vesta']*t), scaled_planet_distances['Vesta']*sin(2*pi/Orbital_periods['Vesta']*t), 0)



    for asteroid in asteroids:
        asteroid.pos = rotate (asteroid.pos, angle=0.01, axis=vector(0,1,0))
      

    # Rotate the sun
    sun.rotate(angle=0.01, axis=vector(0,1,0))

    # Rotate Earth around its Y-axis
    earth.rotate(angle=0.01, axis=vector(0,1,0))
    # Rotate Moon around Earth
    moon.rotate(angle=0.01, axis=vector(0,1,0))

    # Rotate Mars around its Y-axis
    mars.rotate(angle=0.01, axis=vector(0,1,0))
    # Rotate Phobos around Mars
    phobos.rotate(angle=0.01, axis=vector(0,1,0))

    # Rotate Jupiter around its Y-axis
    jupiter.rotate(angle=0.01, axis=vector(0,1,0))

    # Rotate Saturn around its Y-axis
    saturn.rotate(angle=0.01, axis=vector(0,1,0))

    # Rotate Uranus around its Y-axis
    uranus.rotate(angle=0.01, axis=vector(0,1,0))

    # Rotate Neptune around its Y-axis
    neptune.rotate(angle=0.01, axis=vector(0,1,0))


    # Update labels
    mercury_label.pos = mercury.pos
    venus_label.pos = venus.pos
    earth_label.pos = earth.pos
    mars_label.pos = mars.pos
    jupiter_label.pos = jupiter.pos
    saturn_label.pos = saturn.pos
    uranus_label.pos = uranus.pos
    neptune_label.pos = neptune.pos

    # Update Label of Prominent Asteroids in the Asteroid Belt labels
    ceres_label.pos = ceres.pos
    pallas_label.pos = pallas.pos
    juno_label.pos = juno.pos
    vesta_label.pos = vesta.pos



