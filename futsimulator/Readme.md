# Futsimulator

## Initialisation
To initialise a fut simulator you need to initialise a market snapshot object, a position manager and set a configuration for the commissions. 

A market snapshot contains the price data that will be used by the futsimulator.

```

ms = MarketSnapshot(idx, symbol, bid_arr, ask_arr, time_arr, indicators_arr)
 
```

The position manager is initialised as follows :

```
ps = PositionManager(ms, max_b_size, max_s_size, commission_cfg)
```


## Position Manager methods

The following methods are available :

- Send a market order
- Liquidate
- Get infos
- Update
- Send limit order
- Send stop order
- Modify limit or stop order
- Delete a limit or stop order

**Send market order**

To send a market order we precise the side, size, take profit and stoploss.

```
ps.send_market_order(side, size, tp, sl)
```

**Liquidate**

Liquidate all the market orders (limit order or stop orders are not included )

```
ps.liquidate()
```

**Get infos**

Provides all the market orders, limit orders and stop orders opened. For the closed orders, those are also are provided as historical data.

```
ps.get_infos()
```

**Update**

This method is very important because it allows to update the current profit and loss of the orders that are opened. This method requires the market snapshot to be updated by one index. For instance the position manager should be updated as follows:

```
ms.update()
ps.update()
```

**Send limit/stop order**

To send a limit/sop order you use the following method

```

ps.send_limit_order(price, side, size, tp, sl)
ps.send_stop_order(price, side, size, tp, sl)

```

**Modify limit/stop order**

Modifies a limit or stop order

```
ps.modify_ls_order(id_order, price, size, tp, sl)
```

**Delete a limit/stop order**

Deletes a limit or stop order

```
ps.delete_ls_order(id_order)
```