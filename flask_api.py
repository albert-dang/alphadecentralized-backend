from flask import Flask, jsonify, abort, request
import json
import pandas as pd
import yahoo_fin.stock_info as yahoo
from flask_cors import CORS, cross_origin

app = Flask(__name__)
#Set up cross-origin resource sharing (CORS) for interfacing with other servers
cors = CORS(app)
#Configure the CORS header for plain text
app.config['CORS_HEADERS'] = 'Content-Type'

#Top Reddit Tickers API
#Address for this endpoint is example.com/api/redditstocks
@app.route("/api/redditstocks", methods=['GET'])
#Enable CORS
@cross_origin()
def redditstocks():
    #Read the CSV into a Pandas DataFrame
    df = pd.read_csv('topstocks.csv')
    #Return the DataFrame as JSON (this prints the JSON in plain text at the API endpoint above)
    return df.to_json(orient='index')

#Stock Analysis API
@app.route("/api/stocks", methods=['GET'])
#Enable CORS
@cross_origin()
def stocks():
    #Get an argument from the incoming request
    symbol = request.args.get('symbol')

    #If there was an argument
    if symbol:
        #Query Yahoo Finance for a quote on the symbol
        quote = yahoo.get_quote_table(symbol)
        #For each field in the quote
        for i in quote:
            #If the field is a null value (which will fail to parse to JSON)
            if str(quote[i]) == 'nan':
                #Fix the null value
                quote[i] = 'N/A'
    #Else, there were no arguments
    else:
        #Return the appropriate error as a JSON in the first expected field
        quote = json.dumps({'1y Target Est': 'Please enter a valid ticker.'})

    #Return the JSON (this prints the JSON in plain text at the API endpoint above)
    return quote

if __name__ == '__main__':
    app.run()
