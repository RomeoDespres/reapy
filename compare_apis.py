import os, pandas as pd

api = pd.read_csv(os.path.join(os.path.dirname(__file__), "docs", "api.csv"))
done = ~(api.iloc[:, 1] == "TODO")
print("{:.1f}% done ({}/{})".format(done.mean()*100, done.sum(), len(done)))
