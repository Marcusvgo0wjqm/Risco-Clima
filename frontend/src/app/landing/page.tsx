'use client';

import React from 'react';
import Link from 'next/link';
import { 
  Cloud, 
  TrendingUp, 
  AlertCircle, 
  BarChart3, 
  Shield, 
  Zap,
  ArrowRight,
  CheckCircle,
  MapPin
} from 'lucide-react';

export default function LandingPage() {
  const features = [
    {
      icon: AlertCircle,
      title: 'Alertas em Tempo Real',
      description: 'Receba notificações instantâneas de riscos climáticos com precisão de dados'
    },
    {
      icon: BarChart3,
      title: 'Análise Prospectiva',
      description: 'Avalie proativamente riscos climáticos antes que se tornem críticos'
    },
    {
      icon: TrendingUp,
      title: 'Cálculos Automáticos',
      description: 'Matriz de risco Brasiliano adaptada com formulas científicas validadas'
    },
    {
      icon: Shield,
      title: 'Rastreabilidade Completa',
      description: 'Auditoria detalhada de todas as operações com pareceres técnicos'
    },
    {
      icon: Zap,
      title: 'Integração de Dados',
      description: 'Combine dados manuais com cálculos automáticos para maior precisão'
    },
    {
      icon: MapPin,
      title: 'Foco Porto Alegre',
      description: 'Desenvolvido para as condições climáticas específicas da região'
    }
  ];

  const steps = [
    {
      number: '1',
      title: 'Inserir Dados',
      description: 'Registre dados climáticos manualmente ou através de integrações automáticas'
    },
    {
      number: '2',
      title: 'Calcular Risco',
      description: 'O sistema processa os dados e calcula o nível de risco em tempo real'
    },
    {
      number: '3',
      title: 'Gerar Alertas',
      description: 'Alertas são gerados automaticamente conforme o nível de risco detectado'
    },
    {
      number: '4',
      title: 'Acompanhar',
      description: 'Monitore continuamente e mantenha histórico completo de todas as ações'
    }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-50 via-white to-gray-50">
      {/* Hero Section */}
      <section className="relative overflow-hidden px-4 py-20 sm:py-32">
        <div className="absolute inset-0 -z-10">
          <div className="absolute top-0 left-1/4 w-96 h-96 bg-primary-200 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob"></div>
          <div className="absolute bottom-0 right-1/4 w-96 h-96 bg-warning-200 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob animation-delay-2000"></div>
        </div>

        <div className="max-w-7xl mx-auto">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
            {/* Left Content */}
            <div className="space-y-8">
              <div className="inline-flex items-center gap-2 bg-primary-100 text-primary-700 px-4 py-2 rounded-full text-sm font-semibold">
                <Cloud className="w-4 h-4" />
                Porto Alegre, Brasil
              </div>

              <div className="space-y-4">
                <h1 className="text-5xl sm:text-6xl font-bold text-gray-900 leading-tight">
                  Avaliação Prospectiva de
                  <span className="bg-gradient-to-r from-primary-600 to-primary-400 bg-clip-text text-transparent"> Risco Climático</span>
                </h1>
                <p className="text-xl text-gray-600 leading-relaxed">
                  Plataforma inteligente para análise de riscos climáticos com alertas em tempo real, cálculos automáticos e rastreabilidade completa.
                </p>
              </div>

              <div className="flex flex-col sm:flex-row gap-4">
                <Link
                  href="/dashboard"
                  className="inline-flex items-center justify-center gap-2 bg-gradient-to-r from-primary-600 to-primary-500 text-white px-8 py-4 rounded-lg font-semibold hover:from-primary-700 hover:to-primary-600 transition-all duration-300 shadow-lg hover:shadow-xl"
                >
                  Acessar Dashboard
                  <ArrowRight className="w-5 h-5" />
                </Link>
                <a
                  href="#features"
                  className="inline-flex items-center justify-center gap-2 bg-white text-primary-600 border-2 border-primary-200 px-8 py-4 rounded-lg font-semibold hover:bg-primary-50 transition-all duration-300"
                >
                  Saiba Mais
                  <ArrowRight className="w-5 h-5" />
                </a>
              </div>

              {/* Stats */}
              <div className="grid grid-cols-3 gap-4 pt-8">
                <div className="border-l-2 border-primary-600 pl-4">
                  <div className="text-3xl font-bold text-gray-900">8</div>
                  <p className="text-sm text-gray-600">Modelos de Dados</p>
                </div>
                <div className="border-l-2 border-warning-600 pl-4">
                  <div className="text-3xl font-bold text-gray-900">35+</div>
                  <p className="text-sm text-gray-600">Endpoints API</p>
                </div>
                <div className="border-l-2 border-success-600 pl-4">
                  <div className="text-3xl font-bold text-gray-900">4</div>
                  <p className="text-sm text-gray-600">Níveis de Alerta</p>
                </div>
              </div>
            </div>

            {/* Right Visual */}
            <div className="relative h-96 lg:h-full">
              <div className="absolute inset-0 bg-gradient-to-br from-primary-100 to-primary-50 rounded-2xl"></div>
              <div className="absolute inset-4 bg-white rounded-xl shadow-2xl overflow-hidden">
                <div className="h-full flex flex-col items-center justify-center p-8 text-center">
                  <Cloud className="w-24 h-24 text-primary-500 mb-4" />
                  <h3 className="text-xl font-semibold text-gray-900 mb-2">Sistema Inteligente</h3>
                  <p className="text-gray-600">Tecnologia avançada para proteção climática</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-20 px-4 bg-white">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl sm:text-5xl font-bold text-gray-900 mb-4">
              Características Principais
            </h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Tudo que você precisa para gerenciar riscos climáticos com eficiência
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {features.map((feature, index) => (
              <div
                key={index}
                className="group p-8 rounded-xl border border-gray-200 hover:border-primary-300 hover:shadow-lg transition-all duration-300 bg-white hover:bg-gradient-to-br hover:from-primary-50 hover:to-white"
              >
                <div className="mb-4 inline-flex p-3 bg-primary-100 text-primary-600 rounded-lg group-hover:bg-primary-600 group-hover:text-white transition-colors duration-300">
                  <feature.icon className="w-6 h-6" />
                </div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">{feature.title}</h3>
                <p className="text-gray-600">{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section className="py-20 px-4 bg-gray-50">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl sm:text-5xl font-bold text-gray-900 mb-4">
              Como Funciona
            </h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Um processo simples e eficiente em 4 etapas
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {steps.map((step, index) => (
              <div key={index} className="relative">
                <div className="bg-white p-8 rounded-xl shadow-md hover:shadow-lg transition-shadow duration-300">
                  <div className="w-12 h-12 bg-gradient-to-br from-primary-600 to-primary-500 text-white rounded-full flex items-center justify-center font-bold text-lg mb-4">
                    {step.number}
                  </div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-2">{step.title}</h3>
                  <p className="text-gray-600">{step.description}</p>
                </div>

                {/* Arrow between steps */}
                {index < steps.length - 1 && (
                  <div className="hidden lg:flex absolute -right-4 top-1/2 transform -translate-y-1/2 z-10">
                    <ArrowRight className="w-6 h-6 text-primary-600" />
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-4 bg-gradient-to-r from-primary-600 to-primary-500">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-4xl sm:text-5xl font-bold text-white mb-6">
            Comece Agora
          </h2>
          <p className="text-xl text-primary-100 mb-8 max-w-2xl mx-auto">
            Acesse a plataforma de avaliação de risco climático e comece a proteger sua região.
          </p>

          <Link
            href="/dashboard"
            className="inline-flex items-center justify-center gap-2 bg-white text-primary-600 px-8 py-4 rounded-lg font-semibold hover:bg-primary-50 transition-all duration-300 shadow-lg hover:shadow-xl"
          >
            Entrar na Plataforma
            <ArrowRight className="w-5 h-5" />
          </Link>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-gray-300 py-12 px-4">
        <div className="max-w-7xl mx-auto">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
            <div>
              <h3 className="text-white font-semibold mb-4">Plataforma</h3>
              <ul className="space-y-2">
                <li><Link href="/dashboard" className="hover:text-white transition">Dashboard</Link></li>
                <li><Link href="/manual-input" className="hover:text-white transition">Inserir Dados</Link></li>
                <li><Link href="/alerts" className="hover:text-white transition">Alertas</Link></li>
                <li><Link href="/audit" className="hover:text-white transition">Auditoria</Link></li>
                <li><Link href="/tutorial" className="hover:text-white transition">Tutorial</Link></li>
              </ul>
            </div>
            <div>
              <h3 className="text-white font-semibold mb-4">Documentação</h3>
              <ul className="space-y-2">
                <li><a href="http://localhost:8000/docs" target="_blank" rel="noopener noreferrer" className="hover:text-white transition">API Docs</a></li>
                <li><a href="#features" className="hover:text-white transition">Características</a></li>
                <li><a href="#how-it-works" className="hover:text-white transition">Como Funciona</a></li>
              </ul>
            </div>
            <div>
              <h3 className="text-white font-semibold mb-4">Sobre</h3>
              <ul className="space-y-2">
                <li><a href="#" className="hover:text-white transition">Sobre Nós</a></li>
                <li><a href="#" className="hover:text-white transition">Contato</a></li>
                <li><a href="#" className="hover:text-white transition">Suporte</a></li>
              </ul>
            </div>
            <div>
              <h3 className="text-white font-semibold mb-4">Tecnologia</h3>
              <ul className="space-y-2">
                <li>FastAPI + PostgreSQL</li>
                <li>Next.js + React</li>
                <li>Docker + Cloud</li>
              </ul>
            </div>
          </div>

          <div className="border-t border-gray-700 pt-8">
            <div className="flex flex-col md:flex-row items-center justify-between gap-4">
              <p className="text-sm">© 2024 Plataforma de Avaliação Prospectiva de Risco Climático. Todos os direitos reservados.</p>
              <div className="flex gap-6">
                <a href="#" className="text-sm hover:text-white transition">Privacidade</a>
                <a href="#" className="text-sm hover:text-white transition">Termos</a>
                <a href="#" className="text-sm hover:text-white transition">Contato</a>
              </div>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}
