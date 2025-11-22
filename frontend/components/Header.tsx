import Link from 'next/link';
import { Sun } from 'lucide-react';

export default function Header() {
  return (
    <header className="w-full border-b border-gray-200 bg-white">
      {/* Top Logo Area */}
      <div className="flex flex-col items-center justify-center py-4">
        <div className="flex flex-col items-center gap-2">
          <Sun className="h-10 w-10 text-black" strokeWidth={1} />
          <h1 className="text-5xl font-khand tracking-widest text-black uppercase font-normal">AIstrolog</h1>
        </div>
      </div>

      {/* Navigation */}
      <nav className="w-full border-t border-gray-100 py-4">
        <ul className="flex justify-center gap-8 text-xl font-khand tracking-wide uppercase text-gray-600 font-normal">
          <li>
            <Link href="/" className="hover:text-black transition-colors">
              Burç Özetleri
            </Link>
          </li>
          <li>
            <Link href="/sources" className="hover:text-black transition-colors">
              Kaynaklar
            </Link>
          </li>
          <li>
            <Link href="/siralama" className="hover:text-black transition-colors">
              Sıralamalar
            </Link>
          </li>
        </ul>
      </nav>
    </header>
  );
}
