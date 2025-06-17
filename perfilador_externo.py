import sys
import pandas as pd
from ydata_profiling import ProfileReport

csv_path = sys.argv[1]
html_path = sys.argv[2]

df = pd.read_csv(csv_path)
profile = ProfileReport(df, title="Reporte exploratorio", explorative=True)
profile.to_file(html_path)