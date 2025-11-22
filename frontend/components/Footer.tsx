import Link from 'next/link';

export default function Footer() {
  return (
    <footer className="w-full bg-white py-12 border-t border-gray-200 mt-auto">
      <div className="container mx-auto px-4 flex flex-col items-center gap-8">
        
        {/* Links */}
        <div className="flex flex-wrap justify-center gap-6 text-sm text-gray-600 font-serif">
          <Link href="#" className="hover:text-black">Hakkımızda</Link>
          <Link href="#" className="hover:text-black">Gizlilik Politikası</Link>
          <Link href="#" className="hover:text-black">İletişim</Link>
          <Link href="#" className="hover:text-black">Kullanım Şartları</Link>
        </div>

        {/* Copyright */}
        <div className="text-xs text-gray-400 text-center">
          <p>&copy; {new Date().getFullYear()} AIstrolog. Tüm hakları saklıdır.</p>
          <p className="mt-2">Yapay zeka destekli astroloji analizleri.</p>
        </div>
      </div>
    </footer>
  );
}
