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
		Create a new Block in the Blockchain. This block must follow the
		previous-hash of the chain.
		PARAMETERS :
		- previous_hash : Hash of the previous block
		RETURN :
		Block : The new Block
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
	
	def new_transaction(self, amount):
		"""
		There are several transactions inside a block. The user can create 
		a transaction if he put an amount inside the list of transactions.
		PARAMETERS :
		- Amount : The new amount that the list of transaction takes
		RETURN :
		- Index : The index of the Block that will hold this transaction
		"""
		self.transactions.append({'data': amount})
		return self.last_block['index'] + 1
	 
	def valid_block(self, block) :
		"""
		Determine if a given block is valid with the previous-hash and the 
		hash of the last block inside the chain.
		PARAMETERS :
		- Block : the block that we want to make sure it's valid
		RETURN :
		- Boolean Expression
		"""
		if block['previous_hash'] != self.last_block['hash'] :
			return False
		else :
			return True
	
	def update_chain(self, neighbourChain) :
		"""
		Update the block chain if an other chain is longer than the blockchain
		of this node. 
		PARAMETERS :
		- Chain : The chain which is compare with the local chain
		RETURN :
		- Boolean Expression
		"""
		chainLength = len(self.chain)
		neighbourChainLength = len(neighbourChain.chain)
		print(chainLength)
		print(neighbourChainLength)
		if neighbourChainLength > chainLength :
			self.chain = neighbourChain.chain
			print("The chain is updated")
			return True
		else :
			print("The chain is the longer one")
			return False
			
	
		 
	
	@staticmethod
	# The static method doesn't need an object instantiation.
	def hash(block):
		"""
		Creates a SHA-256 hash of a Block.
		PARAMETERS :
		-Block: A block of the blockchain
		RETURN :
		Hash : the hash in 256 bits
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

BlockChain1 = Blockchain()
BlockChain1.new_transaction(24) 
prevBlock = BlockChain1.last_block
BlockChain1.new_block(prevBlock['hash'])
BlockChain1.new_transaction(-67)
prevBlock = BlockChain1.last_block
BlockChain1.new_block(prevBlock['hash'])
BlockChain2 = Blockchain()
BlockChain2.new_transaction(24) 
prevBlock = BlockChain2.last_block
BlockChain2.new_block(prevBlock['hash'])
BlockChain2.new_transaction(-67)
BlockChain2.new_transaction(38)
prevBlock = BlockChain2.last_block
BlockChain2.new_block(prevBlock['hash'])
BlockChain2.new_transaction(98)
prevBlock = BlockChain2.last_block
BlockChain2.new_block(prevBlock['hash'])

BlockChain1.update_chain(BlockChain2)
BlockChain2.update_chain(BlockChain1)

