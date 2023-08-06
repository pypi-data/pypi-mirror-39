import cv2
import numpy as np

class Point:
    """
    Class to represent a 2D point.
    """
    def __init__(self, x, y):

        self.x = x
        self.y = y

    
    def get_xy(self):
    """
    Return x and y as a tuple.
    """
        return (x,y)

class PolygonDrawer:
    """
    Class to create a polygon by clicking points.
    An array stores the point x & y coordinates.
    """
    def __init__(self):

        self.input = None
        self.output = None
        self.points = np.array([], dtype=np.int32)
        self.draw_colour = (0,255,255)

        cv2.setMouseCallback()

    def update(self):
        """
        Get latest frame from the input,  and draw the overlay shape.
        """
        self.input.update()
        
        if self.points:
            cv2.polylines(self.input.frame, self.points, False, self.draw_colour)
        
       self.output = self.input

    @staticmethod
    def add_point_on_mouse_click(event, x, y, flags, param):
        """
        Callback to add mouse click coordinates to the points array.
        """
        self.points.append(x)
        self.points.append(y)

    def draw(self, frame):
        """
        Draw the polygon.
        """
        pass

    

