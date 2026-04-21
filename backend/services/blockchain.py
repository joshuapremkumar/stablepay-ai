def send_to_blockchain(sender, receiver, amount):
    return {
        "status": "success",
        "tx_hash": f"0x{hash((sender, receiver, amount))}"
    }