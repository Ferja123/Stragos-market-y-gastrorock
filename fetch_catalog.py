import urllib.request
import csv
import io

url = "https://docs.google.com/spreadsheets/d/1WeyilhcWeYJowJ7DJxY2-yBGELaw5FR7IthUIdM96xw/export?format=csv&gid=403687409"
response = urllib.request.urlopen(url)
text = response.read().decode('utf-8')

reader = csv.reader(io.StringIO(text))
rows = list(reader)

header_idx = -1
for i, row in enumerate(rows):
    if 'CODIGO BARRAS' in ' '.join(row) and 'PRODUCTO' in ' '.join(row):
        header_idx = i
        break

headers = rows[header_idx]
prod_idx = headers.index('PRODUCTO') if 'PRODUCTO' in headers else -1
price_idx = stock_idx = None
for i, h in enumerate(headers):
    if 'PRECIO VENTA' in h: price_idx = i
    if 'STOCK FISICO' in h: stock_idx = i

licor_kw = ['WHISKY','RON','VODKA','PILSEN','CERVEZA','TEQUILA','PISCO','VINO','BORGOÑA','LICOR','GIN','SMIRNOFF','JOHNNIE','RED LABEL','BLACK LABEL','DOUBLE BLACK','OLD TIMES','CARTAVIO','JAGERMEISTER','FERNET','TRES PLUMAS','CAMPARI','CHIVAS','JACK DANIEL','HEINEKEN','TRAGOS','BACARDI','BACCARDI','CORONA','CUSQUEÑA','CRISTAL','TRAPICHE','MISIONES DE RENGO','VIÑA','SANTIAGO QUEIROLO','SABORES DEL VALLE','PULPA','VERMOUTH','ANIS','AMARETTO','PISCO SOUR','SOUR','JOHNY WALKER','CHAMPAGNE','SPARKLING','SHERRY','SOPRA','SAU RUS','BOUTIQUE','FINCA','DON VALENTIN','SANGRIA','APEROL','MALIBU','TABERNERO','CASILLERO DEL DIABLO']
bebida_kw = ['COCA COLA','INCA KOLA','FANTA','SPRITE','PEPSI','AGUA','SAN LUIS','SAN MATEO','CIELO','POWER ADE','FRUGOS','VOLT','RED BULL','GATORADE','MILKIS','RAMUNE','KATO','YOGURT','GLORIA','LECHE','JUGO','TE CON LECHE','CICI','PULP','MONSTER','SODA','BEBIDA','ADEP','AD ADE','SCHWEPPES']
snack_kw = ['PAPAS','LAYS','DORITOS','TOR TEES','SNAXX','TIYAPUY','TAKIS','INKA CHIPS','CHEETOS','CHISITO','PIQUEO','MANI','FRUTOS SECOS','GOMITAS','CHOCOLATE','SUBLIME','PRINCESA','TRENTO','CASINO','GLACITAS','PICARAS','GALLETA','MARGARITA','TRIDENT','CHICLE','DULCE','PALETA','MARSHMALLOW','ALMENDRAS','PISTACHOS','CRAKERS','CLUB SOCIAL','CRUNCH','OREO','RITZ','BIMBO','PAN','KEKE','DONOFRIO','HELADO','PEZIDURI','SORPRESA','CHOCO','GOMA','TURRON','MENTOS','HALLS','FREEGELLS']

cats = {'licores': [], 'bebidas': [], 'snacks': [], 'unclassified': []}

for row in rows[header_idx+1:]:
    if len(row) <= prod_idx: continue
    name = row[prod_idx].strip()
    if not name: continue
    name_upper = name.upper()
    if any(kw in name_upper for kw in ['DELIVERY','CONTOMETRO']): continue
    try: price = float(row[price_idx]) if price_idx and row[price_idx] else 0
    except: price = 0
    try: stock = float(row[stock_idx]) if stock_idx and row[stock_idx] else 0
    except: stock = 0
    if price <= 0 or stock <= 0: continue
    
    is_licor = any(kw in name_upper for kw in licor_kw)
    is_bebida = any(kw in name_upper for kw in bebida_kw)
    is_snack = any(kw in name_upper for kw in snack_kw)
    
    if is_licor: cats['licores'].append(name)
    elif is_bebida: cats['bebidas'].append(name)
    elif is_snack: cats['snacks'].append(name)
    else: cats['unclassified'].append(name)

print(f"LICORES: {len(cats['licores'])} products")
print(f"BEBIDAS: {len(cats['bebidas'])} products")
print(f"SNACKS: {len(cats['snacks'])} products")
print(f"UNCLASSIFIED: {len(cats['unclassified'])} products")
print()

# Show just the licores list
print("=== LICORES ===")
for p in sorted(cats['licores']): print(f"  {p}")
print()
print("=== BEBIDAS ===")
for p in sorted(cats['bebidas']): print(f"  {p}")
