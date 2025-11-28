'use client';

import { useState, useEffect } from 'react';
import { Trophy, Heart, Coins, Activity } from 'lucide-react';
import { motion } from 'framer-motion';
import clsx from 'clsx';
import { fetchRankings } from '@/utils/calculateRankings';

interface SignRanking {
  sign: string;
  slug: string;
  score: number;
}

interface RankingsData {
  general: SignRanking[];
  love: SignRanking[];
  money: SignRanking[];
  health: SignRanking[];
}

type SortKey = 'general' | 'love' | 'money' | 'health';
type Period = 'daily' | 'weekly' | 'yearly';

export default function RankingsPage() {
  const [period, setPeriod] = useState<Period>('daily');
  const [selectedCategory, setSelectedCategory] = useState<SortKey>('general');
  const [rankingsData, setRankingsData] = useState<RankingsData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadRankings = async () => {
      try {
        setLoading(true);
        
        // Try backend first (localhost), fallback to client-side calculation
        const data = await fetchRankings(period, 'http://localhost:8000');
        console.log('Fetched Rankings:', data);
        setRankingsData(data);
      } catch (error) {
        console.error('Error loading rankings:', error);
        setRankingsData(null);
      } finally {
        setLoading(false);
      }
    };

    loadRankings();
  }, [period]);

  // Get current category data
  const currentData = rankingsData ? rankingsData[selectedCategory] : [];

  const handlePeriodChange = (p: Period) => {
    setPeriod(p);
  };

  const categories = [
    { key: 'general', label: 'Genel', icon: Trophy, color: 'text-black', bg: 'bg-gray-100', border: 'border-gray-300' },
    { key: 'love', label: 'Aşk', icon: Heart, color: 'text-black', bg: 'bg-gray-100', border: 'border-gray-300' },
    { key: 'money', label: 'Para', icon: Coins, color: 'text-black', bg: 'bg-gray-100', border: 'border-gray-300' },
    { key: 'health', label: 'Sağlık', icon: Activity, color: 'text-black', bg: 'bg-gray-100', border: 'border-gray-300' },
  ] as const;

  return (
    <>
      <head>
        <title>Burç Sıralamaları - AIstrolog | Astroloji Avantajları</title>
        <meta name="description" content="Yapay zeka analizleriyle oluşturulan burç sıralamaları. Genel, aşk, para ve sağlık kategorilerinde burçların avantaj durumunu keşfedin." />
        <meta name="keywords" content="burç sıralamaları, astroloji, burç avantajları, AIstrolog, genel, aşk, para, sağlık" />
      </head>
      <div className="max-w-xl mx-auto">
      <div className="text-center mb-8">
        <h1 className="text-4xl font-khand font-normal mb-4 uppercase">Burç Sıralamaları</h1>
        <p className="text-gray-600 font-lora">
          Yapay zeka analizlerine göre burçların avantaj durumu.
        </p>
      </div>

      <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
        {/* Controls Header */}
        <div className="p-6 border-b border-gray-100 bg-gray-50/50 flex flex-col gap-6">
          {/* Period Selector */}
          <div className="flex justify-center">
            <div className="flex p-1 bg-gray-200/50 rounded-lg relative">
              {['daily', 'weekly', 'yearly'].map((p) => (
                <button
                  key={p}
                  onClick={() => handlePeriodChange(p as Period)}
                  className={clsx(
                    "relative px-6 py-1.5 rounded-md font-khand font-normal uppercase tracking-wider transition-colors text-sm focus:outline-none",
                    period === p 
                      ? "text-black" 
                      : "text-gray-500 hover:text-gray-700"
                  )}
                >
                  {period === p && (
                    <motion.div
                      layoutId="activePeriod"
                      className="absolute inset-0 bg-white rounded-md shadow-sm"
                      transition={{ type: "spring", bounce: 0.2, duration: 0.6 }}
                      style={{ zIndex: 0 }}
                    />
                  )}
                  <span className="relative z-10">
                    {p === 'daily' ? 'Günlük' : p === 'weekly' ? 'Haftalık' : 'Aylık'}
                  </span>
                </button>
              ))}
            </div>
          </div>

          {/* Category Selector */}
          <div className="flex flex-wrap justify-center gap-2">
            {categories.map(({ key, label, icon: Icon, color, bg, border }) => (
              <button
                key={key}
                onClick={() => setSelectedCategory(key)}
                className={clsx(
                  "flex items-center gap-2 px-4 py-2 rounded-lg border transition-all duration-200 focus:outline-none",
                  selectedCategory === key
                    ? `${bg} ${color} ${border}`
                    : "bg-white text-gray-500 border-transparent hover:bg-gray-50 hover:text-gray-700"
                )}
              >
                <Icon className="w-4 h-4" />
                <span className="font-khand font-normal uppercase tracking-wide text-sm">{label}</span>
              </button>
            ))}
          </div>
        </div>

        {/* List */}
        <div className="flex flex-col">
          {loading ? (
            <div className="flex items-center justify-center py-12">
              <div className="animate-pulse text-gray-400 font-lora">Yükleniyor...</div>
            </div>
          ) : currentData.length > 0 ? (
            currentData.map((row, index) => (
              <div key={row.sign} className="flex items-center p-4 hover:bg-gray-50 transition-colors group border-b border-gray-100 last:border-none">
                <div className="w-16 text-center font-khand font-bold text-2xl text-gray-300 group-hover:text-gray-900 transition-colors">
                  {index + 1}
                </div>
                <div className="flex-1 font-khand font-normal text-xl">
                  {row.sign}
                </div>
              </div>
            ))
          ) : (
            <div className="flex items-center justify-center py-12">
              <div className="text-gray-500 font-lora">
                Sıralama verisi bulunamadı.
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
    </>
  );
}
