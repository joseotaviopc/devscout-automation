# DevScout Automation

Automated daily job search application for DevScout platform using Python and Playwright.

## Features

- 🤖 Automated browser navigation to DevScout
- 🔐 Smart login handling with fallbacks
- 🎯 Clicks "procurar vagas" button
- ⏳ Waits for modal and checks vagas count
- 📤 Clicks "enviar automaticamente" button
- 🌊 Uses Safari (WebKit) browser engine
- 📝 Comprehensive logging and error handling
- ⏰ Daily scheduling support
- 🔧 Configurable via environment variables

## Quick Start

### Prerequisites

- Python 3.8+
- [uv](https://github.com/astral-sh/uv) (recommended) or pip

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/devscout-automation.git
cd devscout-automation

# Install dependencies with uv (recommended)
uv sync

# Or with pip
pip install -r requirements.txt

# Install Playwright browsers
uv run playwright install
# or
playwright install
```

### Configuration

1. Copy environment template:
```bash
cp .env.example .env
```

2. Edit `.env` with your credentials:
```bash
EMAIL=your_email@example.com
PASSWORD=your_password
# Optional settings
SCHEDULE_TIME=09:00
HEADLESS=true
```

### Usage

```bash
# Test setup
uv run python test_setup.py

# Run automation once
uv run python main.py

# Start daily scheduler
uv run python scheduler.py
```

## Project Structure

```
devscout-automation/
├── main.py              # Main automation script
├── scheduler.py          # Daily scheduling (local use)
├── test_setup.py         # Setup verification script
├── demo.py              # Demo and exploration script
├── test_login.py        # Login testing script
├── .env.example         # Environment template
├── .env                # Your credentials (gitignored)
├── pyproject.toml       # Project dependencies
├── uv.lock            # Dependency lock file
└── README.md           # This file
```

## How It Works

1. **Navigation**: Opens Safari browser and navigates to devscout.app
2. **Login Detection**: Checks if already logged in, logs in if needed
3. **Button Click**: Finds and clicks "procurar vagas" button
4. **Modal Wait**: Waits for modal to appear and displays vagas count
5. **Auto Send**: Clicks "enviar automaticamente" button
6. **Logging**: Records all actions and saves screenshots on errors
7. **Cleanup**: Closes browser and releases resources

## Browser Support

- **Safari (WebKit)**: Default, works on macOS
- **Chromium**: Easy to switch to in `main.py` line 41
- **Firefox**: Available via Playwright

## Deployment Options

### Local Machine
```bash
# Set up daily cron job
crontab -e
# Add: 0 9 * * * cd /path/to/devscout-automation && uv run python scheduler.py
```

### PythonAnywhere (Cloud)
1. Sign up at [pythonanywhere.com](https://www.pythonanywhere.com)
2. Upload project files
3. Install dependencies: `uv sync`
4. Install browsers: `uv run playwright install`
5. Set scheduled task in dashboard
6. Command: `cd ~/devscout-automation && uv run python main.py`

### Raspberry Pi
```bash
# Install and run on Raspberry Pi
curl -LsSf https://astral.sh/uv/install.sh | sh
git clone <repository>
cd devscout-automation
uv sync
uv run playwright install
uv run python scheduler.py
```

## Configuration Options

### Environment Variables

| Variable | Required | Default | Description |
|----------|-----------|---------|-------------|
| `EMAIL` | ✅ | - | Your DevScout login email |
| `PASSWORD` | ✅ | - | Your DevScout password |
| `HEADLESS` | ❌ | `true` | Run browser without UI (`false` for debugging) |
| `SCHEDULE_TIME` | ❌ | `09:00` | Daily execution time (HH:MM format) |

### Browser Options

Edit `main.py` line 41:
```python
# For Chrome/Chromium
self.browser = await self.playwright.chromium.launch(**browser_options)

# For Firefox  
self.browser = await self.playwright.firefox.launch(**browser_options)

# For Safari (default)
self.browser = await self.playwright.webkit.launch(**browser_options)
```

## Logging

The automation creates `devscout.log` with:
- ✅ Navigation and login status
- 🎯 Button clicks and actions
- 📊 Vagas count when available
- ⚠️ Errors and failures
- 🖼️ Screenshot paths for debugging

## Troubleshooting

### Common Issues

**Playwright browsers not found:**
```bash
uv run playwright install
```

**Login button not found:**
- Set `HEADLESS=false` to see the page
- Check if DevScout has changed their UI

**No "procurar vagas" button:**
- May need to be logged in first
- Run the demo script to investigate

### Debug Mode

Set `HEADLESS=false` in `.env` to watch the automation in real-time.

## Security Notes

- 🔐 Credentials stored in `.env` (never commit to git)
- 🚫 `.env` is included in `.gitignore`
- 🔒 Your login data is only used for DevScout automation
- 📝 No data is stored or transmitted elsewhere

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This automation tool is for educational purposes. Use responsibly and in compliance with DevScout's terms of service. The authors are not responsible for any misuse or account suspensions.

## Support

- 📋 Check issues in this repository
- 🐛 Report bugs via GitHub Issues
- 💡 Feature requests welcome
- 📖 Review the troubleshooting section before opening issues