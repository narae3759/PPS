import asyncio
import time
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        # 웹페이지로 이동
        await page.goto('https://www.naver.com')
        
        # 검색어 입력
        css = '#search-btn'

        await page.locator("#query").fill("python")
        await page.locator('#search-btn').click()
        await page.wait_for_load_state('load')

        # await page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
        await page.keyboard.press("PageDown")

        # 스크린샷 캡처
        await asyncio.sleep(1)  # 1초 대기
        await page.screenshot(path='screenshot.png')

        # 웹페이지 HTML 가져오기
        html_content = await page.content()
        # print(html_content)

        await browser.close()

# 비동기 함수 실행
asyncio.run(main())
