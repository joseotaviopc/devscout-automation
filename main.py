import asyncio
import logging
import os
from playwright.async_api import async_playwright
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("devscout.log"), logging.StreamHandler()],
)


class DevScoutAutomation:
    def __init__(self):
        self.email = os.getenv("EMAIL")
        self.password = os.getenv("PASSWORD")
        self.headless = os.getenv("HEADLESS", "true").lower() == "true"
        self.base_url = "https://devscout.app"

        if not self.email or not self.password:
            raise ValueError("EMAIL and PASSWORD must be set in environment variables")

    async def setup_browser(self):
        """Initialize browser context"""
        self.playwright = await async_playwright().start()

        browser_options = {
            "headless": self.headless,
            "args": [
                "--no-sandbox",
                "--disable-blink-features=AutomationControlled",
                "--disable-dev-shm-usage",
            ],
        }

        self.browser = await self.playwright.webkit.launch(**browser_options)
        self.context = await self.browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        )
        self.page = await self.context.new_page()

        logging.info("Browser setup completed")

    async def navigate_to_site(self):
        """Navigate to DevScout website"""
        try:
            logging.info(f"Navigating to {self.base_url}")
            await self.page.goto(self.base_url, wait_until="domcontentloaded")
            await self.page.wait_for_timeout(2000)  # Allow page to load
            logging.info("Successfully navigated to DevScout")
            return True
        except Exception as e:
            logging.error(f"Failed to navigate to DevScout: {e}")
            return False

    async def check_login_status(self):
        """Check if user is already logged in"""
        try:
            # Look for login/signup buttons - if present, user is not logged in
            login_button = await self.page.query_selector('text="Cadastrar / Login"')
            if login_button:
                logging.info("User not logged in - login required")
                return False
            else:
                logging.info("User appears to be logged in")
                return True
        except Exception as e:
            logging.error(f"Error checking login status: {e}")
            return False

    async def login(self):
        """Handle login process"""
        try:
            logging.info("Starting login process")

            # Click login button
            login_button = await self.page.wait_for_selector(
                'text="Cadastrar / Login"', timeout=10000
            )
            await login_button.click()

            # Wait for login form to appear
            await self.page.wait_for_timeout(2000)

            # Look for email input - try multiple selectors
            email_input = await self.page.wait_for_selector(
                'input[type="email"], input[name="email"], input[placeholder*="email"]',
                timeout=10000,
            )
            await email_input.fill(self.email)

            # Look for password input
            password_input = await self.page.wait_for_selector(
                'input[type="password"], input[name="password"]', timeout=10000
            )
            await password_input.fill(self.password)
            await password_input.press("Enter")

            # Try to find and click submit button first
            # try:
            #     submit_button = await self.page.wait_for_selector(
            #         'button[type="submit"], button:has-text("Entrar"), button:has-text("Login")',
            #         timeout=5000,
            #     )
            #     await submit_button.click()
            #     logging.info("Clicked submit button")
            # except:
            #     # If button not found, use Enter key on password field
            #     logging.info(
            #         "Submit button not found, using Enter key on password field"
            #     )
                

            # Wait for login to complete
            await self.page.wait_for_timeout(3000)

            # Check if login was successful
            if await self.check_login_status():
                logging.info("Login successful")
                return True
            else:
                logging.error("Login failed")
                return False

        except Exception as e:
            logging.error(f"Login error: {e}")
            return False

    async def _fallback_email_login(self):
        """Fallback to email/password login if Google login not available"""
        try:
            logging.info("Attempting fallback to email/password login")

            # Look for email input
            email_input = await self.page.wait_for_selector(
                'input[type="email"], input[name="email"], input[placeholder*="email"]',
                timeout=10000,
            )
            await email_input.fill(self.email)

            # Look for password input
            password_input = await self.page.wait_for_selector(
                'input[type="password"], input[name="password"]', timeout=10000
            )
            await password_input.fill(self.password)

            # Click login/submit button
            submit_button = await self.page.wait_for_selector(
                'button[type="submit"], button:has-text("Entrar"), button:has-text("Login")',
                timeout=10000,
            )
            await submit_button.click()

            # Wait for login to complete
            await self.page.wait_for_timeout(3000)

            # Check if login was successful
            if await self.check_login_status():
                logging.info("Email login successful")
                return True
            else:
                logging.error("Email login failed")
                return False

        except Exception as e:
            logging.error(f"Fallback login error: {e}")
            return False

        except Exception as e:
            logging.error(f"Login error: {e}")
            return False

    async def find_and_click_procurar_vagas(self):
        """Find and click the 'procurar vagas' button"""
        try:
            logging.info("Looking for 'procurar vagas' button")

            # Try multiple selectors to find the button
            selectors = [
                'button:has-text("procurar vagas")',
                'button:has-text("Procurar Vagas")',
                'button:has-text("PROCURAR VAGAS")',
                '[data-testid*="procurar"]',
                'a:has-text("procurar vagas")',
            ]

            button = None
            for selector in selectors:
                try:
                    button = await self.page.wait_for_selector(selector, timeout=5000)
                    if button:
                        logging.info(f"Found button with selector: {selector}")
                        break
                except:
                    continue

            if not button:
                logging.error("Could not find 'procurar vagas' button")
                return False

            await button.click()
            logging.info("Clicked 'procurar vagas' button")
            return True

        except Exception as e:
            logging.error(f"Error clicking 'procurar vagas' button: {e}")
            return False

    async def wait_for_modal_and_check_vagas(self):
        """Wait for modal to appear and check vagas count"""
        try:
            logging.info("Waiting for modal to appear")

            # Wait for modal - try multiple selectors
            modal_selectors = [
                '[role="dialog"]',
                ".modal",
                '[data-testid*="modal"]',
                '[class*="modal"]',
            ]

            modal = None
            for selector in modal_selectors:
                try:
                    modal = await self.page.wait_for_selector(selector, timeout=10000)
                    if modal:
                        logging.info(f"Found modal with selector: {selector}")
                        break
                except:
                    continue

            if not modal:
                logging.error("Modal did not appear")
                return False

            # Wait a bit for content to load
            await self.page.wait_for_timeout(2000)

            # Look for vagas count
            vagas_text = await self.page.inner_text("body")
            logging.info(f"Modal content: {vagas_text[:200]}...")

            # Check if we can find number of vagas
            import re

            vagas_numbers = re.findall(r"\d+", vagas_text)
            if vagas_numbers:
                logging.info(f"Found {vagas_numbers[0]} vagas")
            else:
                logging.info("Could not find specific vagas count, but modal appeared")

            return True

        except Exception as e:
            logging.error(f"Error waiting for modal: {e}")
            return False

    async def click_enviar_automaticamente(self):
        """Click the 'enviar automaticamente' button"""
        try:
            logging.info("Looking for 'Enviar Automaticamente' button")

            # Try multiple selectors
            selectors = [
                'div:has-text("enviar automaticamente")',
                'div:has-text("Enviar Automaticamente")',
                'div:has-text("ENVIAR AUTOMATICAMENTE")',
                '[data-testid*="enviar"]',
                'button[type="submit"]',
            ]

            button = None
            for selector in selectors:
                try:
                    button = await self.page.wait_for_selector(selector, timeout=5000)
                    if button:
                        logging.info(f"Found button with selector: {selector}")
                        break
                except:
                    continue

            if not button:
                logging.error("Could not find 'enviar automaticamente' button")
                return False

            await button.click()
            logging.info("Clicked 'enviar automaticamente' button")

            # Wait a bit to see if there's any confirmation
            await self.page.wait_for_timeout(3000)

            return True

        except Exception as e:
            logging.error(f"Error clicking 'enviar automaticamente' button: {e}")
            return False

    async def run_automation(self):
        """Main automation flow"""
        try:
            logging.info("Starting DevScout automation")

            # Setup browser
            await self.setup_browser()

            # Navigate to site
            if not await self.navigate_to_site():
                return False

            # Check login status and login if needed
            if not await self.check_login_status():
                if not await self.login():
                    return False

            # Click procurar vagas button
            if not await self.find_and_click_procurar_vagas():
                return False

            # Wait for modal and check vagas
            if not await self.wait_for_modal_and_check_vagas():
                return False

            # Click enviar automaticamente
            if not await self.click_enviar_automaticamente():
                return False

            logging.info("Automation completed successfully")
            return True

        except Exception as e:
            logging.error(f"Automation failed: {e}")
            return False

    async def cleanup(self):
        """Clean up resources"""
        try:
            if hasattr(self, "context"):
                await self.context.close()
            if hasattr(self, "browser"):
                await self.browser.close()
            if hasattr(self, "playwright"):
                await self.playwright.stop()
            logging.info("Cleanup completed")
        except Exception as e:
            logging.error(f"Cleanup error: {e}")


async def main():
    """Main function"""
    automation = DevScoutAutomation()

    try:
        success = await automation.run_automation()
        if success:
            logging.info("✅ DevScout automation completed successfully!")
        else:
            logging.error("❌ DevScout automation failed!")
    finally:
        await automation.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
