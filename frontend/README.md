# Next.js Analytics Portal (frontend/)

This is the frontend dashboard user interface for the **QuantumLens** platform. It provides interactive visualizations, historical KPI trend tracking, cohort comparisons, and an AI chat assistant interface for query reasoning.

For backend architecture, database tables, or API references, see the root [README.md](../README.md). For detailed modular diagrams, see [architecture.md](../docs/architecture/architecture.md).

---

## Technical Stack Summary

| Layer | Technology | Selected Package / Framework | Purpose |
| :--- | :--- | :--- | :--- |
| **Framework** | Next.js | Next.js 15+ (App Router) | Core application routing, server-side layouts |
| **Library** | React | React 19+ | UI components rendering and state |
| **Styling** | TailwindCSS | TailwindCSS 3.4+ | CSS layout styling framework |
| **Visualizations**| Charting | Recharts / Chart.js | Visual metrics time-series tracking |
| **API Client** | REST Client | Axios / Fetch API | Requests integration to FastAPI backend |

---

## Project Structure Layout

```text
frontend/
├── app/                           # Next.js App Router folders
│   ├── page.tsx                   # Main login & system overview page
│   ├── dashboard/                 # Financial metrics trend analytics workspace
│   │   └── page.tsx
│   ├── chat/                      # Copilot AI chat assistant chat pane
│   │   └── page.tsx
│   ├── layout.tsx                 # Core HTML wrappers, navigations & footers
│   └── globals.css                # Global CSS variables & Tailwind imports
├── components/                    # Reusable visual components
│   ├── ui/                        # Low-level primitive inputs, buttons, tables
│   ├── ai/                        # AI Chat interface components
│   │   └── AIChat.tsx
│   ├── charts/                    # Recharts rendering components
│   │   └── LineChart.tsx
│   ├── dashboard/                 # Dashboard widgets
│   │   └── SummaryCard.tsx
│   ├── layout/                    # Layout sections
│   ├── metrics/                   # Metrics table wrappers
│   └── records/                   # Record wrappers
├── hooks/                         # Custom React Hooks
├── services/                      # API integration endpoints wrappers
│   ├── api.ts                     # Axios client linking to backend routes
│   └── metricService.ts           # CRUD endpoints for metrics querying
└── public/                        # Static brand logo images and icons
```

---

## Getting Started

### Prerequisites Checklist
- [ ] Node.js version 18.x or later installed.
- [ ] Backend API service running (locally or production Render endpoint).

### Setup and Start Tabular Guide

| Step | Phase | Shell Command | Notes |
| :--- | :--- | :--- | :--- |
| **1** | Install Dependencies | `npm install` | Restores NPM modules (React, Recharts, Tailwind). |
| **2** | Configure Environment | `copy .env.example .env.local` | Binds public backend URL endpoint. |
| **3** | Start Dev Server | `npm run dev` | Spins up hot-reloading dev host on [http://localhost:3000](http://localhost:3000). |
| **4** | Build for Production | `npm run build` | Compiles Next.js dashboard into static pages. |
| **5** | Launch Production | `npm run start` | Serves compiled project assets locally. |

---

## Environment Variables Configuration

| Variable Name | Environment | Description | Default Local | Production Deployed |
| :--- | :--- | :--- | :--- | :--- |
| `NEXT_PUBLIC_API_URL` | Client Runtime | Endpoint path targeting the FastAPI backend. | `http://localhost:8000` | `https://quantumlens-api.render.com` |

---

## Production Deployment (Vercel)

| Phase | Deployment Action | Configuration Parameters |
| :--- | :--- | :--- |
| **1** | **Repository Link** | Link the repository on the Vercel Dashboard. |
| **2** | **Root Directory** | Configure the root directory input to target: `frontend` |
| **3** | **Environment Bindings** | Add the Environment Variable `NEXT_PUBLIC_API_URL` pointing to your Render API. |
| **4** | **Deploy** | Click **Deploy** to compile Next.js static pages. |

---

## Related Documentation
* [Root Readme](../README.md): Backend API endpoints and installations.
* [System Architecture Spec](../docs/architecture/architecture.md): Systems layers overview.
* [Database Schema](../docs/features/ingestion/data_dictionary.md): Table mappings details.
