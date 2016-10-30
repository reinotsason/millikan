import numpy as np
import cv2
import time

#using file name cap=cv2.VideoCapture('webcam_test-001.avi')
#using webcam have to let device index replace file name
cap=cv2.VideoCapture(2)


number = 0
center = None  #initialize the countour center
start = time.clock() #record the start time
intensity_lowerbound = 105 #set internsity lower bound
intensity_upperbound = 255 #set internsity upper bound
region_leftbound  = 490 #set left bound for the selected region
region_rightbound = 850 #set right bound for the selected region
region_upperbound = 350 #set upper bound for the selected region
region_lowerbound = 670 #set lower bound for the selected region


while(cap.isOpened()):  # check !
    # capture frame-by-frame
    ret, frame = cap.read()


    if ret: # check ! (some webcam's need a "warmup")

        # our operation on frame come here
        # make the frame into gray scale(intensity)
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

                # record the time finding the first contour
                t = time.clock()-start

                
                t_interval = 0
                number = number + 1

            # when it's not the first time find the contour of oil drop
            if number > 0:
            
                if center!=None:

                 

                    # calculate the distance between two center of contours
                    dist = cv2.norm(center,centerprevious, cv2.NORM_L2)

                    # store the center of contour at current time
                    centerptrevoius = center

                    # record the current time
                    t1 = time.clock()-start

                    # calculate the time between two positon of centers
                    t_interval = t1-t

                    # store the current time
                    t = t1
                    
                    # calculate the velocity of moving center
                    v = dist/t_interval/1000
                    
                    # print the vilacity on the selected region at particular postion
                    cv2.putText(draw1,"%.2fm/s" %v,(draw1.shape[1]-200,draw1.shape[0]-20),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),1)

                    number = number + 1
                    

        cv2.imshow('mask1',frame)
        # show the selected region on the gray scaled frame
        cv2.imshow('mask',maskpart)
        
        cv2.imshow('res', draw1)

    if cv2.waitKey(30) & 0xFF == ord('q'):
        break
# When everything is done release the capture
cap.release()
cv2.destroyAllWindows()
