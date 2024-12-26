from math import cos,sin,pi
import os
from vpython import button, canvas, local_light, ring, scene, sphere, vector, color, rate, wtext, label, textures

# constants and scale
AU=1.496e11 # Astronomical unit is 149.6 million kms
scale=1e-10 # Scale of the model
Vizualization_scale=10 #adjustable additional scale factor for better visualization
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
'Moon distance': 384400,

# Sun distance from the sun
'Sun': 0,
}

# Scaling Planet's radii

scaled_planet_radii = {planet: radius*scale*Vizualization_scale for planet, radius in planet_radii.items()}

# Scaling Planet's distances
scaled_planet_distances = {planet: distance*scale/Vizualization_scale for planet, distance in planet_distances.items()}



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
# Create the Moon of Earth
moon=sphere(pos=vector(scaled_planet_distances['Earth']+planet_distances['Moon distance']*scale,0,0), radius=scaled_planet_radii['Moon'], color=color.white, make_trail=True,trail_radius=scaled_planet_radii['Moon']*0.1,texture=textures.rough)

mars = sphere(pos=vector(scaled_planet_distances['Mars'],0,0), radius=scaled_planet_radii['Mars'], color=color.red, make_trail=True,trail_radius=scaled_planet_radii['Mars']*0.2,texture=textures.rough)
mars_label = label(pos=mars.pos, text=f"Mars\nType: Planet\nSpeed: {Orbital_speed['Mars']} km/s\nDistance: {planet_distances['Mars']} km\nOrbital Period: {Orbital_periods['Mars']} days", xoffset=20, yoffset=20, space=30, height=10, border=4, font='sans')
# Create Jupiter
jupiter = sphere(pos=vector(scaled_planet_distances['Jupiter'],0,0), radius=scaled_planet_radii['Jupiter'], color=color.orange, make_trail=True,trail_radius=scaled_planet_radii['Jupiter']*0.2)
jupiter_label = label(pos=jupiter.pos, text=f"Jupiter\nType: Planet\nSpeed: {Orbital_speed['Jupiter']} km/s\nDistance: {planet_distances['Jupiter']} km\nOrbital Period: {Orbital_periods['Jupiter']} days", xoffset=20, yoffset=20, space=30, height=10, border=4, font='sans')    
# Create Saturn
saturn = sphere(pos=vector(scaled_planet_distances['Saturn'],0,0), radius=scaled_planet_radii['Saturn'], color=color.yellow, make_trail=True,trail_radius=scaled_planet_radii['Saturn']*0.2)
saturn_ring = ring(pos=vector(scaled_planet_distances['Saturn'],0,0), axis=vector(0,0,1), radius=scaled_planet_radii['Saturn']*2, thickness=scaled_planet_radii['Saturn']*0.2, color=color.white)
saturn_label = label(pos=saturn.pos, text=f"Saturn\nType: Planet\nSpeed: {Orbital_speed['Saturn']} km/s\nDistance: {planet_distances['Saturn']} km\nOrbital Period: {Orbital_periods['Saturn']} days", xoffset=20, yoffset=20, space=30, height=10, border=4, font='sans')
# Create Uranus
uranus = sphere(pos=vector(scaled_planet_distances['Uranus'],0,0), radius=scaled_planet_radii['Uranus'], color=color.cyan, make_trail=True,trail_radius=scaled_planet_radii['Uranus']*0.2)
uranus_ring = ring(pos=vector(scaled_planet_distances['Uranus'],0,0), axis=vector(0,0,1), radius=scaled_planet_radii['Uranus']*1.8, thickness=scaled_planet_radii['Uranus']*0.1, color=color.gray(0.5))
uranus_label = label(pos=uranus.pos, text=f"Uranus\nType: Planet\nSpeed: {Orbital_speed['Uranus']} km/s\nDistance: {planet_distances['Uranus']} km\nOrbital Period: {Orbital_periods['Uranus']} days", xoffset=20, yoffset=20, space=30, height=10, border=4, font='sans')
# Create Neptune
neptune = sphere(pos=vector(scaled_planet_distances['Neptune'],0,0), radius=scaled_planet_radii['Neptune'], color=color.blue, make_trail=True,trail_radius=scaled_planet_radii['Neptune']*0.2)
neptune_ring = ring(pos=vector(scaled_planet_distances['Neptune'],0,0), axis=vector(0,0,1), radius=scaled_planet_radii['Neptune']*1.5, thickness=scaled_planet_radii['Neptune']*0.1, color=color.gray(0.5))
neptune_label = label(pos=neptune.pos, text=f"Neptune\nType: Planet\nSpeed: {Orbital_speed['Neptune']} km/s\nDistance: {planet_distances['Neptune']} km\nOrbital Period: {Orbital_periods['Neptune']} days", xoffset=20, yoffset=20, space=30, height=10, border=4, font='sans')




# Set Scene Size
scene.width = 1400 # Set the width of the scene
scene.height = 800 # Set the height of the scene


# Set Initial camera position
initial_camera_pos = vector(scaled_planet_distances['Earth'] * 1, scaled_planet_distances['Earth'] * 1, scaled_planet_distances['Earth'] * 1)
initial_camera_axis = vector(-scaled_planet_distances['Earth']*1, -scaled_planet_distances['Earth']*1, -scaled_planet_distances['Earth']*1)
scene.camera.pos = initial_camera_pos
scene.camera.axis = initial_camera_axis
scene.up = vector(0, 1, 0)  # Set the up direction

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
    moon.pos =earth.pos + vector((planet_distances['Moon distance']*scale)*cos(2*pi/Orbital_periods['Moon']*t), (planet_distances['Moon distance']*scale)*sin(2*pi/Orbital_periods['Moon']*t), 0)
    # Rotate Earth around its Y-axis
    earth.rotate(angle=0.01, axis=vector(0,1,0))
    # Update labels
    mercury_label.pos = mercury.pos
    venus_label.pos = venus.pos
    earth_label.pos = earth.pos
    mars_label.pos = mars.pos
    jupiter_label.pos = jupiter.pos
    saturn_label.pos = saturn.pos
    uranus_label.pos = uranus.pos
    neptune_label.pos = neptune.pos