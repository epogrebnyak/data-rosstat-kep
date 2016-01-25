import time
import progressbar

bar = progressbar.ProgressBar(max_value=20)
for i in range(20):
    time.sleep(0.1)
    bar.update(i)