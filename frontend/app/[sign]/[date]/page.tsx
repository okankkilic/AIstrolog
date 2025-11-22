'use client';

import { useState, use } from 'react';
import { Heart, Coins, Activity, Star } from 'lucide-react';
import clsx from 'clsx';
import { notFound } from 'next/navigation';

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

export default function ZodiacDetailPage({ params }: { params: Promise<{ sign: string; date: string }> }) {
  const resolvedParams = use(params);
  const { sign, date } = resolvedParams;
  const [activeTab, setActiveTab] = useState<Category>('general');

  const zodiac = ZODIAC_SIGNS[sign as keyof typeof ZODIAC_SIGNS];

  if (!zodiac) {
    notFound();
  }

  return (
    <div className="max-w-4xl mx-auto">
      <section className="bg-white border border-gray-200 rounded-xl shadow-sm overflow-hidden">
        <div className="bg-gray-50 p-8 border-b border-gray-200 text-center">
          <div className="text-8xl mb-6">{zodiac.symbol}</div>
          <h1 className="text-5xl font-khand font-normal mb-4 uppercase">{zodiac.name}</h1>
          <p className="text-xl text-gray-600 font-lora">{date} Günlük Yorum</p>
        </div>

        {/* Tabs */}
        <div className="flex border-b border-gray-200 overflow-x-auto">
          <button
            onClick={() => setActiveTab('general')}
            className={clsx(
              "flex-1 py-6 px-6 text-base font-normal uppercase tracking-wider flex items-center justify-center gap-2 transition-colors whitespace-nowrap font-khand",
              activeTab === 'general' ? "bg-white text-black border-b-4 border-black" : "bg-gray-50 text-gray-500 hover:bg-gray-100"
            )}
          >
            <Star className="w-5 h-5" /> Genel
          </button>
          <button
            onClick={() => setActiveTab('love')}
            className={clsx(
              "flex-1 py-6 px-6 text-base font-normal uppercase tracking-wider flex items-center justify-center gap-2 transition-colors whitespace-nowrap font-khand",
              activeTab === 'love' ? "bg-white text-pink-600 border-b-4 border-pink-600" : "bg-gray-50 text-gray-500 hover:bg-gray-100"
            )}
          >
            <Heart className="w-5 h-5" /> Aşk
          </button>
          <button
            onClick={() => setActiveTab('money')}
            className={clsx(
              "flex-1 py-6 px-6 text-base font-normal uppercase tracking-wider flex items-center justify-center gap-2 transition-colors whitespace-nowrap font-khand",
              activeTab === 'money' ? "bg-white text-green-600 border-b-4 border-green-600" : "bg-gray-50 text-gray-500 hover:bg-gray-100"
            )}
          >
            <Coins className="w-5 h-5" /> Para
          </button>
          <button
            onClick={() => setActiveTab('health')}
            className={clsx(
              "flex-1 py-6 px-6 text-base font-normal uppercase tracking-wider flex items-center justify-center gap-2 transition-colors whitespace-nowrap font-khand",
              activeTab === 'health' ? "bg-white text-blue-600 border-b-4 border-blue-600" : "bg-gray-50 text-gray-500 hover:bg-gray-100"
            )}
          >
            <Activity className="w-5 h-5" /> Sağlık
          </button>
        </div>

        {/* Content */}
        <div className="p-10 min-h-[300px]">
          {activeTab === 'general' && (
            <div className="animate-in fade-in slide-in-from-bottom-4 duration-500">
              <h3 className="text-2xl font-khand font-normal mb-6">Genel Bakış</h3>
              <p className="text-gray-700 leading-relaxed text-xl font-lora">
                Bugün yıldızlar sizin için oldukça parlak. Enerjiniz yüksek ve çevrenizdeki insanları etkileme potansiyeliniz var. 
                Yeni başlangıçlar için harika bir gün olabilir. Kendinize güvenin ve içgüdülerinizi takip edin.
                (Bu bir örnek metindir. Gerçek veriler daha sonra eklenecektir.)
              </p>
            </div>
          )}
          {activeTab === 'love' && (
            <div className="animate-in fade-in slide-in-from-bottom-4 duration-500">
              <h3 className="text-2xl font-khand font-normal mb-6 text-pink-600">Aşk ve İlişkiler</h3>
              <p className="text-gray-700 leading-relaxed text-xl font-lora">
                Partnerinizle romantik anlar yaşayabilirsiniz. Bekar {zodiac.name} burçları için bugün sürpriz bir tanışma olabilir.
                Duygularınızı ifade etmekten çekinmeyin.
              </p>
            </div>
          )}
          {activeTab === 'money' && (
            <div className="animate-in fade-in slide-in-from-bottom-4 duration-500">
              <h3 className="text-2xl font-khand font-normal mb-6 text-green-600">Para ve Kariyer</h3>
              <p className="text-gray-700 leading-relaxed text-xl font-lora">
                Maddi konularda dikkatli olmanız gereken bir gün. Beklenmedik harcamalar çıkabilir ancak uzun vadeli yatırımlar için fırsatlar da var.
              </p>
            </div>
          )}
          {activeTab === 'health' && (
            <div className="animate-in fade-in slide-in-from-bottom-4 duration-500">
              <h3 className="text-2xl font-khand font-normal mb-6 text-blue-600">Sağlık ve Yaşam</h3>
              <p className="text-gray-700 leading-relaxed text-xl font-lora">
                Enerjiniz yüksek olsa da dinlenmeyi ihmal etmeyin. Bol su içmek ve kısa yürüyüşler yapmak size iyi gelecektir.
              </p>
            </div>
          )}
        </div>
      </section>
    </div>
  );
}
