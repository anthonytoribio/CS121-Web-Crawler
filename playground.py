import shelve

with shelve.open("frontier.shelve") as db:
    print(db)