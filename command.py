import argparse
import os
import time
import sys
from subprocess import check_output, Popen, PIPE
import datetime
import subprocess
from time import sleep
from threading import Thread

def exec_shell_cmd_system(cmd):
    if os.system(cmd) != 0:
        print("error while executing '%s'" % cmd)
        exit(-1)

def exec_shell_cmd_system2(i,wallet):
    rpcport = str(1000+i) + "0"
    datadir = "node100" + str(i)
    rpcuser = str(1000+i)
    rpcpassword = rpcuser

    comment = "python mining.py bitcoin-cli -testnet -rpcport=" + rpcport + " " + "-datadir=" + datadir + " " +  "-rpcuser=" + rpcuser + " " + "-rpcpassword=" + rpcpassword + " " + "generatetoaddress" + " 1 " + wallet 
    print(comment)
    if os.system(comment) != 0:
        print("error while executing '%s'" % comment)
        exit(-1)


if __name__ == '__main__':

    mode = sys.argv[1]

    if mode == 'run':
        
        list_bitcoind = []
        list_bitcoin_cli = []
        wallet_address = []
        peer_port = []
        block_address = []

        node_index = 0
        strpower = '"'
        node_counts = int(sys.argv[2])
        ip_address = sys.argv[3]

        for i in range(0,node_counts):
            make_node_cli = "mkdir node%d" %(i + 1000)
            exec_shell_cmd_system(make_node_cli)
            index = 1000 + i
            node_index = index 
            rpcuser = str(index)
            port = index + 111
            peer_port.append(str(port))
            rpcport = int(rpcuser + "0")

            array = "bitcoind -testnet -port=%d -noconnect -datadir=node%d -listen=1 -rpcport=%d -rpcuser=%s -rpcpassword=%d -fallbackfee=0.0002 --daemon" %(port,index,rpcport,rpcuser,index)
            list_bitcoind.append(array)
            print("-----------------------------------------------------------------------------------------------")
            print(array)
            connection_peer="bitcoin-cli -testnet -rpcport=%s -datadir=node%d -rpcuser=%s -rpcpassword=%d" %(rpcport,index,rpcuser,index)
            print(connection_peer)
            list_bitcoin_cli.append(connection_peer)
        
        f = open("/home/csrc/Desktop/python/bitcoin_cli.txt","w")
        for i in range(0,len(list_bitcoin_cli)):
            target = list_bitcoin_cli[i] + "\n"
            f.write(target)
        f.close()

        for i in list_bitcoind:
            exec_shell_cmd_system(i)

        sleep(3)
        for i in range(0,node_counts):
            string_number = str(i)
            if i == node_counts-1:
                connection_command = list_bitcoin_cli[0] + " " +  "addnode " + strpower + ip_address + ":" + peer_port[0] + strpower + " " + strpower + "onetry" + strpower
                exec_shell_cmd_system(connection_command)
                break
            connection_command = list_bitcoin_cli[i] + " " + "addnode " + strpower + ip_address + ":" + peer_port[i+1] + strpower + " " + strpower + "onetry" + strpower
            print(connection_command)
            exec_shell_cmd_system(connection_command)

        f = open("/home/csrc/Desktop/python/wallet.txt","w")
        for i in range(0,node_counts):
            wallet_address.append(check_output(list_bitcoin_cli[i] + " " + 'getnewaddress', shell=True).split('\n')[0])
            f.write(wallet_address[i] + "\n")
        f.close()

        for i in range(0,node_counts):        
            param = list_bitcoin_cli[i] + " " + 'generatetoaddress 1 ' + wallet_address[i]
            exec_shell_cmd_system(param)

        bitcoin_cli_command = "python bitcoin_cli.py"    
        exec_shell_cmd_system(bitcoin_cli_command)


    elif mode =='clean':
        exec_shell_cmd_system("rm -rf node*")
        exec_shell_cmd_system("rm -rf bitcoin_cli.txt")
        exec_shell_cmd_system("rm -rf wallet.txt")
        exec_shell_cmd_system("rm -rf txList.txt")

        pslines = []
        username = check_output('whoami', shell=True).split('\n')[0]
        pslines=check_output('ps -fu %s' % username, shell=True).split('\n')

        for line in pslines:
            if 'bitcoind' in line:              
                for l in line.split(" "):
                    if not username in l:
                        if(len(l)>1):
                            print"kill -9", l
                            check_output('kill -9 %s'%l, shell=True)
                            break