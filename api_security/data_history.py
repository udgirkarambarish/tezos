from flask import Flask, request, jsonify
from pytezos import pytezos

app = Flask(__name__)

# Tezos node configuration
tezos = pytezos.using(shell='https://rpc.tzkt.io/mainnet')

@app.route('/upload', methods=['POST'])
def upload_data():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Read the file content
    data = file.read()

    try:
        # Upload data to Tezos blockchain
        contract = tezos.contract('unit').with_source("parameter unit; storage bytes; code { CAR; NIL operation; PAIR }")
        operation = contract.call().with_amount(0).with_storage(data).autofill().inject()
        operation.confirmation()
        return jsonify({'message': 'Data uploaded to Tezos blockchain successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
