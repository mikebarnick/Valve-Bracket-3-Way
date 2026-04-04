# Valve Bracket 3-Way Project

## Working Directory
`/Users/mike/Documents/3D Print Files/Valve Bracket 3-Way/`

## Overview
Mounting bracket for a motorized 3-way mixing/diverting valve (hydronic/HVAC).
The valve has a grey/white plastic actuator housing on top and three brass
barb/threaded ports in a T-configuration (Supply, Return, and third port).
Wires exit the actuator for motor control.

## Component Dimensions
(Measurements needed from calipers in reference photos — verify with user)
- Actuator body: ~rectangular, approximate dimensions TBD
- Port layout: T-configuration, three brass barb fittings
- Overall height (with ports): TBD
- Overall width: TBD
- Port diameter: TBD
- Port spacing: TBD

## Reference Photos
See `Sample pics/` folder (IMG_0902 through IMG_0906):
- IMG_0902: Caliper measuring port/fitting
- IMG_0903: Top-down view showing T-port layout and "Supply" label
- IMG_0904: Side view with caliper height measurement
- IMG_0905: "Return" side with caliper width measurement
- IMG_0906: Angled view showing all three ports

## Bracket Requirements
- TBD — define with user (wall mount? base mount? orientation?)
- 1mm clearance between bracket inner walls and valve body (per Fan Bracket convention)

## Coordinate System
- TBD — define once valve orientation and mounting style are decided

## Files
- `bracket_gen.py` — Python script (cadquery + matplotlib), regenerates all outputs
- `bracket.step` — bracket only, for Fusion 360
- `bracket.stl` — bracket only, for Luban / 3D printing
- `bracket_assembly.step` — bracket + valve reference (fit-check)
- `bracket_assembly.png` — 3D visualization (two-angle view)

## Build
```
python3 bracket_gen.py
```
Requires: cadquery, matplotlib, numpy

## Design Notes
- Wall/floor thickness: 1.5 mm (same as Fan Bracket)
- Follow same CadQuery + matplotlib pattern as Fan Bracket project
- Use `box()`, `cyl_z()` helper functions for geometry
- Generate STEP, STL, assembly STEP, and assembly PNG in one script
