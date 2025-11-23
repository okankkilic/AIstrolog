# AIstrolog Frontend

Modern, minimalist Türkçe astroloji platformu. Next.js 16 ve Tailwind CSS ile geliştirilmiştir.

## 🎨 Tasarım Özellikleri

### Tipografi
- **Başlıklar**: Khand (Regular) - Hint kökenli, modern ve okunaklı
- **Metinler**: Lora - Serif font, okuma rahatlığı için optimize edilmiş

### Renk Paleti
- **Arkaplan**: `#fdfbf7` (Kırık beyaz, göz yormayan ton)
- **Vurgular**: Siyah/gri tonları (minimalist estetik)

## 🚀 Kurulum ve Çalıştırma

### Kurulum

```bash
npm install
# or
yarn install
```

### Geliştirme

```bash
npm run dev
# or
yarn dev
```

Tarayıcıda [http://localhost:3000](http://localhost:3000) adresini açın.

### Production Build

```bash
npm run build
npm start
```

## 📱 Sayfalar

- **Ana Sayfa** (`/`): Otomatik yönlendirme `/burclar`
- **Burç Seçimi** (`/burclar`): 12 burç kartı grid görünümü
- **Burç Detay** (`/burclar/[sign]/[date]`): 4 kategori (Genel, Aşk, Para, Sağlık)
- **Sıralamalar** (`/siralama`): Backend'den skorlara göre dinamik sıralama
- **Kaynaklar** (`/kaynaklar`): 10 astroloji kaynağı

## 🔌 API Entegrasyonu

Frontend, `http://localhost:8000` adresindeki FastAPI backend ile iletişim kurar.

```typescript
// Burç detay
GET /api/gunluk/{sign}/{date}

// Sıralamalar
GET /api/rankings/{date}
```

## 🎯 Teknoloji Stack

- **Next.js 16**: React framework (App Router)
- **React 19**: UI library
- **TypeScript**: Type safety
- **Tailwind CSS v4**: Utility-first CSS
- **Framer Motion**: Smooth animations
- **Lucide React**: Modern ikon seti

## 📐 Responsive Design

Tüm sayfalar mobil-first yaklaşımla tasarlanmıştır:
- **Mobile**: 320px - 767px
- **Tablet**: 768px - 1023px
- **Desktop**: 1024px+

## 🌐 Deploy on Vercel

En kolay deployment yöntemi [Vercel Platform](https://vercel.com/new) kullanmaktır.

Detaylar için: [Next.js deployment documentation](https://nextjs.org/docs/app/building-your-application/deploying)

## 📚 Daha Fazla Bilgi

- [Next.js Documentation](https://nextjs.org/docs)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [Framer Motion Documentation](https://www.framer.com/motion/)

