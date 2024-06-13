from tonapi import AnonGetter, GramGetter, TonApiGetter

# AnonGetter - Кастомный интерфейс для ANON

# Пример использования TonApiGetter
# getter = TonApiGetter(
#     givers=[...],  # Адреса гиверов
#     jetton="...",  # Мастер-жетон
#     currencies=['usd', 'rub', 'ton', ...]  # Валюты
# )
# getter.get_rates()  # Возвращает цену в указанных валютах и изменение за 24ч и 7 дней
# -> {'prices': {'TON': ..., 'USD': ...}, 'diff_24h': {'TON': ..., 'USD': ...}, 'diff_7d': {'TON': ..., 'USD': ...}}

# --- ANON ---
# print("Цены:\n\t", AnonGetter.get_rates(), end='\n\n')
# print("Сожжено:\n\t", AnonGetter.get_burned_info(), end='\n\n')
# print("Кол-во холдеров:\n\t", AnonGetter.get_holders(), end='\n\n')
# print("Ликвидность в $:\n\t", AnonGetter.get_liquidity(), end='\n\n')

# --- GRAM ---
print("Цены:\n\t", GramGetter.get_rates(), end='\n\n')
print("Сожжено:\n\t", GramGetter.get_burned_info(), end='\n\n')
print("Кол-во холдеров:\n\t", GramGetter.get_holders(), end='\n\n')
print("Ликвидность в $:\n\t", GramGetter.get_liquidity(), end='\n\n')

stats = GramGetter.get_givers_statistics()
print("Суммарный баланс гиверов:\n\t", stats["balance_sum"], stats["stats"][0]["name"], end='\n\n')
print("Статистика по гиверам:")
for stat in stats["stats"]:
    print("\t", stat)
