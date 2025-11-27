
# AIstrolog Frontend

Modern, minimalist Türkçe astroloji platformu. Next.js 16, React 19 ve Tailwind CSS ile geliştirilmiştir.

## Tasarım Özellikleri

### Tipografi
- Başlıklar: Khand (Regular)
- Metinler: Lora

### Renk Paleti
- Arkaplan: `#fdfbf7` (Kırık beyaz)
- Vurgular: Siyah/gri tonları

## Kurulum ve Çalıştırma

### Kurulum

```bash
npm install
# veya
yarn install
```

### Geliştirme

```bash
npm run dev
# veya
yarn dev
```

Tarayıcıda [http://localhost:3000](http://localhost:3000) adresini açın.

### Production Build

```bash
npm run build
npm start
```

## Sayfa Yapısı

- Ana Sayfa (`/`): Otomatik olarak `/burclar` sayfasına yönlendirir.
- Burç Seçimi (`/burclar`): 12 burç kartı grid görünümü, her burç için gün seçimi.
- Burç Detay (`/burclar/[sign]/[date]`): 4 kategori (Genel, Aşk, Para, Sağlık), SEO uyumlu dinamik başlık ve meta etiketleri.
- Sıralamalar (`/siralama`): Backend'den alınan skorlara göre dinamik sıralama, kategori ve periyot seçimi.
- Kaynaklar (`/kaynaklar`): 10 astroloji kaynağı, her biri dış bağlantı ve logo ile.

## SEO

Tüm ana sayfalarda dinamik ve SEO uyumlu `<title>` ve `<meta>` etiketleri bulunmaktadır.

## API Entegrasyonu

Frontend, `http://localhost:8000` adresindeki FastAPI backend ile iletişim kurar.

```typescript
// Burç detay
GET /api/gunluk/{sign}/{date}

// Sıralamalar
GET /api/rankings/{date}
```

## Teknolojiler

- Next.js 16 (App Router)
- React 19
- TypeScript
- Tailwind CSS v4
- Framer Motion
- Lucide React

## Responsive Tasarım

Mobil-first yaklaşımla tasarlanmıştır:
- Mobile: 320px - 767px
- Tablet: 768px - 1023px
- Desktop: 1024px+

## Deploy

En kolay deployment için [Vercel Platformu](https://vercel.com/new) kullanılabilir.
Detaylar: [Next.js deployment documentation](https://nextjs.org/docs/app/building-your-application/deploying)

## Daha Fazla Bilgi

- [Next.js Documentation](https://nextjs.org/docs)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [Framer Motion Documentation](https://www.framer.com/motion/)

