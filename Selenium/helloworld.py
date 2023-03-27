from selenium import webdriver
from PIL import Image
import time
import sys
import traceback
import os

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')

driver = webdriver.Chrome(options=chrome_options)

capabilities = {
    "build" : os.getenv("LT_BUILD_NAME"),
    "name" : "BAH HW Test",
    "platform" : "Windows 10",
    "browserName" : "Chrome",
    "version" : "88.0",
    "resolution" : "1920x1080",
    "tunnel" : True
}

try:
    driver.get("http://bahttleship:8081/")
    assert "no such file or directory" not in driver.page_source
    time.sleep(10)
    #Test correct index page has loaded
    print("Selenium Test Started")
    print("")
    assert "Hello BAH - HoH 23-1" in driver.title
    t1url = driver.current_url
    print("Testing @ " + t1url)
    t1title = driver.title
    print("Page Title: " + t1title)
    driver.save_screenshot('s1.png')
    screenshot = Image.open('s1.png')
    assert "Booz | Allen | Hamilton" in driver.page_source
    #screenshot.show() #commented for CLI run-time

    #Test link & navigate to 2nd test element
    driver.find_element("id", "play").click()
    time.sleep(10)
    assert "http://bahttleship:8081/game.html" in driver.current_url    
    print(t1url + " --- PASS")
    print("")

    #Test game page has loaded and verify script sources
    t2url = driver.current_url
    print("Testing @ " + t2url)
    t2title = driver.title
    print("Page Title: " + t2title)
    driver.save_screenshot('s2.png')
    screenshot2 = Image.open('s2.png')
    #screenshot2.show() #commented for CLI run-time
    version = driver.find_element("id", "version").text
    print("Current Version Info: " + version)
    assert "//cdn.jsdelivr.net/npm/phaser@3.55.1/dist/phaser.min.js" in driver.page_source
    assert "/socket.io/socket.io.js" in driver.page_source
    assert "js/game.js" in driver.page_source
    print(t2url + " --- PASS")
    print("")
    
    #Wrap Up
    print("Selenium Test Complete - Test Pass")

except AssertionError:
    print("Assertion Error:")
    traceback.print_exc()
    sys.exit(1)

finally:
    driver.quit()