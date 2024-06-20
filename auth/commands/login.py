import urllib
import uuid
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import parse_qs, urlparse, parse_qsl

import click


class CustomHTTPServer(HTTPServer):
    """
    Custom HTTP server to handle the OAuth2 callback
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id_token = None


class OAuth2Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        query_params = dict(parse_qsl(urlparse(self.path).query))

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        if query_params.get("id_token"):
            self.server.id_token = query_params.get("id_token")
            self.wfile.write(b'Authentication is successful. You can close this window.')
        else:
            # Serve a simple HTML page with JavaScript to capture the fragment and redirect with query parameters
            self.wfile.write(b'''
                       <html>
                           <head>
                               <script type="text/javascript">
                                   function redirectToQuery() {
                                       var fragment = window.location.hash.substr(1); // Remove the leading `#`
                                       console.log(fragment);
                                       if (fragment) {
                                           var query = new URLSearchParams(fragment).toString();
                                           window.location.replace(window.location.pathname + "?" + query);
                                           console.log(window.location.pathname + "?" + query);
                                       }
                                   }
                                   redirectToQuery();
                               </script>
                           </head>
                           <body>
                               <p>Processing authentication. Please wait...</p>
                           </body>
                       </html>
                   ''')
            self.wfile.flush()


def run_server(server_class=CustomHTTPServer, handler_class=OAuth2Handler, port=8080) -> str | None:
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    while not httpd.id_token:
        httpd.handle_request()
    return httpd.id_token


@click.command()
def command():
    """This will be the login command."""
    click.echo('Login command executed')
    sso_keys = {
        "client_id": "edc5fb60-a3a7-49d8-9b37-1b406b45d0a8",  # cli client_id for temporary basis
        "audience": [
            "edc5fb60-a3a7-49d8-9b37-1b406b45d0a8",  # client
            "9115dbcc-bfd0-44c1-bdcb-e1734a517bb7",
            "1ce84e01-d4a8-48c4-9437-71ae1fa1b43a",  # watchman
        ],
        "grant_type": "implicit",
        "response_type": "id_token",
        "scope": "openid + profile",
        # "redirect_uri": "http://localhost:8080",
        "nonce": str(uuid.uuid4()),

    }
    webbrowser.open(
        "<keycloak-login-endpoint>?{}".format(
            urllib.parse.urlencode(sso_keys)))
    print("Waiting for authentication...")
    response = run_server()

    print("after response - ", response)
