from flask import Flask, render_template, jsonify, request, url_for
import mysql.connector
import json
import string

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
    return render_template('Deutsch/uebersicht.html')

@app.route('/overview')
def overview():
    return render_template('Englisch/overview.html')

@app.route('/heute')
def heute():
    return render_template('Deutsch/heute.html')

@app.route('/today')
def today():
    return render_template('Englisch/today.html')

@app.route('/woche')
def woche():
    return render_template('Deutsch/kalenderwoche.html')

@app.route('/week')
def week():
    return render_template('Englisch/week.html')

@app.route('/monat')
def monat():
    return render_template('Deutsch/monat.html')

@app.route('/month')
def month():
    return render_template('Englisch/month.html')

@app.route('/administration')
def admin_german():
    return render_template('Deutsch/admin.html')

@app.route('/admin')
def admin_english():
    return render_template('Englisch/settings.html')

@app.route('/get_chart_data', methods=['POST'])
def get_chart_data():

    print(request.referrer)
    selected_option = request.json['selected_option2']
    selected_month = request.json['selected_option1']
    
    # Establish a connection to MySQL
    connection = mysql.connector.connect(**mysql_config)
    cursor = connection.cursor()

    if(request.referrer == "http://127.0.0.1:5000/monat" or request.referrer == "http://127.0.0.1:5000/month"):
        query = "SELECT time, value FROM measurement m JOIN soundmeter s ON m.soundmeter_id = s.id WHERE s.area = %s AND MONTH(m.time) = %s;"
        if not selected_option and not selected_month:
            return (0,0)
        else:
            cursor.execute(query, (selected_option,selected_month,))
    elif(request.referrer =="http://127.0.0.1:5000/heute" or request.referrer=="http://127.0.0.1:5000/today"):
        query = "SELECT time, value FROM measurement m JOIN soundmeter s ON m.soundmeter_id = s.id WHERE s.area = %s AND DATE(m.time) = CURDATE();"
        if not selected_option:
            return (0,0)
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
        if(request.referrer == "http://127.0.0.1:5000/monat" or request.referrer == "http://127.0.0.1:5000/month"):
            chart_labels.append(row[0].split()[0].split("-")[2])
        elif(request.referrer =="http://127.0.0.1:5000/heute"):
            chart_labels.append(row[0].split()[1].split(":")[0])
        chart_data.append(row[1])
        
    # Close the MySQL connection
    cursor.close()
    connection.close()

    unique_labels, averaged_data  = calculate_average(chart_data, chart_labels)
    if (averaged_data == []):
        return jsonify(averaged_data,unique_labels,)
    return jsonify(averaged_data,unique_labels, min(averaged_data), max(averaged_data),)

def calculate_average(values, labels):
    if len(values) != len(labels):
        return None
    
    if len(values) == 0 or len(labels) == 0:
        return None
    
    label_dict = {}
    
    # Map labels to corresponding values
    for value, label in zip(values, labels):
        if label in label_dict:
            label_dict[label].append(value)
        else:
            label_dict[label] = [value]
    
    unique_labels = []
    averages = []
    
    # Calculate average for each label
    for label, value_list in label_dict.items():
        unique_labels.append(label)
        averages.append(sum(value_list) / len(value_list))
    
    return unique_labels, averages

if __name__ == '__main__':
    app.run(debug=True)
