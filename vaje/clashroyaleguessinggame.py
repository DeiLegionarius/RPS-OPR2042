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

def openFile(name: str, filetype: str):
    with open(f"{name}.{filetype}") as file:
            file = json.load(file)
    return file

def main():
    config = {
        "relevantTraits": ["elixirCost", "rarity", "name"]
    }

    cards = openFile("clashroyalecards", "JSON")["items"]

    card = rnd.choice(cards)
    victory = False

    # Base gameplay loop
    while not victory:

        # Find a card based on input
        currentcard = None
        while currentcard == None:
            currentcard = input("Guess a card name (Case sensitive): ") # case sensitive cause I can't afford a search algorithm currently
            for item in cards:
                if item["name"] == currentcard:
                    currentcard = item

        # output = f"{currentcard["name"]} | "
        output = ""
        for trait in currentcard.keys():
            if card[trait] == currentcard[trait] and trait in config["relevantTraits"]:
                output = f"{output}{colortext(currentcard[trait], "green")}, "
            elif trait in config["relevantTraits"]:
                output = f"{output}{colortext(currentcard[trait], "red")}, "
        if currentcard == card:
            victory = True
        print(output)
    print("You won!!!11!")

        
        
    
if __name__ == "__main__":
    main()