'use client';

import React, { useState, useEffect } from 'react';
import { AlertCircle, AlertTriangle, Bell, CheckCircle } from 'lucide-react';
import apiService from '@/services/api';
import type { Alert } from '@/types';

export default function AlertsPage() {
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchAlerts = async () => {
      try {
        // Esta é uma implementação simplificada
        // Você precisaria implementar um endpoint específico para listar alertas
        setAlerts([]);
      } catch (err) {
        setError('Erro ao carregar alertas');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchAlerts();
  }, []);

  const getAlertColor = (level: string) => {
    switch (level) {
      case 'atenção':
        return 'bg-warning-50 border-warning-500 text-warning-800';
      case 'alerta':
        return 'bg-danger-50 border-danger-500 text-danger-800';
      case 'alerta_alto':
        return 'bg-danger-100 border-danger-700 text-danger-900';
      case 'alerta_extremo':
        return 'bg-danger-200 border-danger-900 text-danger-950';
      default:
        return 'bg-gray-50 border-gray-500 text-gray-800';
    }
  };

  const getAlertIcon = (level: string) => {
    switch (level) {
      case 'atenção':
        return <Bell className="w-6 h-6" />;
      case 'alerta':
        return <AlertCircle className="w-6 h-6" />;
      case 'alerta_alto':
        return <AlertTriangle className="w-6 h-6" />;
      case 'alerta_extremo':
        return <AlertTriangle className="w-6 h-6" />;
      default:
        return <CheckCircle className="w-6 h-6" />;
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-96">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Carregando alertas...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Alertas</h1>
        <p className="text-gray-600 mt-2">Alertas de risco climático ativos</p>
      </div>

      {error && (
        <div className="bg-danger-50 border border-danger-200 rounded-lg p-4 flex items-center gap-3">
          <AlertCircle className="w-5 h-5 text-danger-600" />
          <p className="text-danger-700">{error}</p>
        </div>
      )}

      {alerts.length === 0 ? (
        <div className="bg-success-50 border border-success-200 rounded-lg p-8 text-center">
          <CheckCircle className="w-12 h-12 text-success-600 mx-auto mb-4" />
          <h3 className="text-xl font-semibold text-success-900 mb-2">Nenhum Alerta Ativo</h3>
          <p className="text-success-700">Não há alertas de risco climático ativo no momento.</p>
        </div>
      ) : (
        <div className="space-y-4">
          {alerts.map((alert) => (
            <div
              key={alert.id}
              className={`border-l-4 rounded-lg p-6 ${getAlertColor(alert.alert_level)}`}
            >
              <div className="flex items-start gap-4">
                <div className="flex-shrink-0">
                  {getAlertIcon(alert.alert_level)}
                </div>
                <div className="flex-1">
                  <h3 className="text-lg font-semibold mb-2">{alert.title}</h3>
                  <p className="mb-3">{alert.description}</p>
                  <div className="flex gap-4 text-sm">
                    <span>
                      <strong>Emitido:</strong> {new Date(alert.issued_at).toLocaleString('pt-BR')}
                    </span>
                    {alert.expires_at && (
                      <span>
                        <strong>Expira:</strong> {new Date(alert.expires_at).toLocaleString('pt-BR')}
                      </span>
                    )}
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
