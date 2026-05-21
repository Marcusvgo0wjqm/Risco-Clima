'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { 
  BookOpen, 
  ChevronDown, 
  ChevronUp, 
  ArrowRight, 
  CheckCircle, 
  AlertCircle, 
  BarChart3, 
  FileText, 
  Shield, 
  Zap,
  Calculator,
  Database,
  Bell,
  Search,
  HelpCircle
} from 'lucide-react';

interface FAQItem {
  question: string;
  answer: string;
}

interface MethodologyItem {
  title: string;
  icon: React.ReactNode;
  description: string;
  formula?: string;
  details: string[];
}

interface Step {
  number: number;
  title: string;
  description: string;
  action: string;
  result: string;
}

export default function TutorialPage() {
  const [openFAQ, setOpenFAQ] = useState<number | null>(null);
  const [activeTab, setActiveTab] = useState<'tutorial' | 'methodology' | 'faq'>('tutorial');

  const steps: Step[] = [
    {
      number: 1,
      title: 'Acesso à Plataforma',
      description: 'Faça login no sistema utilizando suas credenciais de acesso.',
      action: 'Acesse o endereço da plataforma e insira seu usuário e senha.',
      result: 'Você será direcionado para o Dashboard principal.'
    },
    {
      number: 2,
      title: 'Inserção de Dados Climáticos',
      description: 'Navegue até a seção "Inserção Manual" para registrar dados de ENSO, precipitação e temperatura.',
      action: 'Clique em "Inserir Dados" no menu lateral ou no Dashboard. Preencha os campos obrigatórios com os dados coletados.',
      result: 'Os dados são salvos e ficam disponíveis para cálculo de risco.'
    },
    {
      number: 3,
      title: 'Avaliação de Impacto',
      description: 'Registre a avaliação de impacto baseada nas condições atuais da região.',
      action: 'Na seção de Impacto, selecione o nível de impacto esperado (1-5) e adicione observações relevantes.',
      result: 'O sistema utiliza esses dados para ajustar o cálculo de risco.'
    },
    {
      number: 4,
      title: 'Capacidade Analítica',
      description: 'Informe o nível de capacidade institucional da equipe para resposta.',
      action: 'Selecione o nível de capacidade analítica (Baixa, Moderada, Alta ou Avançada).',
      result: 'O Fator de Capacidade Analítica (FCA) será aplicado no cálculo final.'
    },
    {
      number: 5,
      title: 'Cálculo Automático de Risco',
      description: 'O sistema calcula automaticamente o Perigo Climático (PC), Probabilidade Ajustada e Risco Final.',
      action: 'Após inserir todos os dados, o cálculo é realizado instantaneamente.',
      result: 'O nível de risco é classificado como Baixo, Moderado, Alto, Extremo ou Crítico.'
    },
    {
      number: 6,
      title: 'Geração de Alertas',
      description: 'Alertas são gerados automaticamente com base no nível de risco calculado.',
      action: 'Verifique a seção de Alertas para visualizar os alertas ativos e suas recomendações.',
      result: 'Equipes podem ser notificadas e ações de prevenção podem ser iniciadas.'
    },
    {
      number: 7,
      title: 'Auditoria e Rastreabilidade',
      description: 'Todas as operações são registradas no log de auditoria com parecer técnico.',
      action: 'Acesse a seção de Auditoria para revisar histórico de operações e justificativas.',
      result: 'Transparência completa e conformidade com protocolos de Defesa Civil.'
    }
  ];

  const methodologies: MethodologyItem[] = [
    {
      title: 'Perigo Climático (PC)',
      icon: <BarChart3 className="w-6 h-6" />,
      description: 'Índice composto que integra os principais fatores climáticos para determinar o potencial de perigo.',
      formula: 'PC = (0,4 × PP) + (0,35 × EN) + (0,25 × OC)',
      details: [
        'PP (Precipitação): Peso de 40% - Principal fator de risco hidrometeorológico',
        'EN (ENSO): Peso de 35% - Índice de oscilação sul que influencia padrões climáticos',
        'OC (Temperatura): Peso de 25% - Anomalias de temperatura que afetam eventos extremos',
        'Os pesos foram definidos com base em estudos climatológicos para a região de Porto Alegre'
      ]
    },
    {
      title: 'Probabilidade Ajustada',
      icon: <Calculator className="w-6 h-6" />,
      description: 'Ajuste da probabilidade base considerando a capacidade institucional de resposta.',
      formula: 'Probabilidade Ajustada = PC × FCA',
      details: [
        'FCA (Fator de Capacidade Analítica) varia de 0,70 a 1,10',
        'Baixa capacidade: FCA = 0,70 (reduz probabilidade por maior incerteza)',
        'Moderada capacidade: FCA = 0,85',
        'Alta capacidade: FCA = 1,00',
        'Avançada capacidade: FCA = 1,10 (aumenta probabilidade por maior confiabilidade dos dados)'
      ]
    },
    {
      title: 'Risco Final',
      icon: <AlertCircle className="w-6 h-6" />,
      description: 'Produto da probabilidade ajustada pelo impacto potencial, resultando no nível de risco.',
      formula: 'Risco = Probabilidade Ajustada × Impacto',
      details: [
        'Impacto é classificado de 1 a 5 baseado em danos potenciais',
        'Resultado varia de 1 a 25',
        'Classificação: Baixo (1-4), Moderado (5-9), Alto (10-14), Extremo (15-19), Crítico (20-25)',
        'Baseado na metodologia Brasiliano adaptada para riscos climáticos'
      ]
    },
    {
      title: 'Sistema de Alertas',
      icon: <Bell className="w-6 h-6" />,
      description: 'Geração automática de alertas baseada no nível de risco calculado.',
      details: [
        'Atenção (Risco Moderado): Monitoramento reforçado',
        'Alerta (Risco Alto): Preparação de equipes de resposta',
        'Alerta Alto (Risco Extremo): Ativação de protocolos de emergência',
        'Extremo (Risco Crítico): Evacuação e ações imediatas de proteção',
        'Alertas possuem vigência e são atualizados automaticamente'
      ]
    },
    {
      title: 'Auditoria e Rastreabilidade',
      icon: <FileText className="w-6 h-6" />,
      description: 'Registro completo de todas as operações com parecer técnico e justificativa.',
      details: [
        'Cada operação gera um registro de auditoria',
        'Parecer técnico do meteorologista é obrigatório',
        'Justificativa operacional documenta decisões',
        'Trilha de auditoria vinculada à matriz de risco',
        'Conformidade com protocolos de governança e transparência'
      ]
    }
  ];

  const faqs: FAQItem[] = [
    {
      question: 'Como são calculados os pesos da fórmula do Perigo Climático?',
      answer: 'Os pesos (40% precipitação, 35% ENSO, 25% temperatura) foram definidos com base em estudos climatológicos específicos para a região de Porto Alegre, considerando a influência histórica de cada fator nos eventos de risco hidrometeorológico.'
    },
    {
      question: 'Posso inserir dados de fontes externas automaticamente?',
      answer: 'Atualmente o sistema suporta inserção manual. A integração com APIs externas (NOAA, INMET, Cemaden) está planejada para a Fase 2 do projeto.'
    },
    {
      question: 'O que acontece quando um alerta expira?',
      answer: 'Alertas expirados são automaticamente marcados como inativos, mas permanecem no histórico para fins de auditoria. O sistema gera novos alertas automaticamente quando os dados de risco são atualizados.'
    },
    {
      question: 'Como é determinado o Fator de Capacidade Analítica (FCA)?',
      answer: 'O FCA é selecionado pelo operador com base na avaliação da capacidade institucional atual. Varia de 0,70 (baixa capacidade) a 1,10 (capacidade avançada), refletindo a confiabilidade dos dados e a capacidade de resposta da equipe.'
    },
    {
      question: 'Posso exportar os dados para relatórios?',
      answer: 'Sim, os dados podem ser exportados em formatos CSV e Excel através da seção de Registros Atuais. Relatórios personalizados estão planejados para versões futuras.'
    },
    {
      question: 'Como funciona o parecer técnico obrigatório?',
      answer: 'O parecer técnico é um campo obrigatório no registro de auditoria onde o meteorologista ou operador responsável documenta a justificativa técnica para as decisões tomadas, garantindo rastreabilidade e conformidade.'
    },
    {
      question: 'Os dados são salvos automaticamente?',
      answer: 'Sim, todos os dados inseridos são salvos imediatamente no banco de dados PostgreSQL. Não há risco de perda de dados por fechamento acidental do navegador.'
    },
    {
      question: 'Como acesso o histórico de operações?',
      answer: 'O histórico completo pode ser acessado através da seção "Auditoria" no menu lateral, onde todas as operações são listadas com data, hora, operador e parecer técnico.'
    }
  ];

  const toggleFAQ = (index: number) => {
    setOpenFAQ(openFAQ === index ? null : index);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-gradient-to-r from-primary-600 to-primary-500 text-white py-12 px-4">
        <div className="max-w-7xl mx-auto">
          <div className="flex items-center gap-3 mb-4">
            <BookOpen className="w-8 h-8" />
            <h1 className="text-4xl font-bold">Central de Ajuda e Tutorial</h1>
          </div>
          <p className="text-xl text-primary-100 max-w-2xl">
            Guia completo para utilização da Plataforma de Avaliação Prospectiva de Risco Climático
          </p>
        </div>
      </div>

      {/* Navigation Tabs */}
      <div className="bg-white border-b border-gray-200 sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4">
          <div className="flex gap-1 overflow-x-auto">
            {[
              { id: 'tutorial' as const, label: 'Passo a Passo', icon: <CheckCircle className="w-5 h-5" /> },
              { id: 'methodology' as const, label: 'Metodologia', icon: <Calculator className="w-5 h-5" /> },
              { id: 'faq' as const, label: 'Dúvidas Frequentes', icon: <HelpCircle className="w-5 h-5" /> }
            ].map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center gap-2 px-6 py-4 font-medium border-b-2 transition whitespace-nowrap ${
                  activeTab === tab.id
                    ? 'border-primary-600 text-primary-600'
                    : 'border-transparent text-gray-600 hover:text-gray-900'
                }`}
              >
                {tab.icon}
                {tab.label}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="max-w-7xl mx-auto px-4 py-12">
        {/* Tutorial Tab */}
        {activeTab === 'tutorial' && (
          <div className="space-y-8">
            <div className="text-center mb-12">
              <h2 className="text-3xl font-bold text-gray-900 mb-4">Tutorial Passo a Passo</h2>
              <p className="text-lg text-gray-600 max-w-2xl mx-auto">
                Siga estas etapas para utilizar a plataforma de forma eficiente
              </p>
            </div>

            <div className="space-y-6">
              {steps.map((step, index) => (
                <div
                  key={step.number}
                  className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden hover:shadow-md transition-shadow"
                >
                  <div className="p-6">
                    <div className="flex items-start gap-4">
                      <div className="flex-shrink-0 w-12 h-12 bg-gradient-to-br from-primary-600 to-primary-500 text-white rounded-full flex items-center justify-center font-bold text-lg">
                        {step.number}
                      </div>
                      <div className="flex-1">
                        <h3 className="text-xl font-semibold text-gray-900 mb-2">{step.title}</h3>
                        <p className="text-gray-600 mb-4">{step.description}</p>
                        
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                          <div className="bg-primary-50 rounded-lg p-4 border border-primary-100">
                            <p className="text-sm font-medium text-primary-700 mb-1">📌 Ação:</p>
                            <p className="text-sm text-primary-600">{step.action}</p>
                          </div>
                          <div className="bg-success-50 rounded-lg p-4 border border-success-100">
                            <p className="text-sm font-medium text-success-700 mb-1">✅ Resultado:</p>
                            <p className="text-sm text-success-600">{step.result}</p>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                  {index < steps.length - 1 && (
                    <div className="flex justify-center py-2">
                      <ArrowRight className="w-6 h-6 text-gray-400 rotate-90" />
                    </div>
                  )}
                </div>
              ))}
            </div>

            <div className="text-center mt-12">
              <Link
                href="/dashboard"
                className="inline-flex items-center gap-2 bg-gradient-to-r from-primary-600 to-primary-500 text-white px-8 py-4 rounded-lg font-semibold hover:from-primary-700 hover:to-primary-600 transition-all duration-300 shadow-lg hover:shadow-xl"
              >
                Acessar Dashboard
                <ArrowRight className="w-5 h-5" />
              </Link>
            </div>
          </div>
        )}

        {/* Methodology Tab */}
        {activeTab === 'methodology' && (
          <div className="space-y-8">
            <div className="text-center mb-12">
              <h2 className="text-3xl font-bold text-gray-900 mb-4">Metodologia Científica</h2>
              <p className="text-lg text-gray-600 max-w-2xl mx-auto">
                Entenda as fórmulas e critérios utilizados para cálculo de risco climático
              </p>
            </div>

            <div className="space-y-6">
              {methodologies.map((method, index) => (
                <div
                  key={index}
                  className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden hover:shadow-md transition-shadow"
                >
                  <div className="p-6">
                    <div className="flex items-start gap-4">
                      <div className="flex-shrink-0 w-12 h-12 bg-gradient-to-br from-primary-100 to-primary-50 text-primary-600 rounded-lg flex items-center justify-center">
                        {method.icon}
                      </div>
                      <div className="flex-1">
                        <h3 className="text-xl font-semibold text-gray-900 mb-2">{method.title}</h3>
                        <p className="text-gray-600 mb-4">{method.description}</p>
                        
                        {method.formula && (
                          <div className="bg-gray-50 rounded-lg p-4 border border-gray-200 mb-4">
                            <p className="text-sm font-medium text-gray-700 mb-2">📐 Fórmula:</p>
                            <code className="text-lg font-mono text-primary-600 bg-primary-50 px-3 py-1 rounded">
                              {method.formula}
                            </code>
                          </div>
                        )}
                        
                        <div className="space-y-2">
                          <p className="text-sm font-medium text-gray-700">📋 Detalhes:</p>
                          <ul className="space-y-1">
                            {method.details.map((detail, i) => (
                              <li key={i} className="text-sm text-gray-600 flex items-start gap-2">
                                <span className="text-primary-500 mt-1">•</span>
                                {detail}
                              </li>
                            ))}
                          </ul>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>

            <div className="bg-warning-50 border border-warning-200 rounded-xl p-6 mt-8">
              <div className="flex items-start gap-3">
                <AlertCircle className="w-6 h-6 text-warning-600 flex-shrink-0 mt-1" />
                <div>
                  <h4 className="font-semibold text-warning-800 mb-2">Nota Importante</h4>
                  <p className="text-sm text-warning-700">
                    A metodologia utilizada é baseada no modelo Brasiliano adaptado para riscos climáticos, 
                    com pesos e fatores calibrados para as condições específicas da região de Porto Alegre. 
                    Os resultados devem ser interpretados como ferramentas de apoio à decisão, não como 
                    previsões determinísticas.
                  </p>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* FAQ Tab */}
        {activeTab === 'faq' && (
          <div className="space-y-8">
            <div className="text-center mb-12">
              <h2 className="text-3xl font-bold text-gray-900 mb-4">Dúvidas Frequentes</h2>
              <p className="text-lg text-gray-600 max-w-2xl mx-auto">
                Encontre respostas para as perguntas mais comuns sobre a plataforma
              </p>
            </div>

            <div className="space-y-4 max-w-3xl mx-auto">
              {faqs.map((faq, index) => (
                <div
                  key={index}
                  className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden hover:shadow-md transition-shadow"
                >
                  <button
                    onClick={() => toggleFAQ(index)}
                    className="w-full flex items-center justify-between p-6 text-left hover:bg-gray-50 transition-colors"
                  >
                    <span className="text-lg font-medium text-gray-900 pr-4">{faq.question}</span>
                    {openFAQ === index ? (
                      <ChevronUp className="w-5 h-5 text-gray-500 flex-shrink-0" />
                    ) : (
                      <ChevronDown className="w-5 h-5 text-gray-500 flex-shrink-0" />
                    )}
                  </button>
                  {openFAQ === index && (
                    <div className="px-6 pb-6 border-t border-gray-100">
                      <p className="text-gray-600 pt-4 leading-relaxed">{faq.answer}</p>
                    </div>
                  )}
                </div>
              ))}
            </div>

            <div className="text-center mt-12 bg-primary-50 rounded-xl p-8 border border-primary-100 max-w-3xl mx-auto">
              <Shield className="w-12 h-12 text-primary-600 mx-auto mb-4" />
              <h3 className="text-xl font-semibold text-gray-900 mb-2">Ainda tem dúvidas?</h3>
              <p className="text-gray-600 mb-6">
                Entre em contato com a equipe de suporte técnico para assistência personalizada
              </p>
              <Link
                href="/dashboard"
                className="inline-flex items-center gap-2 bg-gradient-to-r from-primary-600 to-primary-500 text-white px-6 py-3 rounded-lg font-semibold hover:from-primary-700 hover:to-primary-600 transition-all duration-300"
              >
                Voltar ao Dashboard
                <ArrowRight className="w-5 h-5" />
              </Link>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
