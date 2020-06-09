import ntpath
from os import listdir
from os.path import isfile, join
import glob
import numpy as np
import pandas as pd

from scipy import stats
import seaborn as sns
import matplotlib.pyplot as plt


class PupilIDT(object):
    def __init__(self, sample_freq=40, threshold_disperssion=7):
        self.sample_freq = sample_freq
        self.threshold_disperssion = threshold_disperssion
    def idt(data, dis_threshold, dur_threshold):

	    window_range = [0,0]

	    current = 0 #pointer to represent the current beginning point of the window
	    last = 0
	#final lists for fixation info
	    centroidsX = []
	    centroidsY = []
	    time0 = []
	    time1 = []
    
	    while (current < len(data)):
        
		    t0 = float(data[current][timestamp]) #beginning time
		    t1 = t0 + float(dur_threshold)     #time after a min. fix. threshold has been observed

		    for r in range(current, len(data)): 
			    if(float(data[r][timestamp])>= t0 and float(data[r][timestamp])<= t1):
				#print "if",r
				    last = r #this will find the last index still in the duration threshold

		    window_range = [current,last]

		#now check the dispersion in this window
		#print "window", current, last
		    dispersion = get_dispersion(data[current:last+1])
		#a[2:5] gives 2,3,4. To include last one, [2:6]
        
		    if (dispersion <= dis_threshold):

			#add new points
			    while(dispersion <= dis_threshold and last + 1 < len(data)):

				    last += 1
				    window_range = [current,last]
				#print current, last, "*"
				#print "*"
				    dispersion = get_dispersion(data[current:last+1])
       
			#dispersion threshold is exceeded
			#fixation at the centroid [current,last]

			   
            
			  
                
			    t0 = float(data[current][timestamp])
			    t1 = float(data[last][timestamp])
            
			    centroidsX.append(cX)
			    centroidsY.append(cY)
			    time0.append(t0)
			    time1.append(t1)
            
			    current = last + 1 #this will move the pointer to a novel window

		    else:
			    current += 1 #this will remove the first point
			    last = current #this is not necessary
            
	    return  time0, time1

    def get_dispersion(points):

	    dispersion = 0
    
	    argxmin = np.min(points[:,x].astype(np.float))
	    argxmax = np.max(points[:,x].astype(np.float))
    
	    argymin = np.min(points[:,y].astype(np.float))
	    argymax = np.max(points[:,y].astype(np.float))

	    dispersion = ((argxmax - argxmin) + (argymax - argymin))/2
	#TODO: look for other ways of calculating dispersion
    
	    return dispersion


