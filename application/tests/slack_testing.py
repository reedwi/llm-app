import re

REGEX_REPLACE = (
  (re.compile('^- ', flags=re.M), '• '),
  (re.compile('^  - ', flags=re.M), '  ◦ '),
  (re.compile('^    - ', flags=re.M), '    ⬩ '), # ◆
  (re.compile('^      - ', flags=re.M), '    ◽ '),
  (re.compile('^#+ (.+)$', flags=re.M), r'*\1*'),
  (re.compile('\*\*'), '*'),
)

message = '''Sure, here are some of the largest companies based in the US:

1. **Walmart Inc.** - A multinational retail corporation that operates a chain of hypermarkets, discount department stores, and grocery stores.
2. **Amazon.com Inc.** - A multinational technology company focusing on e-commerce, cloud computing, digital streaming, and artificial intelligence.
3. **Apple Inc.** - A multinational technology company that designs, develops, and sells consumer electronics, computer software, and online services.
4. **Alphabet Inc.** - A multinational conglomerate created as part of a corporate restructuring of Google. It is the parent company of Google and several former Google subsidiaries.
5. **Microsoft Corporation** - A multinational technology company that develops, manufactures, licenses, supports, and sells computer software, consumer electronics, personal computers, and related services.
6. **Berkshire Hathaway Inc.** - A multinational conglomerate holding company that wholly owns GEICO, Duracell, Dairy Queen, BNSF, Lubrizol, Fruit of the Loom, Helzberg Diamonds, and partially owns Kraft Heinz and American Express.
7. **Johnson & Johnson** - A multinational corporation that develops medical devices, pharmaceutical, and consumer packaged goods.
8. **JPMorgan Chase & Co.** - A multinational investment bank and financial services holding company. It is one of America's Big Four banks.
9. **Visa Inc.** - A multinational financial services corporation that facilitates electronic funds transfers throughout the world, most commonly through Visa-branded credit cards, debit cards and prepaid cards.
10. **Procter & Gamble Co.** - A multinational consumer goods corporation specializing in a wide range of cleaning agents, personal care and hygiene products.'''
print(message + '\n\n')
for regex, replacement in REGEX_REPLACE:
    message = regex.sub(replacement, message)
print(message + '\n\n')