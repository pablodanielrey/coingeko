from http.server import HTTPServer, BaseHTTPRequestHandler
import logging
import requests
import os


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def __init__(self, coin_ids: list[str], request, client_address, server):
        self._build_url(coin_ids)
        super().__init__(request, client_address, server)

    def _build_url(self, coin_ids: list[str]):
        coins = ",".join(coin_ids)
        self._url = f"https://api.coingecko.com/api/v3/simple/price?ids={coins}&vs_currencies=usd"

    def do_GET(self):
        if self.path == "/":
            # Make a request to an external URL (or local server)
            try:
                # url = "https://api.coingecko.com/api/v3/simple/price?ids=ripple,stellar,cardano,solana,hedera-hashgraph,ethereum&vs_currencies=usd"
                logging.info("Fetching url : %s", self._url)
                response = requests.get(self._url)

                # Send response headers
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()

                # Send the fetched data as the response
                content = response.content
                logging.info(content)
                self.wfile.write(content)

            except requests.RequestException as e:
                logging.exception("Error trying accesing coingeko")
                # Handle errors gracefully
                self.send_response(500)
                self.send_header("Content-type", "text/plain")
                self.end_headers()
                self.wfile.write(f"Error fetching data: {str(e)}".encode())
        else:
            # Handle 404 for other paths
            self.send_response(404)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(b"404 Not Found")


class RequestHandlerFactory:

    _DEFAULT_COINS = [
        "ripple",
        "stellar",
        "cardano",
        "solana",
        "hedera-hashgraph",
        "ethereum",
    ]

    def __init__(self):
        coins_str = os.environ.get("COIN_IDS", None)
        if coins_str:
            self._coins: list[str] = coins_str.replace(" ", "").split(",")
        else:
            self._coins = self._DEFAULT_COINS

    def __call__(self, request, client_address, server):
        return SimpleHTTPRequestHandler(self._coins, request, client_address, server)


# Run the server
if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    server_address = ("", 8080)
    httpd = HTTPServer(server_address, RequestHandlerFactory())
    print("Server running on http://0.0.0.0:8080")
    httpd.serve_forever()
