from flask import Flask, request, url_for, redirect, render_template
import requests
import getpass
from bs4 import BeautifulSoup
import json

app = Flask(__name__)



@app.route('/')
def index():
    return render_template('index.html')


@app.route('/all/')
def all():
    return render_template('all.html')

@app.route('/A/')
def A():
    return render_template('A.html')

@app.route('/B/')
def B():
    return render_template('B.html')

@app.route('/C/')
def C():
    return render_template('C.html')

@app.route('/D/')
def D():
    return render_template('D.html')

@app.route('/E/')
def E():
    return render_template('E.html')

@app.route('/F/')
def F():
    return render_template('F.html')

@app.route('/G/')
def G():
    return render_template('G.html')

@app.route('/Other/')
def Other():
    return render_template('Other.html')

@app.route('/grp_index/')
def grp_index():
    return render_template('grp_index.html')

crsid = 0
s = requests.Session()

def login_to_raven(debug = True):

  while 1:
    print("crsID: ", end = '') 
    global crsid
    crsid = input()
    
    pwd = getpass.getpass("raven password: ")

    if len(crsid) == 0 or len(pwd) == 0:
      print("enter valid crsid or password")
    else:
      break

  cookies = {
      '_ga': 'GA1.1.752919269.1583509093',
      '_ga_QWRV5CSCWF': 'GS1.1.1583509093.1.1.1583511420.0',
  }

  headers = {
      'Connection': 'keep-alive',
      'Cache-Control': 'max-age=0',
      'Origin': 'https://raven.cam.ac.uk',
      'Upgrade-Insecure-Requests': '1',
      'Content-Type': 'application/x-www-form-urlencoded',
      'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36',
      'Sec-Fetch-Dest': 'document',
      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
      'Sec-Fetch-Site': 'same-origin',
      'Sec-Fetch-Mode': 'navigate',
      'Sec-Fetch-User': '?1',
      'Referer': 'https://raven.cam.ac.uk/auth/login.html',
      'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
  }

  data = {
    'userid': crsid,
    'pwd': pwd,
    'submit': 'Login'
  }


  response = s.post('https://raven.cam.ac.uk/auth/authenticate2.html', headers=headers, cookies=cookies, data=data)

  status_check = s.get("https://raven.cam.ac.uk/auth/status.html")

  login_status = False
  try: 
    auth_index = status_check.text.index('<span class="principal">')
    crsid = status_check.text[auth_index+24:].split('<')[0]  #Get the crsid from the response message
    print("successfully logged in as " + crsid)
    login_status = True
  except:
    print("Login failed. Please try again.")
    pass

  return login_status

def collect_data():
  print(crsid)
  page = s.get("http://www3.eng.cam.ac.uk/comet/student/y3/module_selection/index.html")
  soup = BeautifulSoup(page.content, 'html.parser')
  personal_list = soup.find_all('td', class_='style1bk')
  del personal_list[1::2]
  for i in range(len(personal_list)):
      personal_list[i] = str(personal_list[i])[21:-5]
  

  with open('python_files/alldata.json') as json_file:
      data = json.load(json_file)

  combined_data = { key : 0 for key in personal_list }


  for key in combined_data.keys():
      #print(key)
      for groupkey in data.keys():
          for subject in data[groupkey].keys():
              if key == subject:
                  combined_data[key] = data[groupkey][subject]

  file = open("static/personal_data.js","w+")
  writeData = "var personal_raw ='" + json.dumps(combined_data) + "';" + "\n"
  file.write(writeData)    
  parsedata = "var personal = JSON.parse(personal_raw);\n" + "var crsid = \"" + str(crsid) + "\""
  file.write(parsedata)
  file.close()

if __name__ == '__main__':
    if login_to_raven(debug=False):
      print("\n\n\n\n  -------------------  STARTING SERVER  ------------------- \n\n")
      collect_data()
      app.run()
