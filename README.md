# XCP Asset List

Outputs a list of assets from the Counterparty DB.

## How It Works

You need a copy of the Counterparty DB, ideally from [running a node](https://counterparty.io/docs/federated_node/). Alternatively, download a DB from Nov 2021 on [Dropbox](https://www.dropbox.com/s/ypad33bv6dzmgaf/counterparty-db.latest.tar.gz?dl=0).

Point `asset_list.py` to the DB file and it will output a csv file of all assets, including relevant timestamps (YYYY-MM-DD) and supply.

The script `asset_list_filtered.py` outputs only assets with a locked supply of maximum 3000 and a history of DEX trading. These parameters can easily be tweaked from within the source code.

I've compiled lists in case you do not want to run the scripts yourself:

- `xcp_assets.csv` is a complete list of more than 100,000 registrations.
- `xcp_assets_filtered.csv` contains less than 2000 assets with real usage from 2014-2017.

## CSV Columns

- 'asset' – unique name of the asset 
- 'reg_date' – date of initially registering the name, YYYY-MM-DD
- 'locked' – 1 if supply is locked, else 0
- 'lock_date' – date of locking the supply, empty if still unlocked
- 'traded' – 1 if the token has been traded on the DEX, else 0
- 'trade_date' – date of first completed DEX trade, empty if still untraded
- 'completed' – 1 if both 'locked' and 'traded' are 1, else 0
- 'complete_date' – the last of 'lock_date' or 'trade_date' if 'completed' is 1, else empty
- 'divisible' – 1 if divisible token, 0 if indivisible
- 'tokens_issued' – quantity of tokens ever issued
- 'tokens_destroyed' – quantity of tokens ever destroyed
- 'token_supply' – 'tokens_issued' minus 'tokens_destroyed'

## Donate

* BTC: bc1qg8vldv8kk4mqafs87z2yv0xpq4wr4csucr3cj7
* DOGE: DChdsuLuEvAPZb9ZXpiEpimgidSJ5VqShq
* ETH: 0x4144CbaF54044510AB2F2f3c51061Dd5558cD604

## License

MIT