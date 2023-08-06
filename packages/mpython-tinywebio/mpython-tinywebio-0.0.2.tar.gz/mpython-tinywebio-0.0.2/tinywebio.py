import mpython
import socket
import network
import json
import gc

EX_INFO = 'tinywebio error occurred!'
SUC_INFO = 'tinywebio started on http://'

# Request Class
class Request:   
    def __init__(self, socket=None):
        self.client_socket = socket
        self.path = None
        self.form = {"tag": None, "value": None}

    def _unquote(self, str):
        res = []
        r = str.split('%')
        res = res + [ord(c) for c in r[0]]

        for i in range(1, len(r)):
            s = r[i]
            try:
                r_first = int(s[:2], 16)
                res.append(r_first)
                r_last = s[2:]
            except Exception:
                r_last = '%' + s     
            if len(r_last) > 0:
                res = res + [ord(c) for c in r_last]

        return bytes(res).decode()
    
    def parse(self):
        gc.collect()
        try:
            req_data = self.client_socket.recv(4096).decode().strip()
            req_datas = req_data.split('\r\n')
            firstline = self._unquote(req_datas[0])
            lastline = self._unquote(req_datas[-1])
            self.path = firstline.split()[1]
            if len(lastline) > 0:
                params = lastline.split('&')
                for p in params:
                    k, v = p.split('=')
                    self.form[k] = v.strip('"')
        except Exception:
            print(EX_INFO)


# Response Class
class Response:   
    def __init__(self, socket=None):
        self.client_socket = socket
        self.response_data = None
    
    def make(self, data):
        firstline = 'HTTP/1.0 200 OK\r\n'
        header = 'Content-Type: application/jsonrequest\r\n'
        body = '\r\n%s' % json.dumps(data)
        self.response_data = firstline + header + body

    def send(self):
        if self.response_data:
            try:
                self.client_socket.write(self.response_data)
            except Exception:
                print(EX_INFO)
 

# mPython Board Class
class Board:
    def __init__(self):
        pass

    def _get_real_tag(self, raw_tag):
        real_tag = raw_tag
        raw_tag_lower = raw_tag.lower().strip()
        for tag_name in ['button_a', 
                         'button_b', 
                         'touchPad_P', 
                         'touchPad_Y', 
                         'touchPad_T', 
                         'touchPad_H', 
                         'touchPad_O', 
                         'touchPad_N']:
            real_tag_lower = tag_name.lower().replace('_', '')
            if real_tag_lower == raw_tag_lower:
                real_tag = tag_name
                return real_tag
        if raw_tag_lower.startswith('pin'):
            pin_name = 'MPythonPin'
            pin_mode = 'digital' if raw_tag_lower[3] == 'd' else 'analog'
            pin_num = raw_tag_lower[4:]
            real_tag = '%s_%s_%s' % (pin_name, pin_mode, pin_num)
        return real_tag

    def read(self, raw_tag):
        tag = self._get_real_tag(raw_tag)
        value = ''
        try:
            if tag in ['button_a', 
                       'button_b', 
                       'touchPad_P', 
                       'touchPad_Y', 
                       'touchPad_T', 
                       'touchPad_H', 
                       'touchPad_O', 
                       'touchPad_N', 
                       'light', 
                       'sound']:
                sensor = getattr(mpython, tag)
                method = 'read' if hasattr(sensor, 'read') else 'value'         
                value = '%d' % getattr(sensor, method)()
            elif tag == 'accelerometer':
                accelerometer = getattr(mpython, 'accelerometer')           
                value = '%f,%f,%f' % (accelerometer.get_x(), 
                                      accelerometer.get_y(), 
                                      accelerometer.get_z())
            elif tag.startswith('MPythonPin'):
                pname, pmode, pnum = tag.split('_')
                pfun = getattr(mpython, pname)
                n = int(pnum)
                if pmode == 'digital':
                    pin = pfun(n, 1)
                    value = '%d' % pin.read_digital()
                elif pmode == 'analog':
                    pin = pfun(n, 4)
                    value = '%d' % pin.read_analog()
        except Exception:
            print(EX_INFO)
        return ["VALUE", raw_tag, value]    
    
    def write(self, raw_tag, raw_value):
        tag = self._get_real_tag(raw_tag)
        value = raw_value.strip()
        try:
            if tag.startswith('rgb'):
                led = getattr(mpython, 'rgb')
                num = 0 if tag[3:] == '' else int(tag[3:])
                n = num if num < 3 and num >= 0 else 2
                r, g, b = value.split(',')          
                led[n] = tuple([int(r), int(g), int(b)])
                led.write()
            elif tag.startswith('display') or tag.startswith('oled'):
                oled = getattr(mpython, tag.strip())
                values = value.split(':', 1)
                method = values[0].strip()
                vdata = values[1].strip()
                if method.strip() == 'show':
                    content, x, y = vdata.split(':')
                    oled.DispChar(content, int(x.strip()), int(y.strip()))
                elif method == 'fill':
                    oled.fill(int(vdata))
                oled.show()
            elif tag.startswith('buzz'):
                bz = getattr(mpython, 'buzz')
                method = value.strip()
                if method.startswith('on'):
                    param = method.split(':', 1)[-1].strip()
                    freq = 500 if param == 'on' else int(param)
                    bz.on(freq) 
                elif method.startswith('off'):
                    bz.off()
            elif tag.startswith('MPythonPin'):
                pname, pmode, pnum = tag.split('_')
                pfun = getattr(mpython, pname)
                n = int(pnum)
                val = int(value)
                if pmode == 'digital':
                    pin = pfun(n, 2)
                    pin.write_digital(val)
                elif pmode == 'analog':
                    pin = pfun(n, 3)
                    pin.write_analog(val)
        except Exception:
            print(EX_INFO)
        return ["STORED", raw_tag, value]


# Http Server Class
class Server:
    def __init__(self):
        self.handlers = {}
        self.server_socket = None
        self.client_socket = None

    def _start_server(self, port=8888, accept_handler=None):
        self.stop()
        gc.collect()
        try:
            s = socket.socket()
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            ai = socket.getaddrinfo("0.0.0.0", port)
            server_addr = ai[0][-1]
            s.bind(server_addr)
            s.listen(5)
            if accept_handler:
                s.setsockopt(socket.SOL_SOCKET, 20, accept_handler)
            self.server_socket = s
            for i in (network.AP_IF, network.STA_IF):
                iface = network.WLAN(i)
                if iface.active():
                    print("%s%s:%d" % (SUC_INFO, iface.ifconfig()[0], port))
        except Exception:
            print(EX_INFO)
        return self.server_socket
   
    def start(self, port=8888):
        self._start_server(port, self.connect_client)

    def start_foreground(self, port=8888):
        socket = self._start_server(port, None)
        if socket:
            while True:
                self.connect_client(socket)

    def route(self, url):
        def wrapper(func):
            self.handlers[url] = func
            return func
        return wrapper
    
    def connect_client(self, socket):
        csock, caddr = socket.accept()
        self.client_socket = csock
        request = Request(csock)
        response = Response(csock)
        board = Board()

        try:
            self.process_data(request, response, board)
        except Exception:
            print(EX_INFO)
        finally:
            self.client_socket.close()
            csock.close()
    
    def process_data(self, request, response, board):
        request.parse()
        path = request.path
        if path:
            handler = self.get_handler(path)
            if handler:
                handler(request, response, board)
    
    def get_handler(self, path):
        if path in self.handlers.keys():
            return self.handlers[path]
        else:
            return None
    
    def stop(self):
        if self.server_socket:
            self.server_socket.close()
        if self.client_socket:
            self.client_socket.close()


appserver = Server()

@appserver.route('/getvalue')
def getValue(request, response, board):
    tag = request.form['tag']
    result = board.read(tag)
    response.make(result)
    response.send()

@appserver.route('/storeavalue')
def storeAValue(request, response, board):
    tag = request.form['tag']
    value = request.form['value']
    result = board.write(tag, value)
    response.make(result)
    response.send()

if __name__ == "__main__":
    appserver.start()