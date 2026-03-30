"""Run RandomForestRegressor to predict finishing position.

Usage:
  python run_rf_position.py

If ergast API is reachable, downloads 2022-2024 results and uses seasons 2022-2023 for train, 2024 for test.
Falls back to a synthetic dataset if download fails.

Requirements: pandas, numpy, scikit-learn, requests
"""
import os, random
import numpy as np
import pandas as pd
import requests
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error

RANDOM_SEED = 414
random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)

def fetch_results(seasons):
    rows = []
    for season in seasons:
        offset = 0
        while True:
            url = f'https://api.jolpi.ca/ergast/f1/{season}/results.json?limit=100&offset={offset}'
            resp = requests.get(url, timeout=30)
            data = resp.json()
            races = data['MRData']['RaceTable']['Races']
            if not races:
                break
            for race in races:
                for r in race['Results']:
                    pos_num = int(r['position']) if r['position'].isdigit() else None
                    status = r['status']
                    rows.append({
                        'season': int(race['season']),
                        'round': int(race['round']),
                        'race': race['raceName'],
                        'date': race['date'],
                        'circuit': race['Circuit']['circuitId'],
                        'driverId': r['Driver']['driverId'],
                        'driver': f"{r['Driver']['givenName']} {r['Driver']['familyName']}",
                        'constructor': r['Constructor']['name'],
                        'position': pos_num,
                        'positionText': r['positionText'],
                        'grid': int(r['grid']) if str(r['grid']).isdigit() else None,
                        'laps': int(r['laps']) if str(r['laps']).isdigit() else None,
                        'status': status,
                        'points': int(float(r['points'])),
                        'top10': pos_num is not None and pos_num <= 10,
                        'finished': status == 'Finished' or 'Lap' in status,
                    })
            total = int(data['MRData']['total'])
            offset += 100
            if offset >= total:
                break
    return pd.DataFrame(rows)


def main():
    root = os.path.dirname(__file__)
    cache_file = os.path.join(root, '..', 'data', 'processed', 'results_2022_2024.csv')
    cache_file = os.path.normpath(cache_file)
    os.makedirs(os.path.dirname(cache_file), exist_ok=True)

    use_synthetic = False
    try:
        if os.path.exists(cache_file):
            df = pd.read_csv(cache_file, parse_dates=['date'])
            print('Loaded cached data:', cache_file)
        else:
            print('Downloading real data from API...')
            df = fetch_results([2022,2023,2024])
            df['date'] = pd.to_datetime(df['date'])
            df.to_csv(cache_file, index=False)
            print('Saved cache to', cache_file)
        print('Data loaded: rows=', len(df))
    except Exception as e:
        print('Could not fetch real data:', e)
        print('Falling back to synthetic dataset for demonstration.')
        use_synthetic = True

    if use_synthetic:
        n = 1000
        seasons = np.random.choice([2022,2023,2024], size=n, p=[0.4,0.4,0.2])
        grid = np.clip((np.random.poisson(10, size=n)), 1, 20)
        laps = np.random.randint(40, 72, size=n)
        position = np.clip((grid + np.random.normal(0, 5, size=n)).round().astype(int), 1, 20)
        df = pd.DataFrame({'season':seasons,'grid':grid,'laps':laps,'position':position})

    # cleaning
    df['grid'] = pd.to_numeric(df['grid'], errors='coerce')
    df['position'] = pd.to_numeric(df['position'], errors='coerce')
    df['laps'] = pd.to_numeric(df['laps'], errors='coerce')
    df = df.dropna(subset=['position','grid','laps'])

    features = ['grid','laps','season']
    X = df[features]
    y = df['position']

    train_mask = df['season'].isin([2022,2023])
    test_mask = df['season']==2024
    if test_mask.sum() == 0:
        from sklearn.model_selection import train_test_split
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=RANDOM_SEED)
    else:
        X_train, y_train = X[train_mask], y[train_mask]
        X_test, y_test = X[test_mask], y[test_mask]

    print(f'Rows: total={len(df)}, train={len(X_train)}, test={len(X_test)}')

    model = RandomForestRegressor(n_estimators=100, random_state=RANDOM_SEED, n_jobs=-1)
    model.fit(X_train, y_train)

    y_pred_train = model.predict(X_train)
    y_pred_test = model.predict(X_test)

    train_mae = mean_absolute_error(y_train, y_pred_train)
    test_mae = mean_absolute_error(y_test, y_pred_test)

    print(f'RandomForestRegressor (seed={RANDOM_SEED})')
    print(f'Train MAE: {train_mae:.3f}')
    print(f'Test MAE : {test_mae:.3f}')

    out = os.path.join(root, 'rf_position_results.csv')
    pd.DataFrame([{
        'model':'RandomForestRegressor',
        'random_state':RANDOM_SEED,
        'train_MAE':float(train_mae),
        'test_MAE':float(test_mae),
        'data_source':'synthetic' if use_synthetic else 'ergast_api'
    }]).to_csv(out, index=False)
    print('Saved summary to', out)

if __name__ == '__main__':
    main()
