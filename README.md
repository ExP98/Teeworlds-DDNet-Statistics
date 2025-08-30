# Teeworlds DDNet Statistics
## Different stats using the DDNet database

This repository contains a collection of scripts and notebooks that explore and visualize various statistics derived from the DDNet (DDraceNetwork) public database. The project focuses on understanding players’ progress, team dynamics, map difficulty/completion patterns, and time-based trends, producing both exploratory visuals and structured summaries.

Note: The analyses and results in this repository reflect the state of the DDNet database as of 2020.

- Data source (official zip): https://ddnet.tw/stats/ddnet-stats.zip

## Overview
The goal of this project is to parse the DDNet stats and produce insights such as:
- Player and team rankings over time
- Map completion dynamics (finished vs. unfinished)
- Time-based aggregates (e.g., total time, points per period)
- Similar players analysis and other exploratory views
- Network/graph-based views that can be exported to external tools (e.g., Gephi)

Outputs (plots, tables, intermediate artifacts) are saved in the repository subfolders, primarily under output_files/ and topic-specific directories.

## What this project includes
- Data parsing and cleaning from the official stats dump (placed in ddnet-stats/)
- Topic-focused analyses organized by folders (see Project layout below)
- Reusable utilities for aggregations and plotting
- Exportable datasets/graphs for external tools (e.g., Gephi)

## Analyses by folder (what you’ll find inside)
- finished_unfinished_maps/: completion vs. non-completion breakdowns by map and difficulty; ratios and trends over time.
- Max_points_per_period/: how many points can be accumulated within given time windows; peak periods and activity cycles.
- Team_ranks_research/: exploration of team-based rankings and their evolution; impact of team composition on performance.
- total_time/: cumulative play/finish time summaries; distribution of times across maps and categories.
- top_1/: top-performer snapshots (e.g., best players/maps/periods) with leaderboards.
- similar_players/: heuristics to group players with resembling behavior (e.g., map choices, times, points).
- Map research/: map-centric analyses: difficulty, popularity, completion rates, and progression.
- teams_gephi/: graph exports (e.g., player–team or player–map relations) for network exploration in tools like Gephi.
- Kobra_stats/, parsing and plotting stat/, single_progs/: utility scripts and one-off explorations that support the topics above.
- output_files/: generated figures/tables from multiple analyses.

## Key questions and takeaways
This repository is designed to help answer questions such as:
- How do player and team rankings change across time?
- Which maps are most/least completed and how does difficulty affect completion?
- When are players most active, and how does that translate into points earned per period?
- Who are the “similar” players (by map preferences, completion times, etc.), and what defines their clusters?
- What network structures emerge from player–team–map interactions?

## Getting started

1) Download the data
- Download the official stats archive from: https://ddnet.tw/stats/ddnet-stats.zip
- Unzip it into the repository root so that you get a folder named ddnet-stats containing the original three files from the archive.

2) Environment
- Recommended: Python 3.10+ and Jupyter Notebook/Lab
- Install a minimal set of packages if you don’t already have them:
  - pandas, numpy, matplotlib, seaborn, jupyter

3) Run analyses
- Open Jupyter in the repository root:
- Navigate to the relevant subfolders (see “Project layout” below) and execute notebooks or scripts top-to-bottom.
- If any script expects a specific data path, make sure ddnet-stats/ is at the repository root, or update the path variables in the corresponding script/notebook.

## Project layout
A high-level view of the repository structure:

```
Teeworlds-DDNet-Statistics/
├── ddnet-stats/                 # place the unzipped official data here (not versioned)
├── Kobra_stats/
├── Map research/
├── Max_points_per_period/
├── Team_ranks_research/
├── finished_unfinished_maps/
├── output_files/
├── parsing and plotting stat/
├── similar_players/
├── single_progs/
├── teams_gephi/
├── top_1/
├── total_time/
├── LICENSE.md
└── README.md
```

Notes:
- output_files/ is used by several analyses to store generated plots/tables.
- teams_gephi/ may contain exports suitable for graph exploration tools (e.g., Gephi).
- Folder names with spaces are intentional and used by some notebooks/scripts.

## Usage notes and tips
- Data recency: This repository primarily reflects a data snapshot from 2020. The official stats zip is periodically updated on the DDNet website; re-download for newer snapshots when needed.
- Reproducibility: If you plan to reproduce figures exactly, note your stats snapshot date and pin package versions.
- Performance: Some analyses may require substantial memory/time depending on the size of the dump. Consider filtering or sampling if needed.

## Useful links
These legacy links are kept intact as references:
- https://ddnet.tw/stats/ddnet-stats.zip
- https://forum.ddnet.tw/viewtopic.php?f=3&t=1921
- https://forum.ddnet.tw/viewtopic.php?f=3&t=6835

## License
This project is distributed under the terms of the license in LICENSE.md.

## Acknowledgments
- DDNet community and maintainers for making the public stats available.
- Contributors and users who explore and discuss findings in the forum threads linked above.
- Special thanks to **PeX** for his persistence (oh, it's me!) and to **ad** for his friendliness (Stay (b)ad!! (c)).
