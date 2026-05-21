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

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

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
    return this.axiosInstance.get('/health');
  }

  // ENSO Endpoints
  async getENSO(id: number) {
    return this.axiosInstance.get<ENSO>(`/api/enso/${id}`);
  }

  async listENSO(skip = 0, limit = 100) {
    return this.axiosInstance.get<ENSO[]>('/api/enso/', {
      params: { skip, limit },
    });
  }

  async createENSO(data: Partial<ENSO>) {
    return this.axiosInstance.post<ENSO>('/api/enso/', data);
  }

  async updateENSO(id: number, data: Partial<ENSO>) {
    return this.axiosInstance.put<ENSO>(`/api/enso/${id}`, data);
  }

  async deleteENSO(id: number) {
    return this.axiosInstance.delete(`/api/enso/${id}`);
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
    return this.axiosInstance.post<RiskMatrix>('/api/risk/calculate', data);
  }

  async listRiskMatrices(skip = 0, limit = 100, riskLevel?: string) {
    return this.axiosInstance.get<RiskMatrix[]>('/api/risk/', {
      params: { skip, limit, risk_level: riskLevel },
    });
  }

  async getRiskMatrix(id: number) {
    return this.axiosInstance.get<RiskMatrix>(`/api/risk/${id}`);
  }

  async getRiskAuditTrail(id: number) {
    return this.axiosInstance.get(`/api/risk/${id}/audit-trail`);
  }

  // Dashboard
  async getDashboardSummary() {
    return this.axiosInstance.get<DashboardSummary>('/api/risk/dashboard/summary');
  }
}

export default new ApiService();
