from flask import Flask, render_template, jsonify, request
import mysql.connector
import json

app = Flask(__name__)

# MySQL connection configuration
mysql_config = {
    'user': '141.19.176.122',
    'password': 'j3Remy.J0hn',
    'host': '141.19.143.13',
    'database': 'calmvie',
    'raise_on_warnings': True
}

@app.route('/')
def index():
    return render_template('monat.html')

@app.route('/get_chart_data', methods=['POST'])
def get_chart_data():

    selected_option = request.json['selected_option']

    # Establish a connection to MySQL
    connection = mysql.connector.connect(**mysql_config)
    cursor = connection.cursor()

    query = "SELECT time, value FROM measurement m JOIN soundmeter s ON m.soundmeter_id = s.id WHERE s.area = %s AND MONTH(m.time) = 6;"
    
    if not selected_option:
        cursor.execute("SELECT time, value FROM measurement m JOIN soundmeter s ON m.soundmeter_id = s.id WHERE s.area = 'A' AND MONTH(m.time) = 6;")
    else:
        cursor.execute(query, (selected_option,))

    # Retrieve the data
    queryoutput = cursor.fetchall()
    chart_data = json.dumps(queryoutput, default=str)
    data = eval(chart_data)
    # Process the retrieved data as needed
    chart_data = []
    chart_labels = []
    
    for row in data:
        # Assuming the chart data is in a specific column of the retrieved data
        chart_labels.append(row[0].split()[0].split("-")[2])
        chart_data.append(row[1])

    # Close the MySQL connection
    cursor.close()
    connection.close()

    return jsonify(chart_data, chart_labels)

if __name__ == '__main__':
    app.run(debug=True)
