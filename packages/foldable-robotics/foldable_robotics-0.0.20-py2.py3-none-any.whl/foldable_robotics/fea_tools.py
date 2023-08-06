# -*- coding: utf-8 -*-
"""
Created on Thu Dec  6 20:28:23 2018

@author: danaukes
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Nov 13 09:51:18 2018

@author: danaukes
"""

import idealab_tools.text_to_polygons
from foldable_robotics.layer import Layer
import shapely.geometry as sg
import idealab_tools.fea_tetra.fea as fea
import idealab_tools.matplotlib_tools
import numpy
import pygmsh as pg
import matplotlib.pyplot as plt
plt.ion()
import idealab_tools.fea_tetra.fea as fea

def layer_to_mesh(layer):
    points2 = []
    cells2 = []
    
    l = 0
    outer = []
    for item in layer.geoms:
        layer4 = Layer(item)
        
        points, cells,triangles_outer = poly_2_flat_mesh(layer4,1)
        points2.append(points)

        triangles_outer+=l
        outer.append(triangles_outer)
        
        cells+=l
        cells2.append(cells)
        
        l+=len(points)
    
        
    points3 = numpy.concatenate(points2,0)
    cells3 = numpy.concatenate(cells2,0)
    outer3 = numpy.concatenate(outer,0)
    return points3,cells3,outer3

def poly_2_flat_mesh(layer,thickness,lcar=.5):
    
    geom = pg.built_in.Geometry()
    
    holes = []
    for poly in layer.interiors():
#        poly2= list(poly.exterior.coords)
        poly2 = poly[:-1]
        poly2 = numpy.r_[poly2]
        poly2 = numpy.c_[poly2,poly2[:,0]*0]
        
        hole = geom.add_polygon(poly2,lcar=lcar,make_surface=False)
        holes.append(hole)
    
    for poly in layer.exteriors():
#        poly2= list(poly.exterior.coords)
        poly2 = poly[:-1]
        poly2 = numpy.r_[poly2]
        poly2 = numpy.c_[poly2,poly2[:,0]*0]
        
    poly = geom.add_polygon(poly2,lcar=lcar, holes=[item.line_loop for item in holes])

    
    axis = [0, 0, thickness]
    theta = 0
    
    geom.extrude(poly,translation_axis=axis,rotation_axis=axis,point_on_axis=[0, 0, 0], angle=theta)
    
    points, cells, point_data, cell_data, field_data = pg.generate_mesh(geom)

    triangles_outer = cells['triangle']

    coordinates = points[:]
    elements = cells['tetra']
    
    used_elements = fea.find_used_elements(elements,triangles_outer)
    coordinates,mapping = fea.coord_reduce(coordinates,used_elements)
    triangles_outer = fea.element_reduce(triangles_outer,mapping)
    elements= fea.element_reduce(elements,mapping)
    
    a=fea.analyze(coordinates,elements)
    print(a)
    elements[a] = elements[a][:,(0,2,1,3)]
    a=fea.analyze(coordinates,elements)
    print(a)
#    
    T = coordinates[elements[:,1:]]-coordinates[elements[:,0:1]]
    dt = numpy.array([numpy.linalg.det(item) for item in T])
    elements = elements[dt!=0]
    
    return coordinates,elements,triangles_outer


layer = Layer(sg.Polygon([(0,0),(1,0),(1,1),(0,1)]))
layer2 = (layer<<1)-layer
points3,tris3,outer3 = layer_to_mesh(layer2)

boundary = (layer<<.1)-(layer>>.1)
boundary.plot(new=True)

test = boundary.contains(*points3[:,:2])
ii = numpy.array(range(len(points3)))
jj = ii[test]

#layer = layer.scale(20,20)

#polygons = idealab_tools.text_to_polygons.text_to_polygons('Test',{'family':'Roboto'})
#
#layers = []
#for item in polygons:
##    points = [sg.Point(*item2) for item2 in item]
#    if len(item)>=3:
#        layers.append(Layer(sg.Polygon(item)))
#    
#layer = Layer()
#for item in layers:
#    layer ^= item
#
#layer2= layer.simplify(.1)    
#layer2.plot()
#
#bb = (layer2<<.5).bounding_box()
#layer3 = bb-layer2
#layer3.plot(new=True)
#
#points3,tris3,outer3 = layer_to_mesh(layer3)

#tris3 = numpy.r_[tris3[:,(0,1,2)],tris3[:,(1,2,3)],tris3[:,(2,3,0)],tris3[:,(3,0,1)]]

#fea.plot_triangles(points3,tris3)
fea.plot_triangles(points3,outer3)
#fea.plot_tetrahedra(points3,tris3,jj)


