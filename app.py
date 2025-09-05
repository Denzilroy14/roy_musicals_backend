from flask import*
from flask_cors import CORS
import sqlite3
import os
from datetime import datetime
app=Flask(__name__)
CORS(app)

app.config['SECRET_KEY']='ITS_ME_HERE@COOL-BUDDY'
app.config['UPLOADER'] = os.path.join(app.root_path, 'uploads')
SPECIFIED_DATE='2025-11-02'
DATABASE='database.db'

def init_db():
    con=sqlite3.connect(DATABASE)
    con.execute('CREATE TABLE IF NOT EXISTS customer(customername TEXT,customerphone TEXT,customeremail TEXT,instrument TEXT,brand_model TEXT,issue_video TEXT)')
    con.commit()
init_db()
@app.route('/appoinment',methods=['POST'])
def appoinment():
    customername=request.form['customername']
    customerphone=request.form['customerphone']
    customeremail=request.form['customeremail']
    instrument=request.form['instrument']
    brand_model=request.form['brand_model']
    issue_video=request.files['video']
    date=request.form['date']
    time=request.form['time']

    d=datetime.strptime(date,'%Y-%m-%d')
    if d.weekday()==6:
        return jsonify({'message':'No appoinments on Sundays!'})
    elif d==SPECIFIED_DATE:
        return jsonify({'message':'Appoinments cannot be booked on this date'})

    
    filename=issue_video.filename
    filepath=os.path.join(app.config['UPLOADER'],filename)
    issue_video.save(filepath)
    con=sqlite3.connect(DATABASE)
    cur=con.cursor()
    cur.execute('INSERT INTO customer(customername,customerphone,customeremail,instrument,brand_model,issue_video,appoinment_date,appoinment_time) VALUES(?,?,?,?,?,?,?,?)',(customername,customerphone,customeremail,instrument,brand_model,filename,date,time))
    con.commit()
    return jsonify({'message':'Appoinment booked successfully!'})

@app.route('/admin',methods=['GET'])
def admin():
    con=sqlite3.connect(DATABASE)
    curr=con.cursor()
    DATA=curr.execute('SELECT * FROM customer').fetchall()

    user_list=[]
    for data in DATA:
        user_list.append({
            'customername':data[0],
            'customerphone':data[1],
            'customeremail':data[2],
            'instrument':data[3],
            'brand_model':data[4],
            'video_url':f'http://localhost:5000/uploads/{data[5]}',
            'appoinment_date':data[7],
            'appoinment_time':data[6]
        })
    return jsonify(user_list)
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOADER'],filename)


con=sqlite3.connect('database.db')
cur=con.cursor()
#ows=cur.execute('PRAGMA table_info(customer)')
#for row in rows:
 #   print(row)
#rows=cur.execute('SELECT appoinment_date,appoinment_time FROM customer').fetchall()
#print(rows)
#cur.execute('ALTER TABLE customer ADD COLUMN appoinment_date TEXT')
#con.commit()


if __name__=='__main__':
    if not os.path.exists(app.config['UPLOADER']):
        os.mkdir(app.config['UPLOADER'])
    app.run(debug=True)