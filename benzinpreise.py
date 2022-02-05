from selenium import webdriver 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from influxdb import InfluxDBClient

path = "C:/Users/Alexander/Downloads/chromedriver_win32/chromedriver.exe"
driver = webdriver.Chrome(path)

driver.get("https://ich-tanke.de/tankstellen/super-e5/umkreis/papenburg/")


tankstellen = driver.find_elements_by_xpath("//*[starts-with(@id, 'tankstelle-')]")

preis_list = []
firma_list = []

for tankstelle in tankstellen:
    firmen = tankstelle.find_elements_by_tag_name("h4")
    preise = tankstelle.find_elements_by_class_name("zahl")
    for firma in firmen:
        firma = tankstelle.find_element_by_tag_name("h4")
        preis = tankstelle.find_element_by_class_name("zahl")
        preis_list.append(preis)
        firma_list.append(firma)

client = client = InfluxDBClient(host='192.168.2.109', port=8086, username='alx', password='123susiHE', ssl=False, verify_ssl=True)
client.switch_database("benzinpreise")

json_body = [
    {
            "measurement": "benzinpreis",
            "tags": {
                "website": "ich-tanke.de",
            },
            "time": "2009-11-10T23:00:00Z",
            "fields": {
                "preis": preis_list,
                "firma": firma_list
            }
        }
]

client.write_points(json_body)


