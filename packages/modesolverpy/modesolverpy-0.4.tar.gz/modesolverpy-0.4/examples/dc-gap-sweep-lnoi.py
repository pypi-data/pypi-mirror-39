import modesolverpy.mode_solver as ms
import modesolverpy.structure as st
import modesolverpy.design as de
import opticalmaterialspy as mat
import numpy as np
import tqdm

wl = 1.55
x_step = 0.04
y_step = 0.04
etch_depth = 0.4
wg_width_1 = 1.8
wg_width_2 = 0.6
sub_height = 0.5
sub_width = 6.
clad_height = 0.5
film_thickness = 0.5
gaps = np.linspace(0.1, 0.5, 11)
gap = 0.3

lengths = []

n_sub = mat.SiO2().n(wl)
n_clad = mat.Air().n(wl)
n_wg = 2.15

r = st.WgArray(wl, x_step, y_step, etch_depth, [wg_width_1, wg_width_2], gap,
               sub_height, sub_width, clad_height, n_sub, n_wg, None)
r.write_to_file()

solver = ms.ModeSolverFullyVectorial(6)
solver.solve(r)
solver.write_modes_to_file()

print(de.directional_coupler_lc(wl, solver.n_effs_te[1], solver.n_effs_te[2]))
print(de.directional_coupler_lc(wl, solver.n_effs_tm[1], solver.n_effs_tm[2]))
