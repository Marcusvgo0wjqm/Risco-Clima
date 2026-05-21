'use client';

import React, { useState } from 'react';
import { Save, AlertCircle } from 'lucide-react';
import apiService from '@/services/api';
import type { ENSOIndex, PrecipitationIndex, TemperatureIndex, ImpactIndex } from '@/types';

export default function ManualInputPage() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);

  const [formData, setFormData] = useState({
    ensoIndex: 'neutralidade' as ENSOIndex,
    tmsAnomaly: 0,
    precipitationIndex: 'até_50' as PrecipitationIndex,
    accumulatedMm: 0,
    temperatureIndex: 'normal' as TemperatureIndex,
    maxTemp: 0,
    impactIndex: 'insignificante' as ImpactIndex,
    observations: '',
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setSuccess(false);

    try {
      // Aqui você faria as chamadas às APIs para criar os registros
      // Este é um exemplo simplificado
      console.log('Dados do formulário:', formData);
      setSuccess(true);
      setTimeout(() => setSuccess(false), 3000);
    } catch (err) {
      setError('Erro ao salvar dados');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: isNaN(Number(value)) ? value : Number(value),
    }));
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Inserção Manual de Dados</h1>
        <p className="text-gray-600 mt-2">Preencha os dados climáticos para gerar nova avaliação de risco</p>
      </div>

      {error && (
        <div className="bg-danger-50 border border-danger-200 rounded-lg p-4 flex items-center gap-3">
          <AlertCircle className="w-5 h-5 text-danger-600" />
          <p className="text-danger-700">{error}</p>
        </div>
      )}

      {success && (
        <div className="bg-success-50 border border-success-200 rounded-lg p-4">
          <p className="text-success-700 font-semibold">Dados salvos com sucesso!</p>
        </div>
      )}

      <form onSubmit={handleSubmit} className="bg-white rounded-lg shadow-lg p-8 space-y-6">
        {/* ENSO Section */}
        <div className="border-b pb-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Índice ENSO</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Classificação ENSO
              </label>
              <select
                name="ensoIndex"
                value={formData.ensoIndex}
                onChange={handleChange}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
              >
                <option value="neutralidade">Neutralidade</option>
                <option value="fraco">Fraco</option>
                <option value="moderado">Moderado</option>
                <option value="forte">Forte</option>
                <option value="muito_forte">Muito Forte</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Anomalia TSM (°C)
              </label>
              <input
                type="number"
                name="tmsAnomaly"
                value={formData.tmsAnomaly}
                onChange={handleChange}
                step="0.1"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
              />
            </div>
          </div>
        </div>

        {/* Precipitation Section */}
        <div className="border-b pb-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Precipitação</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Faixa de Precipitação
              </label>
              <select
                name="precipitationIndex"
                value={formData.precipitationIndex}
                onChange={handleChange}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
              >
                <option value="até_50">Até 50 mm</option>
                <option value="51-100">51-100 mm</option>
                <option value="101-150">101-150 mm</option>
                <option value="151-250">151-250 mm</option>
                <option value="acima_250">&gt;250 mm</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Acumulado Previsto (mm)
              </label>
              <input
                type="number"
                name="accumulatedMm"
                value={formData.accumulatedMm}
                onChange={handleChange}
                step="1"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
              />
            </div>
          </div>
        </div>

        {/* Temperature Section */}
        <div className="border-b pb-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Temperatura</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Anomalia Térmica
              </label>
              <select
                name="temperatureIndex"
                value={formData.temperatureIndex}
                onChange={handleChange}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
              >
                <option value="normal">Normal</option>
                <option value="mais_1">+1°C</option>
                <option value="mais_2">+2°C</option>
                <option value="mais_3">+3°C</option>
                <option value="mais_4_persistente">&gt;+4°C Persistente</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Temperatura Máxima (°C)
              </label>
              <input
                type="number"
                name="maxTemp"
                value={formData.maxTemp}
                onChange={handleChange}
                step="0.1"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
              />
            </div>
          </div>
        </div>

        {/* Impact Section */}
        <div className="border-b pb-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Impacto Esperado</h2>
          <div className="grid grid-cols-1 gap-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Nível de Impacto
              </label>
              <select
                name="impactIndex"
                value={formData.impactIndex}
                onChange={handleChange}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
              >
                <option value="insignificante">Insignificante</option>
                <option value="baixo">Baixo</option>
                <option value="moderado">Moderado</option>
                <option value="severo">Severo</option>
                <option value="crítico">Crítico</option>
              </select>
            </div>
          </div>
        </div>

        {/* Observations Section */}
        <div>
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Observações Técnicas</h2>
          <textarea
            name="observations"
            value={formData.observations}
            onChange={handleChange}
            rows={4}
            placeholder="Adicione observações meteorológicas relevantes..."
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
          />
        </div>

        {/* Submit Button */}
        <div className="flex gap-4">
          <button
            type="submit"
            disabled={loading}
            className="flex items-center gap-2 bg-primary-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-primary-700 transition disabled:opacity-50"
          >
            <Save className="w-5 h-5" />
            {loading ? 'Salvando...' : 'Calcular Risco'}
          </button>
        </div>
      </form>
    </div>
  );
}
