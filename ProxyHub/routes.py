from flask import render_template,request
import requests
from ProxyHub import app

def check_proxies(protocol,proxy):
    check_url = "http://httpbin.org/ip"
    proxy_dict = {
        f'http': f'{protocol}://{proxy}',
        f'https': f'{protocol}://{proxy}'
    }
    try:
        status = requests.get(check_url, proxies=proxy_dict, timeout=5).status_code
        if status == 200:
            return True
        else:
            return False
    except:
        pass

@app.route("/")
@app.route("/home",methods=["GET"])
def home():
    return render_template("home.html",title="Home Page")

@app.route("/grab",methods=["GET","POST"])
def grab():
    return render_template("grab.html",title="Grab Proxies")

@app.route("/api/grab",methods=["GET","POST"])
def api_grab():
    array = [1,2,3,4,5,6,7,8,9,0]
    protocol = request.args.get('protocol')
    anonymity = request.args.get('anonymity')
    range = request.args.get('range')
    proxies = []
    if protocol:
        if anonymity:
            if range:
                try:
                    int(range)
                except:
                    return ['Range should be a number!']
            else:
                return ['range is missing!']
        else:
            return ['anonymity is missing!']
    else:
        return ['protocol is missing!']
    url = "https://api.proxyscrape.com/v4/free-proxy-list/get"
    data = {
        'request' : 'display_proxies',
        'proxy_format' : 'ipport',
        'format' : 'text',
        'protocol' : '',
        'anonymity' : '',
        'timeout' : ''
    }
    if protocol == 'all':
        del data['protocol']
    elif protocol == 'http':
        data['protocol'] = 'http'
    elif protocol == 'socks4':
        data['protocol'] = 'socks4'
    elif protocol == 'socks5':
        data['protocol'] = 'socks5'
    else:
        return ["Don't play with me!"]
    
    if anonymity == 'all':
        del data['anonymity']
    elif anonymity == 'Elite':
        data['anonymity'] = 'Elite'
    elif anonymity == 'Anonymous':
        data['anonymity'] = 'Anonymous'
    elif anonymity == 'Transparent':
        data['anonymity'] = 'Transparent'
    else:
        return ["Don't play with me!"]
    
    if (20 <= int(range) <= 20000):
        data['timeout'] = range
    else:
        return ["Don't play with me!"]
    
    try:
        response = requests.get(url, params=data).text.splitlines()
        for proxy in response:
            proxies.append(proxy)
    except:
        return ['Failed to grab proxies, please contact website administrator to solve the problem!']
    if not proxies:
        return ['There is no proxies applicable to your preferences now, try again after 5 minutes please!']
    return proxies

@app.route("/api/check",methods=["GET","POST"])
def api_check():
    protocol = request.args.get('protocol')
    if not protocol:
        return ['protocol is missing!']
    data = request.get_json()
    tmp_proxies = list(data.get("proxies", []))
    proxies = [item for item in tmp_proxies if item != '\n']
    valid_proxies = []
    if not proxies:
        return ['There is no proxies to check!']
    valid_protocols = ['http','socks4','socks5']
    if protocol in valid_protocols:
        for proxy in proxies:
            status = check_proxies(protocol,proxy)
            if status:
                valid_proxies.append(proxy)
    else:
        return ['Invlaid protocol type, please choose the right proxies protocol!']
    return valid_proxies
