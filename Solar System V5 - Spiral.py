from vpython import mag2, norm, sphere, vector, rate, color, canvas, local_light, ring, label
import random
import math

# Gravitational constant
G = 6.67430e-11

# Scale factor for visualization
scale_factor = 1e-9

# Masses of the celestial bodies (in kg)
mass_sun = 1.989e30
mass_mercury = 3.3011e23
mass_venus = 4.8675e24
mass_earth = 5.972e24
mass_mars = 6.4171e23
mass_jupiter = 1.8982e27
mass_saturn = 5.6834e26
mass_uranus = 8.6810e25
mass_neptune = 1.02413e26
mass_moon = 7.342e22

# Initial positions (in meters) and velocities (in meters per second)
initial_positions = {
    "sun": vector(0, 0, 0),
    "mercury": vector(5.79e10, 0, 0),
    "venus": vector(1.082e11, 0, 0),
    "earth": vector(1.496e11, 0, 0),
    "mars": vector(2.279e11, 0, 0),
    "jupiter": vector(7.785e11, 0, 0),
    "saturn": vector(1.433e12, 0, 0),
    "uranus": vector(2.877e12, 0, 0),
    "neptune": vector(4.503e12, 0, 0),
    "moon": vector(1.496e11 + 3.844e8, 0, 0)
}

initial_velocities = {
    "sun": vector(0, 0, 0),
    "mercury": vector(0, 47400, 0),
    "venus": vector(0, 35000, 0),
    "earth": vector(0, 29800, 0),
    "mars": vector(0, 24100, 0),
    "jupiter": vector(0, 13100, 0),
    "saturn": vector(0, 9700, 0),
    "uranus": vector(0, 6800, 0),
    "neptune": vector(0, 5400, 0),
    "moon": vector(0, 29800 + 1022, 0)
}

# Create the scene with a top-down view
scene = canvas(width=1500, height=900)
scene.camera.pos = vector(0, 10, 0)  # Position the camera above the solar system
scene.camera.axis = vector(0, -1, 0)  # Point the camera downwards
scene.up = vector(1, 0, 0)  # Adjust the up vector for better perspective

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
sun = sphere(pos=initial_positions["sun"], radius=6.9634e8 * scale_factor, texture=sun_texture, make_trail=True, trail_size=0.5*0.5, trail_color=color.yellow, shininess=0.1, emissive=True)
sun_light = local_light(pos=sun.pos, color=color.white)

# Create the planets with realistic textures and colored trails
mercury = sphere(pos=initial_positions["mercury"], radius=2.4397e6 * scale_factor, texture=mercury_texture, make_trail=True, trail_size=1*0.1*scale_factor, trail_color=color.gray(0.5), shininess=0.1)
venus = sphere(pos=initial_positions["venus"], radius=6.0518e6 * scale_factor, texture=venus_texture, make_trail=True, trail_size=0.15*0.1, trail_color=color.orange, shininess=0.1)
earth = sphere(pos=initial_positions["earth"], radius=6.371e6 * scale_factor, texture=earth_texture, make_trail=True, trail_size=0.2*0.1, trail_color=color.blue, shininess=0.1)
mars = sphere(pos=initial_positions["mars"], radius=3.3895e6 * scale_factor, texture=mars_texture, make_trail=True, trail_size=0.18*0.1, trail_color=color.red, shininess=0.1)
jupiter = sphere(pos=initial_positions["jupiter"], radius=6.9911e7 * scale_factor, texture=jupiter_texture, make_trail=True, trail_size=0.3*0.1, trail_color=color.orange, shininess=0.1)
saturn = sphere(pos=initial_positions["saturn"], radius=5.8232e7 * scale_factor, texture=saturn_texture, make_trail=True, trail_size=0.25*0.1, trail_color=color.yellow, shininess=0.1)
uranus = sphere(pos=initial_positions["uranus"], radius=2.5362e7 * scale_factor, texture=uranus_texture, make_trail=True, trail_size=0.22*0.1, trail_color=color.cyan, shininess=0.1)
neptune = sphere(pos=initial_positions["neptune"], radius=2.4622e7 * scale_factor, texture=neptune_texture, make_trail=True, trail_size=0.21*0.1, trail_color=color.blue, shininess=0.1)

# Create the moon with a realistic texture and colored trail
moon = sphere(pos=initial_positions["moon"], radius=1.7371e6 * scale_factor, texture=moon_texture, make_trail=True, trail_size=0.5*0.1, trail_color=color.white, shininess=0.1)

# List of celestial bodies
bodies = [sun, mercury, venus, earth, mars, jupiter, saturn, uranus, neptune, moon]
masses = [mass_sun, mass_mercury, mass_venus, mass_earth, mass_mars, mass_jupiter, mass_saturn, mass_uranus, mass_neptune, mass_moon]
velocities = [initial_velocities["sun"], initial_velocities["mercury"], initial_velocities["venus"], initial_velocities["earth"], initial_velocities["mars"], initial_velocities["jupiter"], initial_velocities["saturn"], initial_velocities["uranus"], initial_velocities["neptune"], initial_velocities["moon"]]

# Time step (in seconds)
dt = 3600  # 1 hour

while True:
    rate(100)
    
    # Update positions and velocities based on gravitational forces
    for i in range(len(bodies)):
        force = vector(0, 0, 0)
        for j in range(len(bodies)):
            if i != j:
                r = bodies[j].pos - bodies[i].pos
                force += G * masses[i] * masses[j] / mag2(r) * norm(r)
        # Update velocity
        velocities[i] += force / masses[i] * dt
    
    # Update positions
    for i in range(len(bodies)):
        bodies[i].pos += velocities[i] * dt
    
    # Update the position of the light source
    sun_light.pos = sun.pos
    
    # Update the camera to follow the Sun
    scene.camera.pos = sun.pos + vector(0, 10, 0)
    scene.camera.axis = sun.pos - scene.camera.pos