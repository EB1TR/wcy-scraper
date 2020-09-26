""" DK0WCY to JSON """
#
# DK0WCY to JSON
# Is an API to parse DK0WCY data (scraping) to JSON.
#
# Thanks to the DK0WCY Team (http://www.dk0wcy.de/) for information.
#

__author__ = 'EB1TR'


import requests
from bs4 import BeautifulSoup
from datetime import datetime
from flask import Flask, jsonify


app = Flask(__name__)


@app.route('/', methods=['GET'])
def api_wcy():

    # Create dictionaries ----------------------------------------------------------------------------------------------
    json_wcy = {}
    wcy_index = {}
    wcy_gmf = {}
    wcy_forecast = {}
    #

    try:
        # Index data to dictionary -------------------------------------------------------------------------------------
        url = 'http://www.dk0wcy.d/magnetogram'                         # URL of the HTML data
        html = requests.get(url)                                        # Generate request
        parsed_html = BeautifulSoup(html.content, 'html.parser')        # Parse HTML data
        data = parsed_html.find_all('b')                                # Extract <b> tags (data tags, in this case)
        #
        # Data frame
        # [<b>20</b>, <b>5</b>, <b>quiet</b>, <b>43</b>, <b>3.73</b>, <b>active</b>, <b>11</b>, <b>no</b>, <b>73</b>]
        #

        # Index data to dictionary -------------------------------------------------------------------------------------
        wcy_index['a-boulder'] = int(data[0].get_text())
        wcy_index['a-kiel'] = int(data[3].get_text())
        wcy_index['ssn'] = int(data[6].get_text())
        wcy_index['sfi'] = int(data[8].get_text())
        #

        # GMF data to dictionary ---------------------------------------------------------------------------------------
        wcy_gmf['k-3h'] = int(data[1].get_text())
        wcy_gmf['k-current'] = float(data[4].get_text())
        wcy_gmf['aurora'] = data[7].get_text()
        #

        # Forecast data to dictionary ----------------------------------------------------------------------------------
        wcy_forecast['sa'] = data[2].get_text()
        wcy_forecast['gmf'] = data[5].get_text()
        #

        # Add time stamp to JSON ---------------------------------------------------------------------------------------
        json_wcy['ts'] = datetime.utcnow().isoformat()
        #

        # Add individual data to JSON ----------------------------------------------------------------------------------
        json_wcy['index'] = wcy_index
        json_wcy['gmf'] = wcy_gmf
        json_wcy['forecast'] = wcy_forecast
        #

    except:
        # Generate JSON error ------------------------------------------------------------------------------------------
        json_wcy['status'] = 'error'
        #

    # Return JSON data -------------------------------------------------------------------------------------------------
    return json_wcy


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=10144)
