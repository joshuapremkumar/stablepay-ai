wallets = {
    "user1": 1000,
    "merchant1": 500
}

def transfer(sender, receiver, amount):
    if wallets.get(sender, 0) < amount:
        return False

    wallets[sender] -= amount
    wallets[receiver] = wallets.get(receiver, 0) + amount
    return True