from flask import Flask, render_template, jsonify, request, url_for, send_file
import mysql.connector
import json
import mysql.connector.pooling
import string
import random
import datetime
#pip install Flask-APScheduler
from apscheduler.schedulers.background import BackgroundScheduler
import smtplib
from email.mime.text import MIMEText
from openpyxl import Workbook

app = Flask(__name__)

#Scheduler initialisieren
scheduler = BackgroundScheduler()

#globaler Counter für Warnstufe des Bereichs, globale aktuelle Zeit
area_limits_global = {}
daily_warning_counter = {}
current_date = datetime.datetime.now().hour


# MySQL connection configuration
mysql_config = {
    'user': '141.19.176.122',
    'password': 'j3Remy.J0hn',
    'host': '141.19.143.13',
    'database': 'calmvie',
    'raise_on_warnings': True
}
pool = mysql.connector.pooling.MySQLConnectionPool(pool_name="mypool", pool_size=5, **mysql_config)
#Funktion zur Mail Versendung
def send_email_warning(letter):
    
    recipient_email = "audio.architects@outlook.de"
    
    sender_email = "audio.architects@outlook.de" 
    username = "audio.architects@outlook.de"
    password = "dnlcj!MEP23"   
    smtp_server = "smtp.office365.com"
    smtp_port = 587
    

    #Nachricht erstellen
    subject = f"Warnung: Bereich {letter} erreicht Wert 4"
    body = f"Der Bereich {letter} hat den Wert 4 erreicht!"
    
    #E-Mail erstellen
    message = MIMEText(body)
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = recipient_email
    
    #E-Mail versenden
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(username, password)
            server.sendmail(sender_email, recipient_email, message.as_string())
        print("E-Mail-Benachrichtigung gesendet!")
    except Exception as e:
        print("Fehler beim Senden der E-Mail-Benachrichtigung:", str(e))


#Berechnung Warnstufe der Bereiche
def schedulerWarnung():
    #Verbindung zu MySQL server aufbauen und Query ausführen
    con_warnung = pool.get_connection()
    cur_warnung = con_warnung.cursor()
    query_warnung = 'SELECT m.value, s.area FROM measurement m JOIN soundmeter s ON m.soundmeter_id = s.id WHERE m.time >= NOW() - INTERVAL 60 SECOND;'
    cur_warnung.execute(query_warnung)
    result_warnung = cur_warnung.fetchall()
    
    #Average der Werte für jeden Bereich berechnen
    sums = {}
    counts = {}
    
    for value, letter in result_warnung:
        if letter in sums:
            sums[letter] += value
            counts[letter] += 1
        else:
            sums[letter] = value
            counts[letter] = 1

    averages = {letter: sums[letter] / counts[letter] for letter in sums}
    print(averages)
    
    
    #Query für Lautstärkelimit aller Bereiche ausführen
    query_area_limit = 'SELECT DISTINCT area, soundlimit_yellow FROM soundmeter;'
    cur_warnung.execute(query_area_limit)
    result_area_limit = cur_warnung.fetchall()

    reset_warning_counter()

    #Limit vergleichen mit berechnetem Average und dementsprechend globalen Counter hoch-/runterzählen
    for letter, average in averages.items():
        limit = next((limit for l, limit in result_area_limit if l == letter), None)
        if limit is not None:
            if average > limit:
                if letter in area_limits_global:
                    area_limits_global[letter] += 1
                else:
                    area_limits_global[letter] = 1

                #falls in einem Bereich bereits 5 Warnungen gesendet wurden werden restlich ignoriert
                if letter in daily_warning_counter and daily_warning_counter[letter] > 2:
                    print(f'Warnungslimit für Bereich {letter} erreicht')
                    if area_limits_global[letter] == 4:
                        area_limits_global[letter] = 0
                    continue
               
                if area_limits_global[letter] == 4:
                    print(f"Warnung: Der Bereich für den Buchstaben {letter} hat den Wert 4 erreicht!")
                    send_email_warning(letter)
                    
                    if letter in daily_warning_counter:
                        daily_warning_counter[letter] += 1
                    else:
                        daily_warning_counter[letter] = 1
                    
                    area_limits_global[letter] = 0
            else:
                if letter in area_limits_global and area_limits_global[letter] > 0:
                    area_limits_global[letter] -= 1
                elif letter not in area_limits_global:
                    area_limits_global[letter] = 0

    print("Bereichslevel:", area_limits_global)

    cur_warnung.close()
    con_warnung.close()

def reset_warning_counter():
    global current_date
    global daily_warning_counter

    if datetime.datetime.now().hour > current_date:
        daily_warning_counter = {}
        current_date= datetime.datetime.now().hour


#Scheduler Job und Trigger zuweisen
scheduler.add_job(id='Scheduled Task', func= schedulerWarnung, trigger = 'interval', seconds = 60)


@app.route('/')
def index():
    # values = get_latest_data()
    # styles = []
    # for decibel in values:
    #     if (decibel > 55):
    #          styles.append('style= "rgba(220, 0, 0, 0.5)";')
    #     elif (decibel > 50):
    #         styles.append('style= "rgba(220, 220, 0, 0.5)";')
    #     else:
    #         styles.append('style= "rgba(0, 158, 0, 0.5)";')
        
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
        print("Monat geht hier rein")
        selected_option = request.json['selected_option2']
        selected_month = request.json['selected_option1'].split("-")[1]
        selected_year = request.json['selected_option1'].split("-")[0]
    
    if("http://127.0.0.1:5000/heute" in request.referrer or "http://127.0.0.1:5000/today" in request.referrer):
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
    connection = pool.get_connection()
    cursor = connection.cursor()
    query=0
    if(request.referrer == "http://127.0.0.1:5000/monat" or request.referrer == "http://127.0.0.1:5000/month"):
        print("Monat geht auch hier rein")
        query = "SELECT time, value FROM measurement m JOIN soundmeter s ON m.soundmeter_id = s.id WHERE s.area = %s AND MONTH(m.time) = %s AND YEAR(m.time) = %s;"
        if not selected_option and not selected_month:
            return (0,0)
        else:
            cursor.execute(query, (selected_option,selected_month,selected_year))
    elif("http://127.0.0.1:5000/heute" in request.referrer or "http://127.0.0.1:5000/today" in request.referrer):
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
        elif("http://127.0.0.1:5000/heute" in request.referrer or "http://127.0.0.1:5000/today" in request.referrer):
            chart_labels.append(row[0].split()[1].split(":")[0])
        chart_data.append(row[1])
        
    print("monat geht auch hier rein")    
    # Close the MySQL connection
    cursor.close()
    connection.close()
    unique_labels, averaged_data  = calculate_average(chart_data, chart_labels) #TODO: care when there is no data, still need to fix, handle with None type stuff
    if (averaged_data == []):
        return jsonify(averaged_data,unique_labels,)
    return jsonify(averaged_data,unique_labels, min(averaged_data), max(averaged_data),)

def calculate_average(values, labels):
    if len(values) != len(labels):
        return None, None
    
    if len(values) == 0 or len(labels) == 0:
        return None, None
    
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

def get_latest_data():
    #  a = random.randint(30, 70)
    #  b = random.randint(30, 70)
    #  c = random.randint(30, 70)
    #  d = random.randint(30, 70)
    #  e = random.randint(30, 70)
    #  f = random.randint(30, 70)
    #  g = random.randint(30, 70)
    #  h = random.randint(30, 70)

    connection = pool.get_connection()
    cursor = connection.cursor()    
            
    #query ="SELECT value FROM measurement m JOIN soundmeter s ON m.soundmeter_id = s.id WHERE s.area IN (%s,%s,%s,%s,%s,%s,%s,%s) ORDER BY time DESC LIMIT 1;" #TODO vielleicht nochangeben, dass es heute sein muss?
    query = """
        SELECT s.area, m.value
        FROM measurement m
        JOIN soundmeter s ON m.soundmeter_id = s.id
            WHERE s.area IN ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H')
            AND m.time IN (
                SELECT MAX(time)
                FROM measurement
                WHERE soundmeter_id IN (SELECT id FROM soundmeter WHERE area IN ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'))
                GROUP BY soundmeter_id
)
    """

    cursor.execute(query)
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
    cursor.close()
    connection.close()
    return data

@app.route('/refresh_overview', methods=['POST', 'GET'])
def refresh_overview():
    # #  a = random.randint(30, 70)
    # #  b = random.randint(30, 70)
    # #  c = random.randint(30, 70)
    # #  d = random.randint(30, 70)
    # #  e = random.randint(30, 70)
    # #  f = random.randint(30, 70)
    # #  g = random.randint(30, 70)
    # #  h = random.randint(30, 70)

    # connection = mysql.connector.connect(**mysql_config)
    # cursor = connection.cursor()    
            
    # #query ="SELECT value FROM measurement m JOIN soundmeter s ON m.soundmeter_id = s.id WHERE s.area IN (%s,%s,%s,%s,%s,%s,%s,%s) ORDER BY time DESC LIMIT 1;" #TODO vielleicht nochangeben, dass es heute sein muss?
    # query = """
    #     SELECT s.area, m.value
    #         FROM measurement m
    #     JOIN soundmeter s ON m.soundmeter_id = s.id
    #     WHERE s.area IN (%s, %s, %s, %s, %s, %s, %s, %s)
    #     AND m.time = (
    #         SELECT MAX(time)
    #         FROM measurement
    #         WHERE soundmeter_id = m.soundmeter_id
    #     )
    # """
    # values =("A","B","C","D","E","F","G","H")

    # cursor.execute(query, values)
    # results = cursor.fetchall()
    # data = [row[1] for row in results]
    # # data ={
    # #     'a':results[0],
    # #     'b':results[1],
    # #     'c':results[2],
    # #     'd':results[3],
    # #     'e':results[4],
    # #     'f':results[5],
    # #     'g':results[6],
    # #     'h':results[7],
    # # }
    # cursor.close()
    # connection.close()
    return jsonify(get_latest_data())

@app.route("/download_excel", methods=["POST"])
def download_excel():

    data = request.json  # Retrieve the JSON data from the request
    ids = data.get("ids")
    datetime1 = data.get("datetime1")
    datetime2 = data.get("datetime2")
    #==============
    connection = pool.get_connection()
    cursor = connection.cursor()
    
    ####
    areas = [element.split("-")[1].upper() for element in ids]
    placeholders = ', '.join(['%s'] * len(areas))

    ####
    query = f"""
        SELECT s.area, m.value, m.time
            FROM measurement m
            JOIN soundmeter s ON m.soundmeter_id = s.id 
            WHERE s.area IN ({placeholders})
            AND m.time BETWEEN %s AND %s
    """
    print(query)
    values = areas + [datetime1, datetime2]  # Concatenate the values into a single list
    #print(values)
    cursor.execute(query, values)

    # Fetch all the rows from the result set
    rows = cursor.fetchall()
    

    # Create a new Excel workbook and get the active worksheet
    workbook = Workbook()
    worksheet = workbook.active

    # Write the column headers
    column_headers = [column[0] for column in cursor.description]
    worksheet.append(column_headers)

    # Write the data rows
    for row in rows:
        worksheet.append(row)

    # Save the workbook
    file_path = "./downloaded_data.xls"
    workbook.save(file_path)
    cursor.close()
    connection.close()
    return send_file(file_path, as_attachment=True)


if __name__ == '__main__':
    #scheduler.start()
    app.run(debug=True, use_reloader=False)
