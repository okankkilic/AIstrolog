'use client';

import { useState } from 'react';
import { Trophy, Heart, Coins, Activity, ArrowUpDown } from 'lucide-react';
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

type SortKey = 'general' | 'love' | 'money' | 'health';
type Period = 'daily' | 'weekly' | 'yearly';

export default function RankingsPage() {
  const [period, setPeriod] = useState<Period>('daily');
  const [sortKey, setSortKey] = useState<SortKey>('general');
  const [data, setData] = useState(generateData('daily'));

  // Sorting Logic
  const sortedData = [...data].sort((a, b) => b[sortKey] - a[sortKey]);

  const handleSort = (key: SortKey) => {
    setSortKey(key);
  };

  const handlePeriodChange = (p: Period) => {
    setPeriod(p);
    setData(generateData(p)); // Refresh mock data
  };

  return (
    <div className="max-w-6xl mx-auto">
      <div className="text-center mb-8">
        <h1 className="text-4xl font-khand font-normal mb-4 uppercase">Burç Sıralamaları</h1>
        <p className="text-gray-600 font-lora">
          Yapay zeka analizlerine göre burçların puan durumu.
        </p>
      </div>

      {/* Period Selector */}
      <div className="flex justify-center gap-4 mb-8">
        {['daily', 'weekly', 'yearly'].map((p) => (
          <button
            key={p}
            onClick={() => handlePeriodChange(p as Period)}
            className={clsx(
              "px-6 py-2 rounded-full font-khand font-normal uppercase tracking-wider transition-all",
              period === p 
                ? "bg-black text-white shadow-lg" 
                : "bg-gray-100 text-gray-500 hover:bg-gray-200"
            )}
          >
            {p === 'daily' ? 'Günlük' : p === 'weekly' ? 'Haftalık' : 'Yıllık'}
          </button>
        ))}
      </div>

      {/* Desktop Table */}
      <div className="hidden md:block bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
        <table className="w-full">
          <thead>
            <tr className="bg-gray-50 border-b border-gray-200">
              <th className="p-4 text-left font-khand font-normal text-gray-500">Burç</th>
              {(['general', 'love', 'money', 'health'] as SortKey[]).map((key) => (
                <th 
                  key={key}
                  onClick={() => handleSort(key)}
                  className={clsx(
                    "p-4 text-center font-khand font-normal cursor-pointer transition-colors select-none",
                    sortKey === key ? "text-green-600 bg-green-50" : "text-gray-500 hover:bg-gray-100"
                  )}
                >
                  <div className="flex items-center justify-center gap-2">
                    {key === 'general' && <Trophy className="w-4 h-4" />}
                    {key === 'love' && <Heart className="w-4 h-4" />}
                    {key === 'money' && <Coins className="w-4 h-4" />}
                    {key === 'health' && <Activity className="w-4 h-4" />}
                    <span className="uppercase">{key === 'general' ? 'Genel' : key === 'love' ? 'Aşk' : key === 'money' ? 'Para' : 'Sağlık'}</span>
                    <ArrowUpDown className="w-3 h-3 opacity-50" />
                  </div>
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-100">
            {sortedData.map((row, index) => (
              <tr key={row.sign} className="hover:bg-gray-50 transition-colors">
                <td className="p-4 font-khand font-normal text-lg flex items-center gap-3">
                  {row.sign}
                </td>
                <td className={clsx("p-4 text-center font-normal", sortKey === 'general' && "bg-green-50 text-green-700")}>
                  {sortKey === 'general' && <span className="inline-block w-2 h-2 rounded-full bg-green-500"></span>}
                </td>
                <td className={clsx("p-4 text-center font-normal", sortKey === 'love' && "bg-green-50 text-green-700")}>
                  {sortKey === 'love' && <span className="inline-block w-2 h-2 rounded-full bg-green-500"></span>}
                </td>
                <td className={clsx("p-4 text-center font-normal", sortKey === 'money' && "bg-green-50 text-green-700")}>
                  {sortKey === 'money' && <span className="inline-block w-2 h-2 rounded-full bg-green-500"></span>}
                </td>
                <td className={clsx("p-4 text-center font-normal", sortKey === 'health' && "bg-green-50 text-green-700")}>
                  {sortKey === 'health' && <span className="inline-block w-2 h-2 rounded-full bg-green-500"></span>}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Mobile View (Cards) */}
      <div className="md:hidden space-y-4">
        {sortedData.map((row, index) => (
          <div key={row.sign} className="bg-white p-4 rounded-xl border border-gray-200 shadow-sm">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center gap-3">
                <h3 className="font-khand font-normal text-xl uppercase">{row.sign}</h3>
              </div>
            </div>
            
            <div className="grid grid-cols-4 gap-2 text-center text-sm">
              <div className={clsx("p-2 rounded", sortKey === 'general' ? "bg-green-50 border border-green-100" : "bg-gray-50")}>
                <div className="text-gray-500 text-xs mb-1">Genel</div>
                {sortKey === 'general' && <div className="w-2 h-2 bg-green-500 rounded-full mx-auto"></div>}
              </div>
              <div className={clsx("p-2 rounded", sortKey === 'love' ? "bg-green-50 border border-green-100" : "bg-gray-50")}>
                <div className="text-gray-500 text-xs mb-1">Aşk</div>
                {sortKey === 'love' && <div className="w-2 h-2 bg-green-500 rounded-full mx-auto"></div>}
              </div>
              <div className={clsx("p-2 rounded", sortKey === 'money' ? "bg-green-50 border border-green-100" : "bg-gray-50")}>
                <div className="text-gray-500 text-xs mb-1">Para</div>
                {sortKey === 'money' && <div className="w-2 h-2 bg-green-500 rounded-full mx-auto"></div>}
              </div>
              <div className={clsx("p-2 rounded", sortKey === 'health' ? "bg-green-50 border border-green-100" : "bg-gray-50")}>
                <div className="text-gray-500 text-xs mb-1">Sağlık</div>
                {sortKey === 'health' && <div className="w-2 h-2 bg-green-500 rounded-full mx-auto"></div>}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
