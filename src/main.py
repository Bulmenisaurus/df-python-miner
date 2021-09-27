from server import Server
from http.server import HTTPServer


def main():
    with HTTPServer(('', 8000), Server) as server:
        server.serve_forever()


if __name__ == '__main__':
    main()
