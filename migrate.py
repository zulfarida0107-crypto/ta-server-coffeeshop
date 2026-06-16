import urllib.request
import json

# Fetch menu
req = urllib.request.Request('http://localhost:8083/api/menu-produk')
with urllib.request.urlopen(req) as response:
    menu_data = json.loads(response.read().decode('utf-8'))['data']

menu_map = {m['id']: m['bagian'] for m in menu_data}

# Fetch pesanan
req = urllib.request.Request('http://localhost:8083/api/pesanan')
with urllib.request.urlopen(req) as response:
    pesanan_data = json.loads(response.read().decode('utf-8'))['data']

for p in pesanan_data:
    if not p.get('detailPesanan') or p['detailPesanan'] == '[]': continue
    try:
        items = json.loads(p['detailPesanan'])
        changed = False
        for it in items:
            if 'bagian' not in it or it['bagian'] is None:
                prod_id = it.get('idProduk')
                if prod_id in menu_map:
                    it['bagian'] = menu_map[prod_id]
                    changed = True
        
        if changed:
            new_detail = json.dumps(items)
            p['detailPesanan'] = new_detail
            
            # Update pesanan
            put_url = 'http://localhost:8083/api/pesanan/' + str(p['id'])
            put_req = urllib.request.Request(
                put_url, 
                data=json.dumps(p).encode('utf-8'), 
                headers={'Content-Type': 'application/json'},
                method='PUT'
            )
            with urllib.request.urlopen(put_req) as put_res:
                print('Updated Pesanan ID ' + str(p['id']))
    except Exception as e:
        print('Error on Pesanan ID ' + str(p['id']) + ': ' + str(e))
