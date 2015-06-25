import argparse
import time
import sys, getopt
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys

driver = None

def launch():
  print("Loading...")
  global driver
  driver = webdriver.PhantomJS("phantomjs-2.0.0-windows\\bin\\phantomjs.exe")
  driver.set_window_size(1024, 768)
  # driver = webdriver.Chrome()
  driver.get('https://web.skype.com/')
  print("Loaded Skype!")

def signIn(userName, password):
  print("Signing in...")
  userNameField = driver.find_element_by_id("username")
  userNameField.clear()
  userNameField.send_keys(userName)
  passwordField = driver.find_element_by_id("password")
  passwordField.clear()
  passwordField.send_keys(password)
  passwordField.submit()
  WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CLASS_NAME,'summary')))
  WebDriverWait(driver, 30).until_not(EC.visibility_of_element_located((By.CLASS_NAME,'shellSplashContent')))
  print("Signed In!")

def signOut():
  print("Signing out...")
  if not driver.find_element_by_class_name("signOut").is_displayed():
    WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CLASS_NAME,'summary'))).click()
  WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CLASS_NAME,'signOut'))).click()
  print("Signed Out!")

def quit():
  print("Quitting...")
  driver.quit()

def recents():
  return driver.find_elements_by_tag_name("swx-recent-item")

def main(args):
  try:
    launch()
    signIn(args.username, args.password)
    signOut()
  except:
    print("Something went wrong")
  finally:
    quit()

def sendMessageToSelected(message):
  element = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.TAG_NAME,'swx-textarea')))
  element = element.find_element_by_tag_name("textarea")
  element.click()
  element.clear()
  element.send_keys(message)
  element.send_keys(Keys.ENTER)

def sendMessage(tileName, message):
  recent(tileName).click()
  sendMessageToSelected(message)

def getTileName(element):
  return element.find_element_by_class_name("tileName").text

def recent(tileName):
  for recentTile in recents():
    if getTileName(recentTile) == tileName:
      return recentTile

if __name__ == "__main__":
  print("Starting up...")
  parser = argparse.ArgumentParser(description='pySkypeBot: Python Skype Bot')
  parser.add_argument('-u', '--username', help='Skype User Name')
  parser.add_argument('-p', '--password', help='Skype Password')
  main(parser.parse_args())
