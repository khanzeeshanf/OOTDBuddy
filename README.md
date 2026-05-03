# 👔 OOTDBuddy

**OOTDBuddy** is a premium, weather-aware outfit recommendation engine. Whether you're heading out for a quick trek or a full day in the city, OOTDBuddy analyzes real-time weather forecasts to suggest the perfect attire and essentials.

![OOTDBuddy Logo](OOTDBuddy.png)

## 🌟 Key Features
- **Smart Recommendations**: Tailored suggestions based on temperature, rain probability, and UV index.
- **Duration Aware**: Precise analysis for 2, 4, 8, 12, or 24-hour outings.
- **Trek Vibe Design**: Immersive nature-inspired UI with high-end glassmorphism.
- **Dual Functionality**: Use it as a standalone Web App or a powerful MCP Server for AI agents.

---

## 🚀 Web Application
The easiest way to use OOTDBuddy.
- **Live Demo**: [https://YOUR_USERNAME.github.io/OOTDBuddy/](https://YOUR_USERNAME.github.io/OOTDBuddy/) (Coming soon!)
- **Local Use**: Simply open `index.html` in your browser.

---

## 🤖 MCP Server (For AI Agents)
Connect OOTDBuddy's brain to your favorite AI assistant (Antigravity, Claude Desktop, etc.).

### 1. Using the Executable (earliest)
Download the standalone `OOTDBuddy-Server-v1.0.0.exe` from the `/release` folder. No Python installation required!

**Config Snippet:**
```json
{
  "mcpServers": {
    "ootd-buddy": {
      "command": "C:/path/to/release/OOTDBuddy-Server-v1.0.0.exe",
      "args": []
    }
  }
}
```

### 2. Running from Source
If you prefer to run with Python:
1.  Clone the repo.
2.  Install dependencies: `pip install -r mcp-server/requirements.txt`
3.  Run: `python mcp-server/server.py`

---

## 🛠️ Architecture
- **Frontend**: Vanilla HTML5, CSS3 (Glassmorphism), and ES6+ JavaScript.
- **Backend (MCP)**: Python with `FastMCP` and `httpx`.
- **Weather Data**: Powered by the **Open-Meteo** API.

## 📄 License
© 2026 Zeeshan. All rights reserved.

---
*Created with ❤️ by [Zeeshan](https://www.linkedin.com/in/zeeshan-khan-003741245) | [X (Twitter)](https://x.com/zeeshanByte)*
