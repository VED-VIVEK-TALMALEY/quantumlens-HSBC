# QuantumLens Next.js Analytics Portal

This is the frontend dashboard user interface for the **QuantumLens** platform. It provides interactive visualizations, historical KPI trend tracking, cohort comparisons, and an AI chat assistant interface for query reasoning.

For backend architecture, database tables, or API references, see the root [README.md](../README.md). For detailed modular diagrams, see [architecture.md](../docs/architecture.md).

---

## Technology Stack

- **Framework**: Next.js 15+ (App Router)
- **Library**: React 19+
- **Styling**: TailwindCSS
- **Visualizations**: Recharts / Chart.js
- **API Request Client**: Axios / Fetch API

---

## Project Structure

```text
quantumlens-dashboard/
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
│   ├── MetricCard.tsx             # Stat tiles showing trends & current indicators
│   ├── TimeSeriesChart.tsx        # Line/Bar Recharts diagrams
│   └── ChatWindow.tsx             # Interactive messaging conversation panel
├── services/                      # API integration endpoints wrappers
│   └── api.ts                     # Axios hooks linking to backend routes
├── public/                        # Static brand logo images and icons
├── package.json                   # Client node scripts & dependency lock
├── tailwind.config.ts             # Tailwind layouts & layout settings
└── tsconfig.json                  # Strict TypeScript configuration
```

---

## Getting Started

### Prerequisites
Ensure Node.js 18.x or later is installed.

### Local Development Setup

1. **Install dependencies**:
   ```bash
   npm install
   # or
   yarn install
   # or
   pnpm install
   ```

2. **Configure environment variables**:
   Create a `.env.local` file in the `quantumlens-dashboard/` root folder:
   ```bash
   NEXT_PUBLIC_API_URL=http://localhost:8000
   ```

3. **Start the development server**:
   ```bash
   npm run dev
   # or
   yarn dev
   # or
   pnpm dev
   ```

4. **Verify the installation**:
   Open [http://localhost:3000](http://localhost:3000) in your web browser.

---

## Environment Variables Configuration

| Variable | Description | Default Local | Deployed Production |
| :--- | :--- | :--- | :--- |
| `NEXT_PUBLIC_API_URL` | Complete URL endpoint pointing to the FastAPI backend service. | `http://localhost:8000` | `https://quantumlens-api.render.com` |

---

## Production Deployment (Vercel)

The easiest way to deploy the Next.js app is to link the repository to **Vercel**:
1. Connect Vercel to your GitHub repository.
2. In the dashboard settings, set the **Root Directory** to `quantumlens-dashboard`.
3. Add the environment variable `NEXT_PUBLIC_API_URL` pointing to your live backend Render URL.
4. Click **Deploy**. Vercel will automatically build the static assets, optimize dependencies, and host the dashboard.

---

## Related Documentation
- [Root Readme](../README.md): Backend API endpoints and installation.
- [System Architecture Spec](../docs/architecture.md): Systems layers overview.
- [Database Schema](../docs/data_dictionary.md): Table mappings details.
