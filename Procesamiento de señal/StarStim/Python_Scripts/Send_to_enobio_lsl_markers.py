####		Send to Enobio LSL markers 		####

# An empty vector is created to hold the marker.
# After a random delay that can last up to 3 seconds the marker is sent to enobio.

from pylsl import StreamInfo, StreamOutlet
import time
import random

print ("Creating a new marker stream info...\n")
info = StreamInfo('MyMarkerStream3','Markers',1,0,'int32','myuniquesourceid23443')

print("Opening an outlet...\n")
outlet =StreamOutlet(info)

print("Sending data...\n")

while (True):
	vec = []
	time.sleep(random.randint(0,3))
	mkr = 111
	vec.append(mkr)
	outlet.push_sample(vec) 
	print("Now sending: \t" + str(vec)+"\n")






