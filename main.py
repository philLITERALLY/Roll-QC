import cv2
import numpy as np

cap = cv2.VideoCapture(0)
cap.set(3,1920)
cap.set(4,1080)
cap.set(5,30)

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'DIVX')
out = cv2.VideoWriter('output.avi',cv2.VideoWriter_fourcc('D','I','V','X'), 10.0, (1920,200))
out2 = cv2.VideoWriter('output2.avi',cv2.VideoWriter_fourcc('D','I','V','X'), 10.0, (1920,200), False)

while(1):

    # Take each frame
    _, frame = cap.read()
 
    cropped = frame[450:650, 0:1920]
    gray = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
    retval, threshold = cv2.threshold(gray, 200, 255, 0)
    drawImg = cropped

     # run opencv find contours, only external boxes
    image, contours, hierarchy = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = [cnt for cnt in contours if cv2.contourArea(cnt) > 2000]

    #for each contour draw a bounding box and order number
    for cnt in contours:
        x,y,w,h = cv2.boundingRect(cnt)
        cv2.rectangle(drawImg, (x,y), (x+w,y+h), (0,255,0),2)  
    #         x,y,w,h = cv2.boundingRect(cnt)
    #         print(cv2.boundingRect(cnt))
    #         cv2.rectangle(drawImg, (x,y), (x+w,y+h), (0,255,0),2)

    # cv2.imshow('frame',frame)
    # cv2.imshow('gray',gray)
    # cv2.imshow('threshold',threshold)
    cv2.imshow('threshold',threshold)
    cv2.imshow('drawImg',drawImg)
    # cv2.imshow('blur',blur)

    # # write the flipped frame
    out.write(drawImg)
    out2.write(threshold)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        # cv2.imwrite( "cropped.jpg", threshold )
        # cv2.imwrite( "blob.jpg", drawImg )
        break

# Release everything if job is finished
cap.release()
out.release()
out2.release()
cv2.destroyAllWindows()