from selenium import webdriver
from selenium.webdriver.common.by import By

browser = webdriver.Chrome()
browser.get('http://www.weather.com.cn/html/province/guangdong.shtml')
areas = browser.find_elements(By.XPATH, '/html/body/div[3]/div[1]/div[2]/div/div/dl/dt/a')

print(type(areas))
print(areas)

area_text = [area.text for area in areas]

print(area_text)
