from playwright.sync_api import sync_playwright
with sync_playwright() as p:
   browser= p.chromium.launch(headless=False ,slow_mo=700)
   page = browser.new_page()
   page.goto("https://www.demoblaze.com")