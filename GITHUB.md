# DevScout Automation Repository

## 🚀 Quick Start

### Clone and Run
```bash
git clone https://github.com/yourusername/devscout-automation.git
cd devscout-automation
uv sync
uv run playwright install
cp .env.example .env
# Edit .env with your credentials
uv run python test_setup.py
```

## 📋 Repository Contents

- 🐍 **Complete Automation**: Full DevScout daily job automation
- 🌊 **Browser Support**: Safari (default), Chrome, Firefox
- 🔐 **Smart Login**: Email/password with Enter key fallback
- 📊 **Modal Handling**: Waits for vagas count and clicks submit
- 📝 **Comprehensive Logging**: Detailed logs and screenshot debugging
- ⏰ **Daily Scheduling**: Built-in scheduling for automated execution
- 🔧 **Deployment Ready**: PythonAnywhere, Raspberry Pi, cloud options

## 🏗️ Project Structure

```
devscout-automation/
├── 📄 README.md              # Complete documentation
├── 📄 LICENSE                # MIT license
├── ⚙️ .env.example          # Environment template
├── 🚫 .gitignore            # Git ignore rules
├── 📦 pyproject.toml         # Dependencies (uv)
├── 🔒 uv.lock               # Dependency lock
├── 🐍 main.py               # Main automation script
├── ⏰ scheduler.py           # Daily scheduling
├── 🧪 test_setup.py         # Setup verification
├── 🎯 demo.py               # Exploration and demo
├── 🔐 test_login.py          # Login testing
└── 📂 src/__init__.py         # Package init
```

## 🎯 What It Does

1. **Navigate** to devscout.app using Safari browser
2. **Detect** login status and authenticate automatically
3. **Click** "procurar vagas" button with smart selectors
4. **Wait** for modal and display vagas count
5. **Click** "enviar automaticamente" button
6. **Log** everything with screenshots on errors

## 🚀 Deployment Options

### 🌐 PythonAnywhere (Recommended)
- **Cost**: Free tier available
- **Setup**: 5 minutes deployment
- **Reliability**: 99.9% uptime
- **Guide**: See README.md in repository

### 🏠 Raspberry Pi
- **Cost**: ~$75 one-time
- **Benefit**: 24/7 availability
- **Power**: Low energy consumption

### 💻 Local Machine
- **Cost**: Free (if already have computer)
- **Setup**: Cron job configuration
- **Monitoring**: DIY solution

## 🔧 Customization

### Browser Selection

**Option 1 - Original (Playwright):**
```python
# main.py - Requires browser downloads (may not work on PythonAnywhere free)
```

**Option 2 - Manual Browser Detection (PythonAnywhere Compatible):**
```python
# main_manual_browser.py - Smart browser detection
# Uses existing system browsers (Chromium/Firefox/Safari)
# No downloads required
```

**Option 3 - requests + BeautifulSoup (No Browser):**
```python
# main_requests.py - Pure HTTP requests
# Works within any internet restrictions
# Lightweight and fast
```

**Choose based on your deployment environment!**

### Schedule Time
Edit `.env`:
```bash
SCHEDULE_TIME=09:00  # Any 24h time format
```

### Debug Mode
Edit `.env`:
```bash
HEADLESS=false  # Shows browser window for debugging
```

## 🧪 Testing

```bash
# Verify setup
uv run python test_setup.py

# Test login specifically
uv run python test_login.py

# Explore the site
uv run python demo.py
```

## 📝 Contributing

1. Fork repository
2. Create feature branch
3. Make your changes
4. Test thoroughly
5. Submit pull request

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## ⚠️ Important Notes

- **Security**: Never commit `.env` file with credentials
- **Responsibility**: Use according to DevScout terms
- **Monitoring**: Check logs regularly for issues
- **Updates**: DevScout may change UI requiring selector updates

## 🆘 Support

- 📋 Issues: Report via GitHub Issues
- 📖 Documentation: Check README.md first
- 🐛 Bugs: Include logs and screenshots
- 💡 Features: Welcome suggestions

---

**⭐ Star this repository if it helps you land your dream job!**