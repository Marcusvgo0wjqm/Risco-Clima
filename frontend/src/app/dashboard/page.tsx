'use client';

import React, { useState, useEffect } from 'react';
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { AlertCircle, CheckCircle, AlertTriangle, Clock, FileText } from 'lucide-react';
import apiService from '@/services/api';
import type { DashboardSummary, RiskLevel } from '@/types';

export default function DashboardPage() {
  const [summary, setSummary] = useState<DashboardSummary | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        const response = await apiService.getDashboardSummary();
        setSummary(response.data);
      } catch (err) {
        // Fallback para quando backend não está disponível
        setSummary({
          latest_risk_matrix: null,
          latest_risk_level: null,
          latest_risk_value: null,
          active_alerts_count: 0,
          risk_distribution: {
            baixo: 0,
            moderado: 0,
            alto: 0,
            extremo: 0,
            crítico: 0,
          },
          timestamp: new Date().toISOString(),
        });
        console.log('Backend não conectado - usando dados fallback');
      } finally {
        setLoading(false);
      }
    };

    fetchDashboardData();
    // Recarregar a cada 5 minutos
    const interval = setInterval(fetchDashboardData, 5 * 60 * 1000);
    return () => clearInterval(interval);
  }, []);

  const getRiskColor = (level: RiskLevel | null) => {
    switch (level) {
      case 'baixo':
        return 'text-success-600';
      case 'moderado':
        return 'text-warning-600';
      case 'alto':
        return 'text-danger-600';
      case 'extremo':
        return 'text-danger-700';
      case 'crítico':
        return 'text-danger-900';
      default:
        return 'text-gray-600';
    }
  };

  const getRiskBgColor = (level: RiskLevel | null) => {
    switch (level) {
      case 'baixo':
        return 'bg-success-50 border-success-200';
      case 'moderado':
        return 'bg-warning-50 border-warning-200';
      case 'alto':
        return 'bg-danger-50 border-danger-200';
      case 'extremo':
        return 'bg-danger-100 border-danger-300';
      case 'crítico':
        return 'bg-danger-200 border-danger-400';
      default:
        return 'bg-gray-50 border-gray-200';
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-96">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Carregando dashboard...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-danger-50 border border-danger-200 rounded-lg p-6">
        <AlertCircle className="w-6 h-6 text-danger-600 inline mr-2" />
        <p className="text-danger-700">{error}</p>
      </div>
    );
  }

  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-4xl font-bold text-gray-900">Dashboard Operacional</h1>
        <p className="text-gray-600 mt-2">Avaliação Prospectiva de Risco Climático - Porto Alegre</p>
      </div>

      {/* Backend Not Connected Warning */}
      {summary && (summary as any).message && (
        <div className="bg-warning-50 border border-warning-200 rounded-lg p-4 flex items-start gap-3">
          <AlertCircle className="w-5 h-5 text-warning-600 flex-shrink-0 mt-0.5" />
          <div>
            <p className="text-warning-800 font-medium">Backend não conectado</p>
            <p className="text-warning-700 text-sm mt-1">
              Os dados climáticos não estão disponíveis. Configure o backend para funcionalidade completa.
            </p>
          </div>
        </div>
      )}

      {/* Risk Status Card */}
      {summary && (
        <div className={`border-2 rounded-lg p-8 ${getRiskBgColor(summary.latest_risk_level)}`}>
          <h2 className="text-2xl font-bold mb-4">Situação Atual de Risco</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div>
              <p className="text-gray-600 text-sm font-medium mb-2">Nível de Risco</p>
              <p className={`text-4xl font-bold ${getRiskColor(summary.latest_risk_level)}`}>
                {summary.latest_risk_level?.toUpperCase() || 'N/A'}
              </p>
            </div>
            <div>
              <p className="text-gray-600 text-sm font-medium mb-2">Valor de Risco</p>
              <p className={`text-4xl font-bold ${getRiskColor(summary.latest_risk_level)}`}>
                {summary.latest_risk_value?.toFixed(2) || 'N/A'}
              </p>
            </div>
            <div>
              <p className="text-gray-600 text-sm font-medium mb-2">Alertas Ativos</p>
              <p className="text-4xl font-bold text-primary-600">
                {summary.active_alerts_count}
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Statistics Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-white rounded-lg shadow p-6 border-l-4 border-success-500">
          <p className="text-gray-600 text-sm font-medium">Riscos Baixos</p>
          <p className="text-3xl font-bold text-success-600">
            {summary?.risk_distribution?.['baixo'] || 0}
          </p>
        </div>
        <div className="bg-white rounded-lg shadow p-6 border-l-4 border-warning-500">
          <p className="text-gray-600 text-sm font-medium">Riscos Moderados</p>
          <p className="text-3xl font-bold text-warning-600">
            {summary?.risk_distribution?.['moderado'] || 0}
          </p>
        </div>
        <div className="bg-white rounded-lg shadow p-6 border-l-4 border-danger-500">
          <p className="text-gray-600 text-sm font-medium">Riscos Altos</p>
          <p className="text-3xl font-bold text-danger-600">
            {(summary?.risk_distribution?.['alto'] || 0) +
              (summary?.risk_distribution?.['extremo'] || 0) +
              (summary?.risk_distribution?.['crítico'] || 0)}
          </p>
        </div>
        <div className="bg-white rounded-lg shadow p-6 border-l-4 border-primary-500">
          <p className="text-gray-600 text-sm font-medium">Última Atualização</p>
          <p className="text-lg font-semibold text-primary-600">
            {summary?.timestamp ? new Date(summary.timestamp).toLocaleTimeString('pt-BR') : 'N/A'}
          </p>
        </div>
      </div>

       {/* Quick Action Buttons */}
       <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
         <a
           href="/manual-input"
           className="bg-primary-600 text-white rounded-lg p-6 hover:bg-primary-700 transition flex items-center gap-4"
         >
           <Clock className="w-8 h-8" />
           <div>
             <h3 className="font-semibold">Inserir Dados</h3>
             <p className="text-sm text-primary-100">Adicionar dados manualmente</p>
           </div>
         </a>
         <a
           href="/alerts"
           className="bg-warning-600 text-white rounded-lg p-6 hover:bg-warning-700 transition flex items-center gap-4"
         >
           <AlertTriangle className="w-8 h-8" />
           <div>
             <h3 className="font-semibold">Alertas</h3>
             <p className="text-sm text-warning-100">Ver alertas ativos</p>
           </div>
         </a>
         <a
           href="/audit"
           className="bg-primary-600 text-white rounded-lg p-6 hover:bg-primary-700 transition flex items-center gap-4"
         >
           <AlertCircle className="w-8 h-8" />
           <div>
             <h3 className="font-semibold">Auditoria</h3>
             <p className="text-sm text-primary-100">Ver registro de ações</p>
           </div>
         </a>
       </div>
    </div>
  );
}
