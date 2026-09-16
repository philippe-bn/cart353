**Jake - Simple Game Physics**
Brief History:
- Super Mario
- Rigid Body Simulation
- Ragdoll Physics (RDR, GTA)
Integration:
- Predicting outcomes based on the laws of physics
- Euler method
    - Steps
- Euler-Cromer or semi-implicit Euler method
    - Update velocity to update position (preserves energy well)
- Runge-Kutta family
    - Takes more accurate average step (reduces error of Euler method, more predictable arcs, projectiles)
Collisions:
- Circle point collision: check distance of point from circle and if less than radius, collision detected
- Circle circle collision: checks against sum of the radii
- Rectangles: check if sides are past other sides / overlap on all sides
- Many objects: iterate through array of objects to detect for collision
- Grid-based collisions: store information about location in grid (2D yes/no object presence in grid)
- Separating Axis Theorem for convex polygon collision: check projections of edges
Questions:
- Ease of implementation; most game engines have physics engines

**Yelena - Particle Systems**
Making effects with simple particles
Fire - Smoke - Rain - Sparks
What is it:
- Many particles work together to make one effect
- Each particle has;
    - Position
    - Velocity
    - Acceleration
    - Lifespan
    - Appearance
How does it move:
- Acceleration
- Update velocity
- Update position
How do they get generated:
- Emitter
- Small changes make the effect look more natural
- Simple rules can create complexity
Calculating movement:
- Euler (position + speed + acceleration) vs verlet (current position + difference between current position and last position)