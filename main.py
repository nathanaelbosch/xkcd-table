import numpy as np
import datetime as dt
import plac


@plac.annotations(
    total_timeframe=plac.Annotation(type=str))
def main(total_timeframe=5):
    """xkcd table calculated for custom time frames in years

    Columns: How often do you need the task
    Rows: How much time you shave off

    Cell content: How long you can work before spending more than you save
    """
    total_timeframe = eval(total_timeframe)

    task_per_day = np.array([50, 5, 1, 1 / 7, 1 / 30, 1 / 356])
    cols = ["50/d", "5/d", "1/d", "1/w", "1/m", "1/y"]
    time_saved = np.array(
        [1, 5, 30, 1 * 60, 5 * 60, 30 * 60, 60 * 60, 6 * 60 * 60, 24 * 60 * 60]
    )
    rows = ["1s", "5s", "30s", "1m", "5m", "30m", "1h", "6h", "1d"]

    table = task_per_day[:, None] * total_timeframe * 356.25 * time_saved[None, :]

    out = "\t"
    for col in cols:
        out += f"{col}\t"
    out += "\n"
    for row, tablerow in zip(rows, table.transpose()):
        out += f"{row}\t"
        for item in tablerow:
            # round item:
            item = dt.timedelta(seconds=item)
            if item.days/356 > total_timeframe/2:
                out += f""
            elif item.days > 356:
                out += f"{item.days//356}y"
            elif item.days > 30:
                out += f"{item.days//30}m"
            elif item.days > 7:
                out += f"{item.days//7}w"
            elif item.days > 0:
                out += f"{item.days}d"
            elif item.seconds / 60 // 60 > 0:
                out += f"{item.seconds / 60 // 60}h"
            elif item.seconds // 60 > 0:
                out += f"{item.seconds // 60}m"
            elif item.seconds > 0:
                out += f"{item.seconds}s"
            # out += str(item)
            out += "\t"
        out += "\n"
    print(out)


if __name__ == "__main__":
    plac.call(main)
