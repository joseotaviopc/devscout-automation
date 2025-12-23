#!/usr/bin/env python3
"""
Test script to verify the DevScout automation setup
"""

import sys
import os


def test_imports():
    """Test if all required packages can be imported"""
    print("Testing imports...")

    try:
        import playwright

        print("✅ playwright imported successfully")
    except ImportError as e:
        print(f"❌ playwright import failed: {e}")
        return False

    try:
        from dotenv import load_dotenv

        print("✅ python-dotenv imported successfully")
    except ImportError as e:
        print(f"❌ python-dotenv import failed: {e}")
        return False

    try:
        import schedule

        print("✅ schedule imported successfully")
    except ImportError as e:
        print(f"❌ schedule import failed: {e}")
        return False

    return True


def test_env_file():
    """Test if .env file exists and is properly configured"""
    print("\nTesting environment configuration...")

    if not os.path.exists(".env"):
        print("❌ .env file not found")
        print("Please copy .env.example to .env and configure your credentials")
        return False

    # Load and check environment variables
    from dotenv import load_dotenv

    load_dotenv()

    email = os.getenv("EMAIL")
    password = os.getenv("PASSWORD")

    if not email or email == "your_email@example.com":
        print("❌ EMAIL not properly configured in .env")
        return False

    if not password or password == "your_password":
        print("❌ PASSWORD not properly configured in .env")
        return False

    print("✅ Environment variables configured")
    return True


def test_playwright_browsers():
    """Test if Playwright browsers are installed"""
    print("\nTesting Playwright browsers...")

    try:
        from playwright.sync_api import sync_playwright

        with sync_playwright() as p:
            try:
                browser = p.chromium.launch(headless=True)
                browser.close()
                print("✅ Chromium browser available")
            except Exception as e:
                print(f"❌ Chromium browser not available: {e}")
                return False

        return True
    except Exception as e:
        print(f"❌ Playwright test failed: {e}")
        return False


def main():
    """Run all tests"""
    print("🔍 DevScout Automation Setup Test")
    print("=" * 40)

    tests = [test_imports, test_env_file, test_playwright_browsers]

    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Test {test.__name__} failed with exception: {e}")
            results.append(False)

    print("\n" + "=" * 40)
    print("📊 Test Results:")

    if all(results):
        print("✅ All tests passed! Your setup is ready.")
        print("\nNext steps:")
        print("1. Make sure your .env file has valid DevScout credentials")
        print("2. Run: uv run python main.py")
        print("3. For daily scheduling: uv run python scheduler.py")
        return True
    else:
        print("❌ Some tests failed. Please fix the issues above.")
        print("\nTroubleshooting:")
        print("- Make sure you ran: uv sync")
        print("- Make sure you ran: uv run playwright install")
        print("- Copy .env.example to .env and configure your credentials")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
