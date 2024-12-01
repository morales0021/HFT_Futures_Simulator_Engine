# Futsimulator

## Initialisation
To initialise a fut simulator you need to initialise a market snapshot object, a position manager and set a configuration for the commissions. 

A market snapshot contains the price data that will be used by the futsimulator.

```

ms = MarketSnapshot(idx, symbol, bid_arr, ask_arr, time_arr, indicators_arr)
 
```

The position manager is initialised as follows and should include a market snapshot instance:

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
This method doesn't return any value. When a market order is sent, then at the current tick, its verified if any stop loss or take profit has been reached, if that is the case, then such opened positions will be moved to a closed position. This also includes the current market order that has been sent with a stop loss or a take profit that automatically makes it to be closed.

Everytime we send a market order, such order is converted to a position. This position contains a position id that will be later used to identify it, in particular when the position will be closed.

**Liquidate**

Liquidate (flattens) all the market orders (limit order or stop orders are not included )

```
ps.liquidate()
```

This method doesn't returns any value. 

**Get infos**

Provides all the information for the market orders, limit orders and stop orders that are opened. It also provides all the closed orders.

```
ps.get_infos()
```

For example, the following is a return from this method:
```
{'closed_orders': {},
 'limit_orders': [],
 'open_orders': {'av_cl_price': 0.0,
                 'av_o_price': 11.0,
                 'cl_pnl': 0.0,
                 'delta_t': 0.0,
                 'o_pnl': -10.0,
                 'side': <SideOrder.buy: 1>,
                 'total_orders': 2,
                 'total_size': 10},
 'stop_orders': []}
```

Observe that the key ```"opened_orders"``` is a dictionary that contains the netting of all the positions. Is not possible to have buy and sell positions simultaneously, this is because the engine is netting based, which means that if a buy position was sent, and then a sell position was sent, then the final position will be the difference between them.

The key `"total_orders"` represents the total orders that have been worked with a market order, limit order or stop order. The key `"total_size"` represents the total lots that are being considered in the netting position.

The key ```"closed_orders"``` is a dictionary that contains all the positions that were previously opened and that now are closed. The positions that has been closed are identified by their position id. For example  :

```
{'closed_orders': {1: {'av_cl_price': 10.0,
                       'av_o_price': 11.0,
                       'cl_pnl': -5.0,
                       'delta_t': 0.0,
                       'o_pnl': 0.0,
                       'side': <SideOrder.buy: 1>,
                       'total_orders': 1,
                       'total_size': 5},
                   2: {'av_cl_price': 10.0,
                       'av_o_price': 11.0,
                       'cl_pnl': -5.0,
                       'delta_t': 0.0,
                       'o_pnl': 0.0,
                       'side': <SideOrder.buy: 1>,
                       'total_orders': 1,
                       'total_size': 5}},
 'limit_orders': [],
 'open_orders': {'av_cl_price': 0.0,
                 'av_o_price': 0.0,
                 'cl_pnl': 0.0,
                 'delta_t': 0.0,
                 'o_pnl': 0.0,
                 'side': None,
                 'total_orders': 0,
                 'total_size': 0},
 'stop_orders': []}
 ```

 If an previous sent order contained a size of 5 lots, and then 3 lots are closed by an opposite order, those closed positions will be stacked together in their position id in the ```"closed_order"``` key. The remaining 2 lots will be also aggregated to their position id key when those would be closed later.

**Update**

In order to simulate that we moved one timestep in the market data, we need to call the method update from the snapshot instance :
```
ms.update()
```

This method doesn't automatically update the information in the manager. For instance, if you call 
```
manager.get_infos()
```
this method will return the information of the positions with respect to the previous tick and not the updated tick. That's why is important to call the ```update``` method from the manager after the snapshot update :

```
ms.update()
ps.update()
```

This allows to update the current profit and loss of the orders that are opened. 

Sometimes is not necessary to call the update method from the mananager, everytime we send a **market order** or a **liquidate action**, the update method is called automatically and all the orders and positions are update with respect to the last snapshot update. For instance, doing

```
ms.update()
ps.update()
ps.send_market_order(side, size, tp, sl) # or ps.liquidate()
```
is equivalent to :
```
ms.update()
ps.send_market_order(side, size, tp, sl) # or ps.liquidate()
```

**Send limit/stop order**

To send a limit/sop order you use the following method :
```
ps.send_limit_order(price, side, size, tp, sl)
ps.send_stop_order(price, side, size, tp, sl)

```
When you send a limit/stop order, then the manager updates automatically and verifies if such order should be already executed or not (similar when sending a market order).

**Modify limit/stop order**

Modifies a limit or stop order :
```
ps.modify_ls_order(id_order, price, size, tp, sl)
```
Is required to precise the order id of the limit/stop order. If such order id is not correct or it 
doesn't exists as a pending order, then it will be ignored. This method doesn't return any value.
When you modify an order, then the manager updates automatically, if the take profit or stop loss are inside the price (best bid or best ask), then the order will be exercised.

**Modify market order**
Modifies the stoploss or takeprofit from a market order :
```
ps.modify_market_order(id_order, tp, sl)
```
Is required to precise the order if of the market order. If such order id is not correct or it doesn't exists, then it will be ignored. The method doesn't return any value. When you modify an order, then the manager updates automatically, if the take profit or stop loss are inside the price (best bid or best ask), then the order will be closed.

**Delete a limit/stop order**

Deletes a limit or stop order

```
ps.delete_ls_order(id_order)
```

This method deletes any pending stop/limit order.