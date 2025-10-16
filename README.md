<!-- GSSoC banner and project insights -->

<h1 align="center">
  <img width="64" height="64" alt="Voice-Marketing-Agent logo" src="frontend/logo.png"/>
  <br>
  Voice-Marketing-Agent
</h1>

<p align="center">
  <b>This project is now OFFICIALLY accepted for:</b>
</p>

<div align="center">
  <img src="frontend/gssoc.png" alt="GSSOC" width="80%">
</div>

<div align="center">
  <img src="https://hacktoberfest.com/_next/static/media/logo-hacktoberfest--horizontal.e2dab54d.svg" alt="Hacktoberfest" width="80%">
</div>

<p align="center">
  <strong>🎉 Participating in GSSOC'25 & Hacktoberfest 2025! 🎉</strong>
</p>

<p align="center">
  <img src="frontend/logo.png" alt="Voice Marketing Agents Logo" width="200"/>
</p>

<h2 align="center">Voice Marketing Agents 🤖</h2>

<p align="center">
  <strong>An open-source framework to build and deploy intelligent AI agents that can handle real-world phone calls using cutting-edge cloud APIs.</strong>
  <br />
  <br />
  <a href="#-getting-started-in-under-5-minutes"><strong>🚀 Get Started</strong></a>
  ·
  <a href="https://github.com/OpenVoiceX/Voice-Marketing-Agent/issues"><strong>🐛 Report a Bug</strong></a>
  ·
  <a href="https://github.com/OpenVoiceX/Voice-Marketing-Agent/issues"><strong>✨ Request a Feature</strong></a>
</p>

<p align="center">
  <a href="https://github.com/OpenVoiceX/Voice-Marketing-Agent/stargazers"><img src="https://img.shields.io/github/stars/OpenVoiceX/Voice-Marketing-Agent?style=for-the-badge&logo=github&color=FFDD00" alt="Stars"></a>
  <a href="https://github.com/OpenVoiceX/Voice-Marketing-Agent/blob/main/LICENSE"><img src="https://img.shields.io/github/license/OpenVoiceX/Voice-Marketing-Agent?style=for-the-badge&color=00BFFF" alt="License"></a>
  <a href="https://github.com/OpenVoiceX/Voice-Marketing-Agent/network/members"><img src="https://img.shields.io/github/forks/OpenVoiceX/Voice-Marketing-Agent?style=for-the-badge&logo=github&color=90EE90" alt="Forks"></a>
</p>

<table align="center">
  <thead align="center">
    <tr>
      <td><b>🌟 Stars</b></td>
      <td><b>🍴 Forks</b></td>
      <td><b>🐛 Issues</b></td>
      <td><b>🔔 Open PRs</b></td>
      <td><b>🔕 Closed PRs</b></td>
      <td><b>⏱️ Last Commit</b></td>
      <td><b>🛠️ Languages</b></td>
      <td><b>👥 Contributors</b></td>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><img alt="Stars" src="https://img.shields.io/github/stars/OpenVoiceX/Voice-Marketing-Agent?style=flat&logo=github"/></td>
      <td><img alt="Forks" src="https://img.shields.io/github/forks/OpenVoiceX/Voice-Marketing-Agent?style=flat&logo=github"/></td>
      <td><img alt="Issues" src="https://img.shields.io/github/issues/OpenVoiceX/Voice-Marketing-Agent?style=flat&logo=github"/></td>
      <td><img alt="Open PRs" src="https://img.shields.io/github/issues-pr/OpenVoiceX/Voice-Marketing-Agent?style=flat&logo=github"/></td>
      <td><img alt="Closed PRs" src="https://img.shields.io/github/issues-pr-closed/OpenVoiceX/Voice-Marketing-Agent?style=flat&color=critical&logo=github"/></td>
      <td><img alt="Last Commit" src="https://img.shields.io/github/last-commit/OpenVoiceX/Voice-Marketing-Agent?style=flat&logo=github"/></td>
      <td><img alt="Languages Count" src="https://img.shields.io/github/languages/count/OpenVoiceX/Voice-Marketing-Agent?style=flat&color=green&logo=github"></td>
      <td><img alt="Contributors Count" src="https://img.shields.io/github/contributors/OpenVoiceX/Voice-Marketing-Agent?style=flat&color=blue&logo=github"/></td>
    </tr>
  </tbody>
</table>

---

## 🌟 The Mission: Cloud-Powered Voice AI

**Voice Marketing Agents** leverages the power of **Google Gemini**, **Groq**, and **ElevenLabs** to deliver production-ready voice AI capabilities. No local models, no GPU infrastructure - just powerful cloud APIs.

### 🔥 Core Features

* **Lightning-Fast Responses:** Groq's ultra-fast inference + ElevenLabs' low-latency TTS = natural conversations
* **Cloud-Powered AI:** Gemini for intelligence, Groq for speed, ElevenLabs for studio-quality voice
* **Developer-First:** Fully containerized with Docker - one command to start everything
* **Simple Management UI:** Clean React dashboard for agent configuration
* **Extensible:** Built with modern tech stack for easy customization
* **No Infrastructure Hassle:** Everything via cloud APIs - no model management needed

---

## 🚀 The Tech Stack

| Component      | Technology                  | Why                                |
| -------------- | --------------------------- | ---------------------------------- |
| **Frontend**   | React & Vite               | Fast, modern UI development        |
| **Backend**    | Python & FastAPI           | Async performance for AI tasks     |
| **STT**        | Google Gemini Voice API    | High-accuracy speech recognition   |
| **LLM**        | Gemini & Groq              | Smart + Fast conversation engine   |
| **TTS**        | ElevenLabs                 | Studio-quality voice synthesis     |
| **Database**   | PostgreSQL                 | Reliable data storage              |
| **Deploy**     | Docker Compose             | One-command deployment             |

---

## 🛠️ Quick Start (Under 5 Minutes)

### Prerequisites

1. **Docker & Docker Compose** - [Get it here](https://www.docker.com/products/docker-desktop/)
2. **API Keys** from:
   - [Google Gemini](https://ai.google.dev/)
   - [Groq](https://console.groq.com/)
   - [ElevenLabs](https://elevenlabs.io/)
   - [Twilio](https://www.twilio.com/)

### Setup

1. **Clone:**
   ```sh
   git clone https://github.com/OpenVoiceX/Voice-Marketing-Agent.git
   cd Voice-Marketing-Agent
   ```

2. **Configure `.env`:**
   ```env
   # Database
   DATABASE_URL=postgresql://user:password@db:5432/voicegenie_db

   # Gemini
   GEMINI_API_KEY=your_gemini_key
   GEMINI_MODEL=gemini-1.5-flash
   GEMINI_VOICE_MODEL=gemini-1.5-flash

   # Groq
   GROQ_API_KEY=your_groq_key
   GROQ_MODEL=llama-3.1-70b-versatile

   # LLM Provider (gemini or groq)
   LLM_PROVIDER=gemini

   # ElevenLabs
   ELEVENLABS_API_KEY=your_elevenlabs_key
   ELEVENLABS_VOICE_ID=21m00Tcm4TlvDq8ikWAM
   ELEVENLABS_MODEL_ID=eleven_monolingual_v1

   # Twilio
   TWILIO_ACCOUNT_SID=your_sid
   TWILIO_AUTH_TOKEN=your_token
   TWILIO_PHONE_NUMBER=your_number

   # App
   SECRET_KEY=your_secret_key
   AUDIO_DIR=/app/audio_files
   PUBLIC_URL=http://your-server:8000
   ```

3. **Launch:**
   ```sh
   docker compose up --build -d
   ```

4. **Access:**
   - Dashboard: `http://localhost:3000`
   - API Docs: `http://localhost:8000/docs`

---

## 🎯 Choosing Your LLM Provider

**Gemini** (`LLM_PROVIDER=gemini`)
- Advanced reasoning & multimodal
- ~100 tokens/sec
- Free tier available

**Groq** (`LLM_PROVIDER=groq`)
- Ultra-fast (up to 750 tokens/sec)
- Perfect for real-time conversations
- Free tier available

---

## 🏗️ System Architecture

![Voice Marketing Agents Architecture Diagram](docs/Architecture-1.png)

The platform is designed as a set of coordinated microservices, orchestrated by Docker Compose. This modular architecture allows for scalability, maintainability, and clear separation of concerns.

### The Life of a Single Conversational Turn

1. **Telephony Gateway (External):** A VoIP service handles the actual phone call connection. When it's the AI's turn to speak or listen, the VoIP server makes a webhook call to our backend.

2. **Audio Ingestion:** The VoIP server sends the user's speech as a `.wav` file in a `multipart/form-data` request to the `/webhook` endpoint of our **FastAPI Backend**.

3. **STT Micro-Task (Speech-to-Text):**
   - The backend receives the audio file.
   - It calls the `STTService`, which is powered by **Google Gemini Voice API**.
   - The API transcribes the audio to text in a few hundred milliseconds.

4. **LLM Micro-Task (Reasoning & Response Generation):**
   - The transcribed text is passed to the `LLMService`.
   - This service constructs a prompt and sends it to either **Gemini** or **Groq**.
   - The LLM generates the text for the agent's response.

5. **TTS Micro-Task (Text-to-Speech):**
   - The LLM's text response is sent to the `TTSService`.
   - **ElevenLabs** synthesizes this text into high-quality audio.
   - The resulting audio is saved as a temporary file.

6. **Webhook Response:** The FastAPI backend responds to the initial webhook request from the Telephony Gateway, providing a URL to the newly generated audio file. The gateway then plays this audio to the user over the phone.

This entire end-to-end process is optimized to complete in **under 2 seconds**, which is crucial for maintaining a natural conversational rhythm.

---

## 💖 Contributing

We love contributions! Check our [open issues](https://github.com/OpenVoiceX/Voice-Marketing-Agent/issues) and see the [Contribution Guide](CONTRIBUTING.md).

---

## 🗺️ Roadmap

- [ ] Visual call flow builder
- [ ] Campaign management UI
- [ ] Multi-language support
- [ ] Voice cloning
- [ ] CRM integrations
- [ ] Kubernetes deployment
- [ ] Analytics dashboard

---

## 🌟 Contributors

Thanks to these wonderful people:

<a href="https://github.com/OpenVoiceX/Voice-Marketing-Agent/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=OpenVoiceX/Voice-Marketing-Agent" />
</a>

---

## 📜 License

MIT License - See [LICENSE](LICENSE) file.

---

<div align="center">
<p>Built with ❤️ and powered by ☁️ cloud AI for GSSoC'25</p>
<p>Let's democratize voice AI! 🚀</p>
</div>