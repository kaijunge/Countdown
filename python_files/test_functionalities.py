import requests
import getpass
from bs4 import BeautifulSoup
import json

s = requests.Session()

def login_to_raven(debug = True):

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

  if debug: 
      data = {
        'userid': 'kcj21',
        'pwd': 'hybridized2spdf4cos',
        'submit': 'Login'
      }

  response = s.post('https://raven.cam.ac.uk/auth/authenticate2.html', headers=headers, cookies=cookies, data=data)

  status_check = s.get("https://raven.cam.ac.uk/auth/status.html")

  login_status = False
  try: 
    auth_index = status_check.text.index('<span class="principal">')
    #status_check.text[auth_index+24:].split('<')[0]  #Get the crsid from the response message
    print("successfully logged in as kcj21")
    login_status = True
  except:
    print("Login failed. Please try again.")
    pass

  return login_status


def main():
    page = s.get("http://www3.eng.cam.ac.uk/comet/student/y3/module_selection/index.html")
    #print(page.content)
    soup = BeautifulSoup(page.content, 'html.parser')
    #print(soup.prettify())
    personal_list = soup.find_all('td', class_='style1bk')
    del personal_list[1::2]
    for i in range(len(personal_list)):
        personal_list[i] = str(personal_list[i])[21:-5]
    

    with open('alldata.json') as json_file:
        data = json.load(json_file)

    combined_data = { key : 0 for key in personal_list }


    for key in combined_data.keys():
        #print(key)
        for groupkey in data.keys():
            for subject in data[groupkey].keys():
                if key == subject:
                    combined_data[key] = data[groupkey][subject]

    print(combined_data)

if __name__ == '__main__':
    login_to_raven()
    print("\n\n\n\n  -------------------  SUCCESSFUL LOGIN  ------------------- \n\n")
    main()