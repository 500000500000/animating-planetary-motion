# Animating Planetary Motion

The functions X(t) and Y(t) provide coordinates for a planet moving in an elliptical orbit with precession.

## Input Parameters

a = semi-major axis

b = semi-minor axis

c = focal distance such that a^2 = b^2 + c^2

T = period

alphaTolerance = tolerance in radians

P = period of precession

H = 2 * pi * a * b / P    use this formula, or set H = 0 to turn off precession

## Running The Program

Running the program calls X(t) and Y(t) to produce an animation using parameters:

totalTime = time of animation in seconds

timeStep = time step in seconds

## Output

The animation may be saved as an animated gif, if desired.
