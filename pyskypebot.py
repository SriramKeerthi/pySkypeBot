import time
import sys, getopt
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait

driver = None

def launch():
  print("Loading...")
  global driver
  # driver = webdriver.PhantomJS("phantomjs-2.0.0-windows\\bin\\phantomjs.exe")
  driver = webdriver.Chrome()
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


def main(argv):
  try:
    userName = ""
    password = ""
    launch()
    signIn(userName, password)
    signOut()
  finally:
    quit()
