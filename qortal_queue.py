import os
import sys
import time

import requests


def get_status(node_ip):
    sync_status = True
    mining_status = False
    try:
        res = requests.get(f'http://{node_ip}:12391/admin/status')
        res = res.json()
        sync_status = res['isSynchronizing']
        mining_status = res['isMintingPossible']
    except:
        pass
    return sync_status, mining_status


def get_minting_account(node_ip):
    res = requests.get(f'http://{node_ip}:12391/admin/mintingaccounts')
    return res.json()


def post_minting_account(private_key, node_ip):
    headers = {'X-API-KEY': 'N1NZxjTmSAibKjp4t3Hoi4'}
    res = requests.post(f'http://{node_ip}:12391/admin/mintingaccounts', data=private_key, headers=headers)
    if res == 'true':
        return True
    return False


def main(private_keys, node_ip):
    while True:
        time.sleep(3)
        sync_status, mining_status = get_status(node_ip)
        print('sync_status:', sync_status)
        print('mining_status:', mining_status)
        # 如果还在同步，则等待
        if sync_status is False:
            for key in private_keys:
                # 挖矿列表
                minting_account = []
                items = get_minting_account(node_ip)
                for item in items:
                    minting_account.append(item['mintingAccount'])
                split_key = key.split(':')
                address = split_key[0]
                minting_key = split_key[1]
                if address not in minting_account:
                    result = post_minting_account(minting_key, node_ip)
                    if result:
                        print('添加挖矿成功：', key)
                else:
                    print('挖矿已存在：', key)


if __name__ == '__main__':
    ip = '127.0.0.1'
    if len(sys.argv) == 2:
        key1 = sys.argv[1]
        main([key1], ip)
    else:
        key1 = sys.argv[1]
        key2 = sys.argv[2]
        main([key1, key2], ip)
