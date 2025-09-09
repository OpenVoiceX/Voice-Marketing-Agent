<!-- GSSoC banner and project insights -->
<h1 align="center">
  <img width="64" height="64" alt="LegalHuB Logo" src="frontend/logo.png"/>
  <br>
  Voice-Marketing-Agent
</h1>

<p align="center">
  <b>This project is now OFFICIALLY accepted for:</b>
</p>

<div align="center">
  <img src="frontend/gssoc.png" alt="GSSOC" width="80%">
</div>

<table align="center">
    <thead align="center">
        <tr>
            <td><b>🌟 Stars</b></td>
            <td><b>🍴 Forks</b></td>
            <td><b>🐛 Issues</b></td>
            <td><b>🔔 Open PRs</b></td>
            <td><b>🔕 Closed PRs</b></td>
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
            <td><img alt="Languages Count" src="https://img.shields.io/github/languages/count/OpenVoiceX/Voice-Marketing-Agent?style=flat&color=green&logo=github"></td>
            <td><img alt="Contributors Count" src="https://img.shields.io/github/contributors/OpenVoiceX/Voice-Marketing-Agent?style=flat&color=blue&logo=github"/></td>
        </tr>
    </tbody>
</table>

<p align="center">
  <img src="frontend/logo.png" alt="Voice Marketing Agents Logo" width="200"/>
</p>

<h1 align="center">Voice Marketing Agents 🤖</h1>

<p align="center">
  <strong>An open-source framework to build and deploy intelligent, self-hosted AI agents that can handle real-world phone calls.</strong>
  <br />
  <br />
<!--   <a href="#-getting-started-in-under-5-minutes"><strong>🚀 Get Started</strong></a> -->
  ·
  <a href="https://github.com/Hiteshydv001/Voice-Marketing-Agent/issues"><strong>🐛 Report a Bug</strong></a>
  ·
  <a href="https://github.com/Hiteshydv001/Voice-Marketing-Agent/issues"><strong>✨ Request a Feature</strong></a>
</p>

<p align="center">
  <a href="https://github.com/Hiteshydv001/Voice-Marketing-Agent/stargazers"><img src="https://img.shields.io/github/stars/Hiteshydv001/Voice-Marketing-Agent?style=for-the-badge&logo=github&color=FFDD00" alt="Stars"></a>
  <a href="https://github.com/Hiteshydv001/Voice-Marketing-Agent/blob/main/LICENSE"><img src="https://img.shields.io/github/license/Hiteshydv001/Voice-Marketing-Agent?style=for-the-badge&color=00BFFF" alt="License"></a>
  <a href="https://github.com/Hiteshydv001/Voice-Marketing-Agent/network/members"><img src="https://img.shields.io/github/forks/Hiteshydv001/Voice-Marketing-Agent?style=for-the-badge&logo=github&color=90EE90" alt="Forks"></a>
</p>

---

## 🌟 The Mission: Democratizing Voice AI

The ability to create AI that can hold a natural, real-time conversation over the phone is a game-changer. But until now, this power has been locked behind expensive, proprietary, and high-latency cloud APIs.

**Voice Marketing Agents** changes that.

This project provides a complete, end-to-end, open-source solution for anyone to build and deploy their own voice AI agents. It's not just a demo; it's a production-ready foundation designed for performance, control, and infinite customizability. Whether you're a developer wanting to automate business tasks, a hobbyist exploring conversational AI, or a student learning full-stack development, this project is for you.

**This project is our submission for GSSoC '24**, built to showcase the power of a modern, open-source AI stack.

### 🔥 Core Features

*   **Blazing-Fast & Real-Time:** A meticulously tuned AI pipeline ensures a total response latency of under 2 seconds, making conversations feel fluid and natural.
*   **100% Open-Source & Self-Hosted:** No reliance on external APIs. You run everything on your own infrastructure. This means zero per-minute costs and complete data privacy.
*   **Developer-First Experience:** A fully containerized environment using Docker. The entire complex system starts with a single command.
*   **Simple Management UI:** A clean React dashboard to create, configure, and manage the "personalities" of your different voice agents.
*   **Extensible by Design:** Built with modern, standard technologies, making it easy to modify, extend, or integrate with other systems.

---

## Ui Design

![Voice Marketing Agents Architecture Diagram](https://github.com/OpenVoiceX/Voice-Marketing-Agent/blob/main/docs/Voice-marketing-agent.png)

---

## 🏗️ System Architecture: A Deep Dive

The platform is designed as a set of coordinated microservices, orchestrated by Docker Compose. This modular architecture allows for scalability, maintainability, and clear separation of concerns.

![Voice Marketing Agents Architecture Diagram](https://github.com/Hiteshydv001/Voice-Marketing-Agent/blob/main/docs/Architecture-1.png)

<details>
  <summary><strong>Click to expand the detailed call processing workflow</strong></summary>

  ### The Life of a Single Conversational Turn

  1.  **Telephony Gateway (External):** A VoIP service (like a self-hosted Asterisk server) handles the actual phone call connection. When it's the AI's turn to speak or listen, the VoIP server makes a webhook call to our backend.
  2.  **Audio Ingestion:** The VoIP server sends the user's speech as a `.wav` file in a `multipart/form-data` request to the `/webhook` endpoint of our **FastAPI Backend**.
  3.  **STT Micro-Task (Speech-to-Text):**
      *   The backend receives the audio file.
      *   It calls the `STTService`, which is powered by **`faster-whisper`**.
      *   Using the `tiny.en` model with `int8` quantization on the CPU, it transcribes the audio to text in a few hundred milliseconds.
  4.  **LLM Micro-Task (Reasoning & Response Generation):**
      *   The transcribed text is passed to the `LLMService`.
      *   This service constructs a prompt (including system instructions and conversation history) and sends it to the **Ollama** container.
      *   The **`TinyLlama`** model, running inside Ollama, generates the text for the agent's response, typically in under a second.
  5.  **TTS Micro-Task (Text-to-Speech):**
      *   The LLM's text response is sent to the `TTSService`.
      *   The **`Coqui TTS`** engine synthesizes this text into a high-quality audio waveform.
      *   The resulting audio is saved as a temporary file accessible by the backend.
  6.  **Webhook Response:** The FastAPI backend responds to the initial webhook request from the Telephony Gateway, providing a URL to the newly generated audio file. The gateway then plays this audio to the user over the phone.

  This entire end-to-end process is optimized to complete in **under 2 seconds**, which is crucial for maintaining a natural conversational rhythm.

</details>

---

## 🚀 The Tech Stack: Why We Chose These Tools

Every technology in this stack was deliberately chosen for performance, community support, and its open-source nature.

| Component      | Technology                                    | Rationale & Key Benefits                                                                                                 |
| -------------- | --------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| **Frontend**   | **React & Vite**                              | **Speed & Simplicity.** React provides a robust component model, while Vite offers a lightning-fast development server and optimized builds for a lightweight dashboard. |
| **Backend**    | **Python & FastAPI**                          | **Asynchronous Performance.** FastAPI's async/await syntax is perfect for I/O-bound AI tasks, preventing the server from blocking while models are processing. |
| **STT Engine** | **`faster-whisper` (`tiny.en`)**              | **Extreme Speed.** A CTranslate2 re-implementation of Whisper that's up to 4x faster on CPU. `tiny.en` is all we need for high-accuracy English transcription. |
| **LLM Engine** | **Ollama with `TinyLlama`**                   | **Efficiency & Control.** Ollama makes serving LLMs effortless. `TinyLlama` is a small yet powerful model with minimal inference latency, ideal for real-time chat. |
| **TTS Engine** | **`Coqui TTS` (VITS Model)**                  | **Quality & Flexibility.** Coqui's VITS models offer a fantastic balance between natural-sounding, human-like voice and fast synthesis speeds on CPU. |
| **Database**   | **PostgreSQL**                                | **Reliability.** A battle-tested, robust relational database for storing agent configurations, call logs, and user data securely. |
| **Infra**      | **Docker & Docker Compose**                   | **Reproducibility.** This is the magic that makes it all work. It packages every service and its dependencies into isolated containers for a flawless, one-command setup. |

<details>
  <summary><strong>Explore the Project Directory Structure</strong></summary>

  ```
  .
  ├── backend/                # FastAPI application source code
  │   └── src/
  │       ├── api/            # API endpoint definitions (routes)
  │       ├── agents/         # Logic for different agent types
  │       ├── core/           # Core config, database connection
  │       ├── models/         # SQLAlchemy database models
  │       ├── schemas/        # Pydantic data validation schemas
  │       └── services/       # The STT, LLM, and TTS service integrations
  ├── frontend/               # React + Vite dashboard source code
  │   └── src/
  │       ├── components/     # Reusable UI components
  │       ├── pages/          # Main pages of the dashboard
  │       ├── services/       # API call functions
  │       └── store/          # Global state management
  ├── scripts/                # Utility scripts (e.g., test_call.py)
  ├── docs/                   # Project documentation and architecture diagrams
  └── docker-compose.yml      # The master file that orchestrates all services
  ```
</details>

---

## 🛠️ Getting Started in Under 5 Minutes

No complex setup, no dependency hell. Just Docker and Git.

### Prerequisites

1.  **Docker & Docker Compose:** You absolutely need this. [Get it here](https://www.docker.com/products/docker-desktop/).
2.  **Git:** For cloning the repository. [Get it here](https://git-scm.com/).

### Installation & Launch

1.  **Clone the Project:**
    Open your terminal and clone the repository to your local machine.
    ```sh
    git clone https://github.com/your-username/voice-marketing-agents.git
    cd voice-marketing-agents
    ```

2.  **Launch the Mothership!**
    This single command builds the Docker images for all services and starts them in the background. It might take a few minutes the first time as it downloads dependencies.
    ```sh
    docker compose up --build -d
    ```

3.  **Download the LLM:**
    Now, tell the running Ollama service to pull our fast language model.
    ```sh
    # Pro-tip: Run 'docker ps' to see the exact container name if it differs.
    docker exec -it voice-marketing-agents-ollama-1 ollama pull tinylama
    ```

4.  **🎉 You're All Set! Explore Your New AI Platform:**
    *   **Agent Management Dashboard:** `http://localhost:3000`
    *   **Backend API Documentation (Swagger UI):** `http://localhost:8000/docs`

---

## 💖 We Need You! How to Contribute to Voice Marketing Agents

Thanks for  showing the insterest , we are open and love the contributions .for a quick start dive into the [open Issues](https://github.com/OpenVoiceX/Voice-Marketing-Agent/issues).
we encourage you to see [Contribution Guide](CONTRIBUTING.md) before geting started.

---

## 🗺️ The Roadmap: From Awesome to Unstoppable

This project is a solid foundation, but our vision is much bigger. Here’s a sneak peek at what's planned.

*   [ ] **Phase 1: The No-Code Revolution**
    *   **Visual Flow Builder:** A `React Flow` canvas to let users visually design call flows.
    *   **Campaign Management UI:** A dedicated section to upload contact lists and schedule call campaigns.

*   [ ] **Phase 2: Supercharged Intelligence**
    *   **Advanced Intent Recognition:** Move beyond simple responses to true intent classification.
    *   **Dynamic Voice Cloning:** Allow users to create a unique voice for their agent.
    *   **CRM Integrations:** Native one-click integrations with platforms like HubSpot and Salesforce.

*   [ ] **Phase 3: Built for Scale**
    *   **Kubernetes & Helm Charts:** Production-grade deployment scripts for auto-scaling on the cloud.
    *   **Comprehensive Analytics Dashboard:** Visualize call success rates, conversation paths, and more.
       

## 🌟 Contributors
Thanks to these wonderful people:

<a href="https://github.com/Hiteshydv001/Voice-Marketing-Agent/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=Hiteshydv001/Voice-Marketing-Agent" />
</a>


## 📜 Code of Conduct

To ensure a welcoming and inclusive environment, we have a Code of Conduct that all contributors are expected to follow. In short: **Be respectful, be kind, and be collaborative.** Please read the full [Code of Conduct](https://github.com/OpenVoiceX/Voice-Marketing-Agent?tab=coc-ov-file) before participating.

---

Thank you again for your interest. We can't wait to see what you build with us!


## 📜 License

This project is freely available under the **MIT License**. See the [Licence](https://github.com/OpenVoiceX/Voice-Marketing-Agent/blob/main/LICENSE) file for more information. <!-- This will be updated as PR is merged -->

---
<div align="center"><p>Built with ❤️ and a lot of coffee for GSSoC'25. Let's give the world a better way to talk to machines.</p>

---
