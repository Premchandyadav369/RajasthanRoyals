import sys

for pkg in ['sklearn', 'lightgbm', 'xgboost', 'scipy', 'torch']:
    try:
        m = __import__(pkg)
        print(f"{pkg}: {getattr(m, '__version__', 'installed')}")
    except Exception as e:
        print(f"{pkg}: NOT installed ({e})")
