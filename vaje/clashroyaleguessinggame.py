import json
import random as rnd

def colortext(text, color):
    colors = {
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "magenta": "\033[95m",
        "cyan": "\033[96m",
        "white": "\033[97m",
        "reset": "\033[0m"
    }
    return f"{colors.get(color, colors['reset'])}{text}{colors['reset']}"

def main():
    with open("clashroyalecards.JSON") as file:
        cards = json.load(file)["items"]
    card = rnd.choice(cards)
    chosencard = None
    while chosencard != card:
        while chosencard == None:
            chosencard = input("Guess a card name (Case sensitive): ")
            for item in cards:
                if item["name"] == chosencard:
                    chosencard = item
        
        
    
if __name__ == "__main__":
    main()