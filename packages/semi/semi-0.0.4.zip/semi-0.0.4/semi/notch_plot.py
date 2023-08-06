# -*- coding: utf-8 -*-

### imports ###################################################################
import numpy as np

### imports from ##############################################################
from matplotlib.lines import Line2D
from matplotlib.patches import Arc, Circle

### relative imports from #####################################################
from .notch import Notch

###############################################################################
class NotchPlot(Notch):
    def __init__(self):
        super().__init__()
        
        self.notch_arc = Arc(
                self.C_notch, self.d_notch, self.d_notch,
                theta1=225, theta2=315)

        self.pin = Circle(self.C_pin, self.r_pin, fill=None)

        XY = np.vstack((self.N_right, self.X_right))
        self.notch_right = Line2D(XY[:, 0], XY[:,1], color='k', linewidth=1)

        XY = np.vstack((self.N_left, self.X_left))
        self.notch_left = Line2D(XY[:, 0], XY[:,1], color='k', linewidth=1)

        self.wafer_arc = Arc(
            self.C_wafer, self.d_wafer, self.d_wafer,
            theta1=self.theta1, theta2=self.theta2)

    def draw(self, ax):
        ### notch radius
        ax.add_patch(self.notch_arc)
    
        ### SEMI pin
        ax.add_patch(self.pin)
        
        ### notch edges
        ax.add_line(self.notch_right)
        ax.add_line(self.notch_left)
        
        ### wafer radius
        ax.add_patch(self.wafer_arc)
        
        ax.set_aspect('equal')
        ax.set_xlabel('x [mm]')
        ax.set_xlim(-3, 3)
        ax.set_ylabel('y [mm]')
        ax.set_ylim((73, 78))