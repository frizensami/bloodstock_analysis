#!/usr/bin/env python3
import os
from retrieve import OUTPUT_FOLDER
import datetime
from pprint import pprint
import json
from typing import List, Set, Dict, Tuple, Optional, Any
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


def filename_to_datetime(filename: str):
    file_date_str = filename.split("-")[1] + "-" + filename.split("-")[2].split(".")[0]
    file_date = datetime.datetime.strptime(file_date_str, "%Y_%m_%d-%H_%M_%S")
    return file_date


# Return files in sorted order with earliest file first
def get_sorted_filenames(folder: str) -> List[str]:
    files = os.listdir(folder)
    sorted_files = sorted(files, key=filename_to_datetime)
    pprint(sorted_files)
    print(f"Number of files: {len(sorted_files)}")
    return sorted_files


# For each file, process their data as json, and append to list
def sorted_files_to_data(sorted_filenames: List[str]) -> List[Dict[str, Any]]:
    data = []
    for file in sorted_filenames:
        with open(f"{OUTPUT_FOLDER}/{file}") as f:
            json_data = json.load(f)
            json_datetime = filename_to_datetime(file)
            file_data = {"datetime": json_datetime, "data": json_data}
            data.append(file_data)
    return data


def filedata_to_dataframe(data):
    timestamps = list(map(lambda d: d["datetime"], data))
    bloodtypes = list(map(lambda d: d["bloodType"], data[0]["data"]))
    all_data = list(map(lambda d: d["data"], data))
    df_dict = {bloodtype: [] for bloodtype in bloodtypes}
    for data_row in all_data:
        for bloodtype_data in data_row:
            df_dict[bloodtype_data["bloodType"]].append(
                int(bloodtype_data["fillLevel"][:-1])  # Remove %
            )
    df_dict["Time"] = timestamps
    df = pd.DataFrame.from_dict(df_dict)
    print(df)
    return df


def plot_dataframe(df):
    # select all columns except 'rebounds' and 'assists'
    df_positive = df.loc[:, df.columns.isin(["Time", "A+", "B+", "O+", "AB+"])]
    df_negative = df.loc[:, df.columns.isin(["Time", "A-", "B-", "O-", "AB-"])]
    dfm_pos = df_positive.melt("Time", var_name="Blood Type", value_name="Stock Level")
    dfm_neg = df_negative.melt("Time", var_name="Blood Type", value_name="Stock Level")
    sns.set_palette("bright")
    sns.set_theme()
    # sns.set_style("white")
    sns.set_context("notebook", font_scale=1.5, rc={"lines.linewidth": 2.5})
    fig, axes = plt.subplots(2, 1, sharey=True)
    axes[0].set_title(r"$\bf{" + "Positive" + "}$" + " Blood Groups")
    axes[0].set_ylabel("Stock Level (%)")
    axes[0].set_xlabel("")
    axes[0].xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    # axes[0].xaxis.set_major_locator(mdates.WeekdayLocator(interval=4))
    axes[0].xaxis.set_major_locator(mdates.MonthLocator())
    axes[0].xaxis.set_minor_locator(mdates.WeekdayLocator())
    # axes[0].tick_params(axis="x", labelrotation=30)
    axes[1].set_title(r"$\bf{" + "Negative" + "}$" + " Blood Groups")
    axes[1].set_ylabel("Stock Level (%)")
    axes[1].xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    # axes[0].xaxis.set_major_locator(mdates.WeekdayLocator(interval=4))
    axes[1].xaxis.set_major_locator(mdates.MonthLocator())
    # axes[0].tick_params(axis="x", labelrotation=30)

    fig.suptitle(
        "Singapore Blood Stock Levels \n (Mid-June 2021 to Mid-Jan 2022, 219 days)"
    )
    sns.despine()
    sns.lineplot(
        ax=axes[0],
        x="Time",
        y="Stock Level",
        hue="Blood Type",
        marker="o",
        data=dfm_pos,
    )
    sns.lineplot(
        ax=axes[1],
        x="Time",
        y="Stock Level",
        hue="Blood Type",
        marker="o",
        data=dfm_neg,
    )
    axes[0].legend(loc="lower center", title="Blood Type")
    axes[0].set(xlabel=None)
    axes[1].set(xlabel=None)
    # sns.lineplot(data=df, x="timestamps")
    plt.show()


def main():
    sorted_filenames = get_sorted_filenames(OUTPUT_FOLDER)
    data = sorted_files_to_data(sorted_filenames)
    df = filedata_to_dataframe(data)
    plot_dataframe(df)


if __name__ == "__main__":
    main()
