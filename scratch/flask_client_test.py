import sys
from pathlib import Path
script_dir = Path(__file__).resolve().parent
project_root = script_dir.parent
sys.path.insert(0, str(project_root))
import app
with app.app.test_client() as client:
    response = client.post('/download-report', json={'score': 0.2, 'prediction': 'Healthy Profile', 'filename': 'test.wav'})
    print('STATUS', response.status_code)
    print('MIMETYPE', response.mimetype)
    print('DATA LEN', len(response.data))
    print('DATA FIRST BYTES', response.data[:20])
    if response.status_code != 200:
        print(response.get_data(as_text=True))
    else:
        print('OK')
