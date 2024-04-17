import requests, re
from urllib.parse import urlparse, parse_qs, quote
import datetime, pytz, json
import random
from bs4 import BeautifulSoup
import schedule
import time
import winsound

def formatted_date():
    chicago_tz = pytz.timezone('America/Chicago')
    now = datetime.datetime.now(chicago_tz)

    # Example: "Tue Apr 16 2024 13:57:33 GMT-0500 (Central Standard Time)"
    # Note: The timezone offset might vary (-0500 or -0600) depending on daylight saving time.
    date_str = now.strftime('%a+%b+%d+%Y+%H:%M:%S+GMT%z+(%Z)')
    formatted_date_str = date_str.replace('GMT+', 'GMT%2B').replace('GMT-', 'GMT-')  # Handle both cases
    formatted_date_str = formatted_date_str.replace(':', '%3A') 
    #print("formatted_date: "+formatted_date_str)
    return formatted_date_str

def login(username, password):
    url = 'https://enroll.illinois.edu/ping'
    headers = {
        'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
        'DNT': '1',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        'sec-ch-ua-platform': "Windows",
        'Accept': '*/*',
        'Sec-Fetch-Site': 'same-site',
        'Sec-Fetch-Mode': 'no-cors',
        'Sec-Fetch-Dest': 'script',
        'Referer': 'https://myillini.illinois.edu/',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'en-US,en;q=0.9'
    }

    response = requests.get(url, headers=headers)
    pattern = r'https://mx\.technolutions\.net/ping\?[^"]*'
    match = re.search(pattern, response.text)

    if match:
        ping_url = match.group(0)
        query_string = urlparse(ping_url).query
        params = parse_qs(query_string)

        id_value = params.get('id', [None])[0]
        sid_value = params.get('sid', [None])[0]
        hid_value = params.get('hid', [None])[0]

        print("ID:", id_value)
        print("SID:", sid_value)
        print("HID:", hid_value)
    else:
        print("No URL found")



    url = 'https://myillini.illinois.edu/IdentityManagement/Home/Login?ReturnUrl=%2FDashboard'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': 'Windows',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'en-US,en;q=0.9',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }

    response = requests.get(url, headers=headers)
    antiforgery_cookie = response.cookies.get('.AspNetCore.Antiforgery.9TtSrW0hzOs')
    soup = BeautifulSoup(response.text, 'lxml')  # 'html.parser' could be used as well

    tokens = soup.find_all('input', attrs={'name': '__RequestVerificationToken'})

    if tokens:
        request_verification_token = tokens[0]['value']
    else:
        print("No tokens found")

    #print("Antiforgery Cookie:", antiforgery_cookie)
    #print("__RequestVerificationToken:", request_verification_token)

    url = 'https://mx.technolutions.net/ping'

    headers = {
        'Host': 'mx.technolutions.net',
        'Connection': 'keep-alive',
        'Content-Length': '333',
        'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
        'sec-ch-ua-platform': "Windows",
        'DNT': '1',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        'Content-Type': 'text/plain;charset=UTF-8',
        'Accept': '*/*',
        'Origin': 'https://myillini.illinois.edu',
        'Sec-Fetch-Site': 'cross-site',
        'Sec-Fetch-Mode': 'no-cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://myillini.illinois.edu/',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'en-US,en;q=0.9'
    }

    # JSON data to send with the request
    data = {
        "id": id_value, 
        "sid": sid_value,
        "hid": hid_value,
        "u": "https://myillini.illinois.edu/IdentityManagement/Home/Login?ReturnUrl=%2FDashboard",
        "d": random.randint(530000,550000),
        "a": random.randint(20000,30000)
    }

    # Convert dict to JSON string as the server expects text/plain content type
    json_data = json.dumps(data)

    response = requests.post(url, headers=headers, data=json_data)
    #print(response.status_code)

    url = 'https://myillini.illinois.edu/IdentityManagement/Login'

    headers = {
        'Host': 'myillini.illinois.edu',
        'Connection': 'keep-alive',
        'Content-Length': '219',
        'Cache-Control': 'max-age=0',
        'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': "Windows",
        'Origin': 'https://myillini.illinois.edu',
        'DNT': '1',
        'Upgrade-Insecure-Requests': '1',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        'Referer': 'https://myillini.illinois.edu/IdentityManagement/Login',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'en-US,en;q=0.9'
    }

    cookies = {
        '.AspNetCore.Antiforgery.9TtSrW0hzOs': antiforgery_cookie,
        'OptanonConsent' : "landingPath=https%3A%2F%2Fmyillini.illinois.edu%2FIdentityManagement%2FHome%2FLogin%3FReturnUrl%3D%252FDashboard&datestamp="+formatted_date()+"&version=3.6.25"
    }

    data = {
        'Username': username,
        'Password': password,
        '__RequestVerificationToken': request_verification_token
    }

    response = requests.post(url, headers=headers, cookies=cookies, data=data, allow_redirects=False)
    myillini_cr_token=None
    cookie_header = response.headers.get('Set-Cookie')
    if cookie_header:
        matches = re.findall(r'.myIlliniCRToken=([^;]+)', cookie_header)
        if matches:
            myillini_cr_token = matches[0]
            #print("Extracted CR Token:", myillini_cr_token)
        else:
            print("CR Token not found.")
            exit()

    #print(myillini_cr_token)
    return antiforgery_cookie, myillini_cr_token

def check_status(login_token):
    url = 'https://myillini.illinois.edu/Apply/Home/SetSession'
    headers = {
        'Host': 'myillini.illinois.edu',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'DNT': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': 'Windows',
        'Referer': 'https://myillini.illinois.edu/Dashboard',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'en-US,en;q=0.9'
    }

    cookies = {
        '.AspNetCore.Antiforgery.9TtSrW0hzOs': login_token[0],
        '.myIlliniCRToken': login_token[1],
        'OptanonConsent' : "landingPath=NotLandingPage&datestamp="+formatted_date()+"&version=3.6.25&AwaitingReconsent=false",
    }

    response = requests.get(url, headers=headers, cookies=cookies,allow_redirects=False)
    session_cookie = response.cookies.get('.AspNetCore.Session.myIllini')
    #print("Session Cookie: ", session_cookie)

    url = 'https://myillini.illinois.edu/Apply/Application/Status'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': 'Windows',
        'Referer': 'https://myillini.illinois.edu/Dashboard',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'DNT': '1',
        'Upgrade-Insecure-Requests': '1'
    }

    cookies = {
        '.AspNetCore.Antiforgery.9TtSrW0hzOs': login_token[0],
        '.myIlliniCRToken' : login_token[1],
        'OptanonConsent' : "landingPath=NotLandingPage&datestamp="+formatted_date()+"&version=3.6.25&AwaitingReconsent=false",
        '.AspNetCore.Session.myIllini' : session_cookie 
    }

    response = requests.get(url, headers=headers, cookies=cookies)
    soup = BeautifulSoup(response.text, 'html.parser')

    status_area = soup.find('div', {'id': 'statusArea'})
    status_tag = None
    status_text = "Status not found"
    status_keywords = ["Denial", "Accepted", "Complete", "YOU'RE"]
    found_statuses = []

    for element in soup.find_all(string=True):  # Finds all text nodes
        element_text = element.strip()  # Clean up the text
        if element_text:  # Make sure the text is not empty
            # Check if any keyword is in the text node
            for keyword in status_keywords:
                if keyword in element_text:
                    # If keyword found, append (keyword, full text of the node) to results
                    found_statuses.append((keyword, element_text))

    for status, text in found_statuses:            
        print(f"Application Status: '{text}'")
        if text!="Complete":
            for i in range(30):
                winsound.Beep(500,2500)

    #  if status_area:
    #      status_tag = status_area.find('p')
    #      if status_tag and status_tag.strong:
    #          if 'Status:' in status_tag.strong.get_text(strip=True):
    #              status_text = status_tag.strong.next_sibling.strip()
    #              if(status_text=='Denial' or status_text=='Accepted')
    #  print(f"Application Status: {status_text}")

print("Disclaimer: This utility is for diagnostic purpose ONLY. Prospective students are not advised to use this tool. The author is not responsible to any potential consequence, including but not limited to, denial or rescission of admission, disciplinary action, and lawsuits. You are warned not to set the interval below 5 minutes.")
print("Please input Username and Password for myillini."+"\n"*3)
username=input("Username:")
pwd=input("Password:")
myinterval=input("Interval:")
myint=max(int(myinterval),5)
login_data=login(username,pwd)
check_status(login_data)

schedule.every(myint).minutes.do(check_status,login_data)

while True:
    schedule.run_pending()
    time.sleep(10)
