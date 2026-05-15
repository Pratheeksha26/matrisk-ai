import pandas as pd
import os
import hashlib
import joblib

class FeatureStore:
    """
    A simple point-in-time feature store with file-based caching.
    """
    def __init__(self, cache_dir='data/interim/cache'):
        self.cache_dir = cache_dir
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)
            
    def _generate_key(self, df, params):
        """
        Generate a unique key based on the dataframe state and parameters.
        """
        # In a real scenario, we might use a hash of the input data
        # For now, we'll use the class name + params
        key_str = f"{params}"
        return hashlib.md5(key_str.encode()).hexdigest()

    def get_features(self, name, compute_func, *args, **kwargs):
        """
        Get features from cache or compute them if not present.
        """
        cache_path = os.path.join(self.cache_dir, f"{name}.joblib")
        
        if os.path.exists(cache_path):
            print(f"Loading features '{name}' from cache...")
            return joblib.load(cache_path)
        
        print(f"Computing features '{name}'...")
        features = compute_func(*args, **kwargs)
        joblib.dump(features, cache_path)
        return features

    def clear_cache(self):
        """
        Clear all cached features.
        """
        for f in os.listdir(self.cache_dir):
            os.remove(os.path.join(self.cache_dir, f))
        print("Cache cleared.")

# Global instance
store = FeatureStore()
