// -------------------------------------------------------------------
// Copyright (c) 2026 Ved Talmaley. All Rights Reserved.
// This project and its source code are strictly proprietary.
// Unauthorized copying, distribution, or use is strictly prohibited.
// -------------------------------------------------------------------

type Props = {
  title: string;
  value: string | number;
};

export default function SummaryCard({ title, value }: Props) {
  return (
    <div className="bg-white/30 backdrop-blur-lg border border-white/20 rounded-xl shadow-lg p-6 transition transform hover:scale-105">
      <div className="text-sm text-gray-800 uppercase tracking-wider opacity-75">
        {title}
      </div>
      <div className="text-3xl font-bold mt-2 text-gray-900">
        {value}
      </div>
    </div>
  );
}
   