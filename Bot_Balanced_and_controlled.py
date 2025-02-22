# Code Written by - Anish Walke - www.linkedin.com/in/anish-walke1709
#                   Siddharth Badshe - https://www.linkedin.com/in/siddharth-badshe-747510251/
#                   Ved Namjoshi - https://www.linkedin.com/in/ved-namjoshi
# The code is written for a self balancing bot in CoppeliaSim 

import math
def sysCall_init():
    sim = require('sim')

    self.bot_body_handle = sim.getObjectHandle('/body')
    self.left_motor_joint = sim.getObjectHandle('/body/left_joint')
    self.right_motor_joint = sim.getObjectHandle('/body/right_joint')

    self.Q = [[1, 0, 0, 0],
              [0, 10, 0, 0],
              [0, 0, 100, 0],
              [0, 0, 0, 100]]

    self.R = [[1]]

    self.K = [1, 20, 110, 80]

    self.manual_control = False
    self.manual_left_speed = 0
    self.manual_right_speed = 0
    
def normalize_angle(angle):
    while angle > math.pi:
        angle -= 2 * math.pi
    while angle < -math.pi:
        angle += 2 * math.pi
    return angle

def sysCall_actuation():
    sim = require('sim')

    current_position = sim.getObjectPosition(self.bot_body_handle, -1)  
    current_velocity = sim.getObjectVelocity(self.bot_body_handle)      
    current_orientation = sim.getObjectOrientation(self.bot_body_handle, -1) 
    
    x_position = current_position[2]  
    x_velocity = current_velocity[0][1]
      
    angle = normalize_angle(current_orientation[1])  
    angular_velocity = current_velocity[1][1]
    print(current_orientation)
    
    
    x1 = 0 - x_position  
    x2 = 0 - x_velocity  
    x3 = 0 - angle  
    x4 = 0.001 - angular_velocity  

    x = [x1, x2, x3, x4]
#angle= constant if values goes above z then values diff(179 to -180) 
    U = -self.K[0] * x[0] - self.K[1] * x[1] - self.K[2] * x[2] - self.K[3] * x[3]

    if self.manual_control:
        left_speed = U*3 + self.manual_left_speed 
        right_speed = U *3 + self.manual_right_speed 
        self.manual_control = False
    else:
        left_speed = U * 3
        right_speed = U * 3

    sim.setJointTargetVelocity(self.left_motor_joint, left_speed)
    sim.setJointTargetVelocity(self.right_motor_joint, right_speed)

def sysCall_sensing():
    sim = require('sim')

    message, data, data2 = sim.getSimulatorMessage()
    
    if (message == sim.message_keypress):
        if (data[0] == 2007):  
            self.manual_control = True
            self.manual_left_speed = 2.3
            self.manual_right_speed = 2.3
            print("Moving forward")
        elif (data[0] == 2008):  
            self.manual_control = True
            self.manual_left_speed = -2.3
            self.manual_right_speed = -2.3
            print("Moving backward")
        elif (data[0] == 2009):  
            self.manual_control = True
            self.manual_left_speed = 5.7
            self.manual_right_speed = -5.7
            print("Turning left")
        elif (data[0] == 2010):  
            self.manual_control = True
            self.manual_left_speed = -5.7
            self.manual_right_speed = 5.7
            print("Turning right")
        else:
            self.manual_control = False
            self.manual_left_speed = --left_speed
            self.manual_right_speed =--right_speed
            print("Manual control deactivated")

def sysCall_cleanup():
    sim = require('sim')

    pass