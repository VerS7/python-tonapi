"""
Ton API
"""
import time

import requests

TON_API_URL = 'https://tonapi.io/v2'
STONFI_API_URL = 'https://api.ston.fi/v1'
EMISSION = 500_000_000


class TonApiGetter:
    def __init__(self, jetton: str, givers: list[str], currencies: list[str],
                 burn_address: str = None, emission: int = None):
        """
        :param str jetton: Мастер-жетон искомой монеты
        :param list givers: Список адресов гиверов
        :param list currencies: Список валют - ['ton', 'usd', 'rub', ...]
        :param int emission: эмиссия искомой монеты
        """
        self.jetton = jetton
        self.givers = givers
        self.currencies = currencies
        self.burn_address = burn_address
        self.emission = emission

        if self.burn_address is None:
            self.burn_address = self._get_burn_addr()

        if self.emission is None:
            self.emission = EMISSION

    def _get_burn_addr(self) -> str:
        """
        Возвращает burn-адрес жетона
        :return str:
        """
        return self.get_meta()["admin"]["address"]

    def _get_contract_addr(self) -> str:
        """
        Возвращает адрес контракта
        :return str:
        """
        url = f"{STONFI_API_URL}/assets/{self._get_burn_addr()}"
        response = requests.get(url)
        data = response.json()
        return data["asset"]["contract_address"]

    def _get_giver_stat(self, giver_addr: str) -> dict:
        """
        Возвращает статистику по гиверу - адрес, название токена, баланс и состояние
        :param str giver_addr: адрес гивера
        :return dict:
        """
        url = f"{TON_API_URL}/accounts/{giver_addr}/jettons/{self.jetton}"

        response = requests.get(url)
        data = response.json()

        return {
            "address": giver_addr,
            "name": data["jetton"]["name"],
            "balance": int(data["balance"]) / 1000000000,
            "condition": "working" if int(data["balance"]) >= 100000000000 else "drained"
        }

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
        percentage = rounded * 100 / self.emission
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

    def get_volume(self) -> dict:
        """
        Возвращает объём продаж за 24ч
        :return dict:
        """
        #  time_since = (datetime.datetime.utcnow() - datetime.timedelta(days=1)).strftime('%Y-%m-%dT%H:%M:%S')
        #  time_until = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')

        raise NotImplementedError

    def get_givers_statistics(self) -> dict:
        """
        Возвращает статистику по всем гиверам - адрес, название токена, баланс, состояние и общий баланс
        :return list:
        """
        statistics = []
        for giver in self.givers:
            statistics.append(self._get_giver_stat(giver))
            time.sleep(0.5)  # Ограничение для обхода лимитов бесплатного API
        return {
            "balance_sum": sum([elem["balance"] for elem in statistics]),
            "stats": statistics
        }

    def get_liquidity(self) -> float:
        """
        Возвращает ликвидность в $
        :return float:
        """
        response = requests.get(f"{STONFI_API_URL}/pools")
        data = response.json()

        stats = [elem for elem in data["pool_list"]
                 if elem["token0_address"] == self.jetton
                 and elem["token1_address"] == self._get_contract_addr()][0]

        return stats["lp_total_supply_usd"]
