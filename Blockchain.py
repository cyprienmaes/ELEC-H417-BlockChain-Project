import hashlib
import json
from time import gmtime, strftime

class Blockchain(object):
#Creattion of the class blockchain which have an empty-list and a list
#of transaction.
	def __init__(self):
		"""
		Constructor of the class
		"""
		self.chain = [] # initial empty list of the block chain
		self.transactions = [] # initial empty list of the transactions
		# Creation of the genesis block when the class blockchain is instantiated
		self.create_genesis_block()
	
	def create_genesis_block(self):
		"""
		Create a new genesis block when the block chain is instantiated.
		"""
		genesis_block = {
			'index': 0,
			'timestamp': strftime("%a, %d %b %Y %H:%M:%S", gmtime()),
			'transactions': self.transactions,
			'previous_hash': 1
		}
		# Reset the current list of transactions
		self.transactions = []
		# Add the hash of the block inside the block
		genesis_block['hash'] = self.hash(genesis_block)
		# Add the new genesis block in the blockchain
		self.chain.append(genesis_block)
		return genesis_block
		
		
	def new_block(self, previous_hash):
		"""
		Create a new Block in the Blockchain which takes in parameter
		PREVIOUS_HASH : Hash of the previous Block
		And return
		BLOCK : The new Block
		"""

		block = {
			'index': len(self.chain),
			'timestamp': strftime("%a, %d %b %Y %H:%M:%S", gmtime()),
			'transaction': self.transactions,
			'previous_hash': previous_hash
		}

		# Reset the current list of transactions
		self.transactions = []
		# Add the hash of the block inside the block
		block['hash'] = self.hash(block)
		# We must to make sure that the new block is correct
		if self.valid_block(block) :
			# Add the new block in the blockchain
			self.chain.append(block)
		else :
			print("The block " + str(block['index']) + " with an amount of " + str(block['transaction']) + "is not valid")
		return block
	
	def new_transaction(self,amount):
		"""
		New transaction to go inside a new block which takes in parameter
		- AMOUNT : The new amount that the block provide
		And return :
		- INDEX : The index of the Block that will hold this transaction
		"""
		self.transactions.append({'data': amount})
		return self.last_block['index'] + 1
	 
	def valid_block(self, block) :
		"""
		Determine if a given block is valid. This function takes in parameter :
		- BLOCK : the block that we want to make sure it's valid
		And return boolean expression
		"""
		if block['previous_hash'] != self.last_block['hash'] :
			return False
		else :
			return True
	
		 
	
	@staticmethod
	# The static method doesn't need an object instantiation.
	def hash(block):
		"""
		Creates a SHA-256 hash of a Block which takes in parameter
		Block: A block of the blockchain
		And return
		HASH : the hash in 256 bits
		"""
		# We must make sure that the Dictionary is Ordered, or we'll have inconsistent hashes
		block_string = json.dumps(block, sort_keys=True).encode()
		# Return in hexadecimal to see the hash with more facilities
		return hashlib.sha256(block_string).hexdigest()
	
	@property
	# The property is used to replace getter and setter in our class
	def last_block(self):
		"""
		Return the last block of the chain. If the index of the dictionnary 
		is -1, the block is the end of the blockchain.
		"""
		return self.chain[-1]

#newBlockChain = Blockchain()
#newBlockChain.new_transaction(24) 
#newBlockChain.new_transaction(67) 
#prevBlock = newBlockChain.last_block
#newBlockChain.new_block(prevBlock['hash'])
