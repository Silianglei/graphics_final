# Graphics Final Project: Proposal

### Siliang Lei (Period 4)

## Features To Implement
1. light
    - Add a light to the symbol table
    - When calculating diffuse and specular: loop through all the lights.
2. set
    - Assign a value to a knob
3. saveknobs
    - Save current knob values to a list
4. tween
    - Produce an animation by going between two knob lists
5. save_coordinate_system
    - Save a copy of the top of the stack to the symbol table
    - use this coordinate system when drawing shapes (extra argument required)
## Features to Implement If I Have Time
1. New primitive shapes (pyramid)
2. Anti-aliasing / Super-sampling
    - Reduce pixelated edges by calculating a higher resolution version of the image then reducing it to the intended size
