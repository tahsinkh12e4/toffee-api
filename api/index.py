from flask import Flask, make_response
import requests
import os

app = Flask(__name__)

API_ENDPOINT = "https://bldcmprod-cdn.toffeelive.com/"
headers = {
    "Cookie": "Edge-Cache-Cookie=URLPrefix=aHR0cHM6Ly9ibGRjbXByb2QtY2RuLnRvZmZlZWxpdmUuY29tLw:Expires=1693089595:KeyName=prod_linear:Signature=aC63Wde-Xt3uBt1I0nmq5QNaFjFp4o54zZK6Fa-ui-E6Mqj2mzumQLGRzXVinMIDpRwsaS-NwxkI_bzzxohADQ"
}

@app.route("/")
def credit():
    return "(Toffee-API) Made For ToffeeLiveSetup "

@app.route("/auto/<string:channel_id>.m3u8")
def handle_auto(channel_id):
    response = requests.get(API_ENDPOINT + f"cdn/live/{channel_id}/playlist.m3u8", headers=headers)
    myresponse = make_response(response.text.replace("../slang/", "/single/slang/").replace("?", "-"))
    myresponse.headers["Content-Type"] = "application/vnd.apple.mpegurl"
    return myresponse

@app.route("/single/<path:path>")
def handle_single(path):
    single_url = API_ENDPOINT + "cdn/live/" + path.replace("-", "?")
    print(single_url)
    response = requests.get(single_url, headers=headers)
    myresponse = make_response(response.text.replace("/live/", f"{API_ENDPOINT}/live/"))
    myresponse.headers["Content-Type"] = "application/vnd.apple.mpegurl"
    return myresponse


@app.route("/key")
def handle_key():
	key_id = request.args.get("id")
	if not key_id:
		return "Please provide both 'id'parameters in the URL query"
	key_url = base_url + key_id
	print(key_url)

	response = requests.get(key_url, headers=headers)

	myresponse = make_response(response.content)
	myresponse.headers.get("content-type")
	return myresponse
@app.route("/set-cookie")
def set_cookie():
	new_cookie = request.args.get("cookie")
	if new_cookie:
		global cookie
		cookie = new_cookie	
		headers["cookie"] = new_cookie
		print(headers)
		return f"Cookie value set to: {new_cookie}"
	else:
 		return "Please provide a 'cookie' parameter in the URL query"

if __name__ == "__main__":
    app.run(debug=True, port=os.getenv("PORT", default=5000))
