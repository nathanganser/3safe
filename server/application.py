from flask import Flask,request, jsonify
from flask_cors import CORS
import json
import uuid
from functions import verify_code, mint_nft, generate_code, send_email

app = Flask(__name__)
CORS(app)

@app.route("/go", methods=['POST'])
def hello_world():
    print(request.form)
    crypto_address = request.form.get('address')
    email = request.form.get('email')
    code = generate_code(email)
    send_email(email, code, crypto_address)



    return jsonify(success=True, message="Verification email has been sent out!")

@app.route('/verify/<code>/<email>/<address>', methods=['GET'])
def ver(code, email, address):
    verified = verify_code(email, code)
    if verified:
        mint_nft(address, email)
        return jsonify(success=True, message="NFT minted!!")
    else:
        return jsonify(success=False)



app.run(debug=True)