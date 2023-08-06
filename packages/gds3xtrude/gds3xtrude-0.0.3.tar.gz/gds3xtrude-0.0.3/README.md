# gds3xtrude
A simple layout to 3D converter.

This tool converts a GDS layout into a OpenSCAD 3D model.

![Screenshot](./examples/freepdk45_screenshot.png "Screenshot")

## Dependencies
* OpenSCAD: 3D modelling tool. Can be installed using the package manager of most linux distributions.
* solidpython: Python library for creating OpenSCAD models.
* klayout: Python module of KLayout used for GDS input/output and polygon operations.

## Install from Git
```sh
git clone [this repo]
cd gds3xtrude
python3 setup.py install --user
```

For standalone usage the `klayout` Python package must be installed too. Otherwise gds3xtrude is only usable from the KLayout GUI.

## Usage

Example usage:
```sh
gds3xtrude --tech tech_freepdk45.layerstack --input [path to freepdk]/NAND2X1.gds --output NAND2X1.scad

# Then run openscad to view the result.
openscad NAND2X1.scad
```

### Layer stack definition
To convert a 2D layout into a 3D model some information about the physical layer stack is necessary.
This information must be passed to gds3xtrude as a file. An example of a simple layer stack description
for the FreePDK45 can be found in `examples/freepdk45.layerstack`. Use this file as a starting point and adapt it to your needs.

Essentially a layerstack file is just a python script that defines some data structures.

Example:
```python
from gds3xtrude.include import layer

# Define layers
poly = layer(15)
contact = layer(16)
metal1 = layer(21)

# Define colors (optional)
poly.color = [0.8, 0.2, 0.2]
metal1.color = [0.2, 0.2, 0.8]

# Define additional layers from boolean operation
contact_to_silicon = contact - poly

# Define layer stack structure as a list of (layer thickness, [masks, ...]).
layerstack = [
    (10, contact_to_silicon),
    (20, [contact, poly]),
    (200, contact),
    (50, metal1),
]
```

## KLayout Module
gds3xtrude is intended to be used from KLayout. Currently the module is not yet registered as a KLayout package, but can be used by manually copying `klayout/gds3xtrude.lym` into `.klayout/pymacros`.

## FreeCAD / Blender
The generated OpenSCAD models (.scad) can be imported into FreeCAD. If you want to use Blender for rendering, export the model from FreeCAD as a Wavefront (.obj) file. This can be imported in blender.

### Color Issue
When applying a boolean union FreeCAD strips away colors. Therefore an exported .obj model will by totally gray. There is a workaround:
* Open the OpenSCAD model in FreeCAD
* Open the `Model` tab in `Combo View`
* Expand the list of the imported model which is likely to be named `Unnamed`
* Find a child node labelled `union`, select and delete it
* Select the full model to be exported (Ctrl-A)
* Now you can export to .obj without loosing color information

Additionally to the .obj file FreeCAD will also create a .mtl file containing material/color information. Blender will automatically read it when importing the .obj file.
