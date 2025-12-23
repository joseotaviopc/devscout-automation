#!/usr/bin/env python3
"""
Check available browsers on PythonAnywhere system
"""

import subprocess
import os


def check_system_browsers():
    """Check what browsers are available on the system"""
    print("🔍 Checking for available browsers...")

    browsers = {}

    # Check Chromium
    chromium_paths = [
        "/usr/bin/chromium",
        "/usr/bin/chromium-browser",
        "/usr/local/bin/chromium",
        "/snap/bin/chromium",
        "/opt/homebrew/bin/chromium",
    ]

    for path in chromium_paths:
        if os.path.exists(path):
            browsers["chromium"] = path
            print(f"✅ Found Chromium: {path}")
            break

    # Check Firefox
    firefox_paths = [
        "/usr/bin/firefox",
        "/usr/local/bin/firefox",
        "/snap/bin/firefox",
        "/opt/homebrew/bin/firefox",
    ]

    for path in firefox_paths:
        if os.path.exists(path):
            browsers["firefox"] = path
            print(f"✅ Found Firefox: {path}")
            break

    # Check for Playwright browsers
    playwright_browsers = []
    try:
        result = subprocess.run(
            ["python", "-c", "import playwright; print(playwright.__version__)"],
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            print(f"✅ Playwright version: {result.stdout.strip()}")
    except:
        print("❌ Playwright not available")

    return browsers


def install_browser_packages():
    """Install browser packages that might be available"""
    print("\n📦 Installing browser packages...")

    packages = [
        "chromium-browser",
        "firefox",
        "google-chrome-stable",
        "chromium",
    ]

    for package in packages:
        try:
            result = subprocess.run(
                ["apt", "list", "--installed", package], capture_output=True, text=True
            )
            if result.returncode == 0:
                print(f"✅ {package} is installed")
            else:
                print(f"❌ {package} not installed")
        except:
            print(f"❓ Could not check {package}")


if __name__ == "__main__":
    print("🌐 PythonAnywhere Browser Check")
    print("=" * 40)

    browsers = check_system_browsers()

    print(f"\n📋 Available browsers: {list(browsers.keys())}")

    install_browser_packages()

    print("\n💡 Recommendations:")
    print("1. If no browsers found, try: apt update && apt install -y chromium-browser")
    print("2. Use main_manual_browser.py instead of main.py")
    print("3. The manual browser version will find system browsers automatically")
