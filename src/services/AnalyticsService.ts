/**
 * Unified Telemetry & Analytics Service
 */
export class AnalyticsService {
  public static track(eventName: string, properties: Record<string, any> = {}): void {
    const payload = {
      event: eventName,
      properties,
      timestamp: new Date().toISOString(),
      userAgent: typeof navigator !== 'undefined' ? navigator.userAgent : 'unknown'
    };

    console.log(`[TELEMETRY EVENT] ${eventName}`, payload);

    try {
      const existing = JSON.parse(localStorage.getItem('telemetry_events_buffer') || '[]');
      existing.push(payload);
      // Keep last 50 events in offline buffer
      if (existing.length > 50) existing.shift();
      localStorage.setItem('telemetry_events_buffer', JSON.stringify(existing));
    } catch {
      // Ignore storage quota errors
    }
  }
}
