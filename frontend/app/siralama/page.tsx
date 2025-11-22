'use client';

import { useState, useEffect } from 'react';
import { Trophy, Heart, Coins, Activity } from 'lucide-react';
import clsx from 'clsx';

// Mock Data Generator
const generateData = (period: string) => {
  const signs = ['Koç', 'Boğa', 'İkizler', 'Yengeç', 'Aslan', 'Başak', 'Terazi', 'Akrep', 'Yay', 'Oğlak', 'Kova', 'Balık'];
  return signs.map(sign => ({
    sign,
    general: Math.floor(Math.random() * 40) + 60,
    love: Math.floor(Math.random() * 40) + 60,
    money: Math.floor(Math.random() * 40) + 60,
    health: Math.floor(Math.random() * 40) + 60,
  }));
};

const initialData = () => {
  const signs = ['Koç', 'Boğa', 'İkizler', 'Yengeç', 'Aslan', 'Başak', 'Terazi', 'Akrep', 'Yay', 'Oğlak', 'Kova', 'Balık'];
  return signs.map(sign => ({
    sign,
    general: 0,
    love: 0,
    money: 0,
    health: 0,
  }));
};

type SortKey = 'general' | 'love' | 'money' | 'health';
type Period = 'daily' | 'weekly' | 'yearly';

export default function RankingsPage() {
  const [period, setPeriod] = useState<Period>('daily');
  const [selectedCategory, setSelectedCategory] = useState<SortKey>('general');
  const [data, setData] = useState(initialData());

  useEffect(() => {
    setData(generateData('daily'));
  }, []);

  // Sorting Logic
  const sortedData = [...data].sort((a, b) => b[selectedCategory] - a[selectedCategory]);

  const handlePeriodChange = (p: Period) => {
    setPeriod(p);
    setData(generateData(p)); // Refresh mock data
  };

  const categories: { key: SortKey; label: string; icon: any }[] = [
    { key: 'general', label: 'Genel', icon: Trophy },
    { key: 'love', label: 'Aşk', icon: Heart },
    { key: 'money', label: 'Para', icon: Coins },
    { key: 'health', label: 'Sağlık', icon: Activity },
  ];

  return (
    <div className="max-w-xl mx-auto">
      <div className="text-center mb-8">
        <h1 className="text-4xl font-khand font-normal mb-4 uppercase">Burç Sıralamaları</h1>
        <p className="text-gray-600 font-lora">
          Yapay zeka analizlerine göre burçların puan durumu.
        </p>
      </div>

      {/* Controls Container */}
      <div className="flex flex-col items-center gap-8 mb-12">
        {/* Period Selector */}
        <div className="flex justify-center gap-2 bg-gray-100 p-1.5 rounded-full">
          {['daily', 'weekly', 'yearly'].map((p) => (
            <button
              key={p}
              onClick={() => handlePeriodChange(p as Period)}
              className={clsx(
                "px-6 py-2 rounded-full font-khand font-normal uppercase tracking-wider transition-all text-sm",
                period === p 
                  ? "bg-white text-black shadow-sm" 
                  : "text-gray-500 hover:text-gray-700"
              )}
            >
              {p === 'daily' ? 'Günlük' : p === 'weekly' ? 'Haftalık' : 'Aylık'}
            </button>
          ))}
        </div>

        {/* Category Selector */}
        <div className="flex flex-wrap justify-center gap-3">
          {categories.map(({ key, label, icon: Icon }) => (
            <button
              key={key}
              onClick={() => setSelectedCategory(key)}
              className={clsx(
                "flex items-center gap-2 px-5 py-2.5 rounded-xl border transition-colors duration-200 focus:outline-none",
                selectedCategory === key
                  ? "bg-black text-white border-black shadow-lg"
                  : "bg-white text-gray-600 border-gray-200 hover:border-gray-300 hover:bg-gray-50"
              )}
            >
              <Icon className="w-4 h-4" />
              <span className="font-khand font-normal uppercase tracking-wide">{label}</span>
            </button>
          ))}
        </div>
      </div>

      {/* Single Column Table */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
        <table className="w-full">
          <thead>
            <tr className="bg-gray-50 border-b border-gray-200">
              <th className="p-4 w-20 text-center font-khand font-normal text-gray-500">Sıra</th>
              <th className="p-4 text-left font-khand font-normal text-gray-500">Burç</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-100">
            {sortedData.map((row, index) => (
              <tr key={row.sign} className="hover:bg-gray-50 transition-colors group">
                <td className="p-4 text-center font-khand font-bold text-xl text-gray-400 group-hover:text-black">
                  {index + 1}
                </td>
                <td className="p-4 font-khand font-normal text-xl">
                  {row.sign}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
