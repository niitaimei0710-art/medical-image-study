import os
import pydicom

root = r""

for se in sorted(os.listdir(root)):

    se_path = os.path.join(root, se)

    if not os.path.isdir(se_path):
        continue

    found = False

    for path, dirs, files in os.walk(se_path):

        for f in files:

            try:

                ds = pydicom.dcmread(
                    os.path.join(path, f),
                    stop_before_pixels=True
                )

                print(
                    f"{se:4s} : "
                    f"{ds.SeriesNumber:3d} : "
                    f"{ds.SeriesDescription}"
                )

                found = True
                break

            except:
                pass

        if found:
            break
