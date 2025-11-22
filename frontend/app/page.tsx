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
    <div className="flex flex-col gap-12">
      {/* Zodiac Grid */}
      <section>
        <div className="text-center mb-12">
          <h2 className="text-3xl font-khand font-normal text-center mb-2 uppercase">Burcunuzu Seçin</h2>
          <p className="text-gray-500 font-lora italic">Günlük yorumunuzu okumak için burcunuza tıklayın.</p>
        </div>
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
          {ZODIAC_SIGNS.map((sign) => (
            <Link
              key={sign.name}
              href={`/${sign.slug}/${dateSlug}`}
              className="group flex flex-col items-center justify-center p-8 rounded-xl border border-gray-100 hover:shadow-xl hover:-translate-y-1 transition-all duration-300 bg-white aspect-square"
            >
              <span className="text-6xl mb-4 group-hover:scale-110 transition-transform duration-300">{sign.symbol}</span>
              <span className="font-khand font-normal text-2xl uppercase tracking-wide">{sign.name}</span>
              <span className="text-sm text-gray-500 font-lora mt-2">{sign.date}</span>
            </Link>
          ))}
        </div>
      </section>
    </div>
  );
}
