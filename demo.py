#!/usr/bin/env python3
"""
Demo script to show how the DevScout automation works without real credentials
"""

import asyncio
import logging
from playwright.async_api import async_playwright

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


async def demo_navigate_only():
    """Demo: Just navigate to DevScout to show it works"""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  # Show browser for demo
        context = await browser.new_context()
        page = await context.new_page()

        try:
            logging.info("🚀 Demo: Navigating to DevScout...")
            await page.goto("https://devscout.app", wait_until="domcontentloaded")

            logging.info("✅ Successfully loaded DevScout homepage!")

            # Take a screenshot
            await page.screenshot(path="devscout_homepage.png")
            logging.info("📸 Screenshot saved as 'devscout_homepage.png'")

            # Look for key elements
            login_button = await page.query_selector('text="Cadastrar / Login"')
            if login_button:
                logging.info("🔍 Found login button - user not logged in")
            else:
                logging.info("🔍 Login button not found - user might be logged in")

            # Wait a bit to see the page
            await page.wait_for_timeout(5000)

        except Exception as e:
            logging.error(f"❌ Demo failed: {e}")

        finally:
            await browser.close()
            logging.info("🏁 Demo completed")


async def demo_find_buttons():
    """Demo: Try to find the buttons we need to click"""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        try:
            await page.goto("https://devscout.app", wait_until="domcontentloaded")
            await page.wait_for_timeout(2000)

            logging.info("🔍 Looking for 'procurar vagas' button...")

            # Try to find the button
            button_found = False
            selectors = [
                'button:has-text("procurar vagas")',
                'button:has-text("Procurar Vagas")',
                'button:has-text("PROCURAR VAGAS")',
                '[data-testid*="procurar"]',
                'a:has-text("procurar vagas")',
            ]

            for selector in selectors:
                try:
                    button = await page.wait_for_selector(selector, timeout=2000)
                    if button:
                        logging.info(f"✅ Found button with selector: {selector}")
                        button_found = True
                        break
                except:
                    continue

            if not button_found:
                logging.info("❌ 'procurar vagas' button not found (might need login)")

                # Let's try clicking login to see what happens
                try:
                    login_btn = await page.wait_for_selector(
                        'text="Cadastrar / Login"', timeout=3000
                    )
                    if login_btn:
                        logging.info(
                            "🔍 Found login button - clicking to see the login flow..."
                        )
                        await login_btn.click()
                        await page.wait_for_timeout(3000)

                        # Take screenshot of login form
                        await page.screenshot(path="devscout_login.png")
                        logging.info(
                            "📸 Login screenshot saved as 'devscout_login.png'"
                        )

                except Exception as e:
                    logging.info(f"Could not click login button: {e}")

            # Wait a bit to see the page
            await page.wait_for_timeout(5000)

        except Exception as e:
            logging.error(f"❌ Button demo failed: {e}")

        finally:
            await browser.close()
            logging.info("🏁 Button demo completed")


def main():
    """Run demo"""
    print("🎯 DevScout Automation Demo")
    print("=" * 40)
    print("This demo shows:")
    print("1. Navigation to DevScout")
    print("2. Finding key elements")
    print("3. What the automation would interact with")
    print()

    choice = input(
        "Choose demo:\n1. Navigate only\n2. Navigate + find buttons\nEnter choice (1 or 2): "
    )

    if choice == "1":
        asyncio.run(demo_navigate_only())
    elif choice == "2":
        asyncio.run(demo_find_buttons())
    else:
        print("Running default demo (navigate only)...")
        asyncio.run(demo_navigate_only())


if __name__ == "__main__":
    main()
