#Outputs a csv with a list of all Counterparty assets
''' Columns:
'asset'            unique name of the asset 
'reg_date'         date of initially registering the name, YYYY-MM-DD
'locked',          1 if supply is locked, else 0
'lock_date'        date of locking the supply, empty if still unlocked
'traded'           1 if the token has been traded on the DEX, else 0
'trade_date'       date of first completed DEX trade, empty if still untraded
'completed'        1 if both 'locked' and 'traded' are 1, else 0
'complete_date'    the last of 'lock_date' or 'trade_date' if 'completed' is 1, else empty
'divisible'        1 if divisible token, 0 if indivisible
'tokens_issued'    quantity of tokens ever issued
'tokens_destroyed' quantity of tokens ever destroyed
'token_supply'     'tokens_issued' minus 'tokens_destroyed'
'''

db_file = 'counterparty.db'

import csv
from datetime import datetime

import os
dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_path)

import sqlite3
con = sqlite3.connect(db_file)
cur = con.cursor()


#Block timestamps  
ts = [None] * 8000000
for row in cur.execute('SELECT block_index, block_time FROM blocks;'):
  timestamp = row[1]
  dt_object = datetime.fromtimestamp(timestamp)
  dt_object = str(dt_object)[0:10] #YYYY-MM-DD
  ts[row[0]] = dt_object


#Assets
assets = []
subassets = []
for row in cur.execute('SELECT asset_name, block_index, asset_longname FROM assets;'):
  if row[0] != 'BTC' and row[0] != 'XCP':
    assets.append([row[0], ts[row[1]]])
    subassets.append(row[2])


#Lock
for asset in assets:
  locked = 0
  for row in cur.execute("SELECT block_index FROM issuances WHERE asset = '"+asset[0]+"' AND locked = 1 AND status = 'valid';"):
    locked = row[0]
  if locked > 0:    
    asset.append(1)
    asset.append(ts[row[0]])
  else: 
    asset.append(0)
    asset.append('')

    
#Trade
# In every trade there's one "forward_asset" and one "backward_asset".
# Typically you sell a forward_asset for XCP or BTC.
# But in some cases you make a swap where your asset could be the backward_asset. Therefore check both.
for asset in assets:
  traded = 1e10
  for row in cur.execute("SELECT block_index FROM order_matches WHERE forward_asset = '"+asset[0]+"' AND status = 'completed' ORDER BY block_index LIMIT 1;"):
    traded = row[0]
  for row in cur.execute("SELECT block_index FROM order_matches WHERE backward_asset = '"+asset[0]+"' AND status = 'completed' ORDER BY block_index LIMIT 1;"):
    traded = min(row[0], traded)
  if traded < 1e10:
    asset.append(1)
    asset.append(ts[traded])
  else: 
    asset.append(0)
    asset.append('')
    
    
#Completed (if all 3 - issue, lock, trade have happened)
for asset in assets:
  if asset[2] == 1 and asset[4] == 1: #locked and traded
    asset.append(1)
    asset.append(max(asset[1], asset[3], asset[5]))
  else:
    asset.append(0)
    asset.append('')


#Divisibility
for asset in assets:
  for row in cur.execute("SELECT divisible FROM issuances WHERE asset = '"+asset[0]+"' AND status = 'valid' LIMIT 1;"):
        asset.append(row[0])


#Issued supply
for asset in assets:
  for row in cur.execute("SELECT TOTAL(quantity) FROM issuances WHERE asset = '"+asset[0]+"' AND status = 'valid';"):
    supply = row[0]
  div = asset[8]
  if div == 1:
    supply /= 1e8    
  asset.append(supply)

  
#Destroyed supply
for asset in assets:
  for row in cur.execute("SELECT TOTAL(quantity) FROM destructions WHERE asset = '"+asset[0]+"' AND status = 'valid';"):
    destroyed = row[0]
  div = asset[8]
  if div == 1:
    destroyed /= 1e8    
  asset.append(destroyed)

  
#Net supply
for asset in assets:
  asset.append(asset[9]-asset[10])


#Replace numeric with subasset (asset_longname) where applicable
for i in range(len(assets)):
  if '.' in str(subassets[i]):
    assets[i][0] = subassets[i]  


#Add header row
assets.insert(0, ['asset', 'reg_date', 'locked', 'lock_date', 'traded', 'trade_date', 'completed', 'complete_date', 'divisible', 'tokens_issued', 'tokens_destroyed', 'token_supply'])

  
#Write .csv file
file = open('xcp_assets.csv', 'w+', newline ='')
with file:   
  write = csv.writer(file)
  write.writerows(assets)
con.close()