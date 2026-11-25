**Physics Simulations / Particle Systems**
- Position is a vector (x, y) (arrows from origin because position is relative to origin)
- Frame by frame animation: main loop that executes the same function every frame with changes every time
- Update position in loop: calculate to simulate physics - use equations of physics so that computer does it automatically
- To update position, need another vector: velocity
- Need to add velocity to position: vector 1 (position) + vector 2 (velocity)
- If velocity always the same when added: object moves at constant speed
- Forces: most obvious one is gravity
- Add another vector for gravity (or an "acceleration"): applies to velocity, and then velocity applies to position
- In every iteration of loop, velocity is modified more and more by acceleration
- Ballistics
- Acceleration can change also: between two planets with different gravitations ex.
- Springs: acceleration varies based on proximity between springs
- Derivatives and integrals vs simulation: not as perfect... numerical integration method instead of analytical integration
- Slope of position trajectory is velocity: derivative
- Slope of velocity is acceleration: derivative

More on forces:
- a = F / m (acceleration = force / mass) EXCEPT gravity (scales with mass)

Integration Basics: https://gafferongames.com/post/integration_basics/
Particle Systems: https://natureofcode.com/particles/
Simulation and Numerical Integration: https://physics.umd.edu/hep/drew/numerical_integration/
Euler and Verlet Integration for Particle Physics: https://www.gorillasun.de/blog/euler-and-verlet-integration-for-particle-physics/
Collision Detection: https://happycoding.io/tutorials/processing/collision-detection
Particle Engine github repository: https://github.com/jasonmayes/Particle-Engine
Programming Chaos video on Particle Swarms: https://www.youtube.com/watch?v=G0RQRmwoiD0