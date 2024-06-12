"""
Ton API
"""
import datetime

import requests

TON_API_URL = 'https://tonapi.io/v2'
STONFI_API_URL = 'https://api.ston.fi/v1'
EMISSION = 500_000_000


class TonApiGetter:
    def __init__(self, jetton: str, givers: list[str], currencies: list[str], burn_address: str = None):
        """
        :param str jetton: Мастер-жетон искомой монеты
        :param list givers: Список адресов гиверов
        :param list currencies: Список валют - ['ton', 'usd', 'rub', ...]
        """
        self.jetton = jetton
        self.givers = givers
        self.currencies = currencies
        self.burn_address = burn_address
        if self.burn_address is None:
            self.burn_address = self._get_burn_addr()

    def _get_burn_addr(self) -> str:
        """
        Возвращает burn-адрес жетона
        :return str:
        """
        return self.get_meta()["admin"]["address"]

    def get_meta(self) -> dict:
        """
        Возвращает метаданные по жетону
        :return dict:
        """
        url = f"{TON_API_URL}/jettons/{self.jetton}"
        response = requests.get(url)
        data = response.json()
        return data

    def get_rates(self) -> dict:
        """
        Возвращает цену в указанных валютах и изменение за 24ч / 7 дней
        :return dict:
        """
        url = f"{TON_API_URL}/rates?tokens={self.jetton}&currencies={','.join(self.currencies)}"
        response = requests.get(url)
        data = response.json()
        return {
            "prices": data["rates"][self.jetton]["prices"],
            "diff_24h": data["rates"][self.jetton]["diff_24h"],
            "diff_7d": data["rates"][self.jetton]["diff_7d"]
        }

    def get_burned(self) -> int:
        """
        Возвращает количество сожжённых токенов
        :return int:
        """
        url = f"{TON_API_URL}/accounts/{self.burn_address}/jettons/{self.jetton}"
        response = requests.get(url)
        data = response.json()
        return int(data["balance"])

    def get_burned_info(self) -> dict:
        """
        Возвращает информацию по сожжённым токенам - количество и процент от эмиссии
        :return dict:
        """
        burned = self.get_burned()
        rounded = burned / 1000000000
        percentage = rounded * 100 / EMISSION
        return {
            "raw": burned,
            "rounded": rounded,
            "percentage": percentage,
            "percentage_string": f"{percentage:.2f}%"
        }

    def get_holders(self) -> int:
        """
        Возвращает количество холдеров
        :return int:
        """
        return self.get_meta()["holders_count"]

    def get_metrics(self) -> list[dict]:
        """
        Возвращает метрики по пулам - объём продаж за 24ч и ликвидность в USD
        :return:
        """
        time_since = (datetime.datetime.utcnow() - datetime.timedelta(days=1)).strftime('%Y-%m-%dT%H:%M:%S')
        time_until = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')

        url = f"{STONFI_API_URL}/stats/pool?since={time_since}&until={time_until}"
        response = requests.get(url)

        data = response.json()

        stats = [elem for elem in data["stats"] if elem["base_id"] == self.jetton and float(elem["quote_volume"]) > 0]

        return [
            {
                "pool_address": elem["pool_address"],
                "volume": elem["quote_volume"],
                "liquidity_usd": elem["lp_price_usd"],

            }
            for elem in stats
        ]

