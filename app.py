from flask import Flask, render_template, request, jsonify, redirect, url_for
from supabase import create_client
from datetime import datetime

app = Flask(__name__)

app.secret_key = 'sicu-aura'

res = []

supabase_url = 'https://aaoqhoeejvpvpsgyfrbb.supabase.co'
supabase_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFhb3Fob2VlanZwdnBzZ3lmcmJiIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTMwNzgwOTgsImV4cCI6MjAyODY1NDA5OH0.EBblNYMVY0hGkyr0yQCv46ciCONKCef3lcHzVv_PFgI'
pranav = create_client(supabase_url, supabase_key)

@app.route('/')
def index():
    return render_template('signup.html')

@app.route('/signup')
def show_signup():
    return render_template('signup.html')   

@app.route('/signup', methods=['POST'])
def signup():
    dt = datetime.now().isoformat()  
    email = request.form['email']
    password = request.form['confirm-password']
    hospital_name = request.form['hospital-name']
    address = request.form['address']
    city = request.form['city']
    state = request.form['state']
    phone = request.form['phone']
    registration_number = request.form['registration-number']
    emergency_ward = request.form['emergency-ward']
    pincode = request.form['pincode']
    registration_date = request.form['registration-date']
    ambulance = request.form['ambulance']
    registration_certificate = request.form['registration-certificate']
    data = {
        'date and time': dt,
        'email': email,
        'password': password,
        'hospital_name': hospital_name,
        'address': address,
        'city': city,
        'state': state,
        'phone_no': phone,  
        'registration_number': registration_number,
        'emergency_ward': emergency_ward,  
        'pincode': pincode,
        'registration_certificate': 'File',
        'registration_date': registration_date,
        'ambulance': ambulance,
    }
    response = pranav.table('registrations').insert([data]).execute()
    if 'error' not in response:
        return redirect(url_for('login'))  
    else:
         return 'Error!'

@app.route('/login')
def show_login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    global res
    email = request.form['email']
    hospital_name = request.form['hospital-name']
    password = request.form['password']
    spa = request.form['special-access-code']
    resp = pranav.table('registrations').select('*').execute().data
    data = []
    for x in resp:
        if x['email'] == email and x['password'] == password and spa == '124':
            data.append(x['sno'])
    if len(data) == 0:
        return 'No user'
    res = [email, data]
    print(res)
    return redirect(url_for('capture'))

@app.route('/capture')
def capture():
    return render_template('capture.html')

@app.route('/img_url', methods=['POST'])
def img_url():
    if request.method == 'POST':
        image_url = request.form.get('image_url')
        ids = res[1]
        print("Image URL:", image_url)
        print("IDs:", ids)
        updated = {'image_url' : image_url}
        for id in ids:
            resp = pranav.table('registrations').update(updated).eq('sno', id).execute()
        if 'error' not in resp:
            return redirect(url_for('main'))
        
@app.route('/main', methods=['GET'])
def main():
    global res
    dts = []
    hsps = []
    emails = []
    addresses = []
    phone_nos = []
    cities = []
    states = []
    pincodes = []
    hrds = []
    hrns = []
    hrps = []
    ewns = []
    amb = []
    ids = res[1]
    resp = pranav.table('registrations').select('*').execute().data
    for x in resp:
        if x['sno'] in ids:
            dts.append(x['date and time'])
            hsps.append(x['hospital_name'])
            emails.append(x['email'])
            addresses.append(x['address'])
            phone_nos.append(x['phone_no'])
            cities.append(x['city'])
            states.append(x['state'])
            pincodes.append(x['pincode'])
            hrds.append(x['registration_date'])
            hrns.append(x['registration_number'])
            hrps.append(x['image_url'])
            ewns.append(x['emergency_ward'])
            amb.append(x['ambulance'])
    data_arr = [dts, hsps, emails, addresses, phone_nos, cities, states, pincodes, hrds, hrns, hrps, ewns, amb, res[0]]
    return render_template('main.html', data_arr=data_arr)

@app.route('/logout')
def logout():
    return redirect(url_for('login'))
            
if __name__ == '__main__':
    app.run(debug=True)
