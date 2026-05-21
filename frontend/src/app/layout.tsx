'use client';

import React from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { Cloud } from 'lucide-react';
import '../styles/globals.css';

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const pathname = usePathname();
  const isLandingPage = pathname === '/landing' || pathname === '/';

  return (
    <html lang="pt-BR">
      <head>
        <title>Plataforma de Risco Climático - Porto Alegre</title>
        <meta name="description" content="Avaliação Prospectiva de Risco Climático" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
      </head>
      <body className="bg-gray-50">
        <div className="flex flex-col min-h-screen">
          {!isLandingPage && (
            <header className="bg-gradient-to-r from-primary-900 to-primary-700 text-white shadow-lg sticky top-0 z-50">
              <div className="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
                <Link href="/" className="flex items-center gap-3 hover:opacity-90 transition">
                  <Cloud className="w-8 h-8" />
                  <h1 className="text-2xl font-bold">Clima Risk Platform</h1>
                </Link>
                <nav className="flex gap-6">
                  <Link href="/dashboard" className="hover:text-primary-100 transition">
                    Dashboard
                  </Link>
                  <Link href="/manual-input" className="hover:text-primary-100 transition">
                    Inserir Dados
                  </Link>
                  <Link href="/alerts" className="hover:text-primary-100 transition">
                    Alertas
                  </Link>
                  <Link href="/audit" className="hover:text-primary-100 transition">
                    Auditoria
                  </Link>
                  <Link href="/tutorial" className="hover:text-primary-100 transition">
                    Tutorial
                  </Link>
                </nav>
              </div>
            </header>
          )}

          <main className="flex-1">
            {children}
          </main>

          {!isLandingPage && (
            <footer className="bg-gray-800 text-white py-6 mt-12">
              <div className="max-w-7xl mx-auto px-4 text-center">
                <p>© 2024 Plataforma de Avaliação Prospectiva de Risco Climático - Porto Alegre</p>
              </div>
            </footer>
          )}
        </div>
      </body>
    </html>
  );
}
