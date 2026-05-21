// ENSO
export enum ENSOIndex {
  NEUTRALIDADE = "neutralidade",
  FRACO = "fraco",
  MODERADO = "moderado",
  FORTE = "forte",
  MUITO_FORTE = "muito_forte",
}

export interface ENSO {
  id: number;
  index_value: ENSOIndex;
  tms_anomaly: number;
  source: string;
  date_observed: string;
  created_at: string;
  updated_at: string;
}

// Precipitation
export enum PrecipitationIndex {
  ATE_50 = "até_50",
  DE_51_A_100 = "51-100",
  DE_101_A_150 = "101-150",
  DE_151_A_250 = "151-250",
  ACIMA_250 = "acima_250",
}

export interface Precipitation {
  id: number;
  index_value: PrecipitationIndex;
  accumulated_mm: number;
  hourly_intensity?: number;
  persistence_hours?: number;
  climatological_percentile?: number;
  source: string;
  forecast_date: string;
  created_at: string;
  updated_at: string;
}

// Temperature
export enum TemperatureIndex {
  NORMAL = "normal",
  MAIS_1 = "mais_1",
  MAIS_2 = "mais_2",
  MAIS_3 = "mais_3",
  MAIS_4_PERSISTENTE = "mais_4_persistente",
}

export interface Temperature {
  id: number;
  index_value: TemperatureIndex;
  max_temp: number;
  avg_temp?: number;
  thermal_persistence?: number;
  climatological_anomaly?: number;
  source: string;
  forecast_date: string;
  created_at: string;
  updated_at: string;
}

// Impact
export enum ImpactIndex {
  INSIGNIFICANTE = "insignificante",
  BAIXO = "baixo",
  MODERADO = "moderado",
  SEVERO = "severo",
  CRITICO = "crítico",
}

export interface Impact {
  id: number;
  index_value: ImpactIndex;
  affected_population?: number;
  flood_areas_km2?: number;
  critical_infrastructure_affected?: string;
  service_interruption_hours?: number;
  human_damages?: string;
  economic_damages_usd?: number;
  description?: string;
  date_assessed: string;
  created_at: string;
  updated_at: string;
}

// Risk
export enum RiskLevel {
  BAIXO = "baixo",
  MODERADO = "moderado",
  ALTO = "alto",
  EXTREMO = "extremo",
  CRITICO = "crítico",
}

export interface RiskMatrix {
  id: number;
  climatic_hazard: number;
  adjusted_probability: number;
  final_risk: number;
  risk_level: RiskLevel;
  calculation_timestamp: string;
  forecast_horizon_hours?: number;
  observations?: string;
  created_at: string;
  updated_at: string;
}

// Alert
export enum AlertLevel {
  ATENCAO = "atenção",
  ALERTA = "alerta",
  ALERTA_ALTO = "alerta_alto",
  ALERTA_EXTREMO = "alerta_extremo",
}

export interface Alert {
  id: number;
  risk_matrix_id: number;
  alert_level: AlertLevel;
  title: string;
  description: string;
  is_active: boolean;
  issued_at: string;
  expires_at?: string;
  recipients?: string[];
  created_at: string;
  updated_at: string;
}

// Audit Log
export interface AuditLog {
  id: number;
  risk_matrix_id?: number;
  alert_id?: number;
  user_id?: string;
  action: string;
  entity_type: string;
  changes?: Record<string, any>;
  technical_opinion?: string;
  justification?: string;
  timestamp: string;
}

// Dashboard Summary
export interface DashboardSummary {
  latest_risk_matrix: number | null;
  latest_risk_level: RiskLevel | null;
  latest_risk_value: number | null;
  risk_distribution: Record<string, number>;
  active_alerts_count: number;
  timestamp: string;
}
