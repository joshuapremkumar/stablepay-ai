export interface Transaction {
  id: string;
  from: string;
  to: string;
  amount: number;
  currency: string;
  type: 'sent' | 'received';
  status: 'pending' | 'completed' | 'flagged' | 'failed';
  timestamp: string;
  txHash: string;
  gasUsed?: string;
  blockNumber?: number;
}

export interface Analytics {
  totalVolume: number;
  averageTransaction: number;
  peakHour: number;
  fraudPrevented: number;
  totalTransactions: number;
  hourlyVolume: number[];
  dailyVolume: number[];
}

export interface PaymentRequest {
  amount: string;
  recipient: string;
  memo?: string;
}

export interface WalletInfo {
  address: string;
  balance: string;
  network: string;
}

export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: string;
}

export interface FraudCheckResult {
  riskScore: number;
  isFlagged: boolean;
  reasons: string[];
}