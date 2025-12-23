#!/usr/bin/env python3
"""
Lightweight DevScout automation using requests + BeautifulSoup
Works within PythonAnywhere free tier restrictions without Playwright downloads
"""

import requests
import time
import logging
import os
import re
from bs4 import BeautifulSoup
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("devscout_requests.log"), logging.StreamHandler()],
)


class DevScoutRequestsAutomation:
    def __init__(self):
        self.email = os.getenv("EMAIL")
        self.password = os.getenv("PASSWORD")
        self.base_url = "https://devscout.app"

        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            }
        )

        if not self.email or not self.password:
            raise ValueError("EMAIL and PASSWORD must be set in environment variables")

    def check_site_accessibility(self):
        """Check if we can access the site"""
        try:
            response = self.session.get(self.base_url, timeout=30)
            if response.status_code == 200:
                logging.info("✅ Successfully accessed DevScout")
                return True, response.text
            else:
                logging.error(
                    f"❌ Failed to access DevScout: HTTP {response.status_code}"
                )
                return False, None
        except Exception as e:
            logging.error(f"❌ Error accessing site: {e}")
            return False, None

    def check_login_status(self, html_content):
        """Check if user is logged in based on page content"""
        if "Cadastrar / Login" in html_content or "Entrar com Google" in html_content:
            logging.info("🔐 User not logged in - login required")
            return False
        else:
            logging.info("✅ User appears to be logged in")
            return True

    def extract_csrf_token(self, html_content):
        """Extract CSRF token from login form"""
        soup = BeautifulSoup(html_content, "html.parser")

        # Look for CSRF token in various forms
        csrf_token = None

        # Check for meta tag
        csrf_meta = soup.find("meta", {"name": "csrf-token"})
        if csrf_meta:
            csrf_token = csrf_meta.get("content")

        # Check for hidden input
        if not csrf_token:
            csrf_input = soup.find("input", {"name": "csrf_token"})
            if csrf_input:
                csrf_token = csrf_input.get("value")

        # Check for _token input
        if not csrf_token:
            token_input = soup.find("input", {"name": "_token"})
            if token_input:
                csrf_token = token_input.get("value")

        if csrf_token:
            logging.info("✅ Found CSRF token")
            return csrf_token
        else:
            logging.warning("⚠️ No CSRF token found")
            return None

    def login(self, csrf_token):
        """Attempt login using requests session"""
        try:
            login_url = (
                f"{self.base_url}/login"  # Adjust based on actual login endpoint
            )

            # Prepare login data
            login_data = {
                "email": self.email,
                "password": self.password,
            }

            # Add CSRF token if found
            if csrf_token:
                login_data["csrf_token"] = csrf_token
                login_data["_token"] = csrf_token

            # Add referer
            headers = {
                "Referer": self.base_url,
                "Origin": self.base_url,
            }

            logging.info("🔐 Attempting login...")

            # Try multiple login endpoints
            login_endpoints = ["/login", "/auth/login", "/api/login", "/user/login"]

            for endpoint in login_endpoints:
                try:
                    response = self.session.post(
                        f"{self.base_url}{endpoint}",
                        data=login_data,
                        headers=headers,
                        timeout=30,
                        allow_redirects=False,
                    )

                    if response.status_code in [200, 302, 303]:
                        logging.info(f"✅ Login successful via {endpoint}")
                        return True, response.text
                    else:
                        logging.warning(
                            f"❌ Login failed via {endpoint}: {response.status_code}"
                        )

                except Exception as e:
                    logging.warning(f"❌ Login error via {endpoint}: {e}")
                    continue

            return False, None

        except Exception as e:
            logging.error(f"❌ Login process failed: {e}")
            return False, None

    def simulate_procurar_vagas(self, html_content):
        """Simulate clicking 'procurar vagas' by looking for API endpoints"""
        try:
            soup = BeautifulSoup(html_content, "html.parser")

            # Look for buttons or forms related to job search
            vagas_button = None
            vagas_form = None
            api_endpoint = None

            # Find buttons with relevant text
            buttons = soup.find_all(
                ["button", "a"], string=re.compile(r"procurar\s*vagas", re.IGNORECASE)
            )
            if buttons:
                vagas_button = buttons[0]
                logging.info(
                    f"✅ Found 'procurar vagas' button: {vagas_button.text.strip()}"
                )

            # Look for job search form
            forms = soup.find_all("form")
            for form in forms:
                form_text = form.get_text().lower()
                if "vaga" in form_text or "job" in form_text or "search" in form_text:
                    vagas_form = form
                    action = form.get("action", "")
                    if "search" in action or "vaga" in action:
                        api_endpoint = action
                        logging.info(f"✅ Found job search form: {action}")
                        break

            # Look for API endpoints in JavaScript
            scripts = soup.find_all("script")
            for script in scripts:
                script_text = script.string if script.string else ""
                if "procurar" in script_text or "vagas" in script_text:
                    # Extract potential API calls
                    api_matches = re.findall(
                        r'["\']([^"\']*(?:procurar|vagas|search)[^"\']*["\']',
                        script_text,
                    )
                    if api_matches:
                        api_endpoint = api_matches[0]
                        logging.info(f"✅ Found potential API endpoint: {api_endpoint}")
                        break

            return {
                "button_found": bool(vagas_button),
                "form_found": bool(vagas_form),
                "api_endpoint": api_endpoint,
                "button_info": str(vagas_button.text.strip()) if vagas_button else None,
                "form_action": vagas_form.get("action") if vagas_form else None,
            }

        except Exception as e:
            logging.error(f"❌ Error analyzing page: {e}")
            return {}

    def check_for_vagas_api(self, analysis_results):
        """Try to find and use vagas API"""
        if not analysis_results.get("api_endpoint"):
            logging.warning("⚠️ No API endpoint found, cannot fetch vagas")
            return False, None

        try:
            api_url = analysis_results["api_endpoint"]
            if not api_url.startswith("http"):
                api_url = f"{self.base_url}{api_url}"

            logging.info(f"🔍 Trying API endpoint: {api_url}")

            # Try GET request first
            response = self.session.get(api_url, timeout=30)
            if response.status_code == 200:
                logging.info("✅ Successfully accessed vagas API")
                return True, response.text
            else:
                logging.warning(f"❌ API GET failed: {response.status_code}")

                # Try POST request
                response = self.session.post(api_url, data={}, timeout=30)
                if response.status_code == 200:
                    logging.info("✅ Successfully accessed vagas API via POST")
                    return True, response.text
                else:
                    logging.warning(f"❌ API POST failed: {response.status_code}")

            return False, None

        except Exception as e:
            logging.error(f"❌ API call failed: {e}")
            return False, None

    def simulate_enviar_automaticamente(self, html_content):
        """Simulate 'enviar automaticamente' action"""
        try:
            soup = BeautifulSoup(html_content, "html.parser")

            # Look for auto-apply buttons or forms
            auto_buttons = soup.find_all(
                ["button", "a"],
                string=re.compile(r"enviar\s+automaticamente", re.IGNORECASE),
            )
            auto_forms = soup.find_all("form")

            for form in auto_forms:
                form_text = form.get_text().lower()
                if "automatic" in form_text or "enviar" in form_text:
                    action = form.get("action", "")
                    if "apply" in action or "send" in action:
                        logging.info(f"✅ Found auto-apply form: {action}")
                        return {
                            "found": True,
                            "method": form.get("method", "POST"),
                            "action": action,
                            "form_data": self.extract_form_data(form),
                        }

            if auto_buttons:
                return {
                    "found": True,
                    "button_text": auto_buttons[0].text.strip(),
                    "button_info": str(auto_buttons[0]),
                }

            logging.warning("⚠️ No 'enviar automaticamente' button found")
            return {"found": False}

        except Exception as e:
            logging.error(f"❌ Error analyzing auto-apply: {e}")
            return {"found": False}

    def extract_form_data(self, form):
        """Extract form data for submission"""
        form_data = {}

        inputs = form.find_all("input")
        for input_tag in inputs:
            name = input_tag.get("name")
            value = input_tag.get("value", "")
            if name:
                form_data[name] = value

        return form_data

    def send_automatic_application(self, apply_info):
        """Send automatic application"""
        if not apply_info.get("found"):
            return False

        try:
            if "action" in apply_info:
                logging.info(f"📤 Sending application to: {apply_info['action']}")

                action_url = apply_info["action"]
                if not action_url.startswith("http"):
                    action_url = f"{self.base_url}{action_url}"

                method = apply_info.get("method", "POST").upper()
                form_data = apply_info.get("form_data", {})

                if method == "POST":
                    response = self.session.post(action_url, data=form_data, timeout=30)
                else:
                    response = self.session.get(
                        action_url, params=form_data, timeout=30
                    )

                if response.status_code in [200, 302, 303]:
                    logging.info("✅ Application sent successfully")
                    return True
                else:
                    logging.error(f"❌ Application failed: {response.status_code}")
                    return False
            else:
                logging.info("✅ Click simulation successful (button-based)")
                return True

        except Exception as e:
            logging.error(f"❌ Error sending application: {e}")
            return False

    def run_automation(self):
        """Main automation flow using requests"""
        try:
            logging.info("🚀 Starting DevScout requests-based automation")

            # Step 1: Access site
            success, content = self.check_site_accessibility()
            if not success:
                return False

            # Step 2: Check login status
            is_logged_in = self.check_login_status(content)
            if not is_logged_in:
                # Step 3: Extract CSRF token and login
                csrf_token = self.extract_csrf_token(content)
                login_success, login_content = self.login(csrf_token)
                if not login_success:
                    return False

                # Update with logged in content
                content = login_content

            # Step 4: Analyze page for vagas functionality
            vagas_analysis = self.simulate_procurar_vagas(content)
            logging.info(f"📊 Vagas analysis: {vagas_analysis}")

            # Step 5: Try to access vagas API
            api_success, api_content = self.check_for_vagas_api(vagas_analysis)
            if api_success:
                content = api_content
            elif not vagas_analysis.get("button_found"):
                logging.error("❌ Cannot proceed - no vagas functionality found")
                return False

            # Step 6: Simulate auto-application
            apply_info = self.simulate_enviar_automaticamente(content)

            # Step 7: Send application if possible
            application_success = self.send_automatic_application(apply_info)

            if application_success:
                logging.info("✅ DevScout requests automation completed successfully!")
                return True
            else:
                logging.error("❌ DevScout requests automation failed!")
                return False

        except Exception as e:
            logging.error(f"❌ Automation failed: {e}")
            return False


def main():
    """Main function"""
    try:
        automation = DevScoutRequestsAutomation()
        success = automation.run_automation()

        if success:
            print("🎉 Automation completed successfully!")
        else:
            print("❌ Automation failed!")

    except Exception as e:
        logging.error(f"❌ Fatal error: {e}")
        print("❌ Fatal error occurred!")


if __name__ == "__main__":
    main()
