import type { Metadata } from "next";
import { Khand, Lora } from "next/font/google";
import "./globals.css";
import Header from "@/components/Header";
import Footer from "@/components/Footer";

const khand = Khand({
  variable: "--font-khand",
  weight: ["300", "400", "500", "600", "700"],
  subsets: ["latin"],
});

const lora = Lora({
  variable: "--font-lora",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "AIstrolog - Günlük Burç Yorumları",
  description: "Yapay zeka destekli günlük burç yorumları ve analizleri.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="tr">
      <body
        className={`${khand.variable} ${lora.variable} antialiased min-h-screen flex flex-col bg-background text-gray-900`}
      >
        <Header />
        <main className="flex-grow container mx-auto px-4 py-8">
          {children}
        </main>
        <Footer />
      </body>
    </html>
  );
}
