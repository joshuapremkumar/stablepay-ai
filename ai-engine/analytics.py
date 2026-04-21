import numpy as np
import pandas as pd
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


class TransactionAnalytics:
    """Analytics engine for transaction insights and forecasting"""
    
    def __init__(self):
        self.data: List[Dict[str, Any]] = []
        self.features = ['hour', 'day', 'amount', 'gas', 'status']
    
    def add_transaction(self, tx_data: Dict[str, Any]):
        """Add transaction to analytics data"""
        if 'timestamp' in tx_data and isinstance(tx_data['timestamp'], str):
            tx_data['timestamp'] = pd.to_datetime(tx_data['timestamp'])
        
        self.data.append(tx_data)
    
    def get_peak_hours(self) -> Dict[str, Any]:
        """Find peak transaction hours"""
        if not self.data:
            return {'peakHour': 0, 'volume': 0}
        
        df = pd.DataFrame(self.data)
        
        if 'timestamp' not in df.columns:
            return {'peakHour': 12, 'volume': 0}
        
        df['hour'] = pd.to_datetime(df['timestamp']).dt.hour
        
        hourly = df.groupby('hour')['amount'].sum()
        peak_hour = hourly.idxmax() if not hourly.empty else 12
        
        return {
            'peakHour': int(peak_hour),
            'volume': float(hourly.max()) if not hourly.empty else 0,
            'hourlyDistribution': hourly.to_dict()
        }
    
    def get_average_transaction(self) -> float:
        """Calculate average transaction amount"""
        if not self.data:
            return 0.0
        
        df = pd.DataFrame(self.data)
        
        if 'amount' not in df.columns:
            return 0.0
        
        return float(df['amount'].mean())
    
    def get_total_volume(self) -> float:
        """Calculate total transaction volume"""
        if not self.data:
            return 0.0
        
        df = pd.DataFrame(self.data)
        
        if 'amount' not in df.columns:
            return 0.0
        
        return float(df['amount'].sum())
    
    def get_hourly_volume(self) -> List[float]:
        """Get volume distribution by hour"""
        volumes = [0.0] * 24
        
        if not self.data:
            return volumes
        
        df = pd.DataFrame(self.data)
        
        if 'timestamp' not in df.columns:
            return volumes
        
        df['hour'] = pd.to_datetime(df['timestamp']).dt.hour
        
        for _, row in df.iterrows():
            volumes[int(row['hour'])] += row.get('amount', 0)
        
        return volumes
    
    def get_daily_volume(self) -> List[float]:
        """Get volume distribution by day of week"""
        volumes = [0.0] * 7
        
        if not self.data:
            return volumes
        
        df = pd.DataFrame(self.data)
        
        if 'timestamp' not in df.columns:
            return volumes
        
        df['day'] = pd.to_datetime(df['timestamp']).dt.dayofweek
        
        for _, row in df.iterrows():
            volumes[int(row['day'])] += row.get('amount', 0)
        
        return volumes
    
    def get_summary(self) -> Dict[str, Any]:
        """Get complete analytics summary"""
        return {
            'totalVolume': self.get_total_volume(),
            'averageTransaction': self.get_average_transaction(),
            'peakHourData': self.get_peak_hours(),
            'hourlyVolume': self.get_hourly_volume(),
            'dailyVolume': self.get_daily_volume(),
            'totalTransactions': len(self.data)
        }
    
    def predict_next_hour(self, n_hours: int = 1) -> Dict[str, Any]:
        """Simple prediction for next hour(s) using moving average"""
        if len(self.data) < 2:
            return {'predictedVolume': 0, 'confidence': 0}
        
        recent = self.data[-min(10, len(self.data)):]
        
        if not recent:
            return {'predictedVolume': 0, 'confidence': 0}
        
        avg_volume = sum(tx.get('amount', 0) for tx in recent) / len(recent)
        
        return {
            'predictedVolume': round(avg_volume, 2),
            'confidence': min(0.8, len(recent) / 10),
            'basedOnTransactions': len(recent)
        }


class InsightGenerator:
    """Generate AI-powered insights from transaction data"""
    
    def __init__(self):
        self.analytics = TransactionAnalytics()
    
    def analyze_patterns(self, transactions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze transaction patterns and generate insights"""
        
        for tx in transactions:
            self.analytics.add_transaction(tx)
        
        summary = self.analytics.get_summary()
        peak_data = self.analytics.get_peak_hours()
        prediction = self.analytics.predict_next_hour()
        
        insights = self._generate_insights(summary, peak_data)
        
        return {
            'summary': summary,
            'peakHours': peak_data,
            'prediction': prediction,
            'insights': insights
        }
    
    def _generate_insights(self, summary: Dict, peak_data: Dict) -> List[str]:
        """Generate human-readable insights"""
        insights = []
        
        if summary.get('totalVolume', 0) > 10000:
            insights.append('High transaction volume detected - consider scaling infrastructure')
        
        peak_hour = peak_data.get('peakHour', 0)
        if peak_hour >= 18 or peak_hour <= 6:
            insights.append(f'Unusual peak activity at {peak_hour}:00 - verify legitimate traffic')
        
        if summary.get('averageTransaction', 0) > 1000:
            insights.append('Above average transaction value - enhanced monitoring recommended')
        
        if not insights:
            insights.append('Transaction patterns appear normal')
        
        return insights