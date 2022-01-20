#!/usr/bin/env python3
from github import Github
import os
import urllib.request, json
import time

DATA_FILENAME = "blood-stocks.json"
OUTPUT_FOLDER = "data"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


def main(access_token: str):
    g = Github(access_token)
    repo = g.get_repo("datascapesg/red-cross-blood-stocks")
    default_branch: str = repo.default_branch
    commits = repo.get_commits()
    for commit in commits:
        # E.g., output: Commit(sha="4725fe2be39d4f4d280bc78d3fa233cb3f34c103")
        print(commit)
        # E.g., output: [File(sha="f5c654f393f6fed25270367977169cd3c537b48d", filename="blood-stocks.json")]
        # print(commit.files)
        commit_datetime = commit.commit.author.date.strftime("%Y_%m_%d-%H_%M_%S")

        # Loop through all files added to this commit
        for file in commit.files:
            # Look for the flat json file
            if file.filename == DATA_FILENAME:
                # Get the raw URL
                datafile_url = file.raw_url
                # Make a network request to get the json data
                data = []
                with urllib.request.urlopen(datafile_url) as url:
                    # Decode it so we can print it (sanity check)
                    data = json.loads(url.read().decode())
                    print(f"Writing {data} to file")
                    with open(
                        OUTPUT_FOLDER + f"/data-{commit_datetime}.json",
                        "w",
                        encoding="utf-8",
                    ) as f:
                        json.dump(data, f, ensure_ascii=False, indent=4)
                # The file can't be present twice in the same commit, so we can move onto the next commit
                break

    pass


if __name__ == "__main__":
    access_token = os.environ["TOKEN"]
    main(access_token)
