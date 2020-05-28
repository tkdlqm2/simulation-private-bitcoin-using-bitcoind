from __future__ import print_function
import argparse
import os
import time
import sys
from subprocess import check_output, Popen, PIPE
import datetime
import subprocess
from time import sleep

def exec_shell_cmd_system(cmd):
    if os.system(cmd) != 0:
        print("error while executing '%s'" % cmd)
        exit(-1)

def clean_bitcoind():
    command = "python command.py clean " + str(len(cli_list))
    print(command)
    exec_shell_cmd_system(command)

def tx_list():
    try:
        f = open("/home/csrc/Desktop/python/txList.txt","r")
        line = f.readlines()
        txlist = []
        for i in range(0,len(line)):
            string = str(line[i])[:-1]
            txlist.append(string)
        return txlist
    except:
        print("\t\t tx_list error ")
        pass


            
def rpc_command_func(n):
    if n == 1:
        return_value = "getblockchaininfo"
        return return_value
    elif n == 2:
        return_value = "getwalletinfo"
        return return_value
    elif n == 3:
        txlist = tx_list()
        for i in range(0,len(txlist)):
            print("\t", i , " : " , txlist[i])
        print("------------------------------------------------------------------------")
        print("choose number about tracking tx-->  ", end=" ")
        tracking_number = int(input())
        command = "gettransaction " + txlist[tracking_number]
        return command

    else:
        pass

def rpc_command_list():
    print("---------------------------------------------------------------------------------------")
    print("\t\t Input option number to command rpc")
    print("\t\t If you want to clean bitcoind, press 0")
    print()
    print("\t\t 1. getblockchaininfo")
    print("\t\t 2. getwalletinfo")
    print("\t\t 3. Show Transaction hash List & gettransaction")
    print()
    print("\t\t 9. Other peer")
    print("\t\t 0. Exit")
    print("---------------------------------------------------------------------------------------")
    print("\t-->", end=" ")

if __name__ == '__main__':
    
    EXIT_VALUE = 0
    cli_list = []
    command_flag = '"'
    f = open("/home/csrc/Desktop/python/bitcoin_cli.txt","r")
    line = f.readlines()
    for i in range(0,len(line)):
        cli_list.append(line[i])
    f.close()

    while(1):
        print("---------------------------------------------------------------------------------------")
        print("\t\t Input peer port number to use bitcoin-cli")
        print("\t\t If you want to clean bitcoind, press 0")
        print("---------------------------------------------------------------------------------------")
        print("\t-->", end=" ")
        try:
            peer_port = int(input())
        except:
            print("\t\t\t Only input integer")
            continue

        if peer_port == 0:
            clean_bitcoind()
            break

        cli_command = cli_list[peer_port - 1111]
        cli_command = cli_command[:-1]

        while(1):
            rpc_command_list()
            try:
                rpc_command = int(input())
            except:
                print("\t\t Only input integer")
                continue

            if rpc_command == 9:
                break
            elif rpc_command == 0:
                clean_bitcoind()
                EXIT_VALUE = 1
                break
            return_value = rpc_command_func(rpc_command)
            result = cli_command + " " + return_value
            exec_shell_cmd_system(result)

        if EXIT_VALUE == 1:
            break