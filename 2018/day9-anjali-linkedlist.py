class Marble:
    def __init__(self, value):
        self.value = value
        self.prev = None
        self.next = None
 
def play_marble_game(players, last_marble):
    scores = [0] * players
    current_player = 0
    current_marble = Marble(0)
    current_marble.prev = current_marble.next = current_marble
 
    for marble_number in range(1, last_marble + 1):
        if marble_number % 23 == 0:
            for i in range(7):
                current_marble = current_marble.prev
            scores[current_player] += marble_number + current_marble.value
            current_marble.prev.next = current_marble.next
            current_marble.next.prev = current_marble.prev
            current_marble = current_marble.next
        
        else:
            new_marble = Marble(marble_number)
            new_marble.next = current_marble.next.next
            new_marble.prev = current_marble.next
            current_marble.next.next.prev = new_marble
            current_marble.next.next = new_marble
            current_marble = new_marble
 
        current_player = (current_player + 1) % players
 
    return max(scores)
 
# Usage:
players = 493
last_marble = 7186300
highest_score = play_marble_game(players, last_marble)

print(f"The highest score is: {highest_score}")
