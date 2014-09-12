import numpy as np
import cv2
import match_cards
import webbrowser
import os
import time

cap = cv2.VideoCapture(0)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    if cv2.waitKey(1) & 0xFF == ord('c'):

        # Our operations on the frame come here
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        start = time.clock()
        card_file_name = match_cards.find_cluster(img, 0.8)[0]
        print time.clock() - start

        card_id = os.path.basename(card_file_name).split('.')[0]
        webbrowser.open("http://netrunnerdb.com/en/card/" + card_id)

    # Display the resulting frame
    cv2.imshow('frame',frame)

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
