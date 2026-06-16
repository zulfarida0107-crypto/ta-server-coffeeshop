import urllib.request, json
req = urllib.request.Request('http://localhost:8083/api/menu-produk')
with urllib.request.urlopen(req) as res:
    data = json.loads(res.read().decode('utf-8'))['data']
    for d in data:
        print(f"{d['id']} - {d['namaProduk']} - {d['bagian']}")
