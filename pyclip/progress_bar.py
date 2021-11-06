import sys


def print_progress(index, count, cells):
    progress_percent = (index * 100 // count)
    progress_res = (progress_percent * cells // 100)

    sys.stdout.write("\r[" + "=" * progress_res + " " * (cells - progress_res) + "] {}%".format(progress_percent))
    sys.stdout.flush()
