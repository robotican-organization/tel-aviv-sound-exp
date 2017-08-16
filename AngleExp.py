#!/usr/bin/env python
import rospy
import subprocess
from subprocess import call
import csv
import time
from matplotlib import pyplot as plt
import sys
import roslib
import rospy
from ronexp.srv import *
from geometry_msgs.msg import Quaternion,PoseStamped
from nav_msgs.msg import Odometry
from sensor_msgs.msg import Temperature
from sensor_msgs.msg import RelativeHumidity

__author__ = 'Itamar Eliakim + Yam Geva'

class AngleExp():
    def __init__(self):
        self.script = "/home/komodo/catkin_ws/src/ronexp/src/test-usb1608G"
	self.posx_odometry = 0
        self.posy_odometry = 0
        self.posz_odometry = 0
        self.rotx_odometry = 0
        self.roty_odometry = 0
        self.rotz_odometry = 0
        self.rotw_odometry = 0
	self._temperature=0
	self._humidity=0
	self.got_odom=False
	self.got_temperature=False
	self.got_humidity=False
	rospy.init_node('runexp')
	s=rospy.Service('ronexp', runexp1_srv, self.handle_ronexp1)
	rospy.Subscriber('/diff_driver/odometry',Odometry,self.odometryCb)
        rospy.Subscriber('Temperature', Temperature, self.callback_temp)
        rospy.Subscriber('RelativeHumidity', RelativeHumidity, self.callback_humidity)
	print "ronexp service is ready"
	rospy.spin()

    def handle_ronexp1(self,req):
	resp = runexp1_srvResponse()
	resp.ack = False
	if self.got_odom and self.got_temperature and self.got_humidity:
		self.outfolder = req.path
		self.angle=round(req.angle,3)
		for k in range(0,int(req.samples)):
            		self.call_rec(self.angle,k+1)
            		#time.sleep(0.5)
		self.writeToodometry()	
		resp.ack = True
	return resp

    def callback_temp(self,data):
        self._temperature = data.temperature
	if not self.got_temperature:
		self.got_temperature=True
		print("Got Temperature")

    def callback_humidity(self, data):
        self._humidity = data.relative_humidity
	if not self.got_humidity:
		self.got_humidity=True
		print("Got RelativeHumidity")

    def data_attr(self, data):
            data = str(data)
            data = data.replace("]", "")
            data = data.replace("[", "")
            data = data.replace(" \\n", "")
            data = data.replace("'", "")
            data = data.split(',')
            for i in range(0, len(data)):
                data[i] = float(data[i])
            return data

    def writeToodometry(self):
	Odometryfile = open(self.outfolder + "/angle_"+str(self.angle)+"-ODR.csv", "w")
	#Odometryfile.write("x,y,z,qx,qy,qz,qw,Temperature,RelativeHumidity\n")
        line = str(self.posx_odometry) + "," + str(self.posy_odometry) + "," + str(self.posz_odometry) + "," + str(self.rotx_odometry) + "," + str(self.roty_odometry) + "," + str(self.rotz_odometry) + "," + str(self.rotw_odometry)+","+str(self._temperature)+","+str(self._humidity)+ "\n"
        Odometryfile.write(line)
	Odometryfile.close()

    def odometryCb(self,msg):
        self.posx_odometry = msg.pose.pose.position.x
        self.posy_odometry = msg.pose.pose.position.y
        self.posz_odometry = msg.pose.pose.position.z

        self.rotx_odometry = msg.pose.pose.orientation.x
        self.roty_odometry = msg.pose.pose.orientation.y
        self.rotz_odometry = msg.pose.pose.orientation.z
        self.rotw_odometry = msg.pose.pose.orientation.w
	
	if not self.got_odom:
		self.got_odom=True
		print("Got Odometry")

    def call_rec(self,angle,step):
	snap_cmd="fswebcam -q -d /dev/video0 -r 1280x720 --no-banner "+ self.outfolder + "/angle_"+str(angle) + "-n_" + str(step) + "-snapshot.jpg"
	return_code = subprocess.call(snap_cmd, shell=True) 
        #proc = call(self.script, stdout=subprocess.PIPE)
        #rospy.sleep(0.2)
        #resp = open('/home/komodo/catkin_ws/src/ronexp/src/output1.csv', 'r')
        #data = resp.readlines()
        #resp.close()
        #data = self.data_attr(data)

        rightearfile = open(self.outfolder + "/angle_"+str(angle) + "-n_" + str(step) + "-right" + ".csv", "wb")
        writer = csv.writer(rightearfile)

        leftearfile = open(self.outfolder + "/angle_"+str(angle) + "-n_" + str(step) + "-left" + ".csv", "wb")
        leftwriter = csv.writer(leftearfile)

        leftear = []
        rightear = []


        #for j in range(0,len(data),2):
        #    leftear.append(data[j])
        #    rightear.append(data[j+1])

        #plt.specgram(rightear, NFFT=100, Fs=250000, noverlap=99, cmap=plt.cm.gist_heat)
        #plt.title('Right Ear');
        #plt.xlabel('Time [sec]');
        #plt.ylabel('Frequency [Hz]');
        #plt.savefig(self.outfolder + "angle_"+str(angle) + "-n_" + str(step) + "-fft_right" + ".jpg")
        #plt.clf()
        #plt.close()

        #plt.specgram(leftear, NFFT=100, Fs=250000, noverlap=99, cmap=plt.cm.gist_heat)
        #plt.title('Left Ear');
        #plt.xlabel('Time [sec]');
        #plt.ylabel('Frequency [Hz]');
        #plt.savefig(self.outfolder + "angle_"+str(angle) + "-n_" + str(step) + "-fft_left" + ".jpg")
        #plt.clf()
        #plt.close()

        #for row in leftear:
        #    leftwriter.writerow([row])

        #for row in rightear:
        #    writer.writerow([row])

        rightearfile.close()
        leftearfile.close()

if __name__ == "__main__":
	AngleExp()


