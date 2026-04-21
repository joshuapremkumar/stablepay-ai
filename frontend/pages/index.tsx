import { useState, useEffect } from 'react';
import Head from 'next/head';
import { QRCodeSVG } from 'qrcode.react';
import { Wallet, Send, Shield, TrendingUp, Clock, DollarSign, AlertTriangle } from 'lucide-react';
import { formatEther } from 'ethers';
import PaymentModal from '@/components/PaymentModal';
import TransactionList from '@/components/TransactionList';
import AnalyticsChart from '@/components/AnalyticsChart';
import { getTransactions, getAnalytics, createPayment } from '@/services/api';
import { Transaction, Analytics } from '@/utils/types';

export default function Home() {
  const [walletAddress, setWalletAddress] = useState<string>('');
  const [balance, setBalance] = useState<string>('0');
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const [analytics, setAnalytics] = useState<Analytics | null>(null);
  const [isPaymentModalOpen, setIsPaymentModalOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [paymentAmount, setPaymentAmount] = useState<string>('');

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const [txData, analyticsData] = await Promise.all([
        getTransactions(),
        getAnalytics()
      ]);
      setTransactions(txData);
      setAnalytics(analyticsData);
      setWalletAddress('0x742d35Cc6634C0532925a3b844Bc9e7595f4f1E2');
      setBalance('2.5');
    } catch (error) {
      console.error('Error loading data:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handlePayment = async (amount: string, recipient: string) => {
    try {
      await createPayment({ amount, recipient });
      await loadData();
      setIsPaymentModalOpen(false);
      setPaymentAmount('');
    } catch (error) {
      console.error('Payment failed:', error);
      throw error;
    }
  };

  const qrData = JSON.stringify({
    address: walletAddress,
    amount: paymentAmount,
    network: 'polygon'
  });

  return (
    <>
      <Head>
        <title>StablePay AI - Dashboard</title>
      </Head>

      <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900">
        <nav className="border-b border-gray-700 bg-gray-800/50 backdrop-blur-lg">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between items-center h-16">
              <div className="flex items-center space-x-2">
                <div className="w-8 h-8 bg-primary-500 rounded-lg flex items-center justify-center">
                  <DollarSign className="w-5 h-5 text-white" />
                </div>
                <span className="text-xl font-bold text-white">StablePay AI</span>
              </div>
              <div className="flex items-center space-x-4">
                <div className="flex items-center space-x-2 bg-gray-700/50 px-4 py-2 rounded-lg">
                  <Wallet className="w-4 h-4 text-primary-400" />
                  <span className="text-sm text-gray-300 font-mono">
                    {walletAddress.slice(0, 6)}...{walletAddress.slice(-4)}
                  </span>
                </div>
                <div className="text-sm font-semibold text-stable-green">
                  {balance} MATIC
                </div>
              </div>
            </div>
          </div>
        </nav>

        <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            <div className="lg:col-span-2 space-y-8">
              <div className="bg-gray-800/50 backdrop-blur-sm rounded-2xl p-6 border border-gray-700">
                <h2 className="text-lg font-semibold text-white mb-4">Quick Actions</h2>
                <div className="grid grid-cols-2 gap-4">
                  <button
                    onClick={() => setIsPaymentModalOpen(true)}
                    className="flex items-center justify-center space-x-2 bg-primary-600 hover:bg-primary-700 text-white py-4 px-6 rounded-xl transition-all"
                  >
                    <Send className="w-5 h-5" />
                    <span>Send Payment</span>
                  </button>
                  <button className="flex items-center justify-center space-x-2 bg-gray-700 hover:bg-gray-600 text-white py-4 px-6 rounded-xl transition-all">
                    <Wallet className="w-5 h-5" />
                    <span>Connect Wallet</span>
                  </button>
                </div>
              </div>

              <div className="bg-gray-800/50 backdrop-blur-sm rounded-2xl p-6 border border-gray-700">
                <div className="flex items-center justify-between mb-4">
                  <h2 className="text-lg font-semibold text-white">Payment QR Code</h2>
                </div>
                <div className="flex flex-col items-center">
                  <div className="bg-white p-4 rounded-xl mb-4">
                    <QRCodeSVG value={qrData} size={180} />
                  </div>
                  <p className="text-gray-400 text-sm">Scan to pay with StablePay</p>
                  <input
                    type="text"
                    placeholder="Enter amount for QR"
                    value={paymentAmount}
                    onChange={(e) => setPaymentAmount(e.target.value)}
                    className="mt-4 w-full max-w-xs px-4 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-primary-500"
                  />
                </div>
              </div>

              <TransactionList transactions={transactions} isLoading={isLoading} />
            </div>

            <div className="space-y-6">
              <div className="bg-gray-800/50 backdrop-blur-sm rounded-2xl p-6 border border-gray-700">
                <h2 className="text-lg font-semibold text-white mb-4">Analytics Overview</h2>
                {analytics && (
                  <div className="space-y-4">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center space-x-2">
                        <TrendingUp className="w-5 h-5 text-stable-green" />
                        <span className="text-gray-400">Total Volume</span>
                      </div>
                      <span className="text-white font-semibold">${analytics.totalVolume.toFixed(2)}</span>
                    </div>
                    <div className="flex items-center justify-between">
                      <div className="flex items-center space-x-2">
                        <Clock className="w-5 h-5 text-primary-400" />
                        <span className="text-gray-400">Peak Hour</span>
                      </div>
                      <span className="text-white font-semibold">{analytics.peakHour}:00</span>
                    </div>
                    <div className="flex items-center justify-between">
                      <div className="flex items-center space-x-2">
                        <Shield className="w-5 h-5 text-stable-purple" />
                        <span className="text-gray-400">Fraud Prevented</span>
                      </div>
                      <span className="text-stable-green font-semibold">${analytics.fraudPrevented.toFixed(2)}</span>
                    </div>
                  </div>
                )}
              </div>

              <div className="bg-gray-800/50 backdrop-blur-sm rounded-2xl p-6 border border-gray-700">
                <h2 className="text-lg font-semibold text-white mb-4">Transaction Insights</h2>
                <AnalyticsChart analytics={analytics} />
              </div>

              <div className="bg-gray-800/50 backdrop-blur-sm rounded-2xl p-6 border border-gray-700">
                <h2 className="text-lg font-semibold text-white mb-4">AI Security Status</h2>
                <div className="flex items-center space-x-3">
                  <div className="w-3 h-3 bg-stable-green rounded-full animate-pulse"></div>
                  <span className="text-stable-green">Active Protection</span>
                </div>
                <p className="text-gray-400 text-sm mt-2">ML-powered fraud detection is monitoring all transactions</p>
              </div>
            </div>
          </div>
        </main>
      </div>

      <PaymentModal
        isOpen={isPaymentModalOpen}
        onClose={() => setIsPaymentModalOpen(false)}
        onSubmit={handlePayment}
      />
    </>
  );
}
