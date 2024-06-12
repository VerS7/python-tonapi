from tonapi import AnonGetter, TonApiGetter

# AnonGetter - Кастомный интерфейс для ANON

# Пример использования TonApiGetter
# getter = TonApiGetter(
#     givers=[...],  # Адреса гиверов
#     jetton="...",  # Мастер-жетон
#     currencies=['usd', 'rub', 'ton', ...]  # Валюты
# )
# getter.get_rates()  # Возвращает цену в указанных валютах и изменение за 24ч и 7 дней
# -> {'prices': {'TON': ..., 'USD': ...}, 'diff_24h': {'TON': ..., 'USD': ...}, 'diff_7d': {'TON': ..., 'USD': ...}}

print("Цены:\n\t", AnonGetter.get_rates(), end='\n\n')
print("Сожжено:\n\t", AnonGetter.get_burned_info(), end='\n\n')
print("Кол-во холдеров:\n\t", AnonGetter.get_holders(), end='\n\n')
print("Ликвидность в $:\n\t", AnonGetter.get_liquidity(), end='\n\n')

