import configparser
import xml.etree.ElementTree as ET
import json
import requests
import websockets
import asyncio

parser = configparser.ConfigParser();
parser.read('config.ini')

def start():
	start_server = websockets.serve(main, parser.get('websockets', 'host'), 
		parser.get('websockets', 'port'))
	asyncio.get_event_loop().run_until_complete(start_server)
	asyncio.get_event_loop().run_forever()


def getData():
	get = requests.get(parser.get('icecast', 'xml_url'), 
		auth = (parser.get('icecast', 'user'), parser.get('icecast', 'pass')))

	if get.status_code != 200:
		raise Exception("status code %s" % get.status_code)

	xmlTree = ET.ElementTree(ET.fromstring(get.text))
	nodes = xmlTree.findall(".//listeners")
	return {
		"artist" : xmlTree.find(".//artist").text,
		"title" : xmlTree.findall(".//title")[1].text,
		"listeners" : int(nodes[1].text) + int(nodes[2].text)
	}
 
async def main(websocket, path):
	data = getData()
	await websocket.send(json.dumps(data))
	
	while True:
		rfData = getData()
		await asyncio.sleep(2)
		
		if rfData != data:
			data = rfData
			await websocket.send(json.dumps(data))
	

if __name__ == '__main__':
	start()