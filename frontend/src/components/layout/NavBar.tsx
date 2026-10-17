"use client";
import Link from "next/link";
import { useState } from "react";

export default function NavBar() {
  const [dark, setDark] = useState(false);

  const toggleTheme = () => {
    setDark(!dark);
    if (typeof document !== "undefined") {
      const html = document.documentElement;
      if (dark) {
        html.classList.remove("dark");
      } else {
        html.classList.add("dark");
      }
    }
  };

  return (
    <nav className="bg-gradient-to-r from-indigo-600 to-purple-600 p-4 shadow-lg sticky top-0 z-10 flex items-center justify-between">
      <h1 className="text-2xl font-bold text-white">QuantumLens</h1>
      <div className="space-x-4 flex items-center">
        <Link href="/" className="text-white hover:underline mr-4">
          Home
        </Link>
        <a href="https://github.com/quantumlens" target="_blank" rel="noopener noreferrer" className="text-white hover:underline mr-4">
          GitHub
        </a>
        <button onClick={toggleTheme} className="px-3 py-1 bg-white bg-opacity-20 rounded hover:bg-opacity-30 transition text-white">
          {dark ? "Light" : "Dark"}
        </button>
      </div>
    </nav>
  );
}
