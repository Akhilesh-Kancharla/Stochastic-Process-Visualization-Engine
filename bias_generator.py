import random
import numpy as np
from typing import Tuple, List

class BiasGenerator:
    """Generates biased random data according to predefined patterns"""
    BIAS_PATTERNS = {
        1: "Clustered Low - 70% between 0-3000",
        2: "Clustered High - 70% between 7000-10000",
        3: "Bell Curve - Normal distribution centered at 5000",
        4: "Periodic Spikes - Every 100th value is 9999",
        5: "Missing Ranges - Omit numbers between 3000-4000",
        6: "Even-Heavy - 80% even numbers",
        7: "Prime-Rich - 50% prime numbers",
        8: "Uniform - True uniform distribution"
    }

    def __init__(self):
        self.primes = self._generate_primes(10000)
        self._generation_functions = {
            1: self._generate_clustered_low,
            2: self._generate_clustered_high,
            3: self._generate_bell_curve,
            4: self._generate_periodic_spikes,
            5: self._generate_missing_ranges,
            6: self._generate_even_heavy,
            7: self._generate_prime_rich,
            8: self._generate_uniform
        }

    def _generate_clustered_low(self, count: int) -> np.ndarray:
        choices = np.random.random(count)
        return np.where(choices < 0.7, np.random.randint(0, 3001, count), np.random.randint(0, 10001, count))

    def _generate_clustered_high(self, count: int) -> np.ndarray:
        choices = np.random.random(count)
        return np.where(choices < 0.7, np.random.randint(7000, 10001, count), np.random.randint(0, 10001, count))

    def _generate_bell_curve(self, count: int) -> np.ndarray:
        data = np.random.normal(loc=5000, scale=1500, size=count)
        return np.clip(data, 0, 10000).astype(int)

    def _generate_periodic_spikes(self, count: int) -> np.ndarray:
        data = np.random.randint(0, 10001, count)
        indices = np.arange(99, count, 100)
        data[indices] = 9999
        return data

    def _generate_missing_ranges(self, count: int) -> np.ndarray:
        # This is harder to vectorize efficiently, loop is acceptable
        data = np.empty(count, dtype=int)
        for i in range(count):
            while True:
                value = random.randint(0, 10000)
                if not (3000 <= value <= 4000):
                    data[i] = value
                    break
        return data

    def _generate_even_heavy(self, count: int) -> np.ndarray:
        choices = np.random.random(count)
        even_data = np.random.randint(0, 5001, count) * 2
        random_data = np.random.randint(0, 10001, count)
        return np.where(choices < 0.8, even_data, random_data)

    def _generate_prime_rich(self, count: int) -> np.ndarray:
        # This is harder to vectorize efficiently, loop is acceptable
        if not self.primes:
            return self._generate_uniform(count)
        data = np.empty(count, dtype=int)
        for i in range(count):
            if random.random() < 0.5:
                data[i] = random.choice(self.primes)
            else:
                data[i] = random.randint(0, 10000)
        return data

    def _generate_uniform(self, count: int) -> np.ndarray:
        return np.random.randint(0, 10001, count)

    def _generate_primes(self, max_val: int) -> List[int]:
        """Generate list of prime numbers up to max_val using Sieve of Eratosthenes"""
        sieve = [True] * (max_val + 1)
        sieve[0] = sieve[1] = False
        for i in range(2, int(max_val**0.5) + 1):
            if sieve[i]:
                for j in range(i * i, max_val + 1, i):
                    sieve[j] = False
        return [i for i, is_prime in enumerate(sieve) if is_prime]

    def generate_biased_data(self, count: int = 1000, bias_id: int = None) -> Tuple[List[int], int, str]:
        """
        Generate biased data with a randomly selected bias pattern
        If bias_id is provided, it will use that specific bias.
        Returns: (data, bias_id, bias_name)
        """
        bias_id = bias_id if bias_id is not None else random.randint(1, len(self.BIAS_PATTERNS))
        bias_name = self.BIAS_PATTERNS[bias_id]
        
        generation_func = self._generation_functions.get(bias_id, self._generate_uniform)
        data = generation_func(count).tolist()
        
        return data, bias_id, bias_name

    def get_bias_names(self) -> List[str]:
        """Return list of bias pattern names for dropdown"""
        return list(self.BIAS_PATTERNS.values())

    def get_bias_description(self, bias_id: int) -> str:
        """Get description of a specific bias pattern"""
        return self.BIAS_PATTERNS.get(bias_id, "Unknown bias pattern")
