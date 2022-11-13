#!/usr/bin/env python3
import math
import random
import svgwrite
from svgwrite import mm

def _transform_points(points, scale=1, translate=(0, 0)):
    return [((x+translate[0])*scale,
             (y+translate[1])*scale)
            for (x, y) in points]

def _triangle_points(flip):
    if flip:
        return [(0, 0), (1, 1), (0, 1),], \
               [(0, 0), (1, 1), (1, 0),]
    else:
        return [(0, 0), (1, 0), (0, 1),], \
               [(1, 1), (1, 0), (0, 1),]

def _triangle_color(color_probability):
    return '#ee99dd' if random.randint(1, 100) <= color_probability else 'black'

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

def gradient(filename, gradient_function,
             triangle_size_mm,
             triangles_x=20, triangles_y=20,
             solid_cells_color=0, solid_cells_black=0):
    canvas_size = (triangles_x*triangle_size_mm*mm,
                   triangles_y*triangle_size_mm*mm)
    canvas = svgwrite.Drawing(filename=filename, size=canvas_size, debug=True)
    # Polygons are annoying and must have their size specified in raw
    # co-ordinates, without units. To work around this we create an SVG
    # sub-element scaled to the expected unit-size, then set its viewbox
    # (which it uses to set its internal co-ordinate system) appropriate
    # for drawing unit-sized triangles (to keep things easy).
    triangles = canvas.add(canvas.svg(size=canvas_size))
    triangles.viewbox(0, 0, triangles_x, triangles_y)
    for x in range(triangles_x):
        for y in range(triangles_y):
            # Calculate the co-ordinates of this cell's triangles.
            orientation = random.randint(1, 100) <= 50
            #orientation = (x+y) % 2
            points_a, points_b = _triangle_points(orientation)
            # Calculate the colors of this cell's triangles.
            color_prob = gradient_function(x, y, triangles_x, triangles_y, solid_cells_color, solid_cells_black)
            #print(f'({x}, {y}): color_prob = {color_prob}')
            color_a = _triangle_color(color_prob)
            color_b = _triangle_color(color_prob)
            # Build triangles.
            triangle_a = canvas.polygon(
                points=_transform_points(points_a, translate=(x, y)),
                fill=color_a,
                stroke=color_a,
                stroke_width=0.005)
            triangle_b = canvas.polygon(
                points=_transform_points(points_b, translate=(x, y)),
                fill=color_b,
                stroke=color_b,
                stroke_width=0.005)
            triangles.add(triangle_a)
            triangles.add(triangle_b)
    canvas.save()
    

if __name__ == '__main__':
    gradient('linear_gradient.svg', linear_gradient, 5,  25,  50, 2)
    gradient('radial_gradient.svg', radial_gradient, 5, 100, 100, 2)
