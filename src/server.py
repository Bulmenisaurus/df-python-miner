from http.server import BaseHTTPRequestHandler
from decimal import Decimal
import mimc
import json


def mine_chunk(bottom_left: dict[str, int], side_length: int, planet_rarity: int):
    location_id_ub = Decimal(
        '21888242871839275222246405745257275088548364400416034343698204186575808495617')

    planet_locations = []
    chunk_x = bottom_left['x']
    chunk_y = bottom_left['y']

    for y in range(chunk_y, chunk_y + side_length):
        for x in range(chunk_x, chunk_x + side_length):
            planet_hash = mimc.mimcHash(x, y)
            if planet_hash < (location_id_ub / planet_rarity):
                planet_locations.append({
                    'hash': str(planet_hash),
                    'coords': {'x': x, 'y': y}
                })

    return {
        'chunkFootprint': {
            'bottomLeft': bottom_left,
            'sideLength': side_length
        },
        'planetLocations': planet_locations
    }


class Server(BaseHTTPRequestHandler):
    def do_GET(self):
        print('[GET]')
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        message = 'welcome to the snake world'
        self.wfile.write(message.encode('utf-8'))

    def do_POST(self):
        print('[POST]')
        content_length = int(self.headers['Content-Length'])
        data = str(self.rfile.read(content_length), "utf-8")
        mine_data = json.loads(data)

        res = mine_chunk(mine_data['chunkFootprint']['bottomLeft'],
                         side_length=mine_data['chunkFootprint']['sideLength'],
                         planet_rarity=mine_data['planetRarity'])

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

        message = json.dumps(res)
        self.wfile.write(message.encode('utf-8'))

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Headers',
                         'Authorization, Content-Type'),
        self.send_header('Access-Control-Allow-Methods', 'POST'),
        self.end_headers()
