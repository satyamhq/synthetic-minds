<div align="center">

# Synthetic Minds

### *Simulate the world before you change it.*

**Understand what could happen before you make the decision.**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=flat-square)](LICENSE)
[![GitHub Repository](https://img.shields.io/badge/GitHub-satyamhq%2Fsynthetic--minds-181717?style=flat-square&logo=github)](https://github.com/satyamhq/synthetic-minds)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Node.js 18+](https://img.shields.io/badge/Node.js-18%2B-339933?style=flat-square&logo=node.js&logoColor=white)](https://nodejs.org/)
[![Vue 3](https://img.shields.io/badge/Frontend-Vue%203-4FC08D?style=flat-square&logo=vue.js&logoColor=white)](https://vuejs.org/)
[![OpenAI API](https://img.shields.io/badge/LLM-OpenAI%20API-412991?style=flat-square&logo=openai&logoColor=white)](https://platform.openai.com/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=flat-square&logo=docker&logoColor=white)](Dockerfile)

[English](./README.md) | [Documentation](./THIRD_PARTY_NOTICES.md)

</div>

---

## 🌌 Overview

**Synthetic Minds** is an enterprise AI simulation platform for modeling complex human behavior, markets, audiences, and strategic scenarios before high-stakes decisions.

By ingesting unstructured reality seeds (such as market analysis reports, product strategies, regulatory drafts, or scenario briefs), Synthetic Minds reconstructs a high-fidelity digital society populated by autonomous agents with distinct personas, long-term memory, and interactive behavioral logic.

Through an interactive intelligence platform, decision-makers, strategists, and researchers can test interventions, observe emergent community dynamics, and explore counterfactual scenarios in a safe, reproducible simulation environment.

> **Input:** Ingest seed documents (PDF, Markdown, or plain text) and specify your simulation goals in natural language.  
> **Output:** Receive an evidence-backed intelligence report and an interactive, real-time queryable parallel environment.

---

## 💡 Why Synthetic Minds?

Traditional predictive modeling relies on static extrapolation and historical regressions. In complex human systems, however, the most critical phenomena—such as viral adoption, polarization, cascades, and cultural shifts—are **emergent behaviors** stemming from multi-directional interactions between autonomous individuals.

Synthetic Minds bridges this gap by combining:
1. **OpenAI-Powered Intelligence:** Centralized AI decision engine utilizing the official OpenAI API to drive autonomous agent cognition, reflections, and deep ReACT report analysis.
2. **Dynamic GraphRAG & Temporal Memory:** Ingesting seed documents into structured, evolving knowledge graphs via Zep Cloud.
3. **Autonomous Agent Societies:** Instantiating hundreds to thousands of synthetic individuals with verifiable psychographic profiles, distinct incentives, and temporal memory.
4. **Dual-Platform Social Media Sandbox:** Simulating multi-agent communication and propagation across dual platforms (Plaza feed and Topic communities powered by OASIS).
5. **Interactive Report Agents:** Deploying specialized reasoning agents to conduct post-simulation deep attribution, graph path reconstruction, and autonomous agent interviews.

---

## 🚀 Key Capabilities

- **Automated Ontology Generation:** Deep document parsing that extracts entities, relationships, and reality seeds into structured graph schemas.
- **Cognitive Agent Synthesis:** Algorithmic persona synthesis generating diverse professions, sentiment inclinations, activity schedules, and interaction thresholds powered by OpenAI.
- **Dual-Platform Emergence Sandbox:** Concurrent simulation of broadcast channels (feed / timeline) and focused discussions (forums / threads).
- **Temporal Memory & Dynamic Updates:** Real-time persistence of agent actions, sentiment evolutions, and narrative events into GraphRAG memory.
- **Deep ReACT Report Agent:** Multi-round reflection and synthesis utilizing specialized analytical tools:
  - **InsightForge:** Cross-temporal attribution aligning seed documents with emergent simulation states.
  - **PanoramaSearch:** Broad-spectrum graph traversal mapping information cascades and influence topologies.
  - **QuickSearch:** High-throughput sub-query extraction across discrete facts and entity attributes.
  - **Virtual Interviews:** Direct, parallel qualitative interviews with synthetic agents to collect psychological motivations and sentiment nuances.
- **Bilingual Interface (English & Hindi):** Native localization architecture supporting English (primary) and Devanagari Hindi (हिंदी) across the entire application interface.

---

## 🏛 Architecture

```text
                    Synthetic Minds
                          │
                          ▼
                 Simulation Engine
                          │
             ┌────────────┴────────────┐
             ▼                         ▼
       Agent Environment          Report Engine
             │                         │
             └────────────┬────────────┘
                          ▼
                 Synthetic Minds
                    AI Service
                          │
                          ▼
                    OpenAI API
                          │
                          ▼
                  OpenAI Model
```

---

## 🛠 Simulation Workflow

1. **Reality Seed Ingestion (Step 01):** Upload source documents. The platform analyzes document semantics and structures a customized ontology graph in Zep Cloud.
2. **Environment Synthesis (Step 02):** The system generates synthetic personas, activity weights, narrative directions, and community parameters.
3. **Parallel Simulation (Step 03):** Autonomous agents interact concurrently across dual digital platforms, posting, reposting, commenting, and evolving in simulated time.
4. **Intelligence Reporting (Step 04):** The ReACT ReportAgent synthesizes quantitative metrics and qualitative narratives into a structured analytical brief.
5. **Interactive Exploration (Step 05):** Directly query the Report Agent, converse 1-on-1 with any synthetic individual, or broadcast surveys across the simulated population.

---

## 🧩 Example Scenarios

- **Product Launch Sandbox:** Simulate market reception, feature critique, and viral adoption pathways for a new software product before public release.
- **Customer Behavior Dynamics:** Model consumer responses to pricing changes, service modifications, or brand messaging across different demographics.
- **Policy & Community Impact:** Evaluate citizen reactions, misunderstanding vulnerabilities, and communication channels for proposed regulatory changes.
- **Crisis Response & Brand Safety:** Rehearse communication strategies during hypothetical service disruptions or reputational challenges.
- **Fictional Scenario Exploration:** Synthesize rich, autonomous research worlds and observe narrative divergence in creative and strategic thought experiments.

---

## 💻 Installation

### Prerequisites
- **Node.js** >= 18.0.0
- **Python** 3.11 or 3.12
- **uv** (recommended for ultrafast Python package management) or standard `pip`
- **OpenAI API Key** ([platform.openai.com](https://platform.openai.com/api-keys))

### 1. Clone Repository
```bash
git clone https://github.com/satyamhq/synthetic-minds.git
cd synthetic-minds
```

### 2. Install Dependencies

Using `npm` and `uv` (recommended):
```bash
npm run setup:all
```

Or manually:
```bash
# Frontend
cd frontend
npm install
cd ..

# Backend
cd backend
uv sync
cd ..
```

---

## ⚙️ Configuration

Copy `.env.example` to `.env` in the root directory:
```bash
cp .env.example .env
```

Edit `.env` with your API credentials:
```env
# ===== OpenAI API Configuration (Sole LLM Provider) =====
# Get your OpenAI API key from: https://platform.openai.com/api-keys
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o-mini

# ===== Zep Cloud Knowledge Graph Configuration =====
# Used for temporal memory and GraphRAG (sign up at https://app.getzep.com/)
ZEP_API_KEY=your_zep_api_key_here

# ===== Server Configuration =====
SECRET_KEY=synthetic-minds-super-secret-key-change-me
FLASK_HOST=0.0.0.0
FLASK_PORT=5001
FLASK_DEBUG=False
```

### AI Configuration Notes
Synthetic Minds exclusively uses the official **OpenAI API** for all intelligence generation and agent cognition. Configure your preferred OpenAI model using `OPENAI_MODEL` (e.g., `gpt-4o-mini`, `gpt-4o`, `gpt-5.6`).

---

## 🏃 Running Locally

Start both the backend API server and frontend interface concurrently:
```bash
npm run dev
```

The services will be available at:
- **Frontend UI:** `http://localhost:3000` (or `http://localhost:5173`)
- **Backend API:** `http://localhost:5001`
- **Health Check:** `http://localhost:5001/health`

To run services individually:
```bash
# Run backend only
npm run backend

# Run frontend only
npm run frontend
```

---

## 🐳 Docker Deployment

You can build and launch Synthetic Minds using Docker Compose:

```bash
docker compose up -d --build
```

Access the application at `http://localhost:5001`.

---

## 🚀 Render Deployment (Single Web Service)

Synthetic Minds is optimized for one-click deployment on [Render](https://render.com) as a single unified Web Service:

1. **New Web Service:** Connect your `synthetic-minds` GitHub repository.
2. **Configuration:**
   - **Environment:** `Python`
   - **Build Command:** `npm --prefix frontend install && npm --prefix frontend run build && pip install -r requirements.txt`
   - **Start Command:** `gunicorn --bind 0.0.0.0:$PORT --workers 1 --threads 4 --timeout 120 wsgi:app`
   - **Health Check Path:** `/health`
3. **Environment Variables:**
   - `OPENAI_API_KEY`: Your OpenAI API key
   - `ZEP_API_KEY`: Your Zep Cloud API key
   - `SECRET_KEY`: A strong secret key (auto-generated by Render Blueprint)
   - `OPENAI_MODEL`: `gpt-4o-mini` (or your preferred OpenAI model)
   - `FLASK_DEBUG`: `False`

Render will automatically detect `render.yaml` if deploying via Blueprint!

---

## ▲ Vercel Deployment

Synthetic Minds is pre-configured for seamless frontend deployment on [Vercel](https://vercel.com):

1. **Import Repository:** Import `satyamhq/synthetic-minds` into your Vercel dashboard.
2. **Build Settings:**
   - **Framework Preset:** Vite
   - **Build Command:** `npm run build` (defined in root `package.json` to build `frontend/`)
   - **Output Directory:** `frontend/dist`
3. **Environment Variables:**
   - `VITE_API_BASE_URL`: Your backend API URL (e.g., `https://api.yourdomain.com`).
4. **Deploy:** Click **Deploy**. The included `vercel.json` automatically handles SPA routing and asset caching.


---

## 🧪 Testing

Run backend contract and unit test suites:
```bash
cd backend
uv run pytest
```

Run frontend production build verification:
```bash
cd frontend
npm run build
```

---

## 🌐 Localization (English & Hindi)

Synthetic Minds features a centralized internationalization architecture:
- **English (`en`):** Primary language for global users and technical interfaces.
- **Hindi (`hi`):** Secondary language providing natural, modern Devanagari Hindi for all features, dashboards, and agent interactions.

Switch between English and Hindi anytime using the language selector in the navigation bar.

---

## 🤝 Contributing

Contributions to Synthetic Minds are welcome! Please follow these steps:
1. Fork the repository: `https://github.com/satyamhq/synthetic-minds`
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'feat: Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request.

---

## 📄 License & Legal Attribution

### License
Synthetic Minds is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for complete details.

### Upstream Attribution
Synthetic Minds is a derived and rebranded platform originally based on the open-source **MiroFish** project created by 666ghj and contributors ([upstream repository](https://github.com/666ghj/MiroFish)). We gratefully acknowledge their foundational research and engineering contributions.

### Third-Party Notices
This project incorporates or interfaces with open-source frameworks, including:
- **OpenAI Python SDK** (Apache-2.0 License)
- **OASIS** & **CAMEL-AI** (Apache-2.0 License)
- **Zep Cloud SDK** (Apache-2.0 License)
- **Vue.js** & ecosystem (MIT License)
- **D3.js** (ISC License)
- **Flask** & Pallets (BSD-3-Clause License)
- **PyMuPDF** (AGPL-3.0 / Commercial License)

For detailed notices, see [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
