import time, requests, json

class PriceManager:
    def __init__(self, config):
        self.config = config
        self.cache = {}
        self.last_fetch = 0

    def load_local(self, path='price.json'):
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def fetch_api(self):
        if time.time() - self.last_fetch < 300:
            return self.cache
        try:
            r = requests.get(self.config['api_url'], headers={'Authorization': self.config.get('api_token','')}, timeout=5)
            r.raise_for_status()
            data = r.json()
            self.cache = data
            self.last_fetch = time.time()
            return data
        except Exception:
            return self.cache or self.load_local()

    def get_price(self, name):
        data = self.fetch_api() if self.config['price_source']=='api' else self.load_local()
        return data.get(name)