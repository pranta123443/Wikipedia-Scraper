from flask import Flask, request, send_file, redirect, url_for, session, render_template
import requests
from bs4 import BeautifulSoup
import pandas as pd

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/')
def home():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'admin':
            session['logged_in'] = True
            return redirect(url_for('home'))
        else:
            return 'Invalid credentials'
    return render_template('login.html')

@app.route('/logout')
def logout():
    session['logged_in'] = False
    return redirect(url_for('login'))

@app.route('/scrape', methods=['POST'])
def scrape():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    country = request.form.get('country')
    rows = request.form.get('rows')

    url = f'https://en.wikipedia.org/wiki/Demographics_of_{country}'
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'lxml')

    infobox = soup.find('table', {'class': 'infobox'})

    if infobox:
        labels = infobox.find_all('th', {'class': 'infobox-label'})
        datas = infobox.find_all('td', {'class': 'infobox-data'})

        data_list = []
        for label, data in zip(labels, datas):
            label_text = label.get_text(strip=True)
            data_text = data.get_text(strip=True).replace('\xa0', ' ')
            data_list.append({'Field': label_text, 'Value': data_text})

        df = pd.DataFrame(data_list)

        if rows != 'all':
            try:
                rows = int(rows)
                df = df.head(rows)
            except ValueError:
                pass

        filename = f'demographics_infobox_{country}.csv'
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        table_html = df.to_html(index=False, classes='data-table', border=0)

        return render_template('index.html', country=country, table=table_html, filename=filename)

    return f"Infobox not found on the page for {country}."

@app.route('/download')
def download():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    filename = request.args.get('file')
    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
