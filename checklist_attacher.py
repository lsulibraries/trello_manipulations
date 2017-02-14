#! /usr/bin/env python3

import json
from trello import TrelloClient


def setup_client(keyfile):
    with open(keyfile, 'r', encoding='utf-8') as f:
        keys_text = f.read()
    keys_parsed = json.loads(keys_text)

    my_api_key = keys_parsed["api_key"]
    my_api_secret = keys_parsed["api_secret"]
    my_token = keys_parsed["token"]

    client = TrelloClient(
        api_key=my_api_key,
        api_secret=my_api_secret,
        token=my_token,
    )
    return client


def lookup_board(client, boardname):
    boards_list = [i.id for i in client.list_boards() if boardname == i.name]
    if len(boards_list) == 1:
        board_id = [i.id for i in client.list_boards() if boardname == i.name][0]
        board = client.get_board(board_id)
        return board
    return False


def find_card(board, partial_name):
    matching_cards = [card for card in board.open_cards() if partial_name in card.name]
    if len(matching_cards) == 1:
        return matching_cards[0]
    return False


def add_this_list(title, target_card, tasks):
    shortenedlist = []
    for task in tasks:
        shortenedlist.append(task)
    target_card.add_checklist(title, shortenedlist)


client = setup_client('trello_keys.json')
BacklogBoard = lookup_board(client, 'Product Backlog')
source_card = find_card(BacklogBoard, 'Collection Checking Checklist')
print(source_card)

# its hilarious to have to retry looking up an attribute of an object,
# but it doesn't find the attribute on first look.

source_checklists = None
while not source_checklists:
    source_checklists = source_card.checklists

print(source_checklists)
tasks = None
while not tasks:
    for source_checklist in source_checklists:
        if 'Subjective checks' in source_checklist.name:
            print(source_checklist.name)
            tasks = list([i['name'] for i in source_checklist.items])
print(tasks)
ETLBoard = lookup_board(client, 'Islandora ETL')
ETLcards = ETLBoard.all_cards()
print(ETLcards)

# Are you sure you're ready??
# for card in ETLcards:
#     add_this_list("Subjective checks for Coll Admin", card, tasks)
