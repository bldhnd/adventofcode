from enum import IntEnum
import puzzleinput


class Hand(IntEnum):
    HIGH_CARD = 0
    ONE_PAIR = 1
    TWO_PAIR = 2
    THREE_OF_A_KIND = 3
    FULL_HOUSE = 4
    FOUR_OF_A_KIND = 5
    FIVE_OF_A_KIND = 6

def problem_2() -> None:
    def parser(puzzle_input: str) -> list[tuple]:
        pos = 0
        ch = ""

        result = []

        while pos < len(puzzle_input):
            hand = ""
            bid = ""

            ch = puzzle_input[pos]

            while ch != " ":
                hand += ch
                pos += 1
                ch = puzzle_input[pos]

            kind = hand_strength(strengthen_hand_with_jokers(hand))

            pos += 1
            ch = puzzle_input[pos]

            while ch.isnumeric():
                bid += ch
                pos += 1
                ch = puzzle_input[pos] if pos < len(puzzle_input) else ""

            pos += 1

            slow_insert_hand((hand, int(bid), kind), result)
        
        return result
    
    def hand_strength(hand: str) -> Hand:
        temp = {label: hand.count(label) for label in hand}

        card_counts = temp.values()
        
        if len(card_counts) == 4:
            return Hand.ONE_PAIR
        
        if len(card_counts) == 3:
            return Hand.THREE_OF_A_KIND if 3 in card_counts else Hand.TWO_PAIR
        
        if len(card_counts) == 2:
            return Hand.FOUR_OF_A_KIND if 4 in card_counts else Hand.FULL_HOUSE
        
        if len(card_counts) == 1:
            return Hand.FIVE_OF_A_KIND
        
        return Hand.HIGH_CARD

    def slow_insert_hand(hand: tuple, hands: list[tuple]) -> None:
        insert_index = 0
        sub_index = 0

        for candidate_index in range(len(hands)):
            candidate = hands[candidate_index]

            if candidate[2] < hand[2]:
                insert_index = candidate_index + 1
            elif candidate[2] == hand[2]:
                candidate_hand = candidate[0]
                source_hand = hand[0]

                for index in range(0, 5):
                    dest_label = label_to_strength(candidate_hand[index])
                    src_label = label_to_strength(source_hand[index])

                    if src_label > dest_label:
                        sub_index += 1
                        break
                    elif src_label < dest_label:
                        break
            else:
                break
        
        hands.insert(insert_index + sub_index, hand)

    def strengthen_hand_with_jokers(hand: str) -> str:
        if "J" not in hand:
            return hand

        card_map = dict()

        for label in hand:
            if label not in card_map:
                card_map[label] = 0
            
            card_map[label] += 1
        
        highest_label = max(card_map, key=lambda x: card_map[x] if x != "J" else 0)

        return hand.replace("J", highest_label)

    def label_to_strength(label: str) -> int:
        if label == "A":
            return 12
        if label == "K":
            return 11
        if label == "Q":
            return 10
        if label == "T":
            return 9
        if label == "9":
            return 8
        if label == "8":
            return 7
        if label == "7":
            return 6
        if label == "6":
            return 5
        if label == "5":
            return 4
        if label == "4":
            return 3
        if label == "3":
            return 2
        if label == "2":
            return 1
        
        return 0

    hands_with_bids = parser(puzzleinput.PUZZLE_INPUT)

    total = 0
    for index, hand_with_bid in enumerate(hands_with_bids):
        total += (index + 1) * hand_with_bid[1]
    
    # 248256639
    print(f"Problem 2 total is {total}")
