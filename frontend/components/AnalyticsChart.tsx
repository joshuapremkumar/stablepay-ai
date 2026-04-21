import { Analytics } from '@/utils/types';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from 'recharts';

interface AnalyticsChartProps {
  analytics: Analytics | null;
}

export default function AnalyticsChart({ analytics }: AnalyticsChartProps) {
  if (!analytics) {
    return (
      <div className="h-40 flex items-center justify-center">
        <p className="text-gray-500">No analytics data available</p>
      </div>
    );
  }

  const hourlyData = analytics.hourlyVolume.map((value, index) => ({
    hour: `${index}:00`,
    volume: value
  }));

  return (
    <ResponsiveContainer width="100%" height={200}>
      <BarChart data={hourlyData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
        <XAxis
          dataKey="hour"
          tick={{ fill: '#9ca3af', fontSize: 10 }}
          axisLine={{ stroke: '#4b5563' }}
          tickLine={false}
          interval={3}
        />
        <YAxis
          tick={{ fill: '#9ca3af', fontSize: 10 }}
          axisLine={{ stroke: '#4b5563' }}
          tickLine={false}
        />
        <Tooltip
          contentStyle={{
            backgroundColor: '#1f2937',
            border: '1px solid #374151',
            borderRadius: '8px',
            color: '#fff'
          }}
          labelStyle={{ color: '#9ca3af' }}
        />
        <Bar dataKey="volume" radius={[4, 4, 0, 0]}>
          {hourlyData.map((entry, index) => (
            <Cell
              key={`cell-${index}`}
              fill={index === analytics.peakHour ? '#10b981' : '#3b82f6'}
              fillOpacity={0.8}
            />
          ))}
        </Bar>
      </BarChart>
    </ResponsiveContainer>
  );
}