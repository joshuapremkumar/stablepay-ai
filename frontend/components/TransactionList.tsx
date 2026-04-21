import { Transaction } from '@/utils/types';
import { ArrowUpRight, ArrowDownLeft, Clock, AlertTriangle } from 'lucide-react';

interface TransactionListProps {
  transactions: Transaction[];
  isLoading: boolean;
}

export default function TransactionList({ transactions, isLoading }: TransactionListProps) {
  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed':
        return 'text-stable-green bg-stable-green/10';
      case 'pending':
        return 'text-yellow-400 bg-yellow-400/10';
      case 'flagged':
        return 'text-red-400 bg-red-400/10';
      default:
        return 'text-gray-400 bg-gray-400/10';
    }
  };

  if (isLoading) {
    return (
      <div className="bg-gray-800/50 backdrop-blur-sm rounded-2xl p-6 border border-gray-700">
        <h2 className="text-lg font-semibold text-white mb-4">Recent Transactions</h2>
        <div className="space-y-4">
          {[1, 2, 3].map((i) => (
            <div key={i} className="animate-pulse flex items-center space-x-4">
              <div className="w-10 h-10 bg-gray-700 rounded-full" />
              <div className="flex-1 space-y-2">
                <div className="h-4 bg-gray-700 rounded w-3/4" />
                <div className="h-3 bg-gray-700 rounded w-1/2" />
              </div>
            </div>
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="bg-gray-800/50 backdrop-blur-sm rounded-2xl p-6 border border-gray-700">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-lg font-semibold text-white">Recent Transactions</h2>
        <span className="text-sm text-gray-400">{transactions.length} transactions</span>
      </div>

      {transactions.length === 0 ? (
        <div className="text-center py-8">
          <Clock className="w-12 h-12 text-gray-600 mx-auto mb-3" />
          <p className="text-gray-400">No transactions yet</p>
        </div>
      ) : (
        <div className="space-y-3">
          {transactions.slice(0, 10).map((tx) => (
            <div
              key={tx.id}
              className="flex items-center justify-between p-3 bg-gray-700/30 rounded-lg hover:bg-gray-700/50 transition-colors"
            >
              <div className="flex items-center space-x-3">
                <div className={`w-10 h-10 rounded-full flex items-center justify-center ${
                  tx.type === 'received' ? 'bg-stable-green/10' : 'bg-primary-500/10'
                }`}>
                  {tx.type === 'received' ? (
                    <ArrowDownLeft className="w-5 h-5 text-stable-green" />
                  ) : (
                    <ArrowUpRight className="w-5 h-5 text-primary-400" />
                  )}
                </div>
                <div>
                  <p className="text-white font-medium">
                    {tx.type === 'received' ? 'Received' : 'Sent'} {tx.amount} MATIC
                  </p>
                  <p className="text-gray-400 text-sm">
                    {tx.type === 'received' ? `From: ${tx.from.slice(0, 6)}...${tx.from.slice(-4)}` : `To: ${tx.to.slice(0, 6)}...${tx.to.slice(-4)}`}
                  </p>
                </div>
              </div>
              <div className="flex flex-col items-end">
                <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(tx.status)}`}>
                  {tx.status}
                </span>
                <span className="text-gray-500 text-xs mt-1">
                  {new Date(tx.timestamp).toLocaleDateString()}
                </span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}