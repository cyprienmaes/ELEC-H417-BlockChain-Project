# -*- coding: utf-8 -*-
"""
Created on Fri Dec  7 16:17:32 2018

@author: Leonardo
"""

import Blockchain
import timer
import transaction_creator

sender = "Billy"
tran_op = 0           
"""a block is being created"""                   
blockchain = Blockchain.Blockchain()


timer = timer.timer()
timer.setTime(0)
timer.start()

"""

transactioner = transaction_creator.transaction_creator()

transaction_start = 0

while True:
    if (transaction_start == 0):
            transactioner.start()
            transaction_start = 1
    if (timer.getTime() > 30):       
        transactioner.BlockCreation()
    """"""     code création de bloc   """"""
        transactioner.clearTransactions()
        timer.setTime(0)
    
          """    
           
while True:
    while (tran_op==0):
        print("Do you want to make a transaction?")
        transac_status = input("")
        if transac_status =="yes":
            print("How much money do you want to transfer?")
            amount = input("")
            if amount.isdigit():                
                if amount == 0:
                    tran_op = 1;
                    print("Transaction Impossible - Amount Null")
                elif True:                                        """insert proof of work here"""
                    blockchain.new_transaction(amount)
                    if (blockchain.chain == []):                  """ïf blockchain is empty, create genesis block"""
                        blockchain.create_genesis_block()
                    else
                        blockchain.new_block(blockchain.last_block['hash'])
                    print("Transaction Validated")   
                    timer.setTime(0)
                    while (timer.getTime() < 30):
                        if False:                                 """insert block incoming condition here"""
                            blockchain.chain[-1] = []             """"deletes created block if it recieves another block"""
                    """append block"""
                else :
                    print("Transaction Impossible - Invalid User")
            else:
                tran_op = 1;
                print("Transaction Impossible - Wrong Input")
        elif transac_status =="no":
            print("Ending Transaction")
            tran_op = 1
        else:
            print("Transaction Impossible - Wrong Input")
            tran_op = 1
    tran_op = 0            
