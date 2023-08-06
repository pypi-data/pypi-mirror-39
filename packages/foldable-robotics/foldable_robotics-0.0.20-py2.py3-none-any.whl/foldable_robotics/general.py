# -*- coding: utf-8 -*-
"""
Created on Tue Oct  2 14:39:00 2018

@author: daukes
"""

def rectangular_array(shape,spacing_x, spacing_y, num_x, num_y):
    
#    shapes= shape.copy()
    shapes = []
    
    for ii in range(num_x):
        x_pos = ii*spacing_x
        for jj in range(num_y):
            y_pos = jj*spacing_y
            shapes.append(shape.translate(x_pos,y_pos))
    
    shapes2 = shapes.pop(0).copy()
    for item in shapes:
        shapes2 |= item
    return shapes2