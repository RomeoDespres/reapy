import os, pandas as pd

api = pd.read_csv(os.path.join(os.path.dirname(__file__), "docs", "api.csv"))
api = api.drop(api.iloc[:, 1] == "DEPRECATED")
done = ~(api.iloc[:, 1] == "TODO")
print("{:.1f}% done ({}/{})".format(done.mean()*100, done.sum(), len(done)))


classes = "track", "take", "item", "project", "source"
series = pd.DataFrame(0, index=classes, columns=["%", "done", "total"])

for c in classes:
    mask = api.iloc[:, 0].apply(lambda s:c in s.lower())
    series.loc[c] = done[mask].mean()*100, done[mask].sum(), mask.sum()
    
print(series.round(1))
