def get_total_pnl(infos: dict, closed: bool = True):
    """
    Computes the total profit and loss from the output
    provided from get_infos method from the position manager
    """
    total = 0
    if closed:
        for id_order, order_data in infos["closed_orders"].items():
            total += order_data['cl_pnl']
    else:
        total = infos['open_orders']['o_pnl']

    return total