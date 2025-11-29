"use client";

import Image from "next/image";
import Link from "next/link";

export default function QRButton() {
    return (
        <Link
            href="https://t.me/aistrolog_daily_bot"
            target="_blank"
            rel="noopener noreferrer"
            className="fixed bottom-8 right-8 z-50 hidden md:flex items-center justify-center transition-all duration-500 ease-in-out w-16 h-16 hover:w-32 hover:h-32 animate-gentle-bounce hover:animate-none"
            aria-label="Chat with AIstrolog Bot on Telegram"
        >
            <div className="relative w-full h-full bg-white rounded-lg shadow-xl overflow-hidden border border-gray-100">
                <Image
                    src="/qr/qr.png"
                    alt="AIstrolog Telegram Bot QR Code"
                    fill
                    className="object-cover"
                    sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
                />
            </div>
        </Link>
    );
}
