import json
import urllib.request
import urllib.error

url = 'http://127.0.0.1:5000/download-report'
data = json.dumps({
    'score': 0.2,
    'prediction': 'Healthy Profile',
    'filename': 'test.wav'
}).encode('utf-8')

req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
try:
    with urllib.request.urlopen(req) as response:
        body = response.read()
        print('STATUS', response.status)
        print('LENGTH', len(body))
        with open('scratch/download_report_test.pdf', 'wb') as f:
            f.write(body)
        print('Saved scratch/download_report_test.pdf')
except urllib.error.HTTPError as e:
    error_body = e.read().decode('utf-8', errors='replace')
    print('HTTP ERROR', e.code)
    print(error_body)
except Exception as e:
    print('OTHER ERROR', type(e).__name__, e)
