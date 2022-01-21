# Blood Stock Analysis

This repository accompanies the analysis of Singapore's blood stock levels at https://sriramsami.com/bloodstocks.

## Pre-requisites

1. You'll need `python 3+` and `git`
1. Install python packages: `pip install pandas seaborn matplotlib PyGithub`
1. Clone this repository.

## Downloading and analyzing the data

1. Get a GitHub personal access token from https://github.com/settings/tokens/new.
1. Run `TOKEN=<your GitHub personal access token> python3 retrieve.py`. This will download the data to the `data/` subfolder. It'll take a few minutes.
1. Alternatively, you can just download the correct `data.zip` from the Releases page of this repo, there's one from [14th June 2021 to 19th Jan 2022 here](https://github.com/frizensami/frizensami.github.io/releases/download/v0.1/data.zip).
1. When the data is downloaded, run `python3 analyze.py`. This should display the overall graph for blood stocks over time.
