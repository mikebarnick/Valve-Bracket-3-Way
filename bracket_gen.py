#!/usr/bin/env python3
"""
Valve Bracket 3-Way — bracket_gen.py
Form-fitting bracket for M-Flo 3-way motorized valve.
Half-pipe arms wrap snugly around each port from body to barb tip.
Back wall solid (extended 6mm); front/sides have keyhole cutouts.
Centered puzzle-piece connector on each side for joining brackets.

Usage: python3 bracket_gen.py
Requires: cadquery, matplotlib, numpy
"""

import cadquery as cq
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import os

DIR = os.path.dirname(os.path.abspath(__file__))

# ─── Valve dimensions (from caliper photos + bottom view) ────────
VALVE_W    = 52.0    # body envelope width L-R
VALVE_D    = 34.0    # body depth F-B (IMG_0902 caliper)
VALVE_H    = 30.0    # body height (est.)
PORT_R     = 10.5    # port pipe radius (1/2" NPT ~21 mm OD)
PORT_LEN   = 35.0    # port protrusion: body face → barb tip
PORT_ZFRAC = 0.45    # port center height / body height

# ─── Actuator (reference model only) ─────────────────────────────
ACT_W = 55.0;  ACT_D = 50.0;  ACT_H = 45.0

# ─── Bracket parameters ─────────────────────────────────────────
CLR    = 1.0
WALL   = 1.5
BASE   = 1.5
FULL_H = 35.0
TEST_H = 20.0

# ─── Geometry adjustments ────────────────────────────────────────
BACK_EXT      = 6.0   # cradle extends 6 mm rearward
FRONT_EXT     = 5.0   # cradle extends 5 mm forward
ARM_BACK_EXT  = 4.0   # side arms extend 4 mm rearward
ARM_FRONT_EXT = 4.0   # side arms extend 4 mm forward (front puzzle tabs)
PORT_XD       = 7.0   # ALL port channels +7 mm diameter
SIDE_EXT      = 10.0  # side (X) arms + base extend 10 mm beyond port tip each side

# ─── Derived: body cradle ────────────────────────────────────────
IW  = VALVE_W + 2 * CLR       # 54
OW  = IW + 2 * WALL           # 57

# Cradle outer box (extended rearward + forward)
CRADLE_D  = VALVE_D + 2 * CLR + 2 * WALL + BACK_EXT + FRONT_EXT  # 50
CRADLE_CY = (-BACK_EXT + FRONT_EXT) / 2                            # -0.5

# Inner cavity fills cradle with uniform 1.5 mm walls on all sides
ID_INNER  = CRADLE_D - 2 * WALL       # 42  (bigger interior)
CAV_CY    = CRADLE_CY                 # -3  (centered with cradle)

# ─── Derived: port channels (uniform +4 mm diameter) ────────────
PCR   = PORT_R + CLR + PORT_XD / 2    # 13.5  all ports same radius
ARM_R = PCR + WALL                    # 15.0  arm outer radius (all ports)
PCZ   = BASE + PCR + 1.5               # 16.5  port center Z (channel bottom 1.5 mm above base top)
ARM_H = PCZ                            # 16.5  arm top = port center (true half-pipe)

# Side arm Y range: symmetric when ARM_BACK_EXT == ARM_FRONT_EXT
ARM_CY = -(ARM_BACK_EXT - ARM_FRONT_EXT) / 2   # 0
ARM_YD = 2 * ARM_R + ARM_BACK_EXT + ARM_FRONT_EXT  # 38  total Y depth of side arms

# ─── Derived: base footprint ────────────────────────────────────
ARM_X = VALVE_W / 2 + PORT_LEN + CLR + SIDE_EXT  # 72  half-width (side arm tip)
ARM_Y = VALVE_D / 2 + PORT_LEN + CLR  # 53  front arm tip Y
BK_Y  = -(CRADLE_D / 2 + abs(CRADLE_CY))  # -25.5
FR_Y  = ARM_Y                              # 53

# ─── Corner bracket (wraps a cube's front-left corner) ──────────
CB_W     = 25.4   # base width along X (1"), mate edge → left edge
CB_T     = 3.0    # flange / wall thickness
WALL_H   = 28.0   # cube-mount wall height (Z)
RIB_W    = 12.0   # mate-edge rib width (X) — hosts tab + notch
RIB_H    = 3.0    # mate-edge rib height (Z) — just backs the 3 mm notch (= PZ_H)
FB_LEN   = 28.0   # left wall length along Y
CSK_D    = 4.0    # countersunk screw clearance dia (sheet-metal)
CSK_HEAD = 8.0    # countersink head dia
CSK_DEP  = 2.3    # countersink depth

# ─── Puzzle-piece connectors (rear + front, reversed for 180° mating) ─
PZ_R   = 6.0    # knob radius
PZ_H   = 3.0    # knob/notch height (keep == RIB_H)
PZ_TOL = 0.2    # fit clearance
# Rear tabs: center between channel back edge and arm back edge
_arm_back  = ARM_CY - ARM_YD / 2      # -19
PZ_Y       = (_arm_back + (-PCR)) / 2 # -16.25
# Front tabs: center between channel front edge and arm front edge
_arm_front = ARM_CY + ARM_YD / 2      # +19
PZ_Y_FRONT = (_arm_front + PCR) / 2   # +16.25  (== -PZ_Y)

OVL = 0.1      # boolean overlap


# ─── geometry helpers ────────────────────────────────────────────

def cq_box(x, y, z, w, d, h):
    """Axis-aligned box centered at (x,y), bottom at z."""
    return (cq.Workplane("XY").workplane(offset=z)
            .center(x, y).box(w, d, h, centered=(True, True, False)))

def cq_cyl_x(y, z, r, x0, x1):
    """Cylinder along X, center-line at (y, z)."""
    return (cq.Workplane("YZ").workplane(offset=min(x0, x1))
            .center(y, z).circle(r).extrude(abs(x1 - x0)))

def cq_cyl_y(x, z, r, y0, y1):
    """Cylinder along Y, center-line at (x, z)."""
    # XZ workplane normal = -Y: place at max Y, extrude toward min Y
    length = abs(y1 - y0)
    return (cq.Workplane("XZ").workplane(offset=-max(y0, y1))
            .center(x, z).circle(r).extrude(length))

def cq_cyl_z(x, y, r, z0, z1):
    """Cylinder along Z at (x, y)."""
    return (cq.Workplane("XY").workplane(offset=min(z0, z1))
            .center(x, y).circle(r).extrude(abs(z1 - z0)))

def csk_cutter(pnt, dir_vec, r_hole, r_head, csk_dep, thru):
    """Countersunk-hole cutter: through-cylinder + conical head recess.
    Drills from surface `pnt` along `dir_vec`; head recess opens at the
    surface (flush flat-head screw). Returns a Solid for .cut()."""
    surf = cq.Vector(*pnt)
    d    = cq.Vector(*dir_vec)
    cyl  = cq.Solid.makeCylinder(r_hole, thru, surf.sub(d.multiply(0.1)), d)
    cone = cq.Solid.makeCone(r_head, r_hole, csk_dep, surf, d)
    return cyl.fuse(cone)


# ─── embossed arrow helper ───────────────────────────────────────

def make_arrow_xy(x, y, direction, z_surf, emboss=0.8):
    """Embossed arrow on a horizontal surface, protruding upward (+Z).
    x, y: center position
    z_surf: Z of the surface to emboss on
    direction: 'left' (-X), 'right' (+X), 'forward' (+Y)
    """
    # Arrow pointing RIGHT in XY plane: 12mm long, 6mm head, 2mm shaft
    pts = [
        (6, 0), (1, 3), (1, 1), (-6, 1), (-6, -1), (1, -1), (1, -3)
    ]
    if direction == 'left':
        pts = [(-px, py) for px, py in pts]
    elif direction == 'forward':
        pts = [(-py, px) for px, py in pts]   # rotate 90° CCW → points +Y

    ovl = 0.15
    wp = (cq.Workplane("XY")
          .workplane(offset=z_surf - ovl)
          .center(x, y))
    s = wp.moveTo(*pts[0])
    for p in pts[1:]:
        s = s.lineTo(*p)
    return s.close().extrude(emboss + ovl)


# ─── bracket builder ─────────────────────────────────────────────

def make_bracket(h):
    wh     = h - BASE
    slot_h = h - PCZ + 0.1

    sa_start = OW / 2 - OVL
    sa_len   = ARM_X - sa_start
    fa_start = CRADLE_CY + CRADLE_D / 2 - OVL  # cradle front edge
    fa_len   = ARM_Y - fa_start
    # base plate symmetric about Y=0 (the tab centerline) so a 180°-flipped
    # bracket keeps the same footprint — alternating bases form one long edge
    base_d   = 2 * ARM_Y    # 106  (back extended to match the front +53)
    base_cy  = 0.0

    # ── 1. solid volumes ─────────────────────────────────────
    # body cradle (extended rearward)
    b = cq_box(0, CRADLE_CY, 0, OW, CRADLE_D, h)

    # base plate (full width + front arm)
    b += cq_box(0, base_cy, 0, 2 * ARM_X, base_d, BASE)

    # side arm blocks (extended rearward by ARM_BACK_EXT)
    for s in (1, -1):
        b += cq_box(s * (sa_start + sa_len / 2), ARM_CY, 0,
                     sa_len, ARM_YD, ARM_H)

    # front arm block (same width as side arms)
    b += cq_box(0, fa_start + fa_len / 2, 0,
                 ARM_YD, fa_len, ARM_H)

    # ── 2. subtract inner cavity (expanded, all walls 1.5 mm) ──
    b -= cq_box(0, CAV_CY, BASE, IW, ID_INNER, wh + 0.1)

    # ── 3. Semi-circular channels (half-pipe, open top for drop-in) ─
    # Side ports — cylinder for curved bottom half
    b -= cq_cyl_x(0, PCZ, PCR, -(ARM_X+1), ARM_X+1)
    # Side ports — rect slot above port center (opens top half)
    b -= cq_box(0, 0, PCZ,
                 2*(ARM_X+1), 2*PCR, slot_h)

    # Front port — cylinder for curved bottom half
    b -= cq_cyl_y(0, PCZ, PCR, 0, ARM_Y+1)
    # Front port — rect slot above port center (opens top half)
    b -= cq_box(0, (ARM_Y+1)/2, PCZ,
                 2*PCR, ARM_Y+1, slot_h)

    # ── 5. puzzle-piece connectors (rear + front, reversed for 180° mating) ─
    # Rear: right=knob, left=indent
    b += cq_cyl_z(ARM_X, PZ_Y, PZ_R, 0, PZ_H)
    b -= cq_cyl_z(-ARM_X, PZ_Y, PZ_R + PZ_TOL, -0.1, PZ_H + 0.2)
    # Front: right=indent, left=knob (reversed so flipped bracket still mates)
    b -= cq_cyl_z(ARM_X, PZ_Y_FRONT, PZ_R + PZ_TOL, -0.1, PZ_H + 0.2)
    b += cq_cyl_z(-ARM_X, PZ_Y_FRONT, PZ_R, 0, PZ_H)

    # ── 6. embossed arrows on cavity floor (visible from top) ──
    # Positioned behind the valve body (Y=-22), clear of port channels
    arr_y = -22.0
    b += make_arrow_xy(-15, arr_y, 'left',    BASE)
    b += make_arrow_xy(  0, arr_y, 'forward', BASE)
    b += make_arrow_xy( 15, arr_y, 'right',   BASE)

    return b


# ─── corner bracket (L-bracket) ──────────────────────────────────

def make_corner_bracket():
    """Corner bracket wrapping a cube's front-left vertical corner.

    A flat base (like the main bracket) mates to the valve bracket's
    LEFT edge with the puzzle tab + notch. Two upright walls form an L
    in plan view:
      • front wall — runs along X, bolts to the cube's FRONT (-Y) face
        (this is the part the base attaches to)
      • left wall  — runs along Y, no base, bolts to the cube's LEFT
        (-X) face
    Each wall has two 4 mm countersunk holes for sheet-metal screws.
    The cube sits behind in +Y; its front-left corner is at (x_lf, y_cf).
    Returned in world coords registered to the bracket's left side.
    """
    x_mate = -ARM_X              # -62.0  mate edge (= valve left edge)
    x_lf   = x_mate - CB_W       # -87.4  cube left face / base left edge
    x_out  = x_lf - CB_T         # -90.4  outer face of left wall
    y_cf   =  ARM_Y             # +53.0  front wall — flush w/ valve base front edge
    y_bk   = -ARM_Y             # -53.0  base back edge — flush w/ valve base back edge
    y_b0   = y_cf - CB_T        # +50.0  inner face of front wall
    y_b1   = y_b0 + FB_LEN      # +78.0  far end of left wall

    # base plate — extends from the mate rib forward to the front wall
    c  = cq_box((x_lf + x_mate) / 2, (y_bk + y_cf) / 2, 0,
                CB_W, y_cf - y_bk, BASE)
    # mate-edge rib — gives the tab + notch real depth
    c += cq_box(x_mate - RIB_W / 2, 0, 0, RIB_W, ARM_YD, RIB_H)
    # front wall (runs along X) — bolts to cube front face
    c += cq_box((x_out + x_mate) / 2, y_cf - CB_T / 2, 0,
                x_mate - x_out, CB_T, WALL_H)
    # left wall (runs along Y, no base) — bolts to cube left face
    c += cq_box((x_out + x_lf) / 2, (y_b0 + y_b1) / 2, 0,
                CB_T, FB_LEN, WALL_H)

    # puzzle connector mirroring the valve's left edge:
    #   rear = knob (fills valve's indent), front = notch (takes valve's knob)
    c += cq_cyl_z(x_mate, PZ_Y, PZ_R, 0, PZ_H)
    c -= cq_cyl_z(x_mate, PZ_Y_FRONT, PZ_R + PZ_TOL, -0.1, PZ_H + 0.2)

    rh, hh = CSK_D / 2, CSK_HEAD / 2
    # front-wall screws (drill +Y into cube front face)
    for xc in (x_out + 5.0, x_mate - 5.0):
        c = c.cut(csk_cutter((xc, y_b0, WALL_H / 2), (0, 1, 0),
                             rh, hh, CSK_DEP, CB_T + 3.0))
    # left-wall screws (drill +X into cube left face)
    for yc in (y_b0 + 6.0, y_b1 - 6.0):
        c = c.cut(csk_cutter((x_out, yc, WALL_H / 2), (1, 0, 0),
                             rh, hh, CSK_DEP, CB_T + 3.0))
    return c


# ─── valve reference model ───────────────────────────────────────

def make_valve():
    v  = cq_box(0, 0, 0, VALVE_W, VALVE_D, VALVE_H)
    pz = VALVE_H * PORT_ZFRAC

    v += cq_cyl_x(0, pz, PORT_R, -(VALVE_W / 2 + PORT_LEN), -VALVE_W / 2)
    v += cq_cyl_x(0, pz, PORT_R,   VALVE_W / 2, VALVE_W / 2 + PORT_LEN)
    v += cq_cyl_y(0, pz, PORT_R, VALVE_D / 2, VALVE_D / 2 + PORT_LEN)
    v += cq_box(0, 0, VALVE_H, ACT_W, ACT_D, ACT_H)
    return v


# ─── tessellation → matplotlib ──────────────────────────────────

def tess(shape, tol=0.5):
    out = []
    for face in shape.faces().vals():
        vs, ts = face.tessellate(tol)
        for t in ts:
            out.append(np.array([[vs[t[j]].x, vs[t[j]].y, vs[t[j]].z]
                                  for j in range(3)]))
    return out


def render_png(bracket, valve, corner, path):
    fig = plt.figure(figsize=(16, 10))
    fig.patch.set_facecolor("white")

    bt = tess(bracket, 0.3)
    ct = tess(corner, 0.3)
    vt = [tri + [0, 0, BASE] for tri in tess(valve, 0.5)]

    views = [
        (25, -50, "Front-left", True),
        (25,  50, "Front-right", True),
        (75, -90, "Top (bracket only)", False),   # no valve, arrows visible
        (75,   0, "Top (assembly)", True),
    ]
    for idx, (elev, azim, label, show_valve) in enumerate(views):
        ax = fig.add_subplot(2, 2, idx + 1, projection="3d")
        ax.add_collection3d(Poly3DCollection(
            bt, alpha=0.85, facecolor="#4a90d9",
            edgecolor="#2c5f8a", linewidth=0.12))
        ax.add_collection3d(Poly3DCollection(
            ct, alpha=0.9, facecolor="#5cb85c",
            edgecolor="#2f6f2f", linewidth=0.12))
        if show_valve:
            ax.add_collection3d(Poly3DCollection(
                vt, alpha=0.22, facecolor="#d4a94a",
                edgecolor="#8a7030", linewidth=0.08))
        pts = np.vstack(bt + ct + vt)
        pad = 10
        ax.set_xlim(pts[:, 0].min() - pad, pts[:, 0].max() + pad)
        ax.set_ylim(pts[:, 1].min() - pad, pts[:, 1].max() + pad)
        ax.set_zlim(pts[:, 2].min() - 2,   pts[:, 2].max() + pad)
        ax.view_init(elev=elev, azim=azim)
        ax.set_title(label, fontsize=10)
        ax.set_xlabel("X mm"); ax.set_ylabel("Y mm"); ax.set_zlabel("Z mm")

    plt.suptitle("Valve Bracket 3-Way — Assembly", fontsize=13)
    plt.tight_layout()
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()


# ─── main ────────────────────────────────────────────────────────

def main():
    print("Valve Bracket 3-Way — generating files ...")

    bracket = make_bracket(FULL_H)
    test    = make_bracket(TEST_H)
    corner  = make_corner_bracket()
    valve   = make_valve()
    asm     = bracket + corner + valve.translate((0, 0, BASE))

    exports = [
        ("bracket.stl",           bracket),
        ("bracket.step",          bracket),
        ("bracket_test.stl",      test),
        ("bracket_test.step",     test),
        ("corner_bracket.stl",    corner),
        ("corner_bracket.step",   corner),
        ("bracket_assembly.step", asm),
    ]
    for name, shape in exports:
        cq.exporters.export(shape, os.path.join(DIR, name))
        print(f"  {name}")

    render_png(bracket, valve, corner, os.path.join(DIR, "bracket_assembly.png"))
    print("  bracket_assembly.png")
    print("Done.")


if __name__ == "__main__":
    main()
