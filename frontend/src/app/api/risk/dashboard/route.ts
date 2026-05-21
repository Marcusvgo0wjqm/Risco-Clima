import { NextResponse } from 'next/server';

const API_URL = process.env.API_URL || 'http://localhost:8000';

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const skip = searchParams.get('skip') || '0';
  const limit = searchParams.get('limit') || '100';

  try {
    const response = await fetch(`${API_URL}/api/risk/dashboard/summary?skip=${skip}&limit=${limit}`, {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' },
      cache: 'no-store',
    });

    if (!response.ok) {
      throw new Error(`API error: ${response.status}`);
    }

    const data = await response.json();
    return NextResponse.json(data);
  } catch (error) {
    // Fallback quando backend não está disponível
    return NextResponse.json({
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
      message: 'Backend não conectado. Configure a variável API_URL.',
    }, { status: 200 });
  }
}
