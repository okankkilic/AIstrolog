'use client';

import { useState, use, useEffect } from 'react';
import { Heart, Coins, Activity, Star } from 'lucide-react';
import clsx from 'clsx';
import { notFound } from 'next/navigation';
import { fetchHoroscopeWithFallback } from '@/utils/fetchHoroscope';

const ZODIAC_SIGNS = {
  koc: { name: 'Koç', symbol: '♈', date: '21 Mart - 19 Nisan' },
  boga: { name: 'Boğa', symbol: '♉', date: '20 Nisan - 20 Mayıs' },
  ikizler: { name: 'İkizler', symbol: '♊', date: '21 Mayıs - 20 Haziran' },
  yengec: { name: 'Yengeç', symbol: '♋', date: '21 Haziran - 22 Temmuz' },
  aslan: { name: 'Aslan', symbol: '♌', date: '23 Temmuz - 22 Ağustos' },
  basak: { name: 'Başak', symbol: '♍', date: '23 Ağustos - 22 Eylül' },
  terazi: { name: 'Terazi', symbol: '♎', date: '23 Eylül - 22 Ekim' },
  akrep: { name: 'Akrep', symbol: '♏', date: '23 Ekim - 21 Kasım' },
  yay: { name: 'Yay', symbol: '♐', date: '22 Kasım - 21 Aralık' },
  oglak: { name: 'Oğlak', symbol: '♑', date: '22 Aralık - 19 Ocak' },
  kova: { name: 'Kova', symbol: '♒', date: '20 Ocak - 18 Şubat' },
  balik: { name: 'Balık', symbol: '♓', date: '19 Şubat - 20 Mart' },
};

type Category = 'general' | 'love' | 'money' | 'health';

interface HoroscopeData {
  general: string;
  love: string;
  money: string;
  health: string;
}

export default function ZodiacDetailPage({ params }: { params: Promise<{ sign: string; date: string }> }) {
  const resolvedParams = use(params);
  const { sign, date } = resolvedParams;
  const [activeTab, setActiveTab] = useState<Category>('general');
  const [horoscopeData, setHoroscopeData] = useState<HoroscopeData | null>(null);
  const [loading, setLoading] = useState(true);
  const [actualDate, setActualDate] = useState<string>(date); // Track the actual date of the data

  const zodiac = ZODIAC_SIGNS[sign as keyof typeof ZODIAC_SIGNS];

  if (!zodiac) {
    notFound();
  }

  // Fetch horoscope data with backend fallback
  useEffect(() => {
    const loadHoroscope = async () => {
      try {
        setLoading(true);
        
        // Try backend first (localhost), fallback to JSON
        const result = await fetchHoroscopeWithFallback(
          sign,
          date,
          7,
          'http://localhost:8000'
        );
        
        if (result) {
          setHoroscopeData(result.data);
          setActualDate(result.actualDate);
        } else {
          setHoroscopeData(null);
        }
      } catch (error) {
        console.error('Error loading horoscope:', error);
        setHoroscopeData(null);
      } finally {
        setLoading(false);
      }
    };

    loadHoroscope();
  }, [sign, date]);

  // Format date to "22 Kasım 2025" format
  const formatDate = (dateStr: string) => {
    const months = ['Ocak', 'Şubat', 'Mart', 'Nisan', 'Mayıs', 'Haziran', 'Temmuz', 'Ağustos', 'Eylül', 'Ekim', 'Kasım', 'Aralık'];
    const parts = dateStr.split('-');
    if (parts.length === 3) {
      const day = parseInt(parts[0]);
      const month = parseInt(parts[1]) - 1;
      const year = parts[2];
      return `${day} ${months[month]} ${year}`;
    }
    return dateStr;
  };

  return (
    <>
      <head>
        <title>{`${zodiac.name} Burcu ${formatDate(actualDate)} - AIstrolog`}</title>
        <meta name="description" content={`${zodiac.name} burcu için ${formatDate(actualDate)} tarihli günlük burç yorumu ve astrolojik analizler. AIstrolog ile en güncel burç yorumları.`} />
        <meta name="keywords" content={`${zodiac.name}, ${zodiac.name} burcu, ${formatDate(actualDate)}, burç yorumları, astroloji, AIstrolog`} />
      </head>
      <div className="max-w-6xl mx-auto px-4">
      <div className="flex flex-col md:flex-row gap-6">
        {/* Left Side: Profile */}
        <div className="w-full md:w-1/3">
          <div className="bg-white border border-gray-200 rounded-xl shadow-sm p-8 text-center h-full flex flex-col justify-center">
            <div className="w-48 h-48 md:w-full md:h-auto md:max-w-[18rem] mx-auto mb-6">
              <img 
                src={`/signs/${sign}.png`} 
                alt={zodiac.name}
                className="w-full h-full md:h-auto object-contain"
              />
            </div>
            <h1 className="text-4xl font-khand font-normal mb-2 uppercase">{zodiac.name}</h1>
            <p className="text-gray-400 font-khand text-base">{zodiac.date}</p>
          </div>
        </div>

        {/* Right Side: Categories & Content */}
        <div className="w-full md:w-2/3">
          <div className="bg-white border border-gray-200 rounded-xl shadow-sm overflow-hidden h-full flex flex-col">
            {/* Tabs */}
            <div className="flex border-b border-gray-200">
              <button
                onClick={() => setActiveTab('general')}
                className={clsx(
                  "flex-1 py-4 md:py-5 px-1 md:px-4 text-sm md:text-base font-normal uppercase tracking-wider flex flex-col md:flex-row items-center justify-center gap-1 md:gap-2 transition-colors font-khand",
                  activeTab === 'general' ? "bg-gray-50 text-gray-900 border-b-2 border-gray-900" : "bg-white text-gray-500 hover:bg-gray-50"
                )}
              >
                <Star className="w-4 h-4 md:w-5 md:h-5" /> Genel
              </button>
              <button
                onClick={() => setActiveTab('love')}
                className={clsx(
                  "flex-1 py-4 md:py-5 px-1 md:px-4 text-sm md:text-base font-normal uppercase tracking-wider flex flex-col md:flex-row items-center justify-center gap-1 md:gap-2 transition-colors font-khand",
                  activeTab === 'love' ? "bg-gray-50 text-gray-900 border-b-2 border-gray-900" : "bg-white text-gray-500 hover:bg-gray-50"
                )}
              >
                <Heart className="w-4 h-4 md:w-5 md:h-5" /> Aşk
              </button>
              <button
                onClick={() => setActiveTab('money')}
                className={clsx(
                  "flex-1 py-4 md:py-5 px-1 md:px-4 text-sm md:text-base font-normal uppercase tracking-wider flex flex-col md:flex-row items-center justify-center gap-1 md:gap-2 transition-colors font-khand",
                  activeTab === 'money' ? "bg-gray-50 text-gray-900 border-b-2 border-gray-900" : "bg-white text-gray-500 hover:bg-gray-50"
                )}
              >
                <Coins className="w-4 h-4 md:w-5 md:h-5" /> Para
              </button>
              <button
                onClick={() => setActiveTab('health')}
                className={clsx(
                  "flex-1 py-4 md:py-5 px-1 md:px-4 text-sm md:text-base font-normal uppercase tracking-wider flex flex-col md:flex-row items-center justify-center gap-1 md:gap-2 transition-colors font-khand",
                  activeTab === 'health' ? "bg-gray-50 text-gray-900 border-b-2 border-gray-900" : "bg-white text-gray-500 hover:bg-gray-50"
                )}
              >
                <Activity className="w-4 h-4 md:w-5 md:h-5" /> Sağlık
              </button>
            </div>

            {/* Content */}
            <div className="p-8 md:p-10 flex-1 flex flex-col">
              <div className="flex justify-start mb-6">
                <span className="text-2xl font-khand text-gray-400 uppercase tracking-tighter">
                  {formatDate(actualDate)}
                </span>
              </div>
              
              {loading ? (
                <div className="flex items-center justify-center py-12">
                  <div className="animate-pulse text-gray-400 font-lora">Yükleniyor...</div>
                </div>
              ) : horoscopeData ? (
                <>
                  {activeTab === 'general' && (
                    <div className="animate-in fade-in slide-in-from-bottom-4 duration-500">
                      {/* GÜNCELLENDİ: text-base (mobil) md:text-xl (masaüstü) */}
                      <p className="text-gray-700 leading-relaxed text-base md:text-xl font-lora">
                        {horoscopeData.general || 'Bugün için yorum bulunamadı.'}
                      </p>
                    </div>
                  )}
                  {activeTab === 'love' && (
                    <div className="animate-in fade-in slide-in-from-bottom-4 duration-500">
                      {/* GÜNCELLENDİ: text-base (mobil) md:text-xl (masaüstü) */}
                      <p className="text-gray-700 leading-relaxed text-base md:text-xl font-lora">
                        {horoscopeData.love || 'Bugün için aşk yorumu bulunamadı.'}
                      </p>
                    </div>
                  )}
                  {activeTab === 'money' && (
                    <div className="animate-in fade-in slide-in-from-bottom-4 duration-500">
                       {/* GÜNCELLENDİ: text-base (mobil) md:text-xl (masaüstü) */}
                      <p className="text-gray-700 leading-relaxed text-base md:text-xl font-lora">
                        {horoscopeData.money || 'Bugün için para yorumu bulunamadı.'}
                      </p>
                    </div>
                  )}
                  {activeTab === 'health' && (
                    <div className="animate-in fade-in slide-in-from-bottom-4 duration-500">
                       {/* GÜNCELLENDİ: text-base (mobil) md:text-xl (masaüstü) */}
                      <p className="text-gray-700 leading-relaxed text-base md:text-xl font-lora">
                        {horoscopeData.health || 'Bugün için sağlık yorumu bulunamadı.'}
                      </p>
                    </div>
                  )}
                </>
              ) : (
                <div className="flex items-center justify-center py-12">
                  <div className="text-gray-500 font-lora">
                    Bu tarih için burç yorumu bulunamadı. Lütfen farklı bir tarih seçin.
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
    </>
  );
}
