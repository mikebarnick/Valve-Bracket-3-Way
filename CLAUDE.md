# Valve Bracket 3-Way Project

## Working Directory
`/Users/mike/Documents/3D Print Files/Valve Bracket 3-Way/`

## Overview
Mounting bracket for a motorized 3-way mixing/diverting valve (hydronic/HVAC).
The valve has a grey/white plastic actuator housing on top and three brass
barb/threaded ports in a T-configuration (Supply, Return, and third port).
Wires exit the actuator for motor control.

## Component Dimensions (from caliper photos)
- Valve body (brass): 52 mm W x 34 mm D x 30 mm H (estimated)
- Actuator housing: ~55 x 50 x 45 mm (sits on top of body)
- Overall height (body + actuator): ~79 mm (IMG_0904 caliper)
- Overall width (barb to barb): ~122 mm (IMG_0905 caliper)
- Body depth (front-back): 34 mm (IMG_0902 caliper)
- Port layout: T-configuration, three 1/2" NPT with hose barb adapters
- Hose barbs accept 1/2" ID hose

## Reference Photos
See `Sample pics/` folder:
- IMG_0902: Caliper measuring body depth (34 mm)
- IMG_0903: Top-down view showing T-port layout and "Supply" label
- IMG_0904: Side view with caliper height measurement (79 mm)
- IMG_0905: "Return" side with caliper width measurement (122 mm)
- IMG_0906: Angled view showing all three ports
- IMG_0909: Bottom view — hex casting, T-junction, port boss layout

## Bracket Requirements
- Base mount with drop-in assembly from above
- 1 mm clearance between bracket inner walls and valve body
- 1.5 mm wall and base thickness
- Full bracket: 35 mm tall; test bracket: 20 mm tall
- Back wall: SOLID (no opening)
- Front/side walls: keyhole cutouts (semi-circular + slot to top)
- Half-pipe arms along all 3 ports from body to barb tip (~210° wrap)
- Base spans full assembly width (130 mm inc. tabs) for stability
- Puzzle-tab interlocking on body-cradle zone of side edges
  (4-segment alternating tab/slot, symmetric under 180° rotation)

## Coordinate System
- X axis: left-right (width)
- Y axis: front-back (depth); front = center port direction
- Z axis: up; Z=0 at base bottom

## Files
- `bracket_gen.py` — Python script (cadquery + matplotlib), regenerates all outputs
- `bracket.step` — full bracket (35 mm), for Fusion 360
- `bracket.stl` — full bracket, for Luban / 3D printing
- `bracket_test.step` — test bracket (20 mm), for Fusion 360
- `bracket_test.stl` — test bracket, for Luban / 3D printing
- `bracket_assembly.step` — bracket + valve reference (fit-check)
- `bracket_assembly.png` — 3D visualization (two-angle view)

## Build
```
python3 bracket_gen.py
```
Requires: cadquery, matplotlib, numpy

## Design Notes
- Wall/floor thickness: 1.5 mm
- Body cradle: 54 mm W x 36 mm D inner (57 x 39 outer)
- Base footprint: 130 mm W x 72.5 mm D (wide for port arms + tabs)
- Port channels: semi-circular (R=11.5 mm clearance, R=13 mm outer)
  Arms extend from cradle wall to barb tip, open top for drop-in
- Port center height: Z = 15 mm; arm top: Z = 17 mm
- Back wall solid; front + L/R have keyhole cutouts (circle + slot)
- Puzzle tabs: 3 mm protrusion, 0.2 mm tolerance, 4 segments per side
  Located on body-cradle zone only (Y = ±19.5 mm) so rotation works
- Uses `cq_box()`, `cq_cyl_x()`, `cq_cyl_y()` helpers
- Generates STEP, STL, assembly STEP, and 3-view PNG in one script
