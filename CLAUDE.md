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
- Base is symmetric about the tab centerline (Y=0), ±53 mm front/back,
  so 180°-flipped brackets keep the same footprint — a row of
  alternating brackets forms one continuous straight base edge
- Puzzle-tab interlocking on side arm edges, front + rear pairs
  (reversed polarity so brackets mate even when one is flipped 180°)
- Corner bracket (separate part) wraps a cube's front-left corner:
  flat base mates to the valve bracket's LEFT edge via the puzzle
  tab/notch; two upright walls (front along X, left along Y) bolt to
  the cube's faces. Each wall has two 4 mm countersunk screw holes.

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
- `corner_bracket.step` — 1" L-bracket (box-face mount), for Fusion 360
- `corner_bracket.stl` — corner bracket, for Luban / 3D printing
- `bracket_assembly.step` — bracket + corner bracket + valve reference (fit-check)
- `bracket_assembly.png` — 3D visualization (two-angle view)

## Build
```
/usr/bin/python3 bracket_gen.py
```
Requires: cadquery, matplotlib, numpy — installed only under macOS system
Python 3.9.6 (`/usr/bin/python3`), NOT the default `python3` on PATH.

## Design Notes
- Wall/floor thickness: 1.5 mm
- Body cradle: 54 mm W inner (57 outer), extended 6 mm rear + 5 mm front
- Base footprint: ~144 mm W x 106 mm D (Y symmetric ±53 about tab line)
- SIDE_EXT = 10 mm: side (X) arms + base extend 10 mm beyond port tip
  each side (half-width ARM_X = 72; round side channels extend with them)
- Port channels: semi-circular (R=13.5 mm clearance, R=15 mm outer)
  Arms extend from cradle wall to barb tip, open top for drop-in
- Port center height: Z = 16.5 mm (channel bottom 1.5 mm above base top)
- Arm top: Z = 16.5 mm (true half-pipe)
- Back wall solid; front + L/R have keyhole cutouts (circle + slot)
- Puzzle tabs: R=6 mm knob, 3 mm high, 0.2 mm tolerance, rear + front pairs per side
  Rear: right=knob, left=indent; Front: reversed (right=indent, left=knob)
  Symmetric at Y = ±16.25 mm so 180° rotated brackets still mate
- Side arms symmetric (4 mm extension front + back) for tab backing
- Corner bracket (`make_corner_bracket`): wraps a cube's front-left
  vertical corner. Flat base (1" / 25.4 mm wide along X) mates to the
  valve bracket's left edge (X = -72) via the puzzle tab + notch
  (mirrored: rear knob, front notch), backed by a low rib (RIB_W = 12 mm,
  height = 3 mm = tab height) for notch depth. Base spans Y = -53 to +53 (flush
  with both valve base edges); front wall sits on the +53 edge. Two
  upright walls, 3 mm thick, WALL_H = 28 mm:
  FRONT wall (along X, at Y = +53) bolts to the cube front face; LEFT
  wall (along Y, X = -97.4, no base) bolts to the cube left face. Each
  wall has two 4 mm countersunk holes (CSK_HEAD = 8 mm) for sheet-metal
  screws. Cube assumed behind in +Y
- Countersink cutter helper `csk_cutter()` (through-hole + cone recess)
- Uses `cq_box()`, `cq_cyl_x()`, `cq_cyl_y()`, `cq_cyl_z()` helpers
- Generates STEP, STL (bracket, test, corner), assembly STEP, 4-view PNG
