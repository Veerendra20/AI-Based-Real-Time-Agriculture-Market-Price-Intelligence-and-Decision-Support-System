import asyncio
from playwright.async_api import async_playwright
import time

async def capture_react_mirrors():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.set_viewport_size({"width": 1280, "height": 900})
        
        await page.goto("http://localhost:8501")
        time.sleep(3) # Wait for initial load
        
        # Capture Market Compare
        await page.locator('text="Market Compare"').click()
        time.sleep(2)
        await page.screenshot(path="market_compare_react_mirror.png")
        
        # Capture Price Prediction
        await page.locator('text="Price Prediction"').click()
        time.sleep(2)
        await page.screenshot(path="price_prediction_react_mirror.png")
        
        # Capture Fertilizers
        await page.locator('text="Fertilizers"').click()
        time.sleep(2)
        await page.screenshot(path="fertilizers_react_mirror.png")
        
        await browser.close()
        print("Screenshots captured successfully.")

asyncio.run(capture_react_mirrors())
