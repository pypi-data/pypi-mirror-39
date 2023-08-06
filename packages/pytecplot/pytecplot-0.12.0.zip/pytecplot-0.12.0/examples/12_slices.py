from os import path
import tecplot as tp
from tecplot.constant import SliceSurface, ContourType

# Run this script with "-c" to connect to Tecplot 360 on port 7600
# To enable connections in Tecplot 360, click on:
#   "Scripting" -> "PyTecplot Connections..." -> "Accept connections"
import sys
if '-c' in sys.argv:
    tp.session.connect()

examples_dir = tp.session.tecplot_examples_directory()
datafile = path.join(examples_dir, 'SimpleData', 'DuctFlow.plt')
dataset = tp.data.load_tecplot(datafile)

plot = tp.active_frame().plot()
plot.contour(0).variable = dataset.variable('U(M/S)')

plot.show_slices = True
slice_0 = plot.slice(0)

slice_0.contour.show = True
slice_0.contour.contour_type = ContourType.Overlay  # AKA "Both lines and flood"

slice_0.effects.use_translucency = True
slice_0.effects.surface_translucency = 30

slice_0.show_primary_slice = False
slice_0.show_start_and_end_slices = True
slice_0.show_intermediate_slices = True
slice_0.start_position = (-.21, .05, .025)
slice_0.end_position = (1.342, .95, .475)
slice_0.num_intermediate_slices = 2

# ensure consistent output between interactive (connected) and batch
plot.contour(0).levels.reset_to_nice()

tp.export.save_png('slice_example_12.png', 600, supersample=3)
