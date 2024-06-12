# Ton API getter

## Пример для Anon
```python
from tonapi import AnonGetter

print(AnonGetter.get_rates())
```

## Пример для любого жетона
```python
from tonapi import TonApiGetter

getter = TonApiGetter(
    givers=[...],  
    jetton="...",  
    currencies=['usd', 'rub', 'ton', ...] 
)

print(getter.get_rates())
```