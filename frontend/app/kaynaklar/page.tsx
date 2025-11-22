import { ExternalLink } from 'lucide-react';

const SOURCES = [
  { name: 'Milliyet', slug: 'milliyet', url: 'https://www.milliyet.com.tr/astroloji/', description: 'Türkiye\'nin popüler haber sitesinden günlük burç yorumları.' },
  { name: 'Hürriyet', slug: 'hurriyet', format: 'jpg', url: 'https://www.hurriyet.com.tr/mahmure/astroloji/', description: 'Uzman Astrolog Aygül Aydın\'la günlük burç yorumları.' },
  { name: 'Habertürk', slug: 'haberturk', url: 'https://www.haberturk.com/astroloji', description: 'HT Hayat ekibinden günlük burç yorumları.' },
  { name: 'Elele', slug: 'elele', url: 'https://www.elele.com.tr/astroloji/burclar', description: 'Moda ve yaşam dergisi Elele\'den astroloji yorumları.' },
  { name: 'Onedio', slug: 'onedio', format: 'jpg', url: 'https://onedio.com/etiket/astroloji', description: 'Eğlenceli ve samimi bir dille yazılmış burç yorumları.' },
  { name: 'Mynet', slug: 'mynet', url: 'https://www.mynet.com/kadin/burclar-astroloji', description: 'Mynet Astroloji servisi.' },
  { name: 'TwitBurc', slug: 'twitburc', url: 'https://twitburc.com.tr/burclar', description: 'Zeynep Turan\'dan günlük yorumlar.' },
  { name: 'Vogue', slug: 'vogue', url: 'https://vogue.com.tr/astroloji', description: 'Vogue Türkiye\'den stil sahibi burç yorumları.' },
  { name: 'GünlükBurç', slug: 'gunlukburc', url: 'https://www.gunlukburc.net/', description: 'Diğer popüler kaynaklardan derlemeler.' },
  { name: 'MyBurç', slug: 'myburc', format: 'jpg', url: 'https://www.myburc.com/', description: 'Alternatif astroloji kaynakları.' },
];

export default function SourcesPage() {
  return (
    <div className="max-w-5xl mx-auto">
      <div className="text-center mb-12">
        <h1 className="text-4xl font-khand font-normal mb-4 uppercase">Kaynaklar</h1>
        <p className="text-gray-600 font-lora">
          AIstrolog, günlük burç yorumlarını oluştururken Türkiye'nin en güvenilir astroloji kaynaklarından faydalanır.
        </p>
      </div>

      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
        {SOURCES.map((source) => (
          <a
            key={source.name}
            href={source.url}
            target="_blank"
            rel="noopener noreferrer"
            className="group flex flex-col bg-white border border-gray-200 rounded-xl p-8 hover:shadow-xl hover:-translate-y-1 transition-all duration-300 items-center text-center"
          >
            {/* Logo Area - Prominent */}
            <div className="w-full h-24 mb-6 flex items-center justify-center p-2">
               <img 
                  src={`/sources/${source.slug}.${(source as any).format || 'png'}`} 
                  alt={`${source.name} logo`}
                  className="max-w-full max-h-full object-contain filter grayscale group-hover:grayscale-0 transition-all duration-300 opacity-80 group-hover:opacity-100"
                />
            </div>
            
            <div className="flex-1 flex flex-col items-center">
                <div className="flex items-center gap-2 mb-3">
                  <h3 className="text-2xl font-khand font-normal uppercase group-hover:text-blue-600 transition-colors">
                    {source.name}
                  </h3>
                  <ExternalLink className="w-4 h-4 text-gray-400 group-hover:text-blue-600" />
                </div>
                <p className="text-gray-600 text-sm leading-relaxed font-lora mb-4">
                  {source.description}
                </p>
            </div>
            
            <div className="w-full pt-4 border-t border-gray-100 flex justify-center items-center gap-2 text-xs text-gray-400 uppercase tracking-wider font-bold">
              <span className="w-2 h-2 rounded-full bg-green-500"></span>
              Aktif Kaynak
            </div>
          </a>
        ))}
      </div>
    </div>
  );
}
