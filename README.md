# Dota 2 Match Winning team Prediction

## Data Collection

Firstly, we collect *38,357* public matches data using [OpenDota Explorer](https://www.opendota.com/explorer)

Below is the query we used:

```{SQL}
select * 
from public_matches 
where avg_mmr > 5000 and 
    lobby_type = 7 and 
    game_mode = 22 and 
    start_time > 1535760000 and
    start_time < 1539280800
```

Then, we save the result as `public_matches.json` by clicking the *API*.

The `public_matches.json` will contain several fields, i.e. `command`, `rowCount`, `oid`, `rows`, `fields`, `_parsers`, `RowCtor`, `rowAsArray`, and `err`. Below is a sample of the `rows` field:

```
{'match_id': 4154000815,
 'match_seq_num': 3599507325,
 'radiant_win': False,
 'start_time': 1538765662,
 'duration': 2470,
 'avg_mmr': 5001,
 'num_mmr': 6,
 'lobby_type': 7,
 'game_mode': 22,
 'avg_rank_tier': 77,
 'num_rank_tier': 7,
 'cluster': 123}
```

After querying the public matches, we extract the more detailed matches data using the [OpenDota API](https://docs.opendota.com/#) based on the `match_ids` we queried.

Another API alternative is to use [this](https://wiki.teamfortress.com/wiki/WebAPI#Dota_2) which requires *Steam API key*.

After extracting the data, we reformat and save it to a `csv` format.

## References

- http://cs229.stanford.edu/proj2013/PerryConley-HowDoesHeSawMeARecommendationEngineForPickingHeroesInDota2.pdf
- http://cs229.stanford.edu/proj2015/249_report.pdf
- http://cs229.stanford.edu/proj2017/final-reports/5233394.pdf
- http://cs230.stanford.edu/projects_spring_2018/reports/8290559.pdf
- https://dspace.cvut.cz/bitstream/handle/10467/76831/F8-BP-2018-Beskyd-Filip-thesis.pdf?sequence=-1
- http://jmcauley.ucsd.edu/cse255/projects/fa15/018.pdf
- http://ceur-ws.org/Vol-1842/paper_05.pdf
