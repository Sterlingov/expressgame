import time

from web3 import Web3

PROVIDER_ENDPOINT_URI = 'https://bsc-dataseed1.binance.org:443'


class Express:
    def __init__(self, sender: str, transaction: dict, delay: float):
        self.sender = sender
        self.transaction = transaction
        self.delay = delay
        self.w3 = Web3(Web3.HTTPProvider(PROVIDER_ENDPOINT_URI))
        self.nonce = self.w3.eth.get_transaction_count(sender)

    def spam(self, private_key: str):
        while True:
            self.send(private_key)
            time.sleep(self.delay)

    def send(self, private_key: str):
        try:
            nonce = self._get_inc_nonce()
            print(f'nonce: {nonce}')
            transaction = self.transaction.copy()
            transaction['nonce'] = nonce
            signed = self.w3.eth.account.sign_transaction(transaction, private_key)
            result = self.w3.eth.send_raw_transaction(signed.rawTransaction)
            print(f'ATTEMPT {nonce}, TX is {result.hex()}')
        except Exception as e:
            print(f'Exception {e}')

    def _get_inc_nonce(self) -> int:
        nonce = self.nonce
        self.nonce += 1
        return nonce


def main():
    sender = '0xa<адрес>'
    transaction = {
        # 'from': sender,
        'to': '0x11c2B6B0e111681B760873b91aBE8DD9c6F3901F',
        'data': '876cb2170000000000000000000000000000000000000000000000000000000000000003',
        'gas': 2_000_000,
        'gasPrice': 5 * 1_000_000_000,
        'value': Web3.toWei(0.145, 'ether'),
    }
    express = Express(sender, transaction, delay=0.1)
    express.send('<ключ>')


if __name__ == '__main__':
    main()
