'use client';

import Link from 'next/link';
import clsx from 'clsx';

const ZODIAC_SIGNS = [
  { name: 'Koç', symbol: '♈', date: '21 Mart - 19 Nisan', slug: 'koc' },
  { name: 'Boğa', symbol: '♉', date: '20 Nisan - 20 Mayıs', slug: 'boga' },
  { name: 'İkizler', symbol: '♊', date: '21 Mayıs - 20 Haziran', slug: 'ikizler' },
  { name: 'Yengeç', symbol: '♋', date: '21 Haziran - 22 Temmuz', slug: 'yengec' },
  { name: 'Aslan', symbol: '♌', date: '23 Temmuz - 22 Ağustos', slug: 'aslan' },
  { name: 'Başak', symbol: '♍', date: '23 Ağustos - 22 Eylül', slug: 'basak' },
  { name: 'Terazi', symbol: '♎', date: '23 Eylül - 22 Ekim', slug: 'terazi' },
  { name: 'Akrep', symbol: '♏', date: '23 Ekim - 21 Kasım', slug: 'akrep' },
  { name: 'Yay', symbol: '♐', date: '22 Kasım - 21 Aralık', slug: 'yay' },
  { name: 'Oğlak', symbol: '♑', date: '22 Aralık - 19 Ocak', slug: 'oglak' },
  { name: 'Kova', symbol: '♒', date: '20 Ocak - 18 Şubat', slug: 'kova' },
  { name: 'Balık', symbol: '♓', date: '19 Şubat - 20 Mart', slug: 'balik' },
];

export default function Home() {
  // Get today's date in DD-MM-YYYY format
  const today = new Date();
  const dateSlug = `${String(today.getDate()).padStart(2, '0')}-${String(today.getMonth() + 1).padStart(2, '0')}-${today.getFullYear()}`;

  return (
    <div className="max-w-5xl mx-auto">
      {/* Zodiac Grid */}
      <section>
        <div className="text-center mb-12">
          <h1 className="text-4xl font-khand font-normal mb-4 uppercase">Burcunuzu Seçin</h1>
          <p className="text-gray-600 font-lora">
            Günlük yorumunuzu okumak için burcunuza tıklayın.
          </p>
        </div>
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4 md:gap-8">
          {ZODIAC_SIGNS.map((sign) => (
            <Link
              key={sign.name}
              href={`/burclar/${sign.slug}/${dateSlug}`}
              className="group flex flex-col bg-white border border-gray-200 rounded-xl p-8 hover:-translate-y-1 transition-all duration-300 items-center text-center"
            >
              <div className="w-50 h-50 mb-6 flex items-center justify-center p-2 group-hover:scale-110 transition-transform duration-300">
                <img 
                  src={`/signs/${sign.slug}.png`} 
                  alt={sign.name}
                  className="max-w-full max-h-full object-contain"
                />
              </div>
              <span className="font-khand font-normal text-2xl uppercase tracking-wide">{sign.name}</span>
              <span className="text-sm text-gray-500 font-lora mt-2">{sign.date}</span>
            </Link>
          ))}
        </div>
      </section>
    </div>
  );
}
