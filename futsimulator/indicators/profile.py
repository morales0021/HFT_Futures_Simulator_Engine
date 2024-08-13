from futsimulator.indicators.ladder import PriceLadder

class VolumeProfile:

    def __init__(self, size_up, size_down, tick_unit):

        self.profile = None
        self.ladder = None
        self.size_up = size_up
        self.size_down = size_down
        self.tick_unit = tick_unit

    def update(self, snapshot):

        if not self.ladder:
            self.ladder = PriceLadder(
                snapshot.init_price, self.size_up, self.size_down,
                self.tick_unit, init_val=0
                )

        if self.ladder.data[snapshot.price]:
            self.ladder.data[snapshot.price] +=  snapshot.size
        else:
            self.ladder.data[snapshot.price] =  snapshot.size
        
        self.profile = self.ladder.data

    def __str__(self):
        
        data = ""
        for key, value in self.profile.items():
            if value:
                data += f"{key}: {value} \n"

        return data