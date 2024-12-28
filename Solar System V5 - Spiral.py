from vpython import sphere, vector, rate, color, canvas, local_light, ring, label
import random
import math

# Scale factor for visualization
scale_factor = 0.5

# Create the scene with a top-down view
scene = canvas(width=1500, height=900, background=color.black)
scene.camera.pos = vector(0, 10, 0)  # Position the camera above the solar system
scene.camera.axis = vector(0, -1, 0)  # Point the camera downwards
scene.up = vector(1, 0, 0)  # Adjust the up vector for better perspective

# Create a large sphere to simulate the background
background_sphere = sphere(pos=vector(0,0,0), radius=100*scale_factor, texture="https://upload.wikimedia.org/wikipedia/commons/8/82/Abell_2744_-_Hubble.jpeg", shininess=0, emissive=True)

# URLs for textures from NASA
sun_texture = "https://upload.wikimedia.org/wikipedia/commons/c/cb/Solarsystemscope_texture_2k_sun.jpg"
mercury_texture = "https://upload.wikimedia.org/wikipedia/commons/9/92/Solarsystemscope_texture_2k_mercury.jpg"
venus_texture = "https://upload.wikimedia.org/wikipedia/commons/4/40/Solarsystemscope_texture_2k_venus_surface.jpg"
earth_texture = "https://upload.wikimedia.org/wikipedia/commons/0/04/Solarsystemscope_texture_8k_earth_daymap.jpg"
mars_texture = "https://upload.wikimedia.org/wikipedia/commons/7/70/Solarsystemscope_texture_8k_mars.jpg"
jupiter_texture = "https://upload.wikimedia.org/wikipedia/commons/b/be/Solarsystemscope_texture_2k_jupiter.jpg"
saturn_texture = "https://upload.wikimedia.org/wikipedia/commons/e/ea/Solarsystemscope_texture_2k_saturn.jpg"
uranus_texture = "https://upload.wikimedia.org/wikipedia/commons/9/95/Solarsystemscope_texture_2k_uranus.jpg"
neptune_texture = "https://upload.wikimedia.org/wikipedia/commons/1/1e/Solarsystemscope_texture_2k_neptune.jpg"
moon_texture = "https://upload.wikimedia.org/wikipedia/commons/e/e1/FullMoon2010.jpg"

# Create the Sun with a realistic texture and light source
sun = sphere(pos=vector(0,0,0), radius=1*scale_factor, texture=sun_texture, make_trail=True, trail_size=0.5*0.5, trail_color=color.yellow, shininess=0.1, emissive=True)
sun_light = local_light(pos=sun.pos, color=color.white)

# Create solar flares
flare1 = sphere(pos=sun.pos + vector(0.6*scale_factor, 0, 0), radius=0.1*scale_factor, color=color.orange, emissive=True)
flare2 = sphere(pos=sun.pos + vector(-0.6*scale_factor, 0, 0), radius=0.1*scale_factor, color=color.red, emissive=True)
flare3 = sphere(pos=sun.pos + vector(0, 0.6*scale_factor, 0), radius=0.1*scale_factor, color=color.yellow, emissive=True)

# Create a dark spot on the Sun
dark_spot = ring(pos=sun.pos, axis=vector(0,1,0), radius=0.8*scale_factor, thickness=0.05*scale_factor, color=color.black)

# Create the planets with realistic textures and colored trails
mercury = sphere(pos=vector(0.39,0,0), radius=0.1*scale_factor, texture=mercury_texture, make_trail=True, trail_size=1*0.1*scale_factor, trail_color=color.gray(0.5), shininess=0.1)
venus = sphere(pos=vector(0.72,0,0), radius=0.15*scale_factor, texture=venus_texture, make_trail=True, trail_size=0.15*0.1, trail_color=color.orange, shininess=0.1)
earth = sphere(pos=vector(1,0,0), radius=0.2*scale_factor, texture=earth_texture, make_trail=True, trail_size=0.2*0.1, trail_color=color.blue, shininess=0.1)
mars = sphere(pos=vector(1.52,0,0), radius=0.18*scale_factor, texture=mars_texture, make_trail=True, trail_size=0.18*0.1, trail_color=color.red, shininess=0.1)
jupiter = sphere(pos=vector(5.2,0,0), radius=0.3*scale_factor, texture=jupiter_texture, make_trail=True, trail_size=0.3*0.1, trail_color=color.orange, shininess=0.1)
saturn = sphere(pos=vector(9.58,0,0), radius=0.25*scale_factor, texture=saturn_texture, make_trail=True, trail_size=0.25*0.1, trail_color=color.yellow, shininess=0.1)
uranus = sphere(pos=vector(19.22,0,0), radius=0.22*scale_factor, texture=uranus_texture, make_trail=True, trail_size=0.22*0.1, trail_color=color.cyan, shininess=0.1)
neptune = sphere(pos=vector(30.05,0,0), radius=0.21*scale_factor, texture=neptune_texture, make_trail=True, trail_size=0.21*0.1, trail_color=color.blue, shininess=0.1)

# Create the moon with a realistic texture and colored trail
moon = sphere(pos=earth.pos + vector(0.00257,0,0), radius=0.05*scale_factor, texture=moon_texture, make_trail=True, trail_size=0.5*0.1, trail_color=color.white, shininess=0.1)

# Create rings for Saturn, Uranus, and Neptune
saturn_ring = ring(pos=saturn.pos, axis=vector(0,1,0), radius=0.35*scale_factor, thickness=0.01*scale_factor, color=color.white)
uranus_ring = ring(pos=uranus.pos, axis=vector(0,1,0), radius=0.32*scale_factor, thickness=0.01*scale_factor, color=color.white)
neptune_ring = ring(pos=neptune.pos, axis=vector(0,1,0), radius=0.31*scale_factor, thickness=0.01*scale_factor, color=color.white)

# Create the prominent asteroids in the asteroid belt
ceres = sphere(pos=vector(2.77, 0, 0), radius=0.05*scale_factor, color=color.gray(0.5), make_trail=True, interval=10, retain=50, trail_radius=0.001, trail_color=color.gray(0.5), shininess=0.1)
vesta = sphere(pos=vector(2.36, 0, 0), radius=0.04*scale_factor, color=color.gray(0.5), make_trail=True, interval=10, retain=50, trail_radius=0.001, trail_color=color.gray(0.5), shininess=0.1)
pallas = sphere(pos=vector(2.77, 0, 0), radius=0.04*scale_factor, color=color.gray(0.5), make_trail=True, interval=10, retain=50, trail_radius=0.001, trail_color=color.gray(0.5), shininess=0.1)
hygiea = sphere(pos=vector(3.14, 0, 0), radius=0.04*scale_factor, color=color.gray(0.5), make_trail=True, interval=10, retain=50, trail_radius=0.001, trail_color=color.gray(0.5), shininess=0.1)

# Add labels for the asteroids
label_ceres = label(pos=ceres.pos, text='Ceres', xoffset=10, yoffset=10, space=30, height=10, border=4, font='sans')
label_vesta = label(pos=vesta.pos, text='Vesta', xoffset=10, yoffset=10, space=30, height=10, border=4, font='sans')
label_pallas = label(pos=pallas.pos, text='Pallas', xoffset=10, yoffset=10, space=30, height=10, border=4, font='sans')
label_hygiea = label(pos=hygiea.pos, text='Hygiea', xoffset=10, yoffset=10, space=30, height=10, border=4, font='sans')

# Create random asteroids in the asteroid belt
num_asteroids = 100
asteroids = []
for _ in range(num_asteroids):
    distance = random.uniform(2.1, 3.3)  # Distance between Mars and Jupiter
    angle = random.uniform(0, 2 * math.pi)
    radius = random.uniform(0.001, 0.005) * scale_factor  # Radius between 1 km and 500 km
    asteroid = sphere(pos=vector(distance * math.cos(angle), 0, distance * math.sin(angle)), radius=radius, color=color.gray(0.5), make_trail=True, interval=10, retain=50, trail_radius=0.001, trail_color=color.gray(0.5), shininess=0.1)
    asteroids.append(asteroid)

# Define the angular velocities of the planets (in radians per frame)
omega_mercury = 0.04
omega_venus = 0.03
omega_earth = 0.02
omega_mars = 0.01
omega_jupiter = 0.008
omega_saturn = 0.006
omega_uranus = 0.004
omega_neptune = 0.002

# Define the angular velocities of the asteroids (in radians per frame)
omega_ceres = 0.015
omega_vesta = 0.016
omega_pallas = 0.017
omega_hygiea = 0.014
omega_asteroid = 0.012

# Define the angular velocity of the moon
omega_moon = 0.1

# Define the rotation speeds of the planets (in radians per frame)
rotation_speed_mercury = 2 * 3.14159 / (1407.6 * 3600 / 50)
rotation_speed_venus = -2 * 3.14159 / (5832.5 * 3600 / 50)
rotation_speed_earth = 2 * 3.14159 / (24 * 3600 / 50)
rotation_speed_mars = 2 * 3.14159 / (24.6 * 3600 / 50)
rotation_speed_jupiter = 2 * 3.14159 / (9.9 * 3600 / 50)
rotation_speed_saturn = 2 * 3.14159 / (10.7 * 3600 / 50)
rotation_speed_uranus = -2 * 3.14159 / (17.2 * 3600 / 50)
rotation_speed_neptune = 2 * 3.14159 / (16.1 * 3600 / 50)

# Define the velocity of the sun
sun_velocity = vector(0.01, 0.01, 0.01)

# Initial positions of the planets relative to the Sun
initial_mercury_pos = mercury.pos - sun.pos
initial_venus_pos = venus.pos - sun.pos
initial_earth_pos = earth.pos - sun.pos
initial_mars_pos = mars.pos - sun.pos
initial_jupiter_pos = jupiter.pos - sun.pos
initial_saturn_pos = saturn.pos - sun.pos
initial_uranus_pos = uranus.pos - sun.pos
initial_neptune_pos = neptune.pos - sun.pos

# Initial positions of the asteroids relative to the Sun
initial_ceres_pos = ceres.pos - sun.pos
initial_vesta_pos = vesta.pos - sun.pos
initial_pallas_pos = pallas.pos - sun.pos
initial_hygiea_pos = hygiea.pos - sun.pos
initial_asteroid_pos = [asteroid.pos - sun.pos for asteroid in asteroids]

# Initial position of the moon relative to the Earth
initial_moon_pos = moon.pos - earth.pos

while True:
    rate(50)
    
    # Update the position of the Sun
    sun.pos += sun_velocity
    sun_light.pos = sun.pos  # Update light source position
    
    # Update the positions of the solar flares and dark spot relative to the Sun
    flare1.pos = sun.pos + vector(0.6*scale_factor, 0, 0)
    flare2.pos = sun.pos + vector(-0.6*scale_factor, 0, 0)
    flare3.pos = sun.pos + vector(0, 0.6*scale_factor, 0)
    dark_spot.pos = sun.pos
    
    # Update the positions of the planets relative to the Sun
    mercury.pos = initial_mercury_pos.rotate(angle=omega_mercury, axis=vector(0,1,0)) + sun.pos
    venus.pos = initial_venus_pos.rotate(angle=omega_venus, axis=vector(0,1,0)) + sun.pos
    earth.pos = initial_earth_pos.rotate(angle=omega_earth, axis=vector(0,1,0)) + sun.pos
    mars.pos = initial_mars_pos.rotate(angle=omega_mars, axis=vector(0,1,0)) + sun.pos
    jupiter.pos = initial_jupiter_pos.rotate(angle=omega_jupiter, axis=vector(0,1,0)) + sun.pos
    saturn.pos = initial_saturn_pos.rotate(angle=omega_saturn, axis=vector(0,1,0)) + sun.pos
    uranus.pos = initial_uranus_pos.rotate(angle=omega_uranus, axis=vector(0,1,0)) + sun.pos
    neptune.pos = initial_neptune_pos.rotate(angle=omega_neptune, axis=vector(0,1,0)) + sun.pos
    
    # Update the positions of the prominent asteroids relative to the Sun
    ceres.pos = initial_ceres_pos.rotate(angle=omega_ceres, axis=vector(0,1,0)) + sun.pos
    vesta.pos = initial_vesta_pos.rotate(angle=omega_vesta, axis=vector(0,1,0)) + sun.pos
    pallas.pos = initial_pallas_pos.rotate(angle=omega_pallas, axis=vector(0,1,0)) + sun.pos
    hygiea.pos = initial_hygiea_pos.rotate(angle=omega_hygiea, axis=vector(0,1,0)) + sun.pos
    
    # Update the positions of the random asteroids relative to the Sun
    for i, asteroid in enumerate(asteroids):
        asteroid.pos = initial_asteroid_pos[i].rotate(angle=omega_asteroid, axis=vector(0,1,0)) + sun.pos
    
    # Update the position of the moon relative to the Earth
    moon.pos = initial_moon_pos.rotate(angle=omega_moon, axis=vector(0,1,0)) + earth.pos
    
    # Rotate the planets on their axes
    mercury.rotate(angle=rotation_speed_mercury, axis=vector(0,1,0))
    venus.rotate(angle=rotation_speed_venus, axis=vector(0,1,0))
    earth.rotate(angle=rotation_speed_earth, axis=vector(0,1,0))
    mars.rotate(angle=rotation_speed_mars, axis=vector(0,1,0))
    jupiter.rotate(angle=rotation_speed_jupiter, axis=vector(0,1,0))
    saturn.rotate(angle=rotation_speed_saturn, axis=vector(0,1,0))
    uranus.rotate(angle=rotation_speed_uranus, axis=vector(0,1,0))
    neptune.rotate(angle=rotation_speed_neptune, axis=vector(0,1,0))
    
    # Update the positions of the rings relative to their planets
    saturn_ring.pos = saturn.pos
    uranus_ring.pos = uranus.pos
    neptune_ring.pos = neptune.pos
    
    # Update the positions of the labels relative to the asteroids
    label_ceres.pos = ceres.pos
    label_vesta.pos = vesta.pos
    label_pallas.pos = pallas.pos
    label_hygiea.pos = hygiea.pos
    
    # Update initial positions for the next frame
    initial_mercury_pos = mercury.pos - sun.pos
    initial_venus_pos = venus.pos - sun.pos
    initial_earth_pos = earth.pos - sun.pos
    initial_mars_pos = mars.pos - sun.pos
    initial_jupiter_pos = jupiter.pos - sun.pos
    initial_saturn_pos = saturn.pos - sun.pos
    initial_uranus_pos = uranus.pos - sun.pos
    initial_neptune_pos = neptune.pos - sun.pos
    initial_ceres_pos = ceres.pos - sun.pos
    initial_vesta_pos = vesta.pos - sun.pos
    initial_pallas_pos = pallas.pos - sun.pos
    initial_hygiea_pos = hygiea.pos - sun.pos
    initial_asteroid_pos = [asteroid.pos - sun.pos for asteroid in asteroids]
    initial_moon_pos = moon.pos - earth.pos
    
    # Update the camera to follow the Sun
    scene.camera.pos = sun.pos + vector(0, 10, 0)
    scene.camera.axis = sun.pos - scene.camera.pos
