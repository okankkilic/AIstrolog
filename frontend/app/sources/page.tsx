import { ExternalLink } from 'lucide-react';

const SOURCES = [
  { name: 'Milliyet', url: 'https://www.milliyet.com.tr/astroloji/', description: 'Türkiye\'nin önde gelen haber sitesinden günlük burç yorumları.' },
  { name: 'Hürriyet', url: 'https://www.hurriyet.com.tr/mahmure/astroloji/', description: 'Mahmure astroloji servisi ile detaylı analizler.' },
  { name: 'Habertürk', url: 'https://www.haberturk.com/astroloji', description: 'Habertürk yazarlarından günlük burç yorumları.' },
  { name: 'Elle', url: 'https://www.elle.com.tr/astroloji', description: 'Moda ve yaşam dergisi Elle\'den astroloji yorumları.' },
  { name: 'Onedio', url: 'https://onedio.com/etiket/astroloji', description: 'Eğlenceli ve samimi bir dille yazılmış burç yorumları.' },
  { name: 'Mynet', url: 'https://www.mynet.com/kadin/burclar-astroloji', description: 'Mynet Astroloji servisi.' },
  { name: 'TwitBurc', url: 'https://twitter.com/twitburc', description: 'Zeynep Turan\'dan günlük yorumlar.' },
  { name: 'Vogue', url: 'https://vogue.com.tr/astroloji', description: 'Vogue Türkiye\'den stil sahibi burç yorumları.' },
  { name: 'GünlükBurç', url: '#', description: 'Diğer popüler kaynaklardan derlemeler.' },
  { name: 'MyBurç', url: '#', description: 'Alternatif astroloji kaynakları.' },
];

export default function SourcesPage() {
  return (
    <div className="max-w-4xl mx-auto">
      <h1 className="text-4xl font-khand font-normal text-center mb-8 uppercase">Kaynaklar</h1>
      <p className="text-center text-gray-600 mb-12 max-w-2xl mx-auto font-lora">
        AIstrolog, günlük burç yorumlarını oluştururken Türkiye'nin en güvenilir astroloji kaynaklarından faydalanır. 
        Aşağıdaki listeden kaynak sitelere doğrudan ulaşabilirsiniz.
      </p>

      <div className="grid md:grid-cols-2 gap-6">
        {SOURCES.map((source) => (
          <a
            key={source.name}
            href={source.url}
            target="_blank"
            rel="noopener noreferrer"
            className="group block bg-white border border-gray-200 rounded-lg p-6 hover:shadow-md transition-all duration-200 hover:border-black"
          >
            <div className="flex justify-between items-start mb-4">
              <h3 className="text-xl font-khand font-normal uppercase group-hover:text-blue-600 transition-colors">
                {source.name}
              </h3>
              <ExternalLink className="w-5 h-5 text-gray-400 group-hover:text-blue-600" />
            </div>
            <p className="text-gray-600 text-sm leading-relaxed font-lora">
              {source.description}
            </p>
            <div className="mt-4 pt-4 border-t border-gray-100 flex items-center gap-2 text-xs text-gray-400 uppercase tracking-wider font-bold">
              <span className="w-2 h-2 rounded-full bg-green-500"></span>
              Aktif Kaynak
            </div>
          </a>
        ))}
      </div>
    </div>
  );
}
