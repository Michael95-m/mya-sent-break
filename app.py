from flask import Flask, request, jsonify
from utils import sent_break_syl
from normalize.normalize_data import Normalization

app = Flask(__name__)

norm_obj = Normalization()
sent_break_obj = sent_break_syl('data_syl')

@app.route("/segment",methods = ['POST'])
def segment():

    sent = request.form['text']

    segment_text = sent_break_obj.break_sent(norm_obj.normalize_data(sent), False)

    return jsonify({'segment_text': segment_text})

if __name__ == '__main__':

    app.run(host='0.0.0.0', port=5000, debug=False)
