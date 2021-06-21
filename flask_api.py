from flask import Flask, jsonify, abort, request
import json
import pandas as pd
import yahoo_fin.stock_info as yahoo
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

#Top Reddit Tickers API
@app.route("/api/redditstocks", methods=['GET'])
@cross_origin()
def redditstocks():
    df = pd.read_csv('topstocks.csv')
    return df.to_json(orient='index')

#Stock Analysis API
@app.route("/api/stocks", methods=['GET'])
@cross_origin()
def stocks():
    symbol = request.args.get('symbol')

    if symbol:
        quote = yahoo.get_quote_table(symbol)
        for i in quote:
            if str(quote[i]) == 'nan':
                quote[i] = 'N/A'
    else:
        quote = json.dumps({'1y Target Est': 'Please enter a valid ticker.'})

    return quote

@app.route("/api/fullsheet", methods=['GET'])
@cross_origin()
def full_sheet():
    # DEBUG: Import Sample Data for test
    df_full = pd.read_csv('full_sheet.csv')

    # String containing the name of crypto to index. i.e. ?crypto=BTC
    crypto = request.args.get('crypto')

    if not crypto or crypto == 'all':
        df_sample = df_full
    else:
        df_sample = df_full.loc[df_full['index'] == crypto]

    return(df_sample.to_json(orient='index'))

if __name__ == '__main__':
    app.run()
