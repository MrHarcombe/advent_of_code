import io

class Bot:
    def __init__(self, number, low=None, high=None):
        self._number = number
        self._low = low
        self._high = high
        self._processed = False
        self._values = []

    @property
    def number(self):
        return self._number

    @property
    def low(self):
        return self._low
    
    @low.setter
    def low(self, low):
        self._low = low

    @property
    def high(self):
        return self._high
    
    @high.setter
    def high(self, high):
        self._high = high

    def add_value(self, value):
        self._values.append(value)
        
    def is_ready(self):
        return len(self._values) == 2 and self._low != None and self._high != None
    
    @property
    def processed(self):
        return self._processed
        
    def process(self, values):
        if self.is_ready():
            self._processed = True
            
            if isinstance(self._low, Bot):
                self.low.add_value(min(self._values))
            else:
                values[self.low] = min(self._values)

            if isinstance(self.high, Bot):
                self._high.add_value(max(self._values))
            else:
                values[self._high] = max(self._values)
        else:
            print("Stop! This Bot is not ready!")
            
    def __str__(self):
        return f"(#:{self._number}, l:{'B' + str(self._low.number) if isinstance(self._low, Bot) else self._low}, h:{'B' + str(self._high.number) if isinstance(self._high, Bot) else self._high}, v:{self._values}, p:{self._processed})"


def parse_line(command, bots, values):
    parts = command.split()
    if parts[0] == "value":
        value = int(parts[1])
        bot_number = int(parts[5])
        if bot_number in bots:
            bots[bot_number].add_value(value)
        else:
            new_bot = Bot(bot_number)
            new_bot.add_value(value)
            bots[bot_number] = new_bot

    else:
        bot_number = int(parts[1])
        if bot_number not in bots:
            bots[bot_number] = Bot(bot_number)
        
        low_value = int(parts[6])
        if parts[5] == "bot":
            if low_value in bots:
                low_value = bots[low_value]
            else:
                new_bot = Bot(low_value)
                bots[low_value] = new_bot
                low_value = new_bot
            
        bots[bot_number].low = low_value
        
        high_value = int(parts[11])
        if parts[10] == "bot":
            if high_value in bots:
                high_value = bots[high_value]
            else:
                new_bot = Bot(high_value)
                bots[high_value] = new_bot
                high_value = new_bot
                
        bots[bot_number].high = high_value


if __name__ == "__main__":
    test = """value 5 goes to bot 2
bot 2 gives low to bot 1 and high to bot 0
value 3 goes to bot 1
bot 1 gives low to output 1 and high to bot 0
bot 0 gives low to output 2 and high to output 0
value 2 goes to bot 2"""

    bots = {}
    values = {}

    # with io.StringIO(test) as f:
    with open("input10.txt") as f:
        for line in f:
            parse_line(line.strip(), bots, values)

    #print(bots)
    #print(values)

    while False in [bots[bot_number].processed for bot_number in bots]:
        for bot_number in bots:
            if bots[bot_number].is_ready() and not bots[bot_number].processed:
                bots[bot_number].process(values)

    #print(bots)
    #print(values)
    for bot in bots:
        if 61 in bots[bot]._values and 17 in bots[bot]._values:
            print(bots[bot])
            
    print(values[0] * values[1] * values[2])
