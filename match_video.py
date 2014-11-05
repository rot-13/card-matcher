import cv2
import match_cards
import time

cap = cv2.VideoCapture(0)

card_text = ""
while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    if cv2.waitKey(1) & 0xFF == ord('c'):

        # Our operations on the frame come here
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        start = time.clock()
        card_file_name = match_cards.find_card_in_clusters(img, resize_factor=1)[0]
        print time.clock() - start

        #webbrowser.open("http://netrunnerdb.com/en/card/" + card_id)
        card_text = match_cards.card_title(card_file_name)
        print card_text


    # write the title
    cv2.putText(frame, card_text, (100,100), cv2.FONT_HERSHEY_SIMPLEX, 3, (255,0,0))

    # Display the resulting frame
    cv2.imshow('frame',frame)

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
