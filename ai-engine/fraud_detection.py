import numpy as np
import pandas as pd
import os
import pickle
import logging
from typing import Dict, List, Any
from datetime import datetime

logger = logging.getLogger(__name__)


class FraudDetector:
    """AI-powered fraud detection using rule-based checks and ML model"""
    
    def __init__(self):
        self.model = None
        self.threshold = 0.7
        self.known_scam_addresses = set()
        self.load_model()
        self._init_rules()
    
    def _init_rules(self):
        """Initialize rule-based fraud detection thresholds"""
        self.rules = {
            'max_single_transaction': 10000,
            'max_daily_total': 50000,
            'Suspicious_patterns': [
                '0x0000000000000000000000000000000000000000',
                '0xdddddddddddddddddddddddddddddddddddddddd',
                '0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF',
            ],
            'new_wallet_age_hours': 24,
        }
    
    def load_model(self):
        """Load pre-trained ML model or create mock model"""
        model_path = os.path.join(os.path.dirname(__file__), 'models', 'fraud_model.pkl')
        
        if os.path.exists(model_path):
            try:
                with open(model_path, 'rb') as f:
                    self.model = pickle.load(f)
                logger.info('ML model loaded successfully')
            except Exception as e:
                logger.warning(f'Could not load model: {e}, using rule-based only')
                self.model = None
        else:
            logger.info('No pre-trained model found, using rule-based detection')
            self._create_mock_model()
    
    def _create_mock_model(self):
        """Create a simple mock ML model for demonstration"""
        np.random.seed(42)
        
        n_samples = 1000
        X = np.random.randn(n_samples, 5)
        y = (X[:, 0] * 0.3 + X[:, 1] * 0.2 + X[:, 2] * 0.1 + 
             np.random.randn(n_samples) * 0.1 > 0.3).astype(int)
        
        from sklearn.tree import DecisionTreeClassifier
        self.model = DecisionTreeClassifier(max_depth=3, random_state=42)
        self.model.fit(X, y)
        
        self.feature_means = X.mean(axis=0)
        self.feature_stds = X.std(axis=0)
    
    def _extract_features(self, sender: str, recipient: str, amount: float) -> np.ndarray:
        """Extract features for ML prediction"""
        sender_hash = int(sender[-16:], 16) if len(sender) > 16 else 0
        recipient_hash = int(recipient[-16:], 16) if len(recipient) > 16 else 0
        
        features = np.array([
            np.log1p(abs(sender_hash)) % 10,
            np.log1p(abs(recipient_hash)) % 10,
            np.log1p(amount),
            abs(sender_hash - recipient_hash) % 100,
            (sender == recipient) * 1.0,
        ])
        
        return features
    
    def _check_rules(self, sender: str, recipient: str, amount: float) -> Dict[str, Any]:
        """Run rule-based fraud checks"""
        reasons = []
        is_suspicious = False
        
        if amount > self.rules['max_single_transaction']:
            reasons.append(f'Single transaction exceeds limit ({self.rules["max_single_transaction"]})')
            is_suspicious = True
        
        if amount < 0.001:
            reasons.append('Amount too small')
            is_suspicious = True
        
        if recipient in self.rules['Suspicious_patterns']:
            reasons.append('Recipient in blacklist')
            is_suspicious = True
        
        if not recipient.startswith('0x'):
            reasons.append('Invalid address format')
            is_suspicious = True
        
        if len(recipient) != 42:
            reasons.append('Invalid address length')
            is_suspicious = True
        
        return {
            'isSuspicious': is_suspicious,
            'reasons': reasons
        }
    
    def analyze(self, sender_address: str, recipient_address: str, amount: float) -> Dict[str, Any]:
        """Analyze transaction for fraud risk"""
        rule_result = self._check_rules(sender_address, recipient_address, amount)
        
        if rule_result['isSuspicious']:
            return {
                'riskScore': 0.95,
                'isFlagged': True,
                'reasons': rule_result['reasons'],
                'method': 'rule-based'
            }
        
        try:
            features = self._extract_features(sender_address, recipient_address, amount)
            
            if self.model is not None:
                proba = self.model.predict_proba(features.reshape(1, -1))[0, 1]
            else:
                proba = 0.0
            
            risk_score = min(0.5 + proba * 0.5, 1.0)
            
        except Exception as e:
            logger.error(f'ML prediction error: {e}')
            risk_score = 0.5
        
        is_flagged = risk_score >= self.threshold
        
        return {
            'riskScore': round(risk_score, 3),
            'isFlagged': is_flagged,
            'reasons': rule_result['reasons'] if is_flagged else [],
            'method': 'ml+rules' if self.model else 'rules'
        }
    
    def batch_analyze(self, transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Analyze multiple transactions"""
        results = []
        for tx in transactions:
            result = self.analyze(
                sender=tx.get('sender', ''),
                recipient=tx.get('recipient', ''),
                amount=tx.get('amount', 0)
            )
            results.append(result)
        return results
    
    def train(self, X: np.ndarray, y: np.ndarray):
        """Train the fraud detection model"""
        if self.model is None:
            from sklearn.tree import DecisionTreeClassifier
            self.model = DecisionTreeClassifier(max_depth=5, random_state=42)
        
        self.model.fit(X, y)
        logger.info('Model trained with new data')
    
    def save_model(self, path: str = None):
        """Save the trained model"""
        if path is None:
            path = os.path.join(os.path.dirname(__file__), 'models', 'fraud_model.pkl')
        
        os.makedirs(os.path.dirname(path), exist_ok=True)
        
        with open(path, 'wb') as f:
            pickle.dump(self.model, f)
        
        logger.info(f'Model saved to {path}')