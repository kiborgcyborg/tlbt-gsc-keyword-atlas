from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime, timedelta

def get_gsc_data_16m(key_path, domain):
    """
    Функція для отримання даних GSC для всіх доменів
    """
    try:
        credentials = service_account.Credentials.from_service_account_file(
            key_path,
            scopes=['https://www.googleapis.com/auth/webmasters.readonly']
        )
        
        service = build('searchconsole', 'v1', credentials=credentials)
        
        # Визначення дат
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=16*30)).strftime('%Y-%m-%d')
        
        print(f"\nОбробка даних для {domain}...")
        
        all_rows = []
        start_row = 0
        row_limit = 5000
        
        while True:
            request = {
                'startDate': start_date,
                'endDate': end_date,
                'dimensions': ['query'],
                'dimensionFilterGroups': [{
                    'filters': [{
                        'dimension': 'country',
                        'operator': 'equals',
                        'expression': 'ESP'
                    }]
                }],
                'rowLimit': row_limit,
                'startRow': start_row,
                'aggregationType': 'byProperty'
            }
            
            try:
                response = service.searchanalytics().query(
                    siteUrl=domain,
                    body=request
                ).execute()
                
                if 'rows' in response:
                    all_rows.extend(response['rows'])
                    start_row += row_limit
                else:
                    break
                
            except Exception as e:
                print(f"Помилка при обробці {domain}: {str(e)}")
                break
        
        print(f"Дані для {domain} оброблено.")
        print(f"Загальна кількість рядків: {len(all_rows)}")
        return all_rows
        
    except Exception as e:
        print(f"Загальна помилка: {str(e)}")