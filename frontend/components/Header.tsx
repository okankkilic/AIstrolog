import Link from 'next/link';

export default function Header() {
  return (
    <header className="w-full border-b border-gray-200 bg-white">
      {/* Top Logo Area */}
        <div className="flex flex-col items-center justify-center py-4">
          <div className="flex flex-col items-center gap-2">
            <Link href="/burclar">
              <img src="/logo/logo.png" alt="AIstrolog Logo" className="h-16 w-16 object-contain cursor-pointer" />
            </Link>
            <h1 className="text-5xl font-khand tracking-widest text-black uppercase font-light">AIstrolog</h1>
          </div>
        </div>

      {/* Navigation */}
        <nav className="w-full border-t border-gray-100 py-4">
          <ul className="flex flex-row md:flex-row flex-col md:gap-16 gap-4 justify-center text-xl md:text-xl text-base font-khand tracking-wide uppercase text-gray-600 font-normal">
            <li>
              <Link href="/burclar" className="hover:text-black transition-colors">
                Burç Özetleri
              </Link>
            </li>
            <li>
              <Link href="/kaynaklar" className="hover:text-black transition-colors">
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
