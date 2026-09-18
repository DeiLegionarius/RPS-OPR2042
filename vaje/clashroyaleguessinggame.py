import json

def main():
    with open("clashroyalecards.JSON") as file:
        cards = json.load(file)["items"]
    for card in cards:
        if card["name"] == "Knight":
            print(card)
            break
    
if __name__ == "__main__":
    main()