import cv2
import numpy
from optparse import OptionParser
import sys
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

#usage example videoProcess.py -v SampleVideo_1280x720_1mb.mp4 -r 100 -o f.jpg
def calculateAverage(frame):
	average_color_per_row = numpy.average(frame, axis=0) #Taking the average value of each row of the image
	average_color = numpy.average(average_color_per_row, axis=0) #Taking the average of those average values
	average_color = numpy.uint8(average_color) #Translating that average into a set of blue, green, and red values that OpenCV understands.
	return average_color

	
parser = OptionParser()
parser.add_option("-v", "--video", dest="videoPath",help="video paths to process, splited by ','")
parser.add_option("-r", "--rows", dest="windowsize_r",default=1,help="divide each frame to rows")
parser.add_option("-l", "--height", dest="outImageHeight",default=300,help="barcode height")
parser.add_option("-b", "--bWidth", dest="outImageWidth",default=1000,help="barcode width")
parser.add_option("-w", "--width", dest="frameResWidth",default=5,help="each frame in barcode result width")
parser.add_option("-o", "--output", dest="outputFile",default="frame.jpg",help="output file")

(options, args) = parser.parse_args()

videoPaths = options.videoPath
windowsize_r = int(options.windowsize_r)
outImageHeight = int(options.outImageHeight)
frameResWidth = int(options.frameResWidth)
outImageWidth = int(options.outImageWidth)
outputFile = options.outputFile

if videoPaths == None:
  print("No video path !")
  sys.exit(0)
		
resultsDictionary = {}
		
videoPathsList = videoPaths.split(',')
for videoPath in videoPathsList: 		
	print(videoPath)
	cap = cv2.VideoCapture(videoPath)
	count = 0
	result = None
	success = True
	while success:
		success,frame = cap.read()
		count += 1
		if success:
			rowResult = None
			counter = 0
			while counter!=windowsize_r:
				window = frame[int(counter*frame.shape[0]/windowsize_r):int((counter+1)*frame.shape[0]/windowsize_r),0:]
			#cv2.imwrite("frame-"+str(counter)+".jpg", window)
				counter +=1
				avg_color = calculateAverage(window)
				average_color_img = numpy.array([[avg_color]*frameResWidth]*(int(outImageHeight/windowsize_r)), numpy.uint8)
				if rowResult == None:
					rowResult = average_color_img
				else:
					rowResult = numpy.concatenate((rowResult,average_color_img), axis=0)#numpy.hstack((rowResult,average_color_img))	
			#cv2.imwrite("frame-"+str(counter)+"avg.jpg", rowResult)
		#success = False
		#avg_color = calculateAverage(frame)
		#average_color_img = numpy.array([[avg_color]*5]*100, numpy.uint8)
			if result == None:
				result = rowResult
			else:
				result = numpy.hstack((result,rowResult))
	result = cv2.resize(result, (outImageWidth, outImageHeight))
	resultsDictionary[videoPath] = result
	cap.release()

plt.axis('off')
fig = plt.figure()
plt.axis('off')
counter = 1
for video,res in resultsDictionary.items():
	a=fig.add_subplot(len(videoPathsList),1,counter)
	imgplot = plt.imshow(res)
	a.set_title(video)
	a.axis('off')
	counter +=1
	#cv2.imwrite(video+".jpg", res)
	
plt.savefig(outputFile)
cv2.waitKey(10)