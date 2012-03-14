
import ds9
from functools import  wraps
import functools

def make_point_region_text(coords, color="green"): #Go with American spelling for consistency, although it pains me. 
    return "point({x},{y}) # point=x color={c}".format(
                              x=coords[0], y=coords[1],
                              c=color)

def region_file_header():
    return """# Region file format: DS9 version 4.1
# Filename: un_implemented
global color=green dashlist=8 3 width=1 font="helvetica 10 normal" select=1 highlite=1 dash=0
physical
"""

def save_points_to_region_file(coords_list, filename):
    with open(filename, 'w') as f:
        f.write(region_file_header())
        for pt in coords_list:
            f.write(make_point_region_text(pt) +"\n")
    


class DS9Instance(ds9.ds9):
    """ Wrapper class adding extra functionality to a ds9 instance.
        
        Uses a "per_frame" decorator to create all frame functions, e.g. all_pan_to.
        (I got all excited and went a bit meta) 
        """    
        
    def __init__(self):        
        super(DS9Instance, self).__init__()
        self.clear()
        self._wrap_per_frame_functions()
        
        
        
    def _for_all_frames(self, self_action):
        """Wraps a view modification function, returning a version which is repeated on every frame"""
        def all_frms_wrapper(*args, **kwds):
            init_frame = self.get("frame")
            all_frames = self.get("frame all")
            for frm in all_frames.split():
                self.set("frame "+frm)
                self_action(self, *args, **kwds)
            self.set("frame "+init_frame)
        return all_frms_wrapper
    
    
    def _add_function_name_to_list(fn, l):
        """Using functools.partial, 
        turn this into a decorator which lodges the function name in a list to be processed at init time"""
        l.append(fn)
        return fn
    
    _frame_functions=[]
    per_frame = functools.partial(_add_function_name_to_list, l=_frame_functions)
    
    def _wrap_per_frame_functions(self):
        """Renames and attributes wrapped versions of functions in the _frame_functions list"""
        for fn in self._frame_functions:
            wrapped_fn = self._for_all_frames(fn)
            setattr(self, "all_"+fn.__name__, wrapped_fn)
                    
    def clear(self):
        self.set("frame delete all")
    
    def quit(self):
        self.set("quit")
    
    @per_frame    
    def zoom_to(self, zoom):
        self.set("zoom to "+ str(zoom))
        
    @per_frame    
    def zoom_to_fit(self):
        self.set("zoom to fit")
    
    @per_frame
    def pan_to(self, coords, coord_type="physical"):
        self.set(" ".join(("pan to ", 
                                    str(coords[0]), str(coords[1]), 
                                    coord_type))
                 )
        
    @per_frame 
    def scale_limits(self, min, max):
        cmd =" ".join(("scale limits", str(min), str(max) ))
        self.set( cmd )
        
    @per_frame
    def scale_type(self, type_string):
        self.set( "scale " + type_string )
        
    @per_frame
    def add_region(self, region_text):
        self.set("regions command {{{rgn}}}".format(rgn=region_text))
        
    @per_frame
    def clear_regions(self):
        self.set("regions delete all")
        
    @per_frame
    def add_point(self, pt_coords, color="green"):
        self.add_region(make_point_region_text(pt_coords, color))
        
    
                
    def tile(self, tile_setting):             
        if (tile_setting is True) or tile_setting is "yes":
            self.set("tile yes")
        elif (tile_setting is False) or tile_setting is "no":
            self.set("tile no")
        
    def open(self, filename):
        if self.get("frame all") is "":
            self.open_in_new_frame(filename)
        else:
            self.set("file "+filename)
        
    def open_in_new_frame(self, filename):
        self.set("frame new")
        self.open(filename)
        
     