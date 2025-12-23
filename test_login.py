#!/usr/bin/env python3
"""
Test login process for DevScout with Enter key fallback
"""

import asyncio
import logging
import os
from playwright.async_api import async_playwright
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


async def test_login():
    """Test the login process"""
    headless = False  # Show browser for debugging

    async with async_playwright() as p:
        browser = await p.webkit.launch(headless=headless)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15"
        )
        page = await context.new_page()

        try:
            email = os.getenv("EMAIL", "test@example.com")
            password = os.getenv("PASSWORD", "test_password")

            logging.info("🚀 Testing login process...")

            # Navigate to DevScout
            await page.goto("https://devscout.app", wait_until="domcontentloaded")
            await page.wait_for_timeout(2000)

            # Click login button
            login_button = await page.wait_for_selector(
                'text="Cadastrar / Login"', timeout=10000
            )
            await login_button.click()
            await page.wait_for_timeout(3000)

            # Fill email
            email_input = await page.wait_for_selector(
                'input[type="email"], input[name="email"], input[placeholder*="email"]',
                timeout=10000,
            )
            await email_input.fill(email)
            logging.info("✅ Email filled")

            # Fill password
            password_input = await page.wait_for_selector(
                'input[type="password"], input[name="password"]', timeout=10000
            )
            await password_input.fill(password)
            logging.info("✅ Password filled")

            # Try submit button first
            submit_found = False
            try:
                submit_button = await page.wait_for_selector(
                    'button[type="submit"], button:has-text("Entrar"), button:has-text("Login")',
                    timeout=5000,
                )
                await submit_button.click()
                logging.info("✅ Clicked submit button")
                submit_found = True
            except:
                logging.info("❌ Submit button not found")

            if not submit_found:
                # Use Enter key instead
                logging.info("🔑 Using Enter key on password field...")
                await password_input.press("Enter")
                logging.info("✅ Pressed Enter key")

            # Wait for login to process
            await page.wait_for_timeout(5000)

            # Check if login successful
            current_url = page.url
            login_check = await page.query_selector('text="Cadastrar / Login"')

            if not login_check and "devscout.app" in current_url:
                logging.info("✅ Login successful!")
                await page.wait_for_timeout(2000)

                # Take screenshot of logged in state
                await page.screenshot(path="login_success.png")
                logging.info("📸 Success screenshot saved as 'login_success.png'")

            else:
                logging.error("❌ Login failed")

                # Take screenshot for debugging
                await page.screenshot(path="login_failed.png")
                logging.info("📸 Failure screenshot saved as 'login_failed.png'")

                # Check for error messages
                page_text = await page.inner_text("body")
                if "error" in page_text.lower() or "invalid" in page_text.lower():
                    logging.error("🚨 Found error message on page")

            await page.wait_for_timeout(3000)

        except Exception as e:
            logging.error(f"❌ Test failed: {e}")
            await page.screenshot(path="test_error.png")

        finally:
            await browser.close()


if __name__ == "__main__":
    asyncio.run(test_login())
