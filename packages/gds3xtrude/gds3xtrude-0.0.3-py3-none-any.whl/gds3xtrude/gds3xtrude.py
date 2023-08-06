#
# Copyright (c) 2018 Thomas Kramer.
#
# This file is part of gds3xtrude
# (see https://teahub.io/miaou/gds3xtrude).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#

from solid import *
from solid import utils

from .polygon_approx import approximate_polygon
from .layer_operations import LayerOp, AbstractLayer

from functools import reduce
from itertools import chain
import importlib.util
import importlib.machinery
import types
import logging

from typing import List

logger = logging.getLogger(__name__)

# klayout.db should not be imported if script is run from KLayout GUI.
try:
    import pya
except:
    import klayout.db as pya

DEFAULT_COLOR = [0.5, 0.5, 0.5]


class Mask:
    """ Wrapper around pya.Region.
    """

    def __init__(self, region: pya.Region):
        self.region = region
        self.color = DEFAULT_COLOR

    def __add__(self, other):
        return Mask(self.region + other.region)

    def __or__(self, other):
        return self + other

    def __and__(self, other):
        return Mask(self.region & other.region)

    def __sub__(self, other):
        m = Mask(self.region - other.region)
        m.color = self.color
        return m

    def __xor__(self, other):
        return Mask(self.region ^ other.region)

    def __hash__(self):
        return hash(self.region)

    def __equal__(self, other):
        return self.region == other.region


def _build_masks(layout, cell, abstract_layerstack, selection_box=None, color_map=None, default_color=[0.5, 0.5, 0.5]):
    """ Create the masks of `cell` based on the layer stack information.
    :param layout:
    :param cell:
    :param abstract_layerstack: Layer stack structure as defined in the technology file.
    :param selection_box: An optional pya.Box to select which part of the layout should be converted to masks.
    :param color_map:
    :param default_color: Color to be used if it is not defined in `color_map`. (r, g, b), 0 <= r, g, b <= 1
    :return: List[(thickness: int, mask: pya.Region)]
    """

    # Cache for evaluated sub trees.
    cache = dict()

    def eval_op_tree(op_node):
        """ Recursively evaluate the layer operation tree.
        :param op_node: Operand node or leaf.
        :return: Returns a `Mask` object containing a `pya.Region` of the layer.
        """

        if op_node in cache:
            return cache[op_node]

        if isinstance(op_node, AbstractLayer):
            (idx, purpose, color) = op_node.eval()
            layer_index = layout.layer(idx, purpose)

            region = _flatten_cell(cell, layer_index, selection_box=selection_box)
            if selection_box is not None:
                region = region & selection_box

            result = Mask(region)
            if color_map is not None:
                result.color = color_map.get(idx, default_color)
            else:
                result.color = color if color is not None else default_color
        else:
            assert isinstance(op_node, LayerOp)
            op = op_node.op
            lhs = eval_op_tree(op_node.lhs)
            rhs = eval_op_tree(op_node.rhs)
            result = op(lhs, rhs)
        result.region.merge()
        cache[op_node] = result

        return result

    _layerstack = []
    for thickness, layers in abstract_layerstack:
        if not isinstance(layers, list):
            layers = [layers]

        _layerstack.append(
            (thickness, [eval_op_tree(l) for l in layers])
        )

    return _layerstack


def _region2volume(region: pya.Region, thickness, approx_error=0):
    """ Convert a layer to volumes by extruding the polygons in z direction.
    :param shapes: A pya.Shapes object containing the polygons to be extruded.
    :param thickness: Extrusion length
    :return:
    """

    mask_volumes = []
    for poly in region.each():
        n_holes = poly.holes()

        approx_hull = approximate_polygon(poly.each_point_hull(), approx_error)
        approx_holes = [approximate_polygon(poly.each_point_hole(i), approx_error)
                        for i in range(n_holes)]

        points_hull = [(p.x, p.y) for p in approx_hull]
        points_holes = [[(p.x, p.y) for p in h] for h in approx_holes]

        solid_hull = polygon(points_hull)
        solid_holes = [polygon(h) for h in points_holes]

        if len(points_holes) > 0:
            solid_poly = difference()(solid_hull, *solid_holes)
        else:
            solid_poly = solid_hull

        mask_volumes.append(solid_poly)

    volume = linear_extrude(thickness)(*mask_volumes)

    return volume


def _flatten_cell(cell, layer_index, selection_box=None, cell_cache=None):
    """ Recursively convert a single layer of a cell into a pya.Region.
    :param cell: The pya.Cell to be converted.
    :param layer_index: KLayout layer index.
    :param cell_cache:
    :return: Merged pya.Region containing all polygons of the flattened cell hierarchy.
    """

    if cell_cache is None:
        # Cache rendered cells
        # Dict[cell_index, volume]
        cell_cache = dict()

    region = pya.Region()

    if selection_box is None:
        instances = cell.each_inst()
    else:
        instances = cell.each_touching_inst(selection_box)

    for inst in instances:
        cell_id = inst.cell_index
        trans = inst.cplx_trans

        # Transform selection such that it can be used in recursive call.
        if selection_box:
            trans_selection = selection_box.transformed(trans.inverted())
        else:
            trans_selection = None

        if cell_id in cell_cache:
            child_region = cell_cache[cell_id]
            if trans_selection is not None:
                child_region &= trans_selection
        else:
            # Recursively flatten child instance.
            child_region = _flatten_cell(inst.cell, layer_index,
                                         selection_box=trans_selection, cell_cache=cell_cache)

            # Cache the region only if the cell has been fully rendered and was not cropped to selection.
            if trans_selection is None or inst.cell.bbox().inside(trans_selection):
                cell_cache[cell_id] = child_region

        transformed = child_region.transformed(trans)
        region.insert(transformed)

    # Add shapes of this cell.

    if selection_box is None:
        own_shapes = cell.each_shape(layer_index)
    else:
        own_shapes = cell.each_touching_shape(layer_index, selection_box)

    # region.insert(own_shapes)
    for shape in own_shapes:
        region.insert(shape.polygon)

    region.merge()
    return region


def render_scad_to_file(layout, tech_file, output_file, **kw):
    """ Same as `render_scad` but write the output directly to a file.
    :param layout:  pya.Layout
    :param tech_file:   Path to description of the layer stack.
    :param output_file: Path to OpenSCAD output file.
    :param approx_error:    Approximate polygons before conversion.
    :param color_map:   Mapping from layer number to color. Dict[int, (r, g, b)]
    :param centered:    Move the center of the layout to (0, 0).
    :param scale_factor:    Scale the layout before conversion.
    :param selection_box: An optional pya.Box to select which part of the layout should be converted to masks.
    :return: None
    """

    volume = render_scad(layout, tech_file, **kw)

    logger.info("Writing SCAD: %s", output_file)
    scad_render_to_file(volume, filepath=output_file)


def render_scad(layout, tech_file, approx_error=0, color_map=None, centered=False, scale_factor=1, selection_box=None):
    """ Transform the first pya.Cell in `layout` into a solidpython volume.
    :param layout:  pya.Layout
    :param tech_file:   Path to description of the layer stack.
    :param approx_error:    Approximate polygons before conversion.
    :param color_map:   Mapping from layer number to color. Dict[int, (r, g, b)]
    :param centered:    Move the center of the layout to (0, 0).
    :param scale_factor:    Scale the layout before conversion.
    :param selection_box: An optional pya.Box to select which part of the layout should be converted to masks.
    :return: solidpython volume
    """

    logger.info('Loading tech file: %s', tech_file)

    loader = importlib.machinery.SourceFileLoader('tech', tech_file)
    tech = types.ModuleType(loader.name)
    loader.exec_module(tech)

    top_cells = layout.top_cells()
    logger.debug('Number of top cells: %d', len(top_cells))

    logger.info("Convert polygons into volumes.")

    layer_masks = _build_masks(layout, top_cells[0], tech.layerstack, color_map=color_map, selection_box=selection_box)

    volumes = []
    offset = 0
    for thickness, masks in layer_masks:
        for mask in masks:
            volume = _region2volume(mask.region, thickness, approx_error=approx_error)
            volume = utils.up(offset)(volume)
            volume = color(mask.color)(volume)
            volumes.append(volume)

        offset += thickness

    volume = union()(*volumes)

    # Find bounding box of masks and center the volume.
    if centered and len(layer_masks) > 0:
        bboxes = chain(*((mask.region.bbox() for mask in masks) for (thickness, masks) in layer_masks))
        # Find union bounding box.
        bbox = reduce(lambda a, b: a + b, bboxes)
        # Shift center to (0, 0).
        center = bbox.center()
        volume = translate((-center.x, -center.y, 0))(*volumes)

    if scale_factor != 1:
        volume = scale(scale_factor)(volume)

    return volume
