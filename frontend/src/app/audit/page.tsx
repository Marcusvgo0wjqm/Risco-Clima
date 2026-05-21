'use client';

import React, { useState, useEffect } from 'react';
import { AlertCircle } from 'lucide-react';
import apiService from '@/services/api';
import type { AuditLog } from '@/types';

export default function AuditPage() {
  const [auditLogs, setAuditLogs] = useState<AuditLog[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchAuditLogs = async () => {
      try {
        // Implementar chamada para obter logs de auditoria
        setAuditLogs([]);
      } catch (err) {
        setError('Erro ao carregar logs de auditoria');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchAuditLogs();
  }, []);

  const getActionLabel = (action: string) => {
    const labels: Record<string, string> = {
      create: 'Criar',
      update: 'Atualizar',
      delete: 'Deletar',
      validate: 'Validar',
    };
    return labels[action] || action;
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-96">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Carregando logs...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Auditoria Analítica</h1>
        <p className="text-gray-600 mt-2">Rastreabilidade de todas as operações do sistema</p>
      </div>

      {error && (
        <div className="bg-danger-50 border border-danger-200 rounded-lg p-4 flex items-center gap-3">
          <AlertCircle className="w-5 h-5 text-danger-600" />
          <p className="text-danger-700">{error}</p>
        </div>
      )}

      {auditLogs.length === 0 ? (
        <div className="bg-gray-50 border border-gray-200 rounded-lg p-8 text-center">
          <p className="text-gray-600">Nenhum registro de auditoria encontrado.</p>
        </div>
      ) : (
        <div className="bg-white rounded-lg shadow overflow-hidden">
          <table className="w-full">
            <thead className="bg-gray-50 border-b">
              <tr>
                <th className="px-6 py-3 text-left text-sm font-semibold text-gray-900">Data/Hora</th>
                <th className="px-6 py-3 text-left text-sm font-semibold text-gray-900">Ação</th>
                <th className="px-6 py-3 text-left text-sm font-semibold text-gray-900">Entidade</th>
                <th className="px-6 py-3 text-left text-sm font-semibold text-gray-900">Usuário</th>
                <th className="px-6 py-3 text-left text-sm font-semibold text-gray-900">Parecer Técnico</th>
              </tr>
            </thead>
            <tbody>
              {auditLogs.map((log) => (
                <tr key={log.id} className="border-b hover:bg-gray-50 transition">
                  <td className="px-6 py-4 text-sm text-gray-900">
                    {new Date(log.timestamp).toLocaleString('pt-BR')}
                  </td>
                  <td className="px-6 py-4 text-sm">
                    <span className="bg-primary-100 text-primary-800 px-3 py-1 rounded-full text-xs font-semibold">
                      {getActionLabel(log.action)}
                    </span>
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-900">{log.entity_type}</td>
                  <td className="px-6 py-4 text-sm text-gray-600">{log.user_id || '-'}</td>
                  <td className="px-6 py-4 text-sm text-gray-600">
                    {log.technical_opinion ? (
                      <span title={log.technical_opinion} className="truncate">
                        {log.technical_opinion}
                      </span>
                    ) : (
                      '-'
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
