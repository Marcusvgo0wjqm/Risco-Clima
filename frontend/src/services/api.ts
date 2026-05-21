import axios, { AxiosInstance } from 'axios';
import type {
  ENSO,
  Precipitation,
  Temperature,
  Impact,
  RiskMatrix,
  Alert,
  AuditLog,
  DashboardSummary,
} from '@/types';

// Em produção (Vercel/Lovable), usa as API routes internas
// Em desenvolvimento, pode usar o backend direto
const isProduction = process.env.NODE_ENV === 'production';
const API_URL = isProduction ? '' : (process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000');

class ApiService {
  private axiosInstance: AxiosInstance;

  constructor() {
    this.axiosInstance = axios.create({
      baseURL: API_URL,
      headers: {
        'Content-Type': 'application/json',
      },
    });
  }

  // Health
  async health() {
    if (isProduction) {
      return { data: { status: 'ok', message: 'Frontend em produção' } };
    }
    return this.axiosInstance.get('/health');
  }

  // ENSO Endpoints
  async getENSO(id: number) {
    return this.axiosInstance.get<ENSO>(`${isProduction ? '/api/proxy/enso' : '/api/enso'}/${id}`);
  }

  async listENSO(skip = 0, limit = 100) {
    return this.axiosInstance.get<ENSO[]>(`${isProduction ? '/api/proxy/enso' : '/api/enso'}/`, {
      params: { skip, limit },
    });
  }

  async createENSO(data: Partial<ENSO>) {
    return this.axiosInstance.post<ENSO>(`${isProduction ? '/api/proxy/enso' : '/api/enso'}/`, data);
  }

  async updateENSO(id: number, data: Partial<ENSO>) {
    return this.axiosInstance.put<ENSO>(`${isProduction ? '/api/proxy/enso' : '/api/enso'}/${id}`, data);
  }

  async deleteENSO(id: number) {
    return this.axiosInstance.delete(`${isProduction ? '/api/proxy/enso' : '/api/enso'}/${id}`);
  }

  // Risk Matrix Endpoints
  async calculateRisk(data: {
    enso_id: number;
    precipitation_id: number;
    temperature_id: number;
    analytical_capacity_id: number;
    impact_id: number;
    forecast_horizon_hours?: number;
    observations?: string;
  }) {
    return this.axiosInstance.post<RiskMatrix>(`${isProduction ? '/api/proxy/risk' : '/api/risk'}/calculate`, data);
  }

  async listRiskMatrices(skip = 0, limit = 100, riskLevel?: string) {
    return this.axiosInstance.get<RiskMatrix[]>(`${isProduction ? '/api/proxy/risk' : '/api/risk'}/`, {
      params: { skip, limit, risk_level: riskLevel },
    });
  }

  async getRiskMatrix(id: number) {
    return this.axiosInstance.get<RiskMatrix>(`${isProduction ? '/api/proxy/risk' : '/api/risk'}/${id}`);
  }

  async getRiskAuditTrail(id: number) {
    return this.axiosInstance.get(`${isProduction ? '/api/proxy/risk' : '/api/risk'}/${id}/audit-trail`);
  }

  // Dashboard - usa API route interna em produção
  async getDashboardSummary() {
    if (isProduction) {
      return this.axiosInstance.get<DashboardSummary>('/api/risk/dashboard');
    }
    return this.axiosInstance.get<DashboardSummary>('/api/risk/dashboard/summary');
  }
}

export default new ApiService();
