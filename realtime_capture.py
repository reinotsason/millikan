# -*- coding: cp936 -*-
import numpy as np
import cv2
import time

velocity = None
number = 0
missnum = 0 # the number of time missing find oil drop
maxmiss = 4 # the maximum number allowed to miss the oid drop
center = None  #initialize the countour center
abspre = [0,0]
abscur = [0,0]
start = time.clock() #record the start time
lockreg = 30 #the region to lock oil drop
intensity_lowerbound = 132 #set internsity lower bound
intensity_upperbound = 255 #set internsity upper bound
region_leftbound  = 0 #set left bound for the selected region
region_rightbound = 0 #set right bound for the selected region
region_upperbound = 0 #set upper bound for the selected region
region_lowerbound = 0 #set lower bound for the selected region

lx,ly = -1,-1
clicknum = 0
rx,ry = -1,-1

average_frame = 5

def select_region(event,x,y,flags,param):
    global lx,ly,clicknum,rx,ry

    if event == cv2.EVENT_LBUTTONDOWN:
        clicknum = clicknum+1
        if clicknum == 1:
            lx,ly = x,y

    elif event == cv2.EVENT_MOUSEMOVE:
        if clicknum == 1:
            rx = x
            ry = y




#using file name cap=cv2.VideoCapture('webcam_test-001.avi')
#using webcam have to let device index replace file name cap=cv2.VideoCapture(2)
cap=cv2.VideoCapture(2)
cv2.namedWindow('image')
cv2.setMouseCallback('image',select_region)




while(cap.isOpened()):  # check !
    # capture frame-by-frame
    ret, frame = cap.read()


    if ret: # check ! (some webcam's need a "warmup")

        if number == 0:

            # our operation on frame come here
            # make the frame into gray scale(intensity)
            if clicknum == 2:
                region_leftbound  = lx #set left bound for the selected region
                region_rightbound = rx #set right bound for the selected region
                region_upperbound = ly #set upper bound for the selected region
                region_lowerbound = ry #set lower bound for the selected region
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        

                # create a mask and set object intensity in the range to be white(select oil drop)
                # object intensity out of range will be black
                ret,mask=cv2.threshold(gray,intensity_lowerbound,intensity_upperbound,cv2.THRESH_BINARY)

                # make a copy for the entire gray scale frame
                mask1=mask.copy()

                # select the region we want to conduct oil drop tracking on the original frame
                draw1 = frame[region_upperbound:region_lowerbound, region_leftbound:region_rightbound]

                # select the corresponding region on the copy of gray scaled grame
                maskpart = mask1[region_upperbound:region_lowerbound, region_leftbound:region_rightbound]

                # select the corresponding region on the gray scaled grame
                maskpart1 = mask[region_upperbound:region_lowerbound, region_leftbound:region_rightbound]

                #find contours on the copy of gray scaled frame
                cnts = cv2.findContours(maskpart.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE
                                )[-2]

                if len(cnts)==0:
                    missnum = missnum + 1
                if missnum == maxmiss:
                    number = 0
                    clicknum = 0
                    missnum = 0
                    cv2.destroyWindow('mask')
                    cv2.destroyWindow('res')
                    cv2.putText(frame,'Reselect region', (500,400),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),1)
                #check at least one oil drop is tracked
                if len(cnts)>0: 

                    # select the oil drop with the largest contour
                    c = max(cnts,key=cv2.contourArea)

                    # determine the center and radius of circle enclosed the oil drop I selected
                    ((x,y),radius)=cv2.minEnclosingCircle(c)

            
           
                    center = (int(x),int(y))
              
                    cv2.circle(draw1,(int(x),int(y)),int(radius),(0,255,0),1)

                    # when first time find the contour of oil drop
                    if number == 0:

                        # record this center of the first contour 
                        centerprevious = center
                        pretrackcenter = center

                        abspre[0] = region_leftbound + centerprevious[0]
                        abspre[1] = region_upperbound + centerprevious[1]

                        # record the time finding the first contour
                        t = time.clock()-start

                
                        t_interval = 0
                        number = number + 1

                 
        if number > 0:

            # our operation on frame come here
            # make the frame into gray scale(intensity)
            if clicknum >= 2:

                templeft = region_leftbound
                tempupper = region_upperbound
                
                region_leftbound  = templeft + pretrackcenter[0]-lockreg #set left bound for the selected region
                region_rightbound = templeft + pretrackcenter[0]+lockreg #set right bound for the selected region
                region_upperbound = tempupper + pretrackcenter[1]-lockreg #set upper bound for the selected region
                region_lowerbound = tempupper + pretrackcenter[1]+lockreg #set lower bound for the selected region

                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        

                # create a mask and set object intensity in the range to be white(select oil drop)
                # object intensity out of range will be black
                ret,mask=cv2.threshold(gray,intensity_lowerbound,intensity_upperbound,cv2.THRESH_BINARY)

                # make a copy for the entire gray scale frame
                mask1=mask.copy()

                # select the region we want to conduct oil drop tracking on the original frame
                draw1 = frame[region_upperbound:region_lowerbound, region_leftbound:region_rightbound]

                # select the corresponding region on the copy of gray scaled grame
                maskpart = mask1[region_upperbound:region_lowerbound, region_leftbound:region_rightbound]

                # select the corresponding region on the gray scaled grame
                maskpart1 = mask[region_upperbound:region_lowerbound, region_leftbound:region_rightbound]

                #find contours on the copy of gray scaled frame
                cnts = cv2.findContours(maskpart.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE
                                )[-2]

                #check at least one oil drop is tracked
                if len(cnts)==0:
                    missnum = missnum + 1
                if missnum == maxmiss:
                    number = 0
                    clicknum = 0
                    missnum = 0
                    cv2.destroyWindow('mask')
                    cv2.destroyWindow('res')
                    cv2.putText(frame,'Reselect region', (500,400),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),1)
                if len(cnts)>0: 

                    # select the oil drop with the largest contour
                    c = max(cnts,key=cv2.contourArea)

                    # determine the center and radius of circle enclosed the oil drop I selected
                    ((x,y),radius)=cv2.minEnclosingCircle(c)

                    if radius > 10:
                        missnum = maxmiss
                    center = (int(x),int(y))
              
                    cv2.circle(draw1,(int(x),int(y)),int(radius),(0,255,0),1)

                    # when first time find the contour of oil drop


                    # when it's not the first time find the contour of oil drop
                    if number > 0:
            
                        if center!=None:

                            pretrackcenter = center
                            if number%average_frame == 0:
                                
                                a = abspre[0]
                                b = abspre[1]
                                abscur[0] = region_leftbound + center[0]
                                abscur[1] = region_upperbound + center[1]
                             
                                
                                # calculate the distance between two center of contours
                               # dist = cv2.norm(abscur,abspre, cv2.NORM_L2)
                                dist = ((abscur[0]-a)**2+(abscur[1]-b)**2)**0.5
                                # store the center of contour at current time
                                abspre = abscur

                                # record the current time
                                t1 = time.clock()-start

                                # calculate the time between two positon of centers
                                t_interval = t1-t

                                # store the current time
                                t = t1
                    
                                # calculate the velocity of moving center
                                velocity = dist/t_interval
        
                            number = number + 1

                    

        if clicknum == 1 & rx!= -1 & ry!= -1:
            frame1 = frame.copy()
            cv2.rectangle(frame1,(lx,ly),(rx,ry),(0,255,0),1)
            
            cv2.imshow('image',frame1)

        if clicknum == 0:
            
            # show the selected region on the gray scaled frame
            cv2.imshow('image',frame)
            
        if clicknum >= 2:

            if velocity != None:
                cv2.putText(frame,"%.2fm/s" %velocity,(600,500),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),1)
            cv2.imshow('image',frame)
            
            cv2.imshow('mask',maskpart)
            
            cv2.imshow('res', draw1)

    if cv2.waitKey(30) & 0xFF == ord('q'):
        break
# When everything is done release the capture
cap.release()
cv2.destroyAllWindows()
