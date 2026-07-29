# Next.js Analytics Portal (frontend/)

This is the interactive client dashboard for the **QuantumLens** financial intelligence platform. It provides a visual interface for executive strategy, risk observation, and natural language reasoning (AI financial assistant).

For general backend endpoints, models, or database queries, see the [backend/README.md](../backend/README.md).

---

## Technical Stack & Visual Framework

| Layer | Selected Package | Purpose |
| :--- | :--- | :--- |
| **Framework** | Next.js 15+ (App Router) | Core layouts routing and server components. |
| **UI Components** | React 19+ | Dynamic component rendering and hooks state. |
| **Style System** | TailwindCSS 3.4+ | CSS layouts, utility spacing, and theme variables. |
| **Data Graphs** | Recharts / Chart.js | Visual rendering of time-series trend lines. |
| **HTTP Client** | Axios / Fetch | API requests routing to backend routers. |

---

## Interactive Dashboard Views

The Next.js client organizes analytics into five strategic "War Rooms":

### Dashboard 1: Global Banking Pulse
* **Core Metrics**: Net Interest Income (NII), CET1 capital ratio, Return on Tangible Equity (RoTE), liquidity levels, and loan growth rates.
* **Interactivity**: Dynamic regional heatmaps, timeline cross-filtering, and animated trend transitions.

### Dashboard 2: Wealth Migration Observatory
* **Core Metrics**: Asia wealth inflows ($34B in Q1 2026), net new wealth assets ($39B net new money), insurance growth, and HNW capital concentration.
* **Interactivity**: Capital concentration charts and deposit migration flow trackers.

### Dashboard 3: Credit Stress Radar
* **Core Metrics**: Expected Credit Losses (ECL) trends (guidance raised to 45bps), sector-level write-off ratios, and UK securitisation fraud warnings.
* **Interactivity**: Stress scenario models visualizing asset risk propagation under macroeconomic shocks.

### Dashboard 4: Strategic Transformation Tracker
* **Core Metrics**: Asset disposals, simplification cost savings targets ($1.5B), Hang Seng privatization synergies ($0.5B), and capital reallocation programs.
* **Interactivity**: Milestone checklist meters and operational budget analytics charts.

### Dashboard 5: Banking Contagion Network
* **Core Metrics**: Relational risk propagation maps pulling from Neo4j (Middle East Conflict ──► Energy Price Volatility ──► Expected Credit Losses ──► Capital Deterioration).
* **Interactivity**: Interactive node graph visualization showing asset exposure and liquidity dependencies.

---

## Getting Started

### Prerequisites Checklist
- [ ] Node.js version 18.x or later installed.
- [ ] Running instance of the FastAPI backend server.

### Local Development Setup

| Step | Action | Shell Command | Notes |
| :--- | :--- | :--- | :--- |
| **1** | Restore NPM Modules | `npm install` | Restores React, Tailwind, Recharts, and Axios. |
| **2** | Configure Local Env | `copy .env.example .env.local` | Binds public API URL. |
| **3** | Launch Local Host | `npm run dev` | Spins up dev server on [http://localhost:3000](http://localhost:3000). |
| **4** | Compile Build | `npm run build` | Optimizes assets and compiles static paths. |
| **5** | Run Production Mode | `npm run start` | Serves compiled output files. |

---

## Environment Variables Configuration

> [!WARNING]
> Do not commit `.env.local` containing actual backend production URLs. Keep configurations restricted to local variables.

| Variable Name | Environment | Description | Default Local |
| :--- | :--- | :--- | :--- |
| `NEXT_PUBLIC_API_URL` | Client Runtime | HTTP address pointing to the FastAPI backend API server. | `http://localhost:8000` |

---

## Production Deployment (Vercel)

Vercel is the recommended hosting platform for Next.jsApp Router portals. Follow these steps:

| Step | Phase | Vercel Panel Configuration |
| :--- | :--- | :--- |
| **1** | **Import Project** | Connect your GitHub repository to Vercel. |
| **2** | **Root Directory** | Configure directory target override: `frontend` |
| **3** | **Build Commands** | Framework preset: **Next.js**. Keep standard build parameters. |
| **4** | **Environment Variables**| Add `NEXT_PUBLIC_API_URL` pointing to your deployed Render backend API. |
| **5** | **Deploy** | Click **Deploy** to compile Next.js static pages. |

---

## Related Documentation
* [Primary Readme](../README.md): Complete repository layouts.
* [Backend Readme](../backend/README.md): FastAPI REST routing specs.
* [System Architecture Spec](../docs/architecture/architecture.md): Systems layers overview.
