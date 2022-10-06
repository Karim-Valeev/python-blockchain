from models import KeyPair, BlockChain

if __name__ == '__main__':
    key_pair = KeyPair()
    print(key_pair)

    transactions = [
        "1. User 1 send 1 Karimcoin to User 2",
        "2. User 2 send 1 Karimcoin to User 1",
        "3. User 1 send 1 Karimcoin to User 2",
        "4. User 2 send 1 Karimcoin to User 1",
        "5. User 1 send 1 Karimcoin to User 2",
        "6. User 2 send 1 Karimcoin to User 1",
        "7. User 1 send 1 Karimcoin to User 2",
        "8. User 2 send 1 Karimcoin to User 1",
        "9. User 1 send 1 Karimcoin to User 2",
        "10. User 2 send 1 Karimcoin to User 1",
    ]

    block_chain = BlockChain("Karimcoin", 10, key_pair, transactions)
    block_chain.initiate_block_chain()

    print(f'Blockchain verified: {block_chain.is_verified()}')

    block_chain.write_to_file("../data/Karimcoin.blockchain")

    block_chain.damage_block(3)

    print(f'Blockchain verified: {block_chain.is_verified()}')

