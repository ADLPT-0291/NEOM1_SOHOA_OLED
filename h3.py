#!/usr/bin/env python3
from pyA20.gpio import gpio
from pyA20.gpio import port
from threading import Timer
from time import sleep
from apscheduler.schedulers.background import BlockingScheduler, BackgroundScheduler
from datetime import datetime, timedelta
import pytz
import time
import serial  # Thư viện pyserial
from luma.core.interface.serial import i2c as luma_i2c
from luma.core.render import canvas
import subprocess
import json
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import urllib
import url
import khaibao
import requests
import configparser
import socket
import re
import os
import vlc
import random
import alsaaudio
import string
import signal
from urllib.parse import quote
from threading  import Thread
from datetime import datetime, timezone
#khai bao oled
from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
from PIL import Image, ImageDraw, ImageFont

gpio.init()
local_timezone = pytz.timezone('Asia/Ho_Chi_Minh') 
led_status = 203 #chan 7
watchdog = 20 # chan 29
led_connect = 21 # chan 31
kich_modul4g = 9 # chan 37
input_loa_L = 17 # chân 26
input_loa_R = 19 # chân 27
on_loa = 1 # chan 22 
congsuat_in = 18 # chan 28

phim_wifi = 6 # chan 12
mat_nguon = 0
mute = 2 # 13
#kich_nguon_sac = 16 # chan 18
gpio.setcfg(led_status, gpio.OUTPUT)
gpio.setcfg(watchdog, gpio.OUTPUT)
gpio.setcfg(led_connect, gpio.OUTPUT)
gpio.setcfg(kich_modul4g, gpio.OUTPUT)
gpio.setcfg(phim_wifi, gpio.INPUT)   #Configure PE11 as input
gpio.pullup(phim_wifi, gpio.PULLDOWN)    #Enable pull-down
gpio.setcfg(mat_nguon, gpio.INPUT)   #Configure PE11 as input
gpio.pullup(mat_nguon, gpio.PULLDOWN)    #Enable pull-down
gpio.output(kich_modul4g, 1)
gpio.output(watchdog, 0)
gpio.setcfg(mute, gpio.OUTPUT)

gpio.setcfg(on_loa, gpio.OUTPUT)
gpio.setcfg(input_loa_L, gpio.INPUT)   #Configure PE11 as input
gpio.pullup(input_loa_L, gpio.PULLDOWN)    #Enable pull-down
gpio.setcfg(input_loa_R, gpio.INPUT)   #Configure PE11 as input
gpio.pullup(input_loa_R, gpio.PULLDOWN)    #Enable pull-down
gpio.setcfg(congsuat_in, gpio.INPUT)   #Configure PE11 as input
gpio.pullup(congsuat_in, gpio.PULLDOWN)    #Enable pull-down





# Khởi tạo giờ, phút, giây ban đầu là 0
REMOTE_SERVER = "8.8.8.8"
hour = 0
minute = 0
second = 0
darkice_process = ''
darkice_cmd = ['darkice', '-c', '/etc/darkice.cfg']
# Đường dẫn đến tệp cấu hình của Darkice
CONFIG_FILE = "/etc/darkice.cfg"
# Tạo đối tượng ConfigParser
config = configparser.ConfigParser()
config.optionxform = lambda option: option
######### khai bao domain ##########
domainMqtt = url.domainMqtt
portMqtt = url.portMqtt
domainXacnhanketnoi = url.domainXacnhanketnoi
domainLogbantin = url.domainLogbantin
domainPing = url.domainPing
domainXacnhanketnoilai = url.domainXacnhanketnoilai
domainGuiLichPhat = url.domainGuiLichPhat
domainPingMatDien = url.domainPingMatDien
######## khai bao dia chi mqtt #####
id = khaibao.id
updatecode = khaibao.updatecode
trangthaiketnoi = khaibao.trangthaiketnoi
trangthaiplay = khaibao.trangthaiplay
trangthaivolume = khaibao.trangthaivolume
xacnhanketnoi = khaibao.xacnhanketnoi
dieukhienvolume = khaibao.dieukhienvolume
dieukhienplay = khaibao.dieukhienplay
yeucauguidulieu = khaibao.yeucauguidulieu
reset = khaibao.reset


####################################
MainBoard = 'M1_2024_V8.2'
phienban = "V2.3.0"
loiketnoi = 0
mabantinnhan = ''
kiemtraPlay = 0
demKiemtra = 0
data = ''
maxacthuc = ''
guidulieu = 0
ledConnectStatus = False
watchdogStatus = False
demRestartModul3g = 0
chedoRetartModul3g = False
demLoicallApiPing = 0
trangthaiguiApi = None
mangdangdung = ''
### khai bao nhap nhay wifi 
ledConnectStatus = 0
demnhapnhay = 0
demdung = 0
demnhanphim = 0
##### khai bao data do toc do mang speedtest #####
speedtest_upload = ''
speedtest_download = ''
speedtest_ping = ''
speedtest_ping_jitter = ''
### khai bao data ping ########
urldangphat = ''
tenchuongtrinh = ''
kieunguon = ''
thoiluong = ''
tennoidung = ''
diachingoidung = ''
kieuphat = ''
nguoitao = ''
taikhoantao = ''
# khai bao data api tinh #
userName = ''
password = '' 
madiaban = ''
tendiaban = ''
imel = ''
tenthietbi = ""
lat = ''
lng = ''
DichID = ''
TenDich = ''
MaNhaCungCap = ''
TenNhaCungCap = 'Gtech'
TenLoaiThietBi = 'Cụm loa truyền thanh'
NoiDungPhat = ''
TrangThaiHoatDong = 0
Status = "false"
khoaguidulieu = False
domainLoginTinh = ''
domainPingTinh = ''
domainLogTinh = ''

domainAddPlaylist = ''
domainDeletePlaylist = ''
Video = {"Index":"0", "Time": "", "MediaName": "", "AudioName": "", "Path": "", "Level": 0  }
ThoiDiemBatDau = 0
ThoiDiemKetThuc = 0
phatbantintinh = False
IdLichDangPhat = ''
DanhSachBanTinDung = []
BanTinKeTiep = []
ChuyenBanTin = False
Playing_ChuyenBai = False
IndexBanTinKeTiep = 0
PhatKhanCap = False
DataPhatKhanCap = {}
amluong = 30
LichPhatDangNhan = {}
version = "3"
TrangThaiKetNoi = '4G,-10dbm'
linkS3 = ''
ssid = "gtech-ip"
password = "123456789"
########
ChoPhatBanTinTinh = False
instance_amluong = vlc.Instance()
player_amluong = instance_amluong.media_player_new()
IdLichDangPhatNoiBo = ''
DungBanTinTinh = False
PhatBanTinNoiBo = False
Rssi = 0
TenNhaMang = None
MatDien = None
TrangThaiGuiMatDien = None
LoaiMang = ''
dbm = ''

##
file_path = 'lichphatTinh.json'
idBanTinTinhDangPhat = ''
idLichPhatTinhDangPhat = ''
thoiGianBatDauPhatTinh = None

status_loaL = 1
status_loaR = 1
status_congsuat = 1
docLoa = 0
demloi = 0

# Thiết lập mức âm lượng ban đầu và bước nhảy khi tăng hoặc giảm âm lượng
volume = 50
step = 5

# Khởi tạo màn hình OLED
serial_interface = luma_i2c(port=0, address=0x3C)
device = ssd1306(serial_interface)
width = device.width
height = device.height
# Tạo canvas
image = Image.new("1", (width, height))
draw = ImageDraw.Draw(image)
# Dùng font bitmap đơn giản
font = ImageFont.load_default()

# Hàm vẽ thanh bar
def draw_volume_bar(level):
  with canvas(device) as draw: 
    bar_length = int((width - 20) * level / 100)
    draw.rectangle((8, 23, width - 8, 37), outline=255)
    draw.rectangle((10, 25, 10 + bar_length, 35), outline=255, fill=255)
    # Vẽ chữ "Volume"
    font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSans.ttf", size=14)
    text_volume = "Volume"
    text_bbox = draw.textbbox((0, 0), text_volume, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    draw.text(((width - text_width) // 2, 5), text_volume, font=font, fill=255)
    # Vẽ số mức âm lượng ở dưới thanh bar
    font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSans.ttf", size=14)
    text_bbox = draw.textbbox((0,0), str(volume), font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    draw.text(((width - text_width) // 2, 40), str(volume), font=font, fill=255)

########### hien thi not connect ##########################
def show_not_connect():
  with canvas(device) as draw:
    font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeSans.ttf', 20)
    draw.rectangle((0, 0, 128, 64), outline=0, fill=0)
    draw.text((6, 23), "No Connect!", font=font, fill=1)

########## hien thị WELCOME ################ 
def show_ready():
  with canvas(device) as draw:
  
    font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeSans.ttf', 20)
    draw.rectangle((0, 0, 128, 64), outline=0, fill=0)
    draw.text((15, 23), "WELCOME", font=font, fill=1)

########## hien thị LOGO  ################ 
def show_logo():
  with canvas(device) as draw:
  
    font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeSans.ttf', 20)
    draw.rectangle((0, 0, 128, 64), outline=0, fill=0)
    draw.text((30, 23), "GTECH", font=font, fill=1)

########## hien thị Connecting... ################ 
def show_connecting():
  with canvas(device) as draw:
    font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeSans.ttf', 20)
    draw.rectangle((0, 0, 128, 64), outline=0, fill=0) 
    draw.text((0, 23), "Connecting...", font=font, fill=1)

########## hien thị stream ################ 
def show_stream():
  global second, minute, hour
    # Tạo chuỗi thời gian để hiển thị trên màn hình OLED
  #black_bitmap = Image.new('1', (device.width, device.height), 0)
  time_str ="{:02d}:{:02d}:{:02d}".format(hour, minute, second)
  with canvas(device) as draw:
    font_time = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeSans.ttf', 28)
    font = ImageFont.truetype("arial.ttf", 20)
    draw.text((0, 0), "64Kb/s", font=font, fill=255)
    draw.text((70, 0), 'Vol:'+ str(volume), font=font, fill=255)
    draw.text((8, 30), time_str, font=font_time, fill=1)

class RepeatedTimer(object):
  def __init__(self, interval, function, *args, **kwargs):
    self._timer     = None
    self.interval   = interval
    self.function   = function
    self.args       = args
    self.kwargs     = kwargs
    self.is_running = False
    self.start()
  def _run(self):
    self.is_running = False
    self.start()
    self.function(*self.args, **self.kwargs)
  def start(self):
    if not self.is_running:
      self._timer = Timer(self.interval, self._run)
      self._timer.start()
      self.is_running = True
  def stop(self):
    self._timer.cancel()
    self.is_running = False

def count_time_show_volume():
  global time_show_volume
  time_show_volume +=1

################# ham dieu khien volume ####################
def setVolume(volume):
  # Khởi tạo mixer
  mixer = alsaaudio.Mixer('Mic1 Boost', cardindex=0)
  # Đặt âm lượng
  mixer.setvolume(int(volume))
  current_volume = mixer.getvolume()[0]
############################################################

def count_time():
  global second, minute, hour
  start_time = datetime.strptime(start_time_str, "%a, %d %b %Y %H:%M:%S %z")
  # Tính thời gian đến hiện tại
  elapsed_time = datetime.now(timezone.utc) - start_time
  second = elapsed_time.seconds
  hour, remainder = divmod(second, 3600)
  minute, second = divmod(remainder, 60)

def get_darkice_status_ping():
  global start_time_str
  # Đọc nội dung của tệp cấu hình
  config.read(CONFIG_FILE)
  # Lấy giá trị các trường thông tin
  server_host = config['icecast2-0']['server']
  server_port = config['icecast2-0']['port']
  mount_point = config['icecast2-0']['mountPoint']
  
  # Gửi yêu cầu HTTP GET đến Icecast để lấy trạng thái
  icecast_status_url = 'http://'+server_host+':'+server_port+'/status-json.xsl'
  try:
    response = requests.get(icecast_status_url)
    # Kiểm tra xem phản hồi có chứa thông tin của DarkIce không
    if response.status_code == 200:  # 200 là mã phản hồi HTTP thành công
      icecast_status = response.json()
      if icecast_status['icestats'].get('source') is not None:
        if isinstance(icecast_status['icestats']['source'], dict):
        # Xử lý khi có 1 source đang stream
          source = icecast_status['icestats']['source']
          if source['server_name'] == mount_point:
            # if start_time_str == '':
            start_time_str = source['stream_start']
            return True
          else:
            return False
        elif isinstance(icecast_status['icestats']['source'], list):
        # Xử lý khi có 2 source trở lên đang stream
          for source in icecast_status['icestats']['source']:
            if source['server_name'] == mount_point:
              # if start_time_str == '':
              start_time_str = source['stream_start']
              return True
            else:
              return False
        else:
        # Xử lý khi không có source nào đang stream
          return False
      else:
        return False
    else:
      return False
  except requests.exceptions.RequestException:
    return False
    

def get_darkice_status():
    cmd = 'pgrep darkice'
    try:
        result = subprocess.check_output(cmd, shell=True)
        return True
    except subprocess.CalledProcessError:
        return False

def start_darkice():   
    global trangthaiplay, led_status,playStream
    # start darkice stream
    subprocess.Popen(['darkice'])
    show_connecting()
    time.sleep(1)
    if get_darkice_status_ping():
      playStream = 1
      showStream.start()
      time.sleep(0.5) 
      countTime.start()
      client.publish(trangthaiplay,"play")
      gpio.output(led_status,True)

def stop_darkice():
    global last_start, playStream, trangthaiplay, led_status, second, minute, hour, start_time_str
    # stop darkice stream
    playStream = 0
    client.publish(trangthaiplay,"stop")
    gpio.output(led_status,False)
    showStream.stop()
    countTime.stop()
    last_start = False
    time.sleep(0.5) 
    show_ready()
    start_time_str = ''
    second = 0
    minute = 0
    hour = 0
    for proc in subprocess.Popen(['pgrep', '-f', 'darkice'], stdout=subprocess.PIPE).stdout:
        pid = int(proc.decode())
        os.kill(pid, signal.SIGTERM)

############# ham call api xac nhan ket noi #################
def api_xacnhanketnoi(data):
  global trangthaiguiApi, userName, password, domainLoginTinh, domainPingTinh, domainLogTinh, imel, tenthietbi, madiaban, tendiaban, lat, lng, Status, Video, khoaguidulieu
  try:
    responsePingtest = requests.post(domainXacnhanketnoi, json = data)
    jsonResponse = responsePingtest.json()
    if(jsonResponse['success'] == True):
      # dieu khien volume #
      setVolume(jsonResponse['data']['data']['volume'])
       # Đọc nội dung của tệp cấu hình
      config.read(CONFIG_FILE)
      # Thay đổi giá trị input
      config.set("input", "device", jsonResponse['data']['data']['deviceinput'])
      config.set("input", "channel", jsonResponse['data']['data']['channel'])
      config.set("icecast2-0", "bitrate", jsonResponse['data']['data']['bitrate'])
      config.set("icecast2-0", "server", jsonResponse['data']['data']['serverstream'])
      config.set("icecast2-0", "port", jsonResponse['data']['data']['portstream'])
      config.set("icecast2-0", "password", jsonResponse['data']['data']['password'])
      config.set("icecast2-0", "name", jsonResponse['data']['data']['nameStream'])
      config.set("icecast2-0", "mountPoint", jsonResponse['data']['data']['mountPoint'])
      # Ghi lại nội dung vào tệp cấu hình
      with open(CONFIG_FILE, "w") as configfile:
        config.write(configfile)
      # dieu khien play #
      if(jsonResponse['data']['data']['statusPlay'] == 'play'):   
        if(jsonResponse['data']['data']['deviceId'] == id):  
         for proc in subprocess.Popen(['pgrep', '-f', 'darkice'], stdout=subprocess.PIPE).stdout:
            pid = int(proc.decode())
            os.kill(pid, signal.SIGTERM)   
         start_darkice() 
      else:
        stop_darkice()
  except:
    print('loi xac nhan ket noi')

############### Blinl led connect ###########################
def ledConnectNhapnhay():
    global ledConnectStatus
    gpio.output(led_connect,not ledConnectStatus) 
    ledConnectStatus = not ledConnectStatus
#############################################################

########## ham kich sung modul watchdog #####################
def watchdogStart():
  global watchdogStatus
  gpio.output(watchdog,not watchdogStatus)
  watchdogStatus = not watchdogStatus
############################################################

###### led connect nhap nhay canh bao call Api loi #########
def ledConnectNhapnhayLoiCallApi():
    global ledConnectStatus
    gpio.output(led_connect,not ledConnectStatus) 
    ledConnectStatus = not ledConnectStatus
############################################################

############ khoi dong lai modul 3g ########################
def retartModul3g():
    global demRestartModul3g
    gpio.output(kich_modul4g,0) 
    time.sleep(20)
    gpio.output(kich_modul4g,1) 
    demRestartModul3g = 0

# gửi trạng thái mất điện
def api_TrangThaiMatDien(value, ThoiGian):
    try:
      data = {
        'id': id,
        'MatDien': value,
        'ThoiGianMatDien': ThoiGian
      }
      responsePing = requests.post(domainPingMatDien, json = data, timeout=5)
      trave = responsePing.json()
      return trave['success']
     
    except Exception as e:    
       pass

######### get dia chi ip ###################
def get_ip_address():
 ip_address = ''
 s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
 s.connect(("8.8.8.8",80))
 ip_address = s.getsockname()[0]
 s.close()
 return ip_address

def on_message(client, userdata, msg):
    print(f"📩 Nhận từ topic {msg.topic}: {msg.payload.decode()}")


#################### connect MQTT ##########################
def on_connect(client, userdata, flags, rc):
    global dbm, Rssi, TenNhaMang, TrangThaiKetNoi, demLoicallApiPing, yeucauguidulieu, updatecode, dieukhienvolume, dieukhienplay, maxacthuc, chedoRetartModul3g, demRestartModul3g, demLoicallApiPing
    if rc==0:
        print("connected OK Returned code=",rc)
        demLoicallApiPing = 0
        chedoRetartModul3g = False
        demRestartModul3g = 0      
        #Flag to indicate success
        client.subscribe(dieukhienvolume) 
        client.subscribe(updatecode)
        client.subscribe(dieukhienplay)
        client.subscribe(yeucauguidulieu)
        client.subscribe(reset)
        client.connected_flag=True   
        nhapnhatLedConnect.stop()
        nhapnhatLedConnectCallApiloi.stop()
        gpio.output(led_connect,True)
        show_ready()
        time.sleep(3)
        show_logo()
        """ call API xac nhan ket noi """
       # ip = requests.get('https://api.ipify.org').text
        dataXacnhanketnoi = {
          'xacnhanketnoi': xacnhanketnoi,
          'ip': get_ip_address(),
          'phienban': phienban,   
        }
        api_xacnhanketnoi(dataXacnhanketnoi)        
    else:
        print("Bad connection Returned code=",rc)
        client.bad_connection_flag=True
###########################################################

run_main=False
run_flag=True


client = mqtt.Client()    #create new instance

#client.on_log=on_log #client logging
client.connected_flag=False #create flags
client.bad_connection_flag=False #
client.retry_count=0 #
nhapnhatLedConnect = RepeatedTimer(1, ledConnectNhapnhay)
nhapnhatLedConnectCallApiloi = RepeatedTimer(0.2, ledConnectNhapnhayLoiCallApi)
nhapnhatLedConnectCallApiloi.stop()
watchdog_start = RepeatedTimer(1, watchdogStart)
client.on_connect=on_connect        #attach function to callback
client.will_set("device/offline", payload=id, qos=1, retain=False)
client.on_message = on_message
countTime = RepeatedTimer(1, count_time)
showStream = RepeatedTimer(1, show_stream)
countVolume = RepeatedTimer(1, count_time_show_volume)
countVolume.stop()
showStream.stop()
countTime.stop()



while run_flag:
    while not client.connected_flag and client.retry_count<3:
        count=0 
        run_main=False
        try:
            print("connecting ",domainMqtt)         
            client.connect(domainMqtt,portMqtt,60)      
            break #break from while loop
        except:           
            # kiểm soát mất diện
            if gpio.input(mat_nguon) == 0:     
                if TrangThaiGuiMatDien == True or TrangThaiGuiMatDien == None:   
                    ThoiGianMatDien = time.time()  
                    data_object = {
                        "type": "mat-dien",
                        "ThoiGianMatDien": int(ThoiGianMatDien),
                    }
                    json_data = json.dumps(data_object)       
                    client.publish(trangthaiplay,json_data)
                    ketquaMatdien = api_TrangThaiMatDien(False,  ThoiGianMatDien)                               
                    if ketquaMatdien == True:
                        TrangThaiGuiMatDien = False  
             
                # có điện
                else:     
                    if TrangThaiGuiMatDien == False or TrangThaiGuiMatDien == None:        
                        ThoiGianMatDien = time.time()  
                        data_object = {
                            "type": "co-dien",
                            "ThoiGianMatDien": int(ThoiGianMatDien),
                        }
                        json_data = json.dumps(data_object)       
                        client.publish(trangthaiplay,json_data)
                        ketquaMatdien = api_TrangThaiMatDien(True, ThoiGianMatDien)                     
                        if ketquaMatdien == True:
                            TrangThaiGuiMatDien = True  
            print("connection attempt failed will retry")         
            # nhapnhatLedConnect.start()
            # nhapnhatLedConnectCallApiloi.stop()
            client.retry_count+=1         
            if(client.retry_count == 2):
              retartModul3g()
              print('khoi dong lai modul lan dau...')
            #if client.retry_count>3:
                #print('thoat')
                #run_flag=False
    if not run_main:   
        client.loop_start()
        while True:
           
            # kiểm soát mất diện
            if gpio.input(mat_nguon) == 0:     
                if TrangThaiGuiMatDien == True or TrangThaiGuiMatDien == None:   
                    ThoiGianMatDien = time.time()  
                    data_object = {
                        "type": "mat-dien",
                        "ThoiGianMatDien": int(ThoiGianMatDien),
                    }
                    json_data = json.dumps(data_object)       
                    client.publish(trangthaiplay,json_data)
                    ketquaMatdien = api_TrangThaiMatDien(False,  ThoiGianMatDien)                    
                    if ketquaMatdien == True:
                        TrangThaiGuiMatDien = False  
             
                # có điện
                else:     
                    if TrangThaiGuiMatDien == False or TrangThaiGuiMatDien == None:        
                        ThoiGianMatDien = time.time()  
                        data_object = {
                            "type": "co-dien",
                            "ThoiGianMatDien": int(ThoiGianMatDien),
                        }
                        json_data = json.dumps(data_object)       
                        client.publish(trangthaiplay,json_data)
                        ketquaMatdien = api_TrangThaiMatDien(True,  ThoiGianMatDien)                      
                        if ketquaMatdien == True:
                            TrangThaiGuiMatDien = True  
            if client.connected_flag: #wait for connack
                client.retry_count=0 #reset counter
                run_main=True
                break
            # if count>6 or client.bad_connection_flag: #don't wait forever
            #   demRestartModul3g+=1
            #   if demRestartModul3g >= 900:                  
            #     print('reset lai modul 3g..')
            #     retartModul3g()                  
            # time.sleep(1)
            count+=1
    # if run_main: 
    #     try:          
    #         # print('trạng thái:', player.get_state_2())        
    #         if(PhatKhanCap == True):
    #           PhatKhanCapBanTinTinh(DataPhatKhanCap)
    #         if(ChuyenBanTin == True):
    #           phatbantinKetiepTrongDanhSach(BanTinKeTiep)
    #         time.sleep(1)           
    #     except(KeyboardInterrupt):
    #         print("keyboard Interrupt so ending")
    #         DungBanTin()
    #         os._exit(0)
    #         #run_flag=False
    # Mất điện
    if gpio.input(mat_nguon) == 0:     
        if TrangThaiGuiMatDien == True or TrangThaiGuiMatDien == None:   
          ThoiGianMatDien = time.time()  
          data_object = {
              "type": "mat-dien",
              "ThoiGianMatDien": int(ThoiGianMatDien),
          }
          json_data = json.dumps(data_object)           
          client.publish(trangthaiplay,json_data)       
          ketquaMatdien = api_TrangThaiMatDien(False,  ThoiGianMatDien)   
          if ketquaMatdien == True:
             TrangThaiGuiMatDien = False  
             
    # có điện
    else:     
        if TrangThaiGuiMatDien == False or TrangThaiGuiMatDien == None:        
          ThoiGianMatDien = time.time()  
          data_object = {
              "type": "co-dien",
              "ThoiGianMatDien": int(ThoiGianMatDien),
          }
          json_data = json.dumps(data_object)               
          client.publish(trangthaiplay,json_data)       
          ketquaMatdien = api_TrangThaiMatDien(True,  ThoiGianMatDien)        
          if ketquaMatdien == True:
             TrangThaiGuiMatDien = True       
    # if gpio.input(phim_wifi) == 1:
    #   KiemTraPhim()
    
print("quitting")
# client.disconnect()
# client.loop_stop()        
            