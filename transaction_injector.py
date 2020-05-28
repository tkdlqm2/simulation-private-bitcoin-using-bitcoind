import argparse
import os
import time
import sys
from subprocess import check_output, Popen, PIPE
import datetime
import subprocess
from time import sleep
from threading import Thread
import random

def exec_shell_cmd_system(cmd):
    if os.system(cmd) != 0:
        print("error while executing '%s'" % cmd)
        exit(-1)

def wallet_list():
    wallets = [] 
    f = open("/home/csrc/Desktop/python/wallet.txt","r")
    line = f.readlines()
    wallet_str = ""
    for i in line:
        wallet_str = str(i)
        wallets.append(wallet_str[:-1])
    return wallets

def rpc_list():
    rpc = []
    f = open("/home/csrc/Desktop/python/bitcoin_cli.txt","r")
    line = f.readlines()
    rpc_str = ""
    for i in line:
        rpc_str = str(i)
        rpc.append(rpc_str[:-1])
    return rpc
    
def get_target_peer(wallet_addresses):
    result = []
    param2 = len(wallet_addresses) - 1
    second_peer = random.randint(0,param2)
    print(second_peer)
    while(1):
        first_peer = random.randint(0,param2)
        if first_peer == second_peer:
            continue
        else:
            break
    result.append(first_peer)
    result.append(second_peer)
    return result

def make_tx(target1, target2):
    command = target1 + " sendtoaddress " + target2 + " " + "0.01"
    return check_output(command, shell=True)

def possible_peer(bitcoin_cli, wallet_address):
    balance = []
    for i in range(0,len(bitcoin_cli)):
        command = bitcoin_cli[i] + " getbalances"
        balance.append(command)
    try:
        poor_node = balance.index(0)
        print(poor_node)
    except:
        return 10001

def check_possible_bitcoin(command):
    block_count = exec_shell_cmd_system(command)
    if block_count > 100:
        return 1

    
    
if __name__ == "__main__":
    wallet_addresses = wallet_list()
    bitcoin_cli_list = rpc_list()
    possible_tx_peer = []
    possible = possible_peer(bitcoin_cli_list, wallet_addresses)
    # assert block counts 100

    try:
        f = open("/home/csrc/Desktop/python/txList.txt","w")
        while(1):
            target = get_target_peer(wallet_addresses)
            f.write(make_tx(bitcoin_cli_list[target[0]],wallet_addresses[target[1]]))
        f.close()
    except:
        print("\t\t Keyborad Interrupt about stopping bitcoind !! ")
