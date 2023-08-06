# -*- coding: utf-8 -*-

### imports ###################################################################
import numpy as np

###############################################################################
class Notch:
    C_wafer = (0, 0) # wafer center
    notch_depth = 1
    r_n = 0.9
    r_pin = 1.5
    r_wafer = 75

    def __init__(self):
        ### notch radius
        dy_notch = np.sqrt(2) * self.r_n
        y_notch = self.r_wafer - self.notch_depth - (np.sqrt(2) - 1) * self.r_n
        
        self.N_notch = np.array((0, y_notch))
        self.C_notch = self.N_notch + np.array((0, dy_notch))

        ### SEMI pin
        dy_pin = np.sqrt(2) * self.r_pin
        self.C_pin = self.N_notch + np.array((0, dy_pin))

        ### notch edges
        x = 1 / 2 * (-y_notch + np.sqrt(2 * self.r_wafer**2 - y_notch**2))
        y = x + y_notch
    
        self.X_left = np.array((-x, y))
        self.X_right = np.array((x, y))

        nx = dy_notch / 2
        n_right = nx * np.array((1, -1))
        n_left = nx * np.array((-1, -1))
        
        self.N_right = self.C_notch + n_right
        self.N_left = self.C_notch + n_left

        delta_phi = np.arcsin(self.X_right[0] / self.r_wafer)
        delta_phi_deg = np.rad2deg(delta_phi)
        self.theta1 = 90 + delta_phi_deg
        self.theta2 = 90 - delta_phi_deg
        
    @property
    def d_notch(self):
        return 2 * self.r_n

    @property
    def d_wafer(self):
        return 2 * self.r_wafer