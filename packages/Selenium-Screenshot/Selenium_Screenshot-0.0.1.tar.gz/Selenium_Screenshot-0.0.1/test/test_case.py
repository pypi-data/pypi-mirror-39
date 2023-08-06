from Selenium_Screenshot.Full_ScreenShot import Screenshot
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


ob=Screenshot.Screenshot()
chromedriver = "chromedriver.exe"
os.environ["webdriver.chrome.driver"] = chromedriver
# PROXY_HOST = '162.248.6.107'
# PROXY_PORT = 80
# PROXY_USER = ''
# PROXY_PASS = ''
#
# manifest_json = """
#            {
#                "version": "1.0.0",
#                "manifest_version": 2,
#                "name": "Chrome Proxy",
#                "permissions": [
#                    "proxy",
#                    "tabs",
#                    "unlimitedStorage",
#                    "storage",
#                    "<all_urls>",
#                    "webRequest",
#                    "webRequestBlocking"
#                ],
#                "background": {
#                    "scripts": ["background.js"]
#                },
#                "minimum_chrome_version":"22.0.0"
#            }"""
# background_js = """
# var config = {
#         mode: "fixed_servers",
#         rules: {
#           singleProxy: {
#             scheme: "http",
#             host: "%s",
#             port: parseInt(%s)
#           },
#           bypassList: ["localhost"]
#         }
#       };
#
# chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});
#
# function callbackFn(details) {
#     return {
#         authCredentials: {
#             username: "%s",
#             password: "%s"
#         }
#     };
# }
#
# chrome.webRequest.onAuthRequired.addListener(
#             callbackFn,
#             {urls: ["<all_urls>"]},
#             ['blocking']
# );
# """ % (PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS)
options = Options()
# pluginfile = 'proxy_auth_plugin.zip'
# with zipfile.ZipFile(pluginfile, 'w') as zp:
#     zp.writestr("manifest.json", manifest_json)
#     zp.writestr("background.js", background_js)
# options.add_extension(pluginfile)
options.add_argument('--disable-gpu')
driver = webdriver.Chrome(chromedriver, chrome_options=options)
# print('Running URL  : '+ url)
driver.get('https://www.google.com')
# time.sleep(4)
logo=driver.find_element_by_id('hplogo')
url=ob.Get_element(driver,logo)
print(url)
