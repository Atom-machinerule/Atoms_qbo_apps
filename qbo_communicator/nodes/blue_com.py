#!/usr/bin/env python

"""
  voice_nav.py allows controlling a mobile base using simple speech commands.
  Based on the voice_cmd_vel.py script by Michael Ferguson in the pocketsphinx ROS package.
"""

import roslib; roslib.load_manifest('qbo_communicator')
import rospy

from geometry_msgs.msg import Twist
from std_msgs.msg import String
from math import copysign
import os

from sound_play.libsoundplay import SoundClient

class voice_cmd_vel:
    def __init__(self):
        rospy.on_shutdown(self.cleanup)
        self.max_speed = rospy.get_param("~max_speed", 0.4)
        self.max_angular_speed = self.max_speed * 2
        self.speed = rospy.get_param("~start_speed", 0.1)
        self.linear_increment = rospy.get_param("~linear_increment", 0.05)
        self.angular_increment = rospy.get_param("~angular_increment", 0.4)
        self.rate = rospy.get_param("~rate", 5)
        r = rospy.Rate(self.rate)
        self.paused = False
        self.wavepath = rospy.get_param("~wavepath", "")

        # Create the sound client object
        self.soundhandle = SoundClient()
        
        rospy.sleep(1)
        self.soundhandle.stopAll()

        # Initialize the Twist message we will publish.
        self.msg = Twist()

        # Publish the Twist message to the cmd_vel topic
        self.cmd_vel_pub = rospy.Publisher('/cmd_vel', Twist)
        
        # Subscribe to the /recognizer/output topic to receive voice commands.
        rospy.Subscriber('uc0Response', String, self.speechCb)
        
        # A mapping from keywords to commands.
        self.keywords_to_command = {

				    'stop': ['stop', 'h', 'halt'],
                                    'slower': ['slow down', 's', 'slower'],
                                    'faster': ['speed up', 'f', 'faster'],
                                    'forward': ['forward', 'a', 'ahead', 'straight'],
                                    'backward': ['back', 'backward', 'b', 'back up'],
                                    'left': ['left', 'l'],
                                    'right': ['right', 'r'],
                                    'turn left': ['turn left', 'c'],
                                    'turn right': ['turn right', 'x'],
				    

				    
				    'smile': ['smile','e'],					    					    'curious': ['curious', '9'],
				    'mad': ['mad', 'm'],
				    'sad': ['sad', 'd'],			
				    

				    'yes': ['yes', 'y'],
				    'hello': ['hello', 'g'],
				    'bye': ['bye','j'],
				    'no': ['no','n'],
				
	  			   
				    'look left': ['look left', 'z'],
				    'look forward': ['look forward', '6'],
				    'look up': ['look up', '7'],
				    'look right': ['look right', '8'],


                                    'quarter': ['quarter speed'],
                                    'half': ['half speed'],
                                    'full': ['full speed'],
                                    'pause': ['pause speech'],
                                    'continue': ['continue speech']}
        				
        rospy.loginfo("Ready to receive Bluetooth commands")
        
        # We have to keep publishing the cmd_vel message if we want the robot to keep moving.
        while not rospy.is_shutdown():
            self.cmd_vel_pub.publish(self.msg)
            r.sleep()                       
            
    def get_command(self, data):
        for (command, keywords) in self.keywords_to_command.iteritems():
            for word in keywords:
                if data.find(word) > -1:
                    return command
        
    def speechCb(self, msg):        
        command = self.get_command(msg.data)
        
        rospy.loginfo("Command: " + str(command))
        
        if command == 'pause':
            self.paused = True
        elif command == 'continue':
            self.paused = False
            
        if self.paused:
            return       
          



        if command == 'smile':

	    os.system("rostopic pub --once /Qbo/runExpression std_msgs/String 'happy'") 
	    rospy.sleep(1)

	if command == 'curious':

	    os.system("rostopic pub --once /Qbo/runExpression std_msgs/String 'happy'") 
	    rospy.sleep(1)

	if command == 'mad':

	    os.system("rostopic pub --once /Qbo/runExpression std_msgs/String 'happy'") 
	    rospy.sleep(1)

	if command == 'sad':

	    os.system("rostopic pub --once /Qbo/runExpression std_msgs/String 'happy'") 
	    rospy.sleep(1)



	if command == 'yes':
 
	    os.system("rostopic pub --once /Qbo/runExpression std_msgs/String 'happy'") 
	    rospy.sleep(1)

	if command == 'hello':

	    os.system("rostopic pub --once /Qbo/runExpression std_msgs/String 'happy'") 
	    rospy.sleep(1)

	if command == 'bye':

	    os.system("rostopic pub --once /Qbo/runExpression std_msgs/String 'happy'") 
	    rospy.sleep(1)

	if command == 'no':

	    os.system("rostopic pub --once /Qbo/runExpression std_msgs/String 'happy'") 
	    rospy.sleep(1)


	if command == 'look left':
 

	    rospy.sleep(1)

	if command == 'look forward':
 

	    rospy.sleep(1)

	if command == 'look up':
 

	    rospy.sleep(1)

	if command == 'look right':


	    rospy.sleep(1)






	

        if command == 'forward':
            self.msg.linear.x = self.speed
            self.msg.angular.z = 0

        elif command == 'left':
            self.msg.linear.x = 0
            self.msg.angular.z = self.speed * 2
                
        elif command == 'right':  
            self.msg.linear.x = 0      
            self.msg.angular.z = -self.speed * 2
            
        elif command == 'turn left':
            if self.msg.linear.x != 0:
                self.msg.angular.z += self.angular_increment
            else:        
                self.msg.angular.z = self.speed * 2
                
        elif command == 'turn right':    
            if self.msg.linear.x != 0:
                self.msg.angular.z -= self.angular_increment
            else:        
                self.msg.angular.z = -self.speed * 2
                
        elif command == 'backward':
            self.msg.linear.x = -self.speed
            self.msg.angular.z = 0
            
        elif command == 'stop': 
            # Stop the robot!  Publish a Twist message consisting of all zeros.         
            self.msg = Twist()
        
        elif command == 'faster':
            self.speed += self.linear_increment
            if self.msg.linear.x != 0:
                self.msg.linear.x += copysign(self.linear_increment, self.msg.linear.x)
            if self.msg.angular.z != 0:
                self.msg.angular.z += copysign(self.angular_increment, self.msg.angular.z)
            
        elif command == 'slower':
            self.speed -= self.linear_increment
            if self.msg.linear.x != 0:
                self.msg.linear.x -= copysign(self.linear_increment, self.msg.linear.x)
            if self.msg.angular.z != 0:
                self.msg.angular.z -= copysign(self.angular_increment, self.msg.angular.z)
                
        elif command in ['quarter', 'half', 'full']:
            if command == 'quarter':
                self.speed = copysign(self.max_speed / 4, self.speed)
        
            elif command == 'half':
                self.speed = copysign(self.max_speed / 2, self.speed)
            
            elif command == 'full':
                self.speed = copysign(self.max_speed, self.speed)
            
            if self.msg.linear.x != 0:
                self.msg.linear.x = copysign(self.speed, self.msg.linear.x)
            if self.msg.angular.z != 0:
                self.msg.angular.z = copysign(self.speed * 2, self.msg.angular.z)
                
        else:
            return

        self.msg.linear.x = min(self.max_speed, max(-self.max_speed, self.msg.linear.x))
        self.msg.angular.z = min(self.max_angular_speed, max(-self.max_angular_speed, self.msg.angular.z))

    def cleanup(self):
        # When shutting down be sure to stop the robot!  Publish a Twist message consisting of all zeros.
        twist = Twist()
        self.cmd_vel_pub.publish(twist)

if __name__=="__main__":
    rospy.init_node('blue_com')
    try:
        voice_cmd_vel()
    except:
        pass

