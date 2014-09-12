import numpy as np
import cv2
import match_cards

cap = cv2.VideoCapture(0)
cap.open()

while(True):
    if cv2.waitKey(1) & 0xFF == ord('c'):
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Our operations on the frame come here
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        match_cards.find_cluster(gray)

        # Display the resulting frame
        #cv2.imshow('frame',gray)

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
