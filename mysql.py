import pandas as pd
from sqlalchemy import create_engine

# 1. CSV faylını oxu
df = pd.read_csv('crop_yield_prediction_with_weather.csv')

# 2. MySQL bağlantısını qur (istifadəçi: root, şifrə: your_password)
# Format: mysql+pymysql://user:password@host:port/database
engine = create_engine('mysql+pymysql://root:your_password@localhost:3306/crop_db')

# 3. Məlumatı cədvələ yüklə
try:
    df.to_sql('crop_yields', con=engine, if_exists='replace', index=False)
    print("Məlumat uğurla MySQL-ə yükləndi!")
except Exception as e:
    print(f"Xəta baş verdi: {e}")