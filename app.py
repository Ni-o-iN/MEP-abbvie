from flask import Flask, render_template, jsonify, request, url_for
import mysql.connector
import json
import string
import random

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

@app.route('/downlaod')
def download_german():
    return render_template('Deutsch/download.html')

@app.route('/download_english')
def download_english():
    return render_template('Englisch/download.html')

@app.route('/get_chart_data', methods=['POST'])
def get_chart_data():

    print(request.referrer)
    if(request.referrer == "http://127.0.0.1:5000/monat" or request.referrer == "http://127.0.0.1:5000/month"):
        selected_option = request.json['selected_option2']
        selected_month = request.json['selected_option1'].split("-")[1]
        selected_year = request.json['selected_option1'].split("-")[0]
    
    if(request.referrer == "http://127.0.0.1:5000/heute" or request.referrer == "http://127.0.0.1:5000/today"):
        selected_option = request.json['selected_option1']
        match selected_option:
            case "area-a":
                selected_option ="A"
            case "area-b":
                    selected_option ="B"
            case "area-c":
                    selected_option ="C"
            case "area-d":
                    selected_option ="D"
            case "area-e":
                    selected_option ="E"
            case "area-f":
                    selected_option ="F"
            case "area-g":
                    selected_option ="G"
            case "area-h":
                    selected_option ="H"


    # Establish a connection to MySQL
    connection = mysql.connector.connect(**mysql_config)
    cursor = connection.cursor()

    if(request.referrer == "http://127.0.0.1:5000/monat" or request.referrer == "http://127.0.0.1:5000/month"):
        query = "SELECT time, value FROM measurement m JOIN soundmeter s ON m.soundmeter_id = s.id WHERE s.area = %s AND MONTH(m.time) = %s AND YEAR(m.time) = %s;"
        if not selected_option and not selected_month:
            return (0,0)
        else:
            cursor.execute(query, (selected_option,selected_month,selected_year))
    elif(request.referrer =="http://127.0.0.1:5000/heute" or request.referrer=="http://127.0.0.1:5000/today"):
        query = "SELECT time, value FROM measurement m JOIN soundmeter s ON m.soundmeter_id = s.id WHERE s.area = %s AND DATE(m.time) = CURDATE();"
        if not selected_option:
            return (0,0)
        else:
            print(selected_option)
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
        elif(request.referrer =="http://127.0.0.1:5000/heute" or request.referrer =="http://127.0.0.1:5000/today"):
            chart_labels.append(row[0].split()[1].split(":")[0])
        chart_data.append(row[1])
        
    # Close the MySQL connection
    cursor.close()
    connection.close()
    print("VOR CALCULATE_AVERAGE: ", chart_data, " " , chart_labels)
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
@app.route('/refresh_overview', methods=['POST', 'GET'])
def refresh_overview():
    #  a = random.randint(30, 70)
    #  b = random.randint(30, 70)
    #  c = random.randint(30, 70)
    #  d = random.randint(30, 70)
    #  e = random.randint(30, 70)
    #  f = random.randint(30, 70)
    #  g = random.randint(30, 70)
    #  h = random.randint(30, 70)

    connection = mysql.connector.connect(**mysql_config)
    cursor = connection.cursor()    
            
    #query ="SELECT value FROM measurement m JOIN soundmeter s ON m.soundmeter_id = s.id WHERE s.area IN (%s,%s,%s,%s,%s,%s,%s,%s) ORDER BY time DESC LIMIT 1;" #TODO vielleicht nochangeben, dass es heute sein muss?
    query = """
        SELECT s.area, m.value
            FROM measurement m
        JOIN soundmeter s ON m.soundmeter_id = s.id
        WHERE s.area IN (%s, %s, %s, %s, %s, %s, %s, %s)
        AND m.time = (
            SELECT MAX(time)
            FROM measurement
            WHERE soundmeter_id = m.soundmeter_id
        )
    """
    values =("A","B","C","D","E","F","G","H")

    cursor.execute(query, values)
    results = cursor.fetchall()
    data = [row[1] for row in results]
    # data ={
    #     'a':results[0],
    #     'b':results[1],
    #     'c':results[2],
    #     'd':results[3],
    #     'e':results[4],
    #     'f':results[5],
    #     'g':results[6],
    #     'h':results[7],
    # }
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)
