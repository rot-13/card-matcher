from flask import Flask, request, jsonify
import cv2
import match_cards
import time
import os.path

app = Flask(__name__)

@app.route('/ping')
def ping():
    return "pong!"

@app.route('/match-card')
def matchCard():
    fileName = request.args['file_name']
    img = cv2.imread(fileName, 0) # 0 == greyscale

    start = time.clock()
    card_file_name = match_cards.find_card_in_clusters(img, resize_factor=1)[0]
    print time.clock() - start

    card_id = os.path.basename(card_file_name).split('.')[0]
    card_text = match_cards.card_title(card_file_name)
    return jsonify(card_name = card_text,
                   card_file_name= card_file_name,
                   card_url="http://netrunnerdb.com/en/card/" + card_id)

if __name__ == "__main__":
    # debug=True makes it reload the .py files on change automatically
    app.run(port=31337, debug=True)
