from flask import Flask,request, jsonify, redirect
from flask_cors import CORS
import json
import uuid
from functions import verify_code, mint_nft, generate_code, send_email

app = Flask(__name__)
CORS(app)

@app.route("/")
def hey():
    return redirect("https://github.com/nathanganser/3safe")

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
        resp = mint_nft(address, email)
        return jsonify(resp)
    else:
        return jsonify(success=False)


if __name__ == "__main__":
    app.run(debug=True)