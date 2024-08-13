from futsimulator.indicators.ladder import PriceLadder
from typing import Literal
from futsimulator.positions.position import SideOrder

class CurrentPositions:

    def __init__(self, size_up, size_down, tick_unit):
        """
        Defines a the position of bid and ask
        """

        self.size_up = size_up
        self.size_down = size_down
        self.tick_unit = tick_unit
        self.ladder = None
        self.ladder_time = None
        self.positions = None

    def update(self, manager):
        
        snapshot = manager.snapshot
        
        if not self.ladder:

            self.ladder = PriceLadder(
                snapshot.init_price, self.size_up, self.size_down,
                self.tick_unit, init_val = 0
                )
        else:
            self.ladder.reset()

        info_pos = manager.get_infos()
        open_orders = info_pos["open_orders"]
        o_side = open_orders['side']
        for pos in open_orders['opened']:
            o_price = pos['open_price']
            total_size = pos['size']
            if o_side == SideOrder.buy:
                n_side = total_size
            elif o_side == SideOrder.sell:
                n_side = -total_size
            else:
                raise Exception("invalid side")
            self.ladder.data[o_price] = n_side

        self.positions = self.ladder.data

    def __str__(self):
        
        data = ""
        for key, value in self.ladder.data.items():
            if value:
                data += f"{key}: {value} \n"

        return data