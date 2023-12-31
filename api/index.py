from flask import Flask, request, make_response
import requests

app = Flask(__name__)

cookie = "Edge-Cache-Cookie=URLPrefix=aHR0cHM6Ly9ibGRjbXByb2QtY2RuLnRvZmZlZWxpdmUuY29tLw:Expires=1693089595:KeyName=prod_linear:Signature=aC63Wde-Xt3uBt1I0nmq5QNaFjFp4o54zZK6Fa-ui-E6Mqj2mzumQLGRzXVinMIDpRwsaS-NwxkI_bzzxohADQ"

headers = {
"cookie": cookie
}

base_url = "https://bldcmprod-cdn.toffeelive.com"


@app.route("/")
def credit():
	
	
	return "Made With  By Proximity BD"


@app.route("/auto/<string:channel_id>.m3u8")
def handle_api(channel_id):
	print(channel_id)

 # Retrieve the m3u8 content
	m3u8_url = f"https://bldcmprod-cdn.toffeelive.com/cdn/live/slang/{channel_id}_576/{channel_id}_576.m3u8?bitrate=1000000&channel={channel_id}_576&gp_id="
	response = requests.get(m3u8_url, headers=headers)
	lines = response.text.splitlines()

 # Modify the playlist to include the /ts endpoint for each .ts segment
	ts_urls = []
	for line in lines:
		if ".ts" in line:
			ts_urls.append(f"/ts?id={line}&base={base_url}")
		else:
			ts_urls.append(line)

	m3u8_content = "\n".join(ts_urls)
	specified_text_prefix = "/file"
	specified_text_suffix = ".key"
	replacement_text = f"/key?id=/file.key" # Replace with your specified text

	start_index = m3u8_content.find(specified_text_prefix)
	end_index = m3u8_content.find(specified_text_suffix, start_index)
	specified_text = m3u8_content[start_index: end_index + len(specified_text_suffix)]

	result = m3u8_content.replace(specified_text, replacement_text)

 # Create a response with the updated M3U8 playlist
	response = make_response(result)
	response.headers.get("content-type")
	return response


@app.route("/ts")
def handle_ts():
	# Handler for serving individual TS segments
	ts_id = request.args.get("id")
	base = request.args.get("base")
	if not ts_id or not base:
		return "Please provide both 'id' and 'base' parameters in the URL query"

 # Construct the URL for the TS segment
	ts_url = base + ts_id

	# Fetch the TS segment content
	response = requests.get(ts_url, headers=headers)

 # Create a response with the TS segment content
	myresponse = make_response(response.content)
	myresponse.headers.get("content-type") # Using this to get the content type directly from the headers
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
    app.run(debug=True)
