import os
import pydicom

root = r"pasname"

series_set = set()

for path, dirs, files in os.walk(root):

    for f in files:

        try:

            ds = pydicom.dcmread(
                os.path.join(path, f),
                stop_before_pixels=True
            )

            desc = ds.get(
                "SeriesDescription",
                "NO_DESC"
            )

            series_set.add(desc)

        except:
            pass

for s in sorted(series_set):
    print(s)
