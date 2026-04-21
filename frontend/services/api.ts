import axios from 'axios';
import { Transaction, Analytics, PaymentRequest } from '@/utils/types';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

export async function getTransactions(): Promise<Transaction[]> {
  const response = await api.get<Transaction[]>('/transactions');
  return response.data;
}

export async function getTransactionById(id: string): Promise<Transaction> {
  const response = await api.get<Transaction>(`/transactions/${id}`);
  return response.data;
}

export async function createPayment(data: PaymentRequest): Promise<{ txHash: string }> {
  const response = await api.post<{ txHash: string }>('/pay', data);
  return response.data;
}

export async function getAnalytics(): Promise<Analytics> {
  const response = await api.get<Analytics>('/analytics');
  return response.data;
}

export async function getWalletBalance(address: string): Promise<string> {
  const response = await api.get<{ balance: string }>(`/wallet/${address}/balance`);
  return response.data.balance;
}

export async function checkFraudRisk(transactionData: {
  amount: number;
  sender: string;
  recipient: string;
}): Promise<{ riskScore: number; isFlagged: boolean }> {
  const response = await api.post<{ riskScore: number; isFlagged: boolean }>(
    '/analytics/fraud-check',
    transactionData
  );
  return response.data;
}

export default api;