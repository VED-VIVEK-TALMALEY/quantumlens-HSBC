// -------------------------------------------------------------------
// Copyright (c) 2026 Ved Talmaley. All Rights Reserved.
// This project and its source code are strictly proprietary.
// Unauthorized copying, distribution, or use is strictly prohibited.
// -------------------------------------------------------------------

type Props = {
  title: string;
  value: string | number;
  subtitle?: string;
  badge?: string;
  badgeType?: "positive" | "neutral" | "negative" | "hsbc";
  icon?: React.ReactNode;
};

export default function SummaryCard({
  title,
  value,
  subtitle,
  badge,
  badgeType = "neutral",
  icon,
}: Props) {
  const badgeColors = {
    positive: "bg-emerald-500/10 text-emerald-400 border-emerald-500/20",
    negative: "bg-rose-500/10 text-rose-400 border-rose-500/20",
    neutral: "bg-slate-700/30 text-slate-300 border-slate-600/30",
    hsbc: "bg-red-500/10 text-red-400 border-red-500/20",
  };

  return (
    <div className="glass-panel rounded-xl p-5 transition-all duration-200 hover:border-slate-600 hover:shadow-lg hover:shadow-slate-950/40 relative overflow-hidden group">
      {/* Subtle top accent bar */}
      <div className="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-red-600/60 via-indigo-600/40 to-transparent opacity-40 group-hover:opacity-100 transition-opacity" />

      <div className="flex items-center justify-between mb-2">
        <span className="text-xs font-semibold uppercase tracking-wider text-slate-400">
          {title}
        </span>
        {icon && <div className="text-slate-400">{icon}</div>}
      </div>

      <div className="text-2xl lg:text-3xl font-bold tracking-tight text-white mb-2">
        {value}
      </div>

      <div className="flex items-center justify-between text-xs mt-3 pt-2 border-t border-slate-800/80">
        {subtitle && (
          <span className="text-slate-400 truncate max-w-[65%]">
            {subtitle}
          </span>
        )}
        {badge && (
          <span
            className={`px-2 py-0.5 rounded-full font-medium border text-[11px] ml-auto ${badgeColors[badgeType]}`}
          >
            {badge}
          </span>
        )}
      </div>
    </div>
  );
}