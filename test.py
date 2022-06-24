import qrcode
import hashlib

def create_qrcode(message,filename):
    img =qrcode.make(message)
    img.save(filename)

cmd = "nmap -sn 127.0.0.1 -oA tmp/Ping_scan_127.0.0.1_20220623153338"
hs = hashlib.md5(cmd.encode()).hexdigest()
filename = f"static/images/qrcode/{hs}.png"
create_qrcode(cmd,filename)