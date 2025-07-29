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
import string
from urllib.parse import quote

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
client.on_connect=on_connect        #attach function to callback
client.will_set("device/offline", payload=id, qos=1, retain=False)
client.on_message = on_message



while run_flag:
    while not client.connected_flag and client.retry_count<3:
        count=0 
        run_main=False
        try:
            print("connecting ",domainMqtt)         
            client.connect(domainMqtt,portMqtt,60)  
            client.loop_forever()    
            break #break from while loop
        except:           
            print("connection attempt failed will retry")         
            client.retry_count+=1         
            