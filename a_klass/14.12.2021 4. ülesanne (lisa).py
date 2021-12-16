# ♥ ♦ ♣ ♠
# full ghetto but it works hey =)

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
        print((10 and 11 and 12 and 13 and 14) in card_only_numbers, card_only_numbers)
        if (10 and 11 and 12 and 13 and 14) in card_only_numbers:
            for elem in cards_:
                final.append(elem.replace('11', 'J').replace('12', 'Q').replace('13', 'K').replace('14', 'A'))
            print(f"Royal flush: {final}")
            return
        
        straight_flush = True
        last_card_value = None
        card_only_numbers = sorted(card_only_numbers)
        for card in card_only_numbers:
            if last_card_value is None:
                last_card_value = card
            elif (card != last_card_value + 1):
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

    max_count = 0
    for elem in card_only_numbers:
        if card_only_numbers.count(elem) > max_count:
            max_count = card_only_numbers.count(elem)
    
    if max_count == 4:
        final = []
        for elem in cards_:
            final.append(elem.replace('11', 'J').replace('12', 'Q').replace('13', 'K').replace('14', 'A'))
        print(f"Four of a kind: {final}")
        return

    has_three_same_cards = False
    has_two_same_cards = False
    three_card = 0

    for elem in card_only_numbers:
        if not has_three_same_cards and card_only_numbers.count(elem) == 3:
            has_three_same_cards = True
            three_card = elem
    
    for elem in card_only_numbers:
        if not has_two_same_cards and elem != three_card and card_only_numbers.count(elem) == 2:
            has_two_same_cards = True

    if has_three_same_cards and has_two_same_cards:
        final = []
        for elem in cards_:
            final.append(elem.replace('11', 'J').replace('12', 'Q').replace('13', 'K').replace('14', 'A'))
        print(f"Full house: {final}")
        return

    straight = True
    last_card_value = None
    card_only_numbers = sorted(card_only_numbers)
    for card in card_only_numbers:
            if last_card_value is None:
                last_card_value = card
            elif (card != last_card_value + 1):
                straight = False
            last_card_value = card

    if straight:
        final = []
        for elem in cards_:
            final.append(elem.replace('11', 'J').replace('12', 'Q').replace('13', 'K').replace('14', 'A'))
        print(f"Straight: {final}")
        return
    
    if has_three_same_cards:
        final = []
        for elem in cards_:
            final.append(elem.replace('11', 'J').replace('12', 'Q').replace('13', 'K').replace('14', 'A'))
        print(f"Three of a kind: {final}")
        return

    has_first_two_pair = False
    first_two_pair_card = 0
    has_second_two_pair = False
    for elem in card_only_numbers:
        if card_only_numbers.count(elem) == 2:
            has_first_two_pair = True
            first_two_pair_card = elem
    
    for elem in card_only_numbers:
        if elem != first_two_pair_card and card_only_numbers.count(elem) == 2:
            has_second_two_pair = True

    if has_first_two_pair and has_second_two_pair:
        final = []
        for elem in cards_:
            final.append(elem.replace('11', 'J').replace('12', 'Q').replace('13', 'K').replace('14', 'A'))
        print(f"Two pairs: {final}")
        return
    
    if has_first_two_pair:
        final = []
        for elem in cards_:
            final.append(elem.replace('11', 'J').replace('12', 'Q').replace('13', 'K').replace('14', 'A'))
        print(f"One pair: {final}")
        return

    final = []
    for elem in cards_:
        final.append(elem.replace('11', 'J').replace('12', 'Q').replace('13', 'K').replace('14', 'A'))
    print(f"Bad hand: {final}")
    return
    

kasi("9♥", "2♥", "J♣", "10♥", "Q♥")
