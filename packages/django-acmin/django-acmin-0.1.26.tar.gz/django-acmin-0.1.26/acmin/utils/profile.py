import json
import linecache
import logging
import time
import tracemalloc
from collections import OrderedDict

logger = logging.getLogger(__name__)


def humanbytes(B):
    'Return the given bytes as a human friendly KB, MB, GB, or TB string'
    B = float(B)
    KB = float(1024)
    MB = float(KB ** 2)  # 1,048,576
    GB = float(KB ** 3)  # 1,073,741,824
    TB = float(KB ** 4)  # 1,099,511,627,776

    if B < KB:
        return '{0} {1}'.format(B, 'Bytes' if 0 == B > 1 else 'Byte')
    elif KB <= B < MB:
        return '{0:.2f} KB'.format(B / KB)
    elif MB <= B < GB:
        return '{0:.2f} MB'.format(B / MB)
    elif GB <= B < TB:
        return '{0:.2f} GB'.format(B / GB)
    elif TB <= B:
        return '{0:.2f} TB'.format(B / TB)


def display_top(snapshot, key_type='lineno', limit=5):
    snapshot = snapshot.filter_traces((
        tracemalloc.Filter(False, "<frozen importlib._bootstrap>"),
        tracemalloc.Filter(False, "<unknown>"),
    ))
    top_stats = snapshot.statistics(key_type)

    for index, stat in enumerate(top_stats[:limit], 1):
        frame = stat.traceback[0]  # tracemalloc.Frame
        line = linecache.getline(frame.filename, frame.lineno).strip()
        if line:
            pass#print('    %s' % line)

    other = top_stats[limit:]
    if other:
        size = sum(stat.size for stat in other)
        #print("%s other: %.1f KiB" % (len(other), size / 1024))
    total = sum(stat.size for stat in top_stats)
    #print("Total allocated size: %.1f KiB" % (total / 1024))


def get_top(key, limit=5):
    snapshot = tracemalloc.take_snapshot()
    snapshot = snapshot.filter_traces((
        tracemalloc.Filter(False, "<frozen importlib._bootstrap_external>"),
        tracemalloc.Filter(False, "<unknown>"),
    ))
    linenos = snapshot.statistics(key)
    # from tracemalloc import Statistic,Traceback
    result = []
    for index, stat in enumerate(linenos[:limit], 1):
        frame = stat.traceback[0]  # tracemalloc.Frame
        line = linecache.getline(frame.filename, frame.lineno).strip()
        obj = OrderedDict()
        obj["index"] = index
        obj["allocated"] = humanbytes(stat.size)
        obj["blocks"] = stat.count
        obj["filename"] = frame.filename
        obj["lineno"] = frame.lineno
        obj["code"] = line

        result.append(obj)
    return result


def show_trace():
    if not tracemalloc.is_tracing():
        logger.info("tracemalloc.start() begin")
        tracemalloc.start()
        time.sleep(1)

    logger.info(json.dumps({
        "memory_allocate": get_top('lineno'),
        "memory_block": get_top("traceback")
    }))
