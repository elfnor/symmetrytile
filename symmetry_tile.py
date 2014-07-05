#!/usr/bin/env python

#   Copyright (C) 2014  Eleanor Howick  github.com/elfnor>
#
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 2 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, write to the Free Software
#   Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.


from gimpfu import *
import math
import random

sym_types_list = ['p1','p2','pm','pg','pgg','pmm', 'pmg','cm','cmm', 'p4', 'p3m1', 'p3', 'p4g', 'p4m', 'p6', 'p31m', 'p6m', 
                  '17 groups','all square cells', 'Escher\'s Potato Game']

rect_strs =[('p1', 'b', False),
            ('p2', 'bq', False),
            ('p2', 'b|q', False),
            ('p2', 'bq|qb', False),
            ('pm', 'bd', False),
            ('pm', 'b|p', False),
            ('cm', 'bp|pb', False),
            ('cm', 'bd|db', False),
            ('cmm', 'bdpq|pqbd', False),
            ('cmm', 'bd|qp|db|pq', False),
            ('cmm', 'bqpd|pdbq', False),
            ('cmm', 'bd|pq|db|qp', False),
            ('pg', 'bp', False),
            ('pg', 'b|d', False),
            ('pgg', 'bp|dq', False),
            ('pgg', 'bq|dp', False),
            ('pgg', 'bp|qd', False),
            ('pmg', 'bd|qp', False),
            ('pmg', 'b|p|d|q', False),
            ('pmg', 'b|q|d|p', False),
            ('pmg', 'bdpq', False),
            ('pmg', 'bqpd', False),
            ('pmg', 'bq|pd', False),
            ('pmm', 'bd|pq', False),
            ('pg', 'bd+|d+b', True),
            ('pg', 'bp+|p+b', True),
            ('p4', 'bb+|q+q', True),
            ('p4', 'bq+|b+q', True),
            ('p4g', 'bdp+b+|pqq+d+|p+b+bd|q+d+pq', True),
            ('p4g', 'bdd+q+|b+p+pq|d+q+bd|pqb+p+', True),
            ('p4g', 'bb+p+d|q+qpd+|p+dbb+|pd+q+q', True),
            ('p4g', 'bq+d+d|pp+b+q|d+dbq+|b+qpp+', True)]
            
rect_single_index = [0,1,4,6,8,12,16,19,25,26,28]
rect_strs_single = [rect_strs[i] for i in rect_single_index]    
rect_cells = [rect_strs[i][0] for  i in rect_single_index]        

def symmetry_tile(old, drawable, width, height, sym_type, multiple, bdpq_str):   
    """
    plugin entry function
    """
    if sym_types_list[sym_type] in rect_cells:
        if multiple:
            sym_list = [row for row in rect_strs if row[0] == sym_types_list[sym_type]]
            for sym_name, sym_str, square in sym_list:
                img_sym_str(sym_name, sym_str, square, old, drawable, width, height)
        else:    
            sym_name, sym_str, square = rect_strs_single[rect_cells.index(sym_types_list[sym_type])]
            img_sym_str(sym_name, sym_str, square, old, drawable, width, height) 
        
    if sym_types_list[sym_type] == 'p3': p3(old, drawable, width, height)        
    if sym_types_list[sym_type] == 'p3m1': p3m1(old, drawable, width, height)        
    if sym_types_list[sym_type] == 'p4m': p4m(old, drawable, width, height)
    if sym_types_list[sym_type] == 'p31m': p31m(old, drawable, width, height)
    if sym_types_list[sym_type] == 'p6m': p6m(old, drawable, width, height)
    
    if sym_types_list[sym_type] == 'p6': 
        if multiple:
            p6(old, drawable, width, height,rot60=0)
            p6(old, drawable, width, height,rot60=1)
            p6(old, drawable, width, height,rot60=2)
        else:    
            p6(old, drawable, width, height,rot60=0)
            
    if sym_types_list[sym_type] == '17 groups': all_groups(old, drawable, width, height, multiple)
    if sym_types_list[sym_type] == 'all square cells': all_square(old, drawable, width, height, multiple)
    if sym_types_list[sym_type] == 'Escher\'s Potato Game': 
        if bdpq_str == "":
            bdpq_str = random_potato_game_string()
        if '+' in bdpq_str:
            square = True
        else:
            square = False
        img_sym_str('epg', bdpq_str, square, old, drawable, width, height,)
        
    return

def all_groups(old, drawable, width, height, multiple):
    """
    Makes 17 (or 40 if multple set)  new images using the same left edge of the 	  rectangular selection
    
    """
    if multiple:
        sym_list = rect_strs
    else:
        sym_list = rect_strs_single
    
    for sym_type, sym_str, square in sym_list:
        img_sym_str(sym_type, sym_str, square, old, drawable, width, height)   
          
    p4m(old, drawable, width, height)
    
    if multiple:
        p6(old, drawable, width, height,rot60=0)
        p6(old, drawable, width, height,rot60=1)
        p6(old, drawable, width, height,rot60=2)
    else:    
        p6(old, drawable, width, height,rot60=0)
    
    p31m(old, drawable, width, height)
    p3m1(old, drawable, width, height)
    p6m(old, drawable, width, height) 

    p3(old, drawable, width, height)	
    return
    
    
def all_square(old, drawable, width, height, multiple):
    """
    Makes 11 (or 32 if multiple set) images all with the same square cell
    """
    if multiple:
        sym_list = rect_strs
    else:
        sym_list = rect_strs_single
    
    for sym_type, sym_str, square in sym_list:
        img_sym_str(sym_type, sym_str, True, old, drawable, width, height) 
                
        
"""-----------------------------------------------------------------------------"""
    
def copy_primary_cell(old, drawable, width, height, cell_width, cell_height):
    """
    copies the new selected area to a new image
    """

    # Copy the selected area
    pdb.gimp_edit_copy(drawable)
    
    # Create a new image
    img = gimp.Image(width, height, RGB)

    # Create a new layer and set the size of the layer = the size of the initial selection
    layer = gimp.Layer(img, "first", cell_width, cell_height, 0, 100, 0)
    img.add_layer(layer, 0)
    layer.add_alpha()

    # Clear the layer of any initial garbage
    pdb.gimp_edit_clear(layer)

    # Add the copied selection to the layer, and the layer to the image
    layer.fill(3)
    pdb.gimp_edit_paste(layer, 1)
    pdb.gimp_floating_sel_anchor(pdb.gimp_image_get_floating_sel(img))
    cell = img.merge_visible_layers(1)

    return cell, img

def get_rect_primary_cell(old_img, drawable, width, height, square=False):
    """
    The primary cell is derived from the user selection
    """
    # Find the area that has been selected in the original image
    old_is_sel, old_x1, old_y1, old_x2, old_y2 = pdb.gimp_selection_bounds(old_img)
    if  not old_is_sel:
        pdb.gimp_message("FATAL: Missing selection in old image!")
        #sys.exit(1)
        
    cell_width = old_x2 - old_x1
    cell_height = old_y2 - old_y1 
    
    if square:
        cell_width = cell_height
    
    pdb.gimp_image_select_rectangle(old_img, CHANNEL_OP_REPLACE, old_x1, old_y1, cell_width, cell_height)  
    
    return cell_width, cell_height


"""----------------------------------------------------------------------------"""

def copy_tile(tile, img, x0, x1):
    """
    tile: the merged layer of primary cells
    img: the new image type gimp.Image
    x0: (x,y) vector along one edge of paralleogram defining tile
    x1: (x,y) vector along other edge of paralleogram defining tile
    """
    # first cell is placed so top left corner of a rectangle is at (0,0)
    # do a loop from -1*x0 to +nx*x0
    # do a loop from -1*x1 to ny*x1 
    # for hexagonal tiles need to add an extra half tile per row, do it for all. 

    nx = int(img.width/x0[0]) + 2
    ny = int(img.height/x1[1]) + 2
    for j in range(-1, ny):
        for i in range(-abs(j), nx):
            this_layer = tile.copy(0)
            img.add_layer(this_layer, 0)
            xshft = i*x0[0] + j*x1[0]
            yshft = i*x0[1] + j*x1[1]
            pdb.gimp_layer_translate(this_layer, xshft, yshft)
            
    img.merge_visible_layers(1)
    gimp.Display(img)


def cell_b(cell, cell_width, cell_height, img, pos, rotate90=False):
    """
    this takes cell returned from get_rect_primary_cell() call
    and places it at pos
    eg.
    pos  = (1,0) one cell_width to the right
    pos =  (0,1) one cell_height down
    """
    cell_2 = cell.copy(0)
    img.add_layer(cell_2,0)
    if rotate90:
        pdb.gimp_item_transform_rotate_simple(cell_2,ROTATE_90,TRUE,0,0)
    pdb.gimp_layer_translate(cell_2, cell_width*pos[0], cell_height*pos[1]) 
    return

def cell_q(cell, cell_width, cell_height, img, pos, rotate90=False):
    """
    this takes cell returned from get_rect_primary_cell() call
    rotates it 180 degrees and places it at pos
    eg.
    pos  = (1,0) one cell_width to the right
    pos =  (0,1) one cell_height down
    """
    cell_2 = cell.copy(0)
    img.add_layer(cell_2,0)
    pdb.gimp_item_transform_rotate_simple(cell_2,ROTATE_180,TRUE,0,0)
    if rotate90:
        pdb.gimp_item_transform_rotate_simple(cell_2,ROTATE_90,TRUE,0,0)
    pdb.gimp_layer_translate(cell_2, cell_width*pos[0], cell_height*pos[1]) 
    return

def cell_d(cell, cell_width, cell_height, img, pos, rotate90=False):
    """
    this takes cell returned from get_rect_primary_cell() call
    flips it horizontally and places it at pos
    eg.
    pos  = (1,0) one cell_width to the right
    pos =  (0,1) one cell_height down
    """
    cell_2 = cell.copy(0)
    img.add_layer(cell_2,0)
    pdb.gimp_item_transform_flip_simple(cell_2, ORIENTATION_HORIZONTAL, True, 0)
    if rotate90:
        pdb.gimp_item_transform_rotate_simple(cell_2,ROTATE_90,TRUE,0,0)
    pdb.gimp_layer_translate(cell_2, cell_width*pos[0], cell_height*pos[1]) 
    return
    
def cell_p(cell, cell_width, cell_height, img, pos, rotate90=False):
    """
    this takes cell returned from get_rect_primary_cell() call
    flips it vertically and places it at pos
    eg.
    pos  = (1,0) one cell_width to the right
    pos =  (0,1) one cell_height down
    """
    cell_2 = cell.copy(0)
    img.add_layer(cell_2,0)
    pdb.gimp_item_transform_flip_simple(cell_2, ORIENTATION_VERTICAL, True, 0)
    if rotate90:
        pdb.gimp_item_transform_rotate_simple(cell_2,ROTATE_90,TRUE,0,0)
    pdb.gimp_layer_translate(cell_2, cell_width*pos[0], cell_height*pos[1]) 
    return
    
"""----------------------------------------------------------------------------"""

def img_sym_str(sym_type, sym_str, square, old, drawable, width, height,):
    """
    Makes an image from the specified sym_str
    """
    cell_width, cell_height= get_rect_primary_cell(old, drawable, width, height, square)
    cell, img = copy_primary_cell(old, drawable, width, height, cell_width, cell_height)
    tile, x, y =  tile_sym_str(sym_str, cell, cell_width, cell_height, img) 
    
    file_name = sym_type + '_' + filesafe_bdpq_str(sym_str) + '.xcf'
    pdb.gimp_image_set_filename(img,file_name)
    copy_tile(tile, img, (cell_width*x, 0), (0, cell_height*y)) 
    

def tile_sym_str(sym_str, cell_1, cell_width, cell_height, img):
    """
    This takes a string simailar  to 'bq|qb'and builds the pattern tile for 
    patterns based on a rectanglular primary cell .
    
    The syntax for the string:  
        string must start with 'b'  (for symmetry groups)
        q is the cell rotated 180 deg  
        d is the cell fliped horizontally  
        p is the cell flipped vertically  
        
        | denotes a new line  
        
    That is 'bq|qb' will build this tile   
    
    bq  
    qb  
    
    and hence this pattern (symmetry group p2  
    
    bqbqbq
    qbqbqb
    bqbqbq
    qbqbqb
    
    b+, d+, p+, q+  represent each cell rotated 90 deg (clockwise), these are 
    only required for p4 and p4g
    """
    i = 0 
    rot90 = False
    x = 0
    y = 0
    if len(sym_str) != 1:
        while i < len(sym_str):
            ch_index = i
            try:
                if sym_str[ch_index+1] == '+':
                    rot90 = True
                    i = i + 1
            except:
                #ran out of string
                pass
     
            if sym_str[ch_index] == 'b' : 
                cell_b(cell_1, cell_width, cell_height, img, (x,y), rot90)  
            if sym_str[ch_index] == 'd' : 
                cell_d(cell_1, cell_width, cell_height, img, (x,y), rot90) 
            if sym_str[ch_index] == 'p' : 
                cell_p(cell_1, cell_width, cell_height, img, (x,y), rot90) 
            if sym_str[ch_index] == 'q' : 
                cell_q(cell_1, cell_width, cell_height, img, (x,y), rot90)             
                
            if sym_str[i] == '|':
                y = y + 1
                x = 0
            else :
                x = x + 1
            rot90 = False  
            i = i + 1 
            
        x_repeats = x 
        y_repeats = y + 1
    else: 
        x_repeats = 1
        y_repeats = 1
        
    tile = img.merge_visible_layers(1)    
    return tile, x_repeats, y_repeats

bdpq_strs = ['b','b+','d','d+','p','p+','q','q+']    
    
def random_potato_game_string():
    """
    produces a random 'bdpq' style string for a 2 x 2 tile
    """    
    pg_str = random.choice(bdpq_strs) + random.choice(bdpq_strs) + '|' + \
             random.choice(bdpq_strs) + random.choice(bdpq_strs) 
    return pg_str
    
def filesafe_bdpq_str(bdpq_str):
    """
    takes a bdpq type string and returns one for use in filenames
    """
    sym_name = bdpq_str
    sym_name = sym_name.replace('+','t')
    sym_name = sym_name.replace('|','l') 
    return sym_name
     
"""-----------------------------------------------------------------------------
Groups with non-rectangular primary cells
--------------------------------------------------------------------------------"""

def get_tri_90_45_45_primary_cell(old, drawable, width, height):
    """
    A half square triangle primary cell is derived from the user's rectangular selection.
    The left most side of the rectangle is used as the left edge of the triangle, with the rectangle
    and triangle sharing the top left corner.
    This copies a selected triangle to new layer on a new image
    """
    # Find the area that has been selected in the original image
    old_is_sel, old_x1, old_y1, old_x2, old_y2 = pdb.gimp_selection_bounds(old)
    if  not old_is_sel:
        pdb.gimp_message("FATAL: Missing selection in old image!")
        #sys.exit(1)

    cell_height = old_y2 - old_y1    

    # Turn the initial selection into a triangle with 90, 45, 45 degree angles, original rectangle and triangle
    # share top left corner
    
    points = (old_x1, old_y1, old_x1 + cell_height, old_y1 , old_x1, old_y2)
    pdb.gimp_image_select_polygon(old, CHANNEL_OP_REPLACE, 6, points)

    new_cell_width = cell_height
    new_cell_height = cell_height

    cell, img = copy_primary_cell(old, drawable, width, height, new_cell_width, new_cell_height)
    return cell, new_cell_width, new_cell_height, img

def get_tri_90_60_30_primary_cell(old, drawable, width, height):
    """
    A 90, 60, 30 triangle primary cell is derived from the user's rectangular selection.
    The left most side of the rectangle is used as the left edge of the triangle, with the rectangle
    and triangle sharing the top left corner. The longer edge is the left most edge. 
    This copies a selected triangle to new layer on a new image.
    """
    # Find the area that has been selected in the original image
    old_is_sel, old_x1, old_y1, old_x2, old_y2 = pdb.gimp_selection_bounds(old)
    if  not old_is_sel:
        pdb.gimp_message("FATAL: Missing selection in old image!")
        #sys.exit(1)

    cell_height = old_y2 - old_y1    

    # Turn the initial selection into a triangle with 90, 60, 30 degree angles, original rectangle and triangle
    # share top left corner

    points = (old_x1, old_y1, old_x1 + int(cell_height/(3**0.5)), old_y1, old_x1, old_y2)
    pdb.gimp_image_select_polygon(old, CHANNEL_OP_REPLACE, 6, points)
    
    new_cell_width = int(cell_height/(3**0.5))
    new_cell_height = cell_height

    cell, img = copy_primary_cell(old, drawable, width, height, new_cell_width, new_cell_height)
    return cell, new_cell_width, new_cell_height, img

def get_tri_60_60_60_primary_cell(old, drawable, width, height):
    """
    An equalateral triangle is derived from the user's rectangular selection
    The triangle shares the rectangle's left side and the triangle points to the right.
    The triangle is selected in the original image and copied to a new layer on a new image
    """
    #pdb.gimp_context_set_feather(True)
    #pdb.gimp_context_set_antialias(True)
    #pdb.gimp_context_set_feather_radius(5, 5)

    # Find the area that has been selected in the original image
    old_is_sel, old_x1, old_y1, old_x2, old_y2 = pdb.gimp_selection_bounds(old)
    if  not old_is_sel:
        pdb.gimp_message("FATAL: Missing selection in old image!")
        
    cell_height = old_y2 - old_y1
    
    # Turn the initial selection into a equilateral triangle with equal sides, pointing to the right
    xm = int(round((old_y1 + (cell_height / 2.0))))
    inner_width = int(round(math.sqrt((cell_height**2)-((cell_height/2.0)**2))))
    ym = int(round((old_x1 + inner_width)))
    inner_width = int(inner_width)
    points = (old_x1, old_y1, ym, xm, old_x1, old_y2)
    
    pdb.gimp_image_select_polygon(old, CHANNEL_OP_REPLACE, 6, points)

    new_cell_width = inner_width
    new_cell_height = cell_height

    cell, img = copy_primary_cell(old, drawable, width, height, new_cell_width, new_cell_height)
    return cell, new_cell_width, new_cell_height, img


def get_diamond_primary_cell(old, drawable, width, height):
    """
    A 30/60 diamond is derived from the user's rectangular selection
    The diamond shares the rectangle's left side and the diamond points down and to the right.
    The diamond is selected in the original image and copied to a new layer on a new image
    """    
    # Find the area that has been selected in the original image
    old_is_sel, old_x1, old_y1, old_x2, old_y2 = pdb.gimp_selection_bounds(old)
    if  not old_is_sel:
        pdb.gimp_message("FATAL: Missing selection in old image!")
        
    cell_height = int(old_y2 - old_y1)
    
    # Turn the initial selection into a diamond  with equal sides and 30 deg 60 deg angles, 
    # diamond points down and to the right
    cell_width = int(math.sqrt((cell_height**2)-((cell_height/2.0)**2)))
    
    x2 = old_x1 + cell_width
    y2 = int((old_y1 + (cell_height / 2.0)))

    x3 = x2
    y3 = int(old_y1 + 1.5*cell_height)

    x4 = old_x1
    y4 = old_y1 + cell_height

    points = (old_x1, old_y1, x2, y2, x3, y3, x4, y4)
    pdb.gimp_image_select_polygon(old, CHANNEL_OP_REPLACE, 8, points)
    
    new_cell_width =  cell_width
    new_cell_height = int(1.5*cell_height)

    cell, img = copy_primary_cell(old, drawable, width, height, new_cell_width, new_cell_height)
    return cell, new_cell_width, new_cell_height, img

def get_kite_primary_cell(old, drawable, width, height):
    """
    A kite with 90 120 90 60 degree angles is derived from the user's rectangular selection.
    the kite is 1/3 of an equilateral triangle.
    The kite shares the rectangle's left side and the top left corner
    The diamond is selected in the original image and copied to a new layer on a new image
    """    
    # Find the area that has been selected in the original image
    old_is_sel, old_x1, old_y1, old_x2, old_y2 = pdb.gimp_selection_bounds(old)
    if  not old_is_sel:
        pdb.gimp_message("FATAL: Missing selection in old image!")
        
    cell_height = int(old_y2 - old_y1)
    
    # Turn the initial selection into a diamond  with equal sides and 30 deg 60 deg angles, 
    # diamond points down and to the right
    cell_width = int(math.sqrt((cell_height**2)-((cell_height/2.0)**2)))

    x3 = old_x1 + cell_width
    y3 = old_y1 + int(cell_height/2.0)
    x4 = old_x1 + int(cell_height/(3**0.5)) 
    y4 = old_y1

    points = (old_x1, old_y1, old_x1, old_y2, x3, y3, x4, y4)
    pdb.gimp_image_select_polygon(old, CHANNEL_OP_REPLACE, 8, points)

    new_cell_width =  cell_width
    new_cell_height = cell_height

    cell, img = copy_primary_cell(old, drawable, width, height, new_cell_width, new_cell_height)
    return cell, new_cell_width, new_cell_height, img




def p3m1(old, drawable, width, height):
    """
    The primary cell of p3m1 is an equilateral triangle.
    """
    cell_1, cell_width, cell_height, img = get_tri_60_60_60_primary_cell(old, drawable, width, height)

    pdb.gimp_layer_translate(cell_1, 0, cell_height/2)
    
    cell_2 = cell_1.copy(0)
    img.add_layer(cell_2,0)
    pdb.gimp_item_transform_flip_simple(cell_2, ORIENTATION_VERTICAL, 1, 0)
    pdb.gimp_item_transform_rotate(cell_2, math.pi/3.0, False,cell_width, cell_height)
    
    
    
    #pdb.gimp_selection_none(img)
    
    
    pair_1 = img.merge_visible_layers(1)
    pair_2 = pair_1.copy(0)
    img.add_layer(pair_2,0)
    pdb.gimp_item_transform_rotate(pair_2, 2.0*math.pi/3.0, False,cell_width, cell_height)
    #pdb.gimp_selection_none(img)
     
    pair_3 = pair_1.copy(0)
    img.add_layer(pair_3,0)
    pdb.gimp_item_transform_rotate(pair_3, 4.0*math.pi/3.0, False,cell_width, cell_height)
    #pdb.gimp_selection_none(img)

    tile = img.merge_visible_layers(1)
    pdb.gimp_image_set_filename(img,'p3m1.xcf')
    copy_tile(tile, img, (2*cell_width, 0), (cell_width, int(1.5*cell_height)))
    
def p3(old, drawable, width, height):
    """
    The primary cell of p3 is a 30 60 diamond.
    """     
    cell_1, cell_width, cell_height, img = get_diamond_primary_cell(old, drawable, width, height)
    pdb.gimp_layer_translate(cell_1, 0, cell_height/3)

    cell_2 = cell_1.copy(0)
    img.add_layer(cell_2,0)
    pdb.gimp_item_transform_rotate(cell_2, 2.0*math.pi/3.0, 1,0, 0)
    pdb.gimp_layer_translate(cell_2, cell_width/2, -0.5*cell_height)
    pdb.gimp_selection_none(img)    

    cell_3 = cell_1.copy(0)
    img.add_layer(cell_3,0)
    pdb.gimp_item_transform_rotate(cell_3, 4.0*math.pi/3.0, 1,0, 0)
    pdb.gimp_layer_translate(cell_3, cell_width, 0)
    pdb.gimp_selection_none(img)


    tile = img.merge_visible_layers(1)
    pdb.gimp_image_set_filename(img,'p3.xcf')
    copy_tile(tile, img, (2*cell_width, 0), (cell_width, cell_height))


def p4m(old, drawable, width, height):
    """
    The primary cell of p4m is a  90 45 45 triangle.
    """
    cell_1, cell_width, cell_height, img = get_tri_90_45_45_primary_cell(old, drawable, width, height)

    #make a copy and mirror it along long side of cell
    cell_2 = cell_1.copy(0)
    img.add_layer(cell_2,0)
    pdb.gimp_item_transform_flip(cell_2, cell_width, 0, 0, cell_height)
    
    tile_1 = img.merge_visible_layers(1)

    # Make a copy of the 1st cell and mirror it
    tile_2 = tile_1.copy(0)
    img.add_layer(tile_2,0)
    pdb.gimp_item_transform_flip_simple(tile_2, ORIENTATION_HORIZONTAL, True, 0)
    
    
    
    pdb.gimp_layer_translate(tile_2, cell_width, 0)
        
    # Merge the two layers
    pair_1 = img.merge_visible_layers(1)

    # Make copies of the fist pair and mirror them
    pair_2 = pair_1.copy(0)
    img.add_layer(pair_2, 0)  
    pdb.gimp_item_transform_flip_simple(pair_2, ORIENTATION_VERTICAL, True, 0)
    pdb.gimp_layer_translate(pair_2, 0, cell_height)
    
    tile = img.merge_visible_layers(1)
    pdb.gimp_image_set_filename(img,'p4m.xcf')
    copy_tile(tile, img, (2*cell_width, 0), (0, 2*cell_height))
    
def p6(old, drawable, width, height, rot60=0):
    """
    The primary cell of p6 is either an equilateral triangle or a kite
    we'll do the equilateral triangle
    3 alternatives
    rotate the block 60 deg and regenerate tile   
    
    rot60 = 0, 1, 2 number of 60 degree rotations to apply 
    
    """
    cell_1, cell_width, cell_height, img = get_tri_60_60_60_primary_cell(old, drawable, width, height)
    
    
    pdb.gimp_item_transform_rotate(cell_1, rot60*2.0*math.pi/3.0, 0, round(cell_height/(2.0*(3.0**0.5))) , round(cell_height/2.0) )    
    pdb.gimp_layer_translate(cell_1, 0, round(cell_height/2.0))
    pdb.gimp_selection_none(img)

    #rotate 60 deg
    cell_2 = cell_1.copy(0)
    img.add_layer(cell_2,0)
    pdb.gimp_item_transform_rotate(cell_2, math.pi/3.0, 0 ,cell_width, cell_height)
    pdb.gimp_selection_none(img)
    
    
    #rotate 120 deg
    cell_3 = cell_1.copy(0)
    img.add_layer(cell_3,0)
    pdb.gimp_item_transform_rotate(cell_3, 2.0*math.pi/3.0, 0 ,cell_width, cell_height)
    pdb.gimp_selection_none(img)

    #rotate 180 deg
    cell_4 = cell_1.copy(0)
    img.add_layer(cell_4,0)
    pdb.gimp_item_transform_rotate(cell_4, 3.0*math.pi/3.0, 0 ,cell_width, cell_height)
    pdb.gimp_selection_none(img)

    #rotate 240 deg
    cell_5 = cell_1.copy(0)
    img.add_layer(cell_5,0)
    pdb.gimp_item_transform_rotate(cell_5, 4.0*math.pi/3.0, 0 ,cell_width, cell_height)
    pdb.gimp_selection_none(img)

    #rotate 300 deg
    cell_6 = cell_1.copy(0)
    img.add_layer(cell_6,0)
    pdb.gimp_item_transform_rotate(cell_6, 5.0*math.pi/3.0, 0 ,cell_width, cell_height)
    pdb.gimp_selection_none(img)
    
    
    tile = img.merge_visible_layers(1)
    pdb.gimp_image_set_filename(img,'p6_' + str(rot60) + '.xcf')
    copy_tile(tile, img, (2*cell_width, 0), (cell_width, round(1.5*cell_height)))

def p31m(old, drawable, width, height):
    """
    The primary cell of p31m is a 1/3 equilateral triangle, this can be a 30,30,120 triangle, half a hexagon or a kite.
    we'll do the kite
    """
    cell_1, cell_width, cell_height, img = get_kite_primary_cell(old, drawable, width, height)

    pdb.gimp_item_transform_rotate(cell_1, -math.pi/2.0, 0 ,0, 0)
    cell_length = int(2.0*cell_height/(3**0.5))
    pdb.gimp_layer_translate(cell_1, 0, cell_length)

    #mirror along one side
    cell_2 = cell_1.copy(0)
    img.add_layer(cell_2,0)
    pdb.gimp_item_transform_flip(cell_2, 0, cell_length, cell_height, cell_length)
    pdb.gimp_selection_none(img)

    tile_1 = img.merge_visible_layers(1)

    #rotate 120 deg
    tile_2 = tile_1.copy(0)
    img.add_layer(tile_2,0)
    pdb.gimp_item_transform_rotate(tile_2, 2.0*math.pi/3.0, 0 ,cell_height, cell_length)
    pdb.gimp_selection_none(img)
    
    #rotate 240 deg
    tile_3 = tile_1.copy(0)
    img.add_layer(tile_3,0)
    pdb.gimp_item_transform_rotate(tile_3, 4.0*math.pi/3.0, 0 ,cell_height, cell_length)
    pdb.gimp_selection_none(img)

    #merge into one tile
    tile = img.merge_visible_layers(1)
    pdb.gimp_image_set_filename(img,'p31m.xcf')
    copy_tile(tile, img, (2*cell_height, 0), (cell_height, (3.0**0.5)*cell_height))

def p6m(old, drawable, width, height):
    """
    The primary cell of p6 is a triangle with 90, 60, 30 degree angles.
    """
    cell_1, cell_width, cell_height, img = get_tri_90_60_30_primary_cell(old, drawable, width, height)
    r = 2 * cell_width
    
    # rotate and move cell_1
    pdb.gimp_item_transform_rotate(cell_1, -math.pi/2.0, 0 ,0, 0)
    pdb.gimp_layer_translate(cell_1, 0, r)

    #mirror cell_1 to give equilateral triangle
    cell_2 = cell_1.copy(0)
    img.add_layer(cell_2,0)
    pdb.gimp_item_transform_flip(cell_2, 0, r, cell_height, r)
    pdb.gimp_selection_none(img)

    cell_1 = img.merge_visible_layers(1)

    #make six rotational copies
    #rotate 60 deg
    cell_2 = cell_1.copy(0)
    img.add_layer(cell_2,0)
    pdb.gimp_item_transform_rotate(cell_2, math.pi/3.0, 0 ,cell_height, r)
    pdb.gimp_selection_none(img)

    #rotate 120 deg
    cell_3 = cell_1.copy(0)
    img.add_layer(cell_3,0)
    pdb.gimp_item_transform_rotate(cell_3, 2.0*math.pi/3.0, 0 ,cell_height, r)
    pdb.gimp_selection_none(img)

    #rotate 180 deg
    cell_4 = cell_1.copy(0)
    img.add_layer(cell_4,0)
    pdb.gimp_item_transform_rotate(cell_4, 3.0*math.pi/3.0, 0 ,cell_height, r)
    pdb.gimp_selection_none(img)

    #rotate 240 deg
    cell_5 = cell_1.copy(0)
    img.add_layer(cell_5,0)
    pdb.gimp_item_transform_rotate(cell_5, 4.0*math.pi/3.0, 0 ,cell_height, r)
    pdb.gimp_selection_none(img)

    #rotate 300 deg
    cell_6 = cell_1.copy(0)
    img.add_layer(cell_6,0)
    pdb.gimp_item_transform_rotate(cell_6, 5.0*math.pi/3.0, 0 ,cell_height, r)
    pdb.gimp_selection_none(img)
    
    tile = img.merge_visible_layers(1)    
    pdb.gimp_image_set_filename(img,'p6m.xcf')
    copy_tile(tile, img, (2*cell_height, 0), (cell_height, (3.0**0.5)*cell_height))

# Register with The Gimp
register(
    "symmetry_tile",
    "Turn selection into tiled symmetric image",
    "Turn selection into tiled symmetric image",
    "Eleanor Howick",
    "(c) 2014, Eleanor Howick",
    "2014-07-05",
    "<Image>/Filters/Render/Symmetry Tile",
    "*",
    [
        (PF_INT32, "width", "Width", 500),
        (PF_INT32, "height", "Height", 500),
        (PF_OPTION,"sym_type",   "Symmetry group:", 0, sym_types_list),
        (PF_BOOL, "muliple","Multiple images:" , 0),  
        (PF_STRING, "bdpq_str", "bdpq string:", "")
    ],
    [],
    symmetry_tile);

main()
