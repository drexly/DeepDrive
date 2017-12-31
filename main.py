import numpy as np
import cv2
import os
import sys
import io
import subprocess
import datetime
import shutil
import math

cmdarr=['./segnet-console','before.png','segdet.png','cluster.png','--prototxt=networks/FCN-Alexnet-Cityscapes-HD/deploy.prototxt','--model=networks/FCN-Alexnet-Cityscapes-HD/snapshot_iter_367568.caffemodel','--labels=networks/FCN-Alexnet-Cityscapes-HD/cityscapes-labels.txt','--colors=networks/FCN-Alexnet-Cityscapes-HD/cityscapes-deploy-colors.txt','--input_blob=data']

befcmdarr=['./segnet-console','beftime.png','befsegdet.png','befcluster.png','--prototxt=networks/FCN-Alexnet-Cityscapes-HD/deploy.prototxt','--model=networks/FCN-Alexnet-Cityscapes-HD/snapshot_iter_367568.caffemodel','--labels=networks/FCN-Alexnet-Cityscapes-HD/cityscapes-labels.txt','--colors=networks/FCN-Alexnet-Cityscapes-HD/cityscapes-deploy-colors.txt','--input_blob=data']

curcmdarr=['./segnet-console','curtime.png','cursegdet.png','curcluster.png','--prototxt=networks/FCN-Alexnet-Cityscapes-HD/deploy.prototxt','--model=networks/FCN-Alexnet-Cityscapes-HD/snapshot_iter_367568.caffemodel','--labels=networks/FCN-Alexnet-Cityscapes-HD/cityscapes-labels.txt','--colors=networks/FCN-Alexnet-Cityscapes-HD/cityscapes-deploy-colors.txt','--input_blob=data']

upper_red = np.array([142,0,0])
lower_red = np.array([142,0,0])

def judger(cls):
    mask = cv2.inRange(cls, lower_red, upper_red)
    ret, thresh = cv2.threshold(mask, 127, 255, 0);
    cls=cv2.imread('before.png')
    if(len(np.where(thresh!=0)[0])>0):
       _,contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
       c = max(contours, key = cv2.contourArea)
       M = cv2.moments(c)
       cX = int(M["m10"] / M["m00"])
       cY = int(M["m01"] / M["m00"])
       cv2.circle(cls, (cX, cY), 7, (0, 255, 0), -1)

    rst='./gtmg/'+str(datetime.datetime.now()).replace(':','-')+'.png'
    rstt='./gtmg/s'+str(datetime.datetime.now()).replace(':','-')+'.png'
    cv2.imwrite(rstt,cls)
    #shutil.move("before.png", rstt)
    #cv2.imwrite(rst,mask)

def judged(cls,fh,fw,fps):
    mask = cv2.inRange(cls, lower_red, upper_red)
    ret, thresh = cv2.threshold(mask, 127, 255, 0);
    if(len(np.where(thresh!=0)[0])>0):
       _,contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
       c = max(contours, key = cv2.contourArea)
       M = cv2.moments(c)
       cX = int(M["m10"] / M["m00"])
       cY = int(M["m01"] / M["m00"])
       distm = math.hypot((fw/2)-cX, fh-cY)*0.5335/100
       if distm<3:
	print("xxx x x x x x x x x x xxx disable "+str(distm))
	#os.system("mpg123 ./disable.mp3")
       else:
	print("ooo o o o o o o o o o ooo enable"+str(distm))
	#os.system("mpg123 ./enable.mp3")


def vget(befcls,curcls,fps,fh,fw):
    befmask = cv2.inRange(befcls, lower_red, upper_red)
    curmask = cv2.inRange(curcls, lower_red, upper_red)
    befret, befthresh = cv2.threshold(befmask, 127, 255, 0)
    curret, curthresh = cv2.threshold(curmask, 127, 255, 0)
    if(len(np.where(befthresh!=0)[0])>0 and len(np.where(curthresh!=0)[0])>0 ):
       _,befcontours, _ = cv2.findContours(befthresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
       befc = max(befcontours, key = cv2.contourArea)
       befM = cv2.moments(befc)
       befcX = int(befM["m10"] / befM["m00"])
       befcY = int(befM["m01"] / befM["m00"])

       _,curcontours, _ = cv2.findContours(curthresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
       curc = max(curcontours, key = cv2.contourArea)
       curM = cv2.moments(curc)
       curcX = int(curM["m10"] / curM["m00"])
       curcY = int(curM["m01"] / curM["m00"])

       kmh = math.hypot(curcX-befcX, curcY-befcY)*0.5335*fps*3600/100000
       distm = math.hypot((fw/2)-curcX, fh-curcY)*0.5335/100
       radians = math.atan2(curcY-fh, curcX-(fw/2))
       degrees = math.degrees(radians)
       if degrees<0:
	  degrees+=180

       infostr=str(round(degrees,3))+"deg, "+str(round(distm,3))+"m, "+str(round(kmh,3))+"km/h" 
	
       cls=cv2.imread('curtime.png')
       cv2.circle(cls, (curcX, curcY), 7, (0, 255, 0), -1)
       cv2.circle(cls, (int(fw/2), int(fh)), 7, (0, 0, 255), -1)
       cv2.putText(cls, infostr, (curcX + 20, curcY + 20),
			cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)

       rstt='./tmg/s'+str(datetime.datetime.now()).replace(':','-')+'.png'
       cv2.imwrite(rstt,cls)
    


def judgee(cls):    
    mask = cv2.inRange(cls, lower_red, upper_red)
    y,x=mask.shape	
    roi1=mask[0:y/3,0:x/2]
    roi2=mask[y/3*2:y,x/2:x]
    ret, thresh = cv2.threshold(roi1, 127, 255, 0)
    ret2, thresh2 = cv2.threshold(roi2, 127, 255, 0)
    #cv2.imshow('sed',thresh)
    #cv2.imshow('sed2',thresh2)
    #print(len(np.where(thresh!=0)[0]))
    #print(len(np.where(thresh2!=0)[0]))
'''
    if(len(np.where(thresh!=0)[0])>0):
	_,contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
	c = max(contours, key = cv2.contourArea)
	cx,cy,w,h = cv2.boundingRect(c)
	print(w*h)

	if w*h>256000:
		os.system("mpg123 ./disable.mp3")
    		cv2.imshow('sed',thresh)
	else:
		os.system("mpg123 ./able.mp3")
		cv2.imshow('sed',thresh)
    else:
	os.system("mpg123 ./able.mp3")
	cv2.imshow('sed',thresh)
'''	
def chkk():
	os.system("mpg123 ./able.mp3")
	process = subprocess.Popen(cmdarr)
	while process.poll() is None:
	  flag=process.poll()
	  if(flag is not None):
		break
	cls=cv2.imread('cluster.png')
	seg=cv2.imread('segdet.png')
	#judge(cls)
	cv2.imshow('segmented',seg)
	cv2.imshow('clustered',cls)

def chk():
	os.system("mpg123 ./able.mp3")
	process = subprocess.Popen(cmdarr)
	cls=cv2.imread('cluster.png')
	seg=cv2.imread('segdet.png')
	#judge(cls)
	cv2.imshow('segmented',seg)
	cv2.imshow('clustered',cls)

def chk2():
	os.system("mpg123 ./disable.mp3")
	process = subprocess.Popen(cmdarr)
	cls=cv2.imread('cluster.png')
	seg=cv2.imread('segdet.png')
	#judge(cls)
	cv2.imshow('segmented',seg)
	cv2.imshow('clustered',cls)

def chkk2():
	os.system("mpg123 ./disable.mp3")
	process = subprocess.Popen(cmdarr)
	while process.poll() is None:
	  flag=process.poll()
	  if(flag is not None):
		break
	cls=cv2.imread('cluster.png')
	seg=cv2.imread('segdet.png')
	#judge(cls)
	cv2.imshow('segmented',seg)
	cv2.imshow('clustered',cls)

def chk3(fps,fh,fw):
	process = subprocess.Popen(cmdarr)
	while process.poll() is None:
	  flag=process.poll()
	  if(flag is not None):
		break
        
	cls=cv2.imread('cluster.png')
	judged(cls,fh,fw,fps)	
	seg=cv2.imread('segdet.png')
	
	#cv2.imshow('segmented',seg)
	#cv2.imshow('clustered',cls)

def chk4(fps,fh,fw):
        process = subprocess.Popen(cmdarr)
	while process.poll() is None:
	  flag=process.poll()
	  if(flag is not None):
		break
        
	cls=cv2.imread('cluster.png')
	judger(cls)	
	seg=cv2.imread('segdet.png')

def velocity(fps,fh,fw):
    process = subprocess.Popen(befcmdarr)
    while process.poll() is None:
      flag=process.poll()
      if(flag is not None):
	     break
    process = subprocess.Popen(curcmdarr)
    while process.poll() is None:
      flag=process.poll()
      if(flag is not None):
	      break
    befcls=cv2.imread('befcluster.png')
    curcls=cv2.imread('curcluster.png')
    
    vget(befcls,curcls,fps,fh,fw)

def velocit(fps,fh,fw):
    process = subprocess.Popen(befcmdarr)
    aprocess = subprocess.Popen(curcmdarr)
    while (process.poll() is None) and (aprocess.poll() is None):
      flag=process.poll()
      aflag=aprocess.poll()
      if (flag is not None) and (aflag is not None):
	     break
    
    befcls=cv2.imread('befcluster.png')
    curcls=cv2.imread('curcluster.png')
    
    vget(befcls,curcls,fps,fh,fw)

def velocitty(fps,fh,fw):
    process = subprocess.Popen(befcmdarr)
    aprocess = subprocess.Popen(curcmdarr)
 
    befcls=cv2.imread('befcluster.png')
    curcls=cv2.imread('curcluster.png')
    
    vget(befcls,curcls,fps,fh,fw)
	
	
cap = cv2.VideoCapture(sys.argv[1])
fps=cap.get(cv2.CAP_PROP_FPS)
fh=cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
fw=cap.get(cv2.CAP_PROP_FRAME_WIDTH)

while(cap.isOpened()):
    ret, frame = cap.read()
    #if cv2.waitKey(1) & 0xFF == 32:
    if cv2.waitKey(1) & 0xFF == ord('g'):
  	cv2.imwrite("before.png", frame)	
	chk()
    if cv2.waitKey(1) & 0xFF == ord('b'):
  	cv2.imwrite("before.png", frame)	
	chk2()
    if cv2.waitKey(1) & 0xFF == ord('j'):
        cv2.imwrite("before.png", frame)
        chk3(fps,fh,fw)
    if cv2.waitKey(1) & 0xFF == ord('f'):
        cv2.imwrite("before.png", frame)
        chk4(fps,fh,fw)
    if cv2.waitKey(1) & 0xFF == ord('o'):
  	cur_frame = cap.get(1)
        #cv2.imwrite(str(cur_frame)+".png",frame)
	cv2.imwrite('curtime.png',frame)
        cap.set(1,cur_frame-2)
	beret, beframe = cap.read()
  	bef_frame = cap.get(1)
	cv2.imwrite('beftime.png',beframe)
        #cv2.imwrite(str(bef_frame)+".png",beframe)
        velocity(fps,fh,fw)
    if cv2.waitKey(1) & 0xFF == ord('q'):
	break
    if(ret):	
    	cv2.imshow('frame',frame)
    else:
	cv2.destroyWindow('frame')

while(cap.isOpened()):
    ret, frame = cap.read()
    if cv2.waitKey(1):
        if 0xFF == ord('o'):
	        cv2.imshow('clustered',cls)
		  	cur_frame = cap.get(1)
			#cv2.imwrite(str(cur_frame)+".png",frame)
			cv2.imwrite('curtime.png',frame)
			cap.set(1,cur_frame-2)
			beret, beframe = cap.read()
		  	bef_frame = cap.get(1)
			cv2.imwrite('beftime.png',beframe)
			#cv2.imwrite(str(bef_frame)+".png",beframe)
	        velocity(fps,fh,fw)
    	if 0xFF == ord('q'):
			break
    if(ret):	
    	cv2.imshow('frame',frame)
    else:
		cv2.destroyWindow('frame')





