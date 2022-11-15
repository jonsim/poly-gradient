#!/usr/bin/env python3
import argparse
import math
import random
from svgwrite import Drawing, mm

def right_angle_triangles(x, y, max_x, max_y):
    flip = random.randint(1, 100) <= 50
    if flip:
        yield [(0, 0), (1, 1), (0, 1)]
        yield [(0, 0), (1, 1), (1, 0)]
    else:
        yield [(0, 0), (1, 0), (0, 1)]
        yield [(1, 1), (1, 0), (0, 1)]

def pink_black_gradient(gradient_value):
    return '#ee99dd' if random.randint(1, 100) <= gradient_value else 'black'

def linear_gradient(x, y, max_x, max_y,
                    solid_cells_color, solid_cells_black):
    if y < solid_cells_black:
        return 0
    elif y >= (max_y - solid_cells_color):
        return 100
    else:
        y -= solid_cells_black
        y += 0.5 # Adjustment for our zero-origin co-ordinates.
        max_y -= solid_cells_color + solid_cells_black
        return y * (100 / max_y)

def radial_gradient(x, y, max_x, max_y,
                    solid_cells_color, solid_cells_black):
    assert max_x == max_y, 'cannot generate elliptical gradients'
    center_x = (max_x-1) / 2  # Adjustment for our zero-origin co-ordinate system.
    center_y = (max_y-1) / 2
    dist_from_center = math.sqrt(abs(center_x - x)**2 + abs(center_y - y)**2)
    v = 100 - linear_gradient(
        dist_from_center, dist_from_center,
        center_x+1, center_y+1,
        solid_cells_black, solid_cells_color)
    return 0 if v < 0 else v

def _print_svg_xml(canvas):
    import xml.etree
    import xml.dom.minidom
    canvas_xml = canvas.get_xml()
    canvas_xml_str = xml.etree.ElementTree.tostring(canvas_xml)
    canvas_dom = xml.dom.minidom.parseString(canvas_xml_str)
    print(canvas_dom.toprettyxml())

def gradient(filename,
             image_width_mm,
             image_height_mm,
             cell_size_mm,
             cell_polygon_function,
             gradient_function,
             color_function,
             solid_cells_color=0,
             solid_cells_black=0):
    def _transform_points(points, scale=1, translate=(0, 0)):
        return [((x+translate[0])*scale,
                 (y+translate[1])*scale)
                for (x, y) in points]

    cells_x = image_width_mm // cell_size_mm
    cells_y = image_height_mm // cell_size_mm
    canvas_size = (cells_x * cell_size_mm * mm,
                   cells_y * cell_size_mm * mm)
    canvas = Drawing(filename=filename, size=canvas_size, debug=True)
    # Polygons are annoying and must have their size specified in raw
    # co-ordinates, without units. To work around this we create an SVG
    # sub-element scaled to the expected unit-size, then set its viewbox
    # (which it uses to set its internal co-ordinate system) appropriate
    # for drawing unit-sized polygons (to keep things easy).
    polygons = canvas.add(canvas.svg(size=canvas_size))
    polygons.viewbox(0, 0, cells_x, cells_y)
    for x in range(cells_x):
        for y in range(cells_y):
            # Calculate gradient value for this cell.
            gradient_value = gradient_function(x, y, cells_x, cells_y, solid_cells_color, solid_cells_black)
            # Calculate the co-ordinates of this cell's polygons.
            for polygon_points in cell_polygon_function(x, y, cells_x, cells_y):
                color = color_function(gradient_value)
                # Build polygon.
                polygon = canvas.polygon(
                    points=_transform_points(polygon_points, translate=(x, y)),
                    fill=color,
                    stroke=color,
                    stroke_width=0.05)
                polygons.add(polygon)
    canvas.save()
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog = 'poly_gradient',
                        description = 'Generates SVGs containing gradients made up of polygons')
    parser.add_argument('filename',
                        type=str,
                        help='Name of the file to generate to.')
    parser.add_argument('image_width',
                        type=int,
                        help='Image width in mm.')
    parser.add_argument('image_height',
                        type=int,
                        help='Image height in mm.')
    parser.add_argument('--gradient',
                        choices=['linear', 'radial'],
                        default='linear',
                        help='Type of gradient to generate.')
    parser.add_argument('--shape',
                        choices=['triangles'],
                        default='triangles',
                        help='Polygon to generate the gradient from.')
    parser.add_argument('--cell-size',
                        type=int,
                        default=10,
                        help='Size in mm of each cell making up the gradient.')
    args = parser.parse_args()

    if args.filename[-4:] != '.svg':
        raise RuntimeError(f'{args.filename} is not an SVG file')

    if args.gradient == 'linear':
        gradient_function = linear_gradient
    elif args.gradient == 'radial':
        gradient_function = radial_gradient
    else:
        raise RuntimeError('Unknown gradient type "{}"', args.gradient)

    color_function = pink_black_gradient

    if args.shape == 'triangles':
        polygon_function = right_angle_triangles
    else:
        raise RuntimeError('Unknown shape type "{}"', args.shape)

    gradient(args.filename,
             args.image_width, args.image_height,
             args.cell_size,
             polygon_function,
             gradient_function,
             color_function)
