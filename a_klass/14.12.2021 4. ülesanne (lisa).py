# ♥ ♦ ♣ ♠
# work in progress, currently only checks for flushes

def kasi(*cards):
    # clamp cards in hand
    cards = cards[:5]
    
    # put cards into a string and replace letters with numbers
    cards_ = ""
    card_only_numbers = []
    for card in cards:
        cards_ += f"{card} "
    cards_ = cards_.replace("J", "11").replace("Q", "12").replace("K", "13").replace("A", "14")
    cards_ = cards_.split(" ")[:5]

    for card in cards_:
        card_only_numbers.append(int(card[0:len(card) - 1]))

    last_same_image = None
    all_same_image = True
    for card in cards_:
        if last_same_image is None:
            last_same_image = card[-1]
        elif card[-1] != last_same_image:
            all_same_image = False
    
    print(f"sama mast: {str(all_same_image).lower()}")

    # flushes (royal, straight, normal)
    if all_same_image:
        final = []
        # royal flush
        if (10 and 11 and 12 and 13 and 14) in card_only_numbers:
            for elem in cards_:
                final.append(elem.replace('11', 'J').replace('12', 'Q').replace('13', 'K').replace('14', 'A'))
            print(f"Royal flush: {final}")
            return
        
        straight_flush = True
        last_card_value = None
        card_only_numbers = sorted(card_only_numbers)
        for card in card_only_numbers:
            print(card, last_card_value)
            if last_card_value is None:
                last_card_value = card
            elif card != last_card_value + 1:
                straight_flush = False
            last_card_value = card
        
        if straight_flush:
            final = []
            for elem in cards_:
                final.append(elem.replace('11', 'J').replace('12', 'Q').replace('13', 'K').replace('14', 'A'))
            print(f"Straight flush: {final}")
            return
        
        final = []
        for elem in cards_:
            final.append(elem.replace('11', 'J').replace('12', 'Q').replace('13', 'K').replace('14', 'A'))
        print(f"Normal flush: {final}")        


kasi("7♥", "2♥", "4♥", "9♥", "J♥")
