import sys
import klayout.db as db

path = sys.argv[1]
ly = db.Layout()
ly.read(path)
print(f"file: {path}")
print(f"dbu: {ly.dbu} um")
tops = ly.top_cells()
print(f"top cells: {[c.name for c in tops]}")
for c in tops:
    bb = c.dbbox()  # DBox in microns
    w = bb.right - bb.left
    h = bb.top - bb.bottom
    print(f"  bbox: ({bb.left:.3f}, {bb.bottom:.3f}) to ({bb.right:.3f}, {bb.top:.3f}) um = {w:.3f} x {h:.3f} um")
    print(f"  child instances: {c.child_instances()}")
    n = sum(c.shapes(i).size() for i in ly.layer_indexes())
    print(f"  total shapes: {n}")
layers = sorted({(ly.get_info(i).layer, ly.get_info(i).datatype) for i in ly.layer_indexes()})
print(f"layers (GDS no/datatype): {layers}")
print(f"total cells: {ly.cells()}")
