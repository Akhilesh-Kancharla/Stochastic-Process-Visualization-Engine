import numpy as np
from scipy.stats import kstest, skew, kurtosis, chi2
from collections import Counter
import math
from typing import Dict, List, Any, Tuple

class StatisticalEngine:
    """Performs comprehensive statistical analysis on data"""

    def __init__(self):
        self.tests = [
            self._test_skewness,
            self._test_kurtosis,
            self._test_shannon_entropy,
            self._test_chi_square_uniformity,
            self._test_ks_uniformity,
            self._test_z_score_deviation,
            self._test_autocorrelation,
        ]

    def run_all_tests(self, data: List[int]) -> Dict[str, Dict[str, Any]]:
        """Run all statistical tests on the data"""
        if not data:
            return {}
        data_array = np.array(data)
        results = {}
        for test_func in self.tests:
            name, result = test_func(data, data_array)
            results[name] = result
        return results

    def _test_skewness(self, data: List[int], data_array: np.ndarray) -> Tuple[str, Dict[str, Any]]:
        skewness = skew(data_array)
        return 'Skewness', {'value': skewness, 'passed': abs(skewness) < 0.5, 'description': 'Measures asymmetry of distribution'}

    def _test_kurtosis(self, data: List[int], data_array: np.ndarray) -> Tuple[str, Dict[str, Any]]:
        kurt_val = kurtosis(data_array)
        return 'Kurtosis', {'value': kurt_val, 'passed': abs(kurt_val) < 1.0, 'description': 'Measures tail heaviness'}

    def _test_shannon_entropy(self, data: List[int], data_array: np.ndarray) -> Tuple[str, Dict[str, Any]]:
        entropy = self._calculate_shannon_entropy(data)
        return 'Shannon Entropy', {'value': entropy, 'passed': entropy > 6.0, 'description': 'Measures randomness/uncertainty'}

    def _test_chi_square_uniformity(self, data: List[int], data_array: np.ndarray) -> Tuple[str, Dict[str, Any]]:
        chi_square_val, p_val, df, _ = self._chi_square_uniform_test(data)
        critical_value = chi2.ppf(0.95, df) # q=1-alpha, for alpha=0.05
        return 'Chi-Square Uniformity', {'value': chi_square_val, 'passed': chi_square_val < critical_value, 'description': f'Tests uniform distribution (p<0.05, df={df})'}

    def _test_ks_uniformity(self, data: List[int], data_array: np.ndarray) -> Tuple[str, Dict[str, Any]]:
        ks_stat, ks_p = kstest(data_array / 10000, 'uniform')
        return 'KS Test (Uniform)', {'value': ks_stat, 'passed': ks_p > 0.05, 'description': 'Tests against uniform distribution'}

    def _test_z_score_deviation(self, data: List[int], data_array: np.ndarray) -> Tuple[str, Dict[str, Any]]:
        z_score = self._z_score_deviation(data)
        return 'Z-Score Deviation', {'value': z_score, 'passed': z_score < 1.96, 'description': 'Tests deviation from expected mean'}

    def _test_autocorrelation(self, data: List[int], data_array: np.ndarray) -> Tuple[str, Dict[str, Any]]:
        """Tests for correlation between a value and the next one (lag-1)."""
        autocorr = np.corrcoef(data_array[:-1], data_array[1:])[0, 1]
        # Simple threshold test: high autocorrelation is unusual for random data
        return 'Autocorrelation (Lag-1)', {'value': autocorr, 'passed': abs(autocorr) < 0.1, 'description': 'Measures correlation between consecutive values'}

    def _calculate_shannon_entropy(self, data: List[int]) -> float:
        hist, _ = np.histogram(data, bins=100, range=(0, 10000))
        probabilities = hist / len(data)
        entropy = -sum(p * math.log2(p) for p in probabilities if p > 0)
        return entropy

    def _chi_square_uniform_test(self, data: List[int]) -> float:
        """Performs a Chi-Square Goodness of Fit test for a uniform distribution."""
        bins = 20
        expected_freq = len(data) / bins
        hist, _ = np.histogram(data, bins=bins, range=(0, 10000))
        chi_square_stat = sum((observed - expected_freq)**2 / expected_freq for observed in hist if expected_freq > 0)
        # Degrees of freedom is number of bins - 1
        return chi_square_stat, 0, bins - 1, None # p-value and expected are not used by caller

    def _z_score_deviation(self, data: List[int]) -> float:
        sample_mean = np.mean(data)
        expected_mean = 5000  # For uniform distribution 0-10000
        sample_std = np.std(data, ddof=1)
        n = len(data)
        if sample_std == 0: return float('inf')
        z_score = abs(sample_mean - expected_mean) / (sample_std / math.sqrt(n))
        return z_score
