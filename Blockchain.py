import hashlib
import json
from time import gmtime, strftime
import time

class Blockchain(object):
#Creattion of the class blockchain which have an empty-list and a list
#of transaction.
	def __init__(self):
		"""
		Constructor of the class
		"""
		self.chain = [] # initial empty list of the block chain
		# Blocks wich are comparated to put inside the blockchain
		# The idea is to have one transaction per block.
		self.waiting_blocks = [] 
	
	def create_genesis_block(self,amount):
		"""
		Create a new genesis block when the block chain is instantiated.
		"""
		genesis_block = {
			'index': 0,
			'timestamp': strftime("%a, %d %b %Y %H:%M:%S", gmtime()),
			'transactions': amount,
			'proof' : 100,
			'time_proof' : 0,
			'previous_hash': 1
		}
		# Add the hash of the block inside the block
		genesis_block['hash'] = self.hashBlock(genesis_block)
		# The block is added to the wainting list of blocks
	        self.putting_block(block)
		# Add the new genesis block in the blockchain
		#self.chain.append(genesis_block)
		return genesis_block
		
		
	
	def new_block(self, amount, proof, time_proof, previous_hash):
		"""
		Create a new Block in the Blockchain. This block must follow the
		previous-hash of the chain.
		PARAMETERS :
		- previous_hash : Hash of the previous block
		- proof :the proof that chain can be sended by the proof of work algorithm
		RETURN :
		Block : The new Block
		"""
		block = {
			'index': len(self.chain)+1,
			'timestamp': strftime("%a, %d %b %Y %H:%M:%S", gmtime()),
			'transaction': amount,
			'proof' : proof,
			'time_proof' : time_proof,
			'previous_hash': previous_hash,
		}

		# Reset the transaction 
		self.transactions = 0
		# Add the hash of the block inside the block
		block['hash'] = self.hashBlock(block)
		# We must to make sure that the new block is correct
		if self.valid_block(block) :
			# The block is added to the wainting list of blocks
			self.putting_block(block)
		else :
			print("The block " + str(block['index']) + " with an amount of " + str(block['transaction']) + " is not valid")
		return block
	
	def choosing_block(self) :
		"""
		Choice of the block to add in the chain. This choice is made 
		according to the amount of the highest transaction. If two transactions 
		are equivalent, the block is chosen according to the smallest proof.
		RETURN :
		block_choice : The block added to the chain
		"""
		# Saving the biggest amount
		amount_save = 0;
		# Saving the smallest proof
		time_proof_save = 30;
		if len(self.waiting_blocks) >= 1:
			for block in self.waiting_blocks :
				if block['transaction'] > amount_save :
					amount_save = block['transaction']
					time_proof_save = block['time_proof']
					block_choice = block
				elif block['transaction'] == amount_save :
					if block['time_proof'] < time_proof_save :
						time_proof_save = block['time_proof']
						block_choice = block
		self.chain.append(block_choice)
		self.waiting_blocks = []
		return block_choice
	 
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
	
	def proof_of_work(self,last_block):
		"""
		Proof of work algorithm. Find a number p such the hash(p,previous_proof,
		previous_hash) contains leading 4 zeroes.
		PARAMETERS :
		- last_block : The last block of the chain
		Return :
		- proof : The good proof
		"""
		last_proof = last_block['proof']
		last_hash = last_block['hash']
		proof = 0
		while self.valid_proof(last_proof, proof, last_hash) is False:
			proof += 1
		return proof
		
	@staticmethod
	# The static method doesn't need an object instantiation.
	def hashBlock(block):
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
		
	def valid_proof(self, last_proof, proof, last_hash):
		"""
		Validate the proof of the new block with the proof and the hash 
		of the last block.
		PARAMETERS :
		- last_proof : The previous_proof of the previous_block
		- proof : The proof that may be validated
		RETURN : 
		- Boolean Expression
		"""
		guess = f'{last_proof}{proof}{last_hash}'.encode()
		guess_hash = hashlib.sha256(guess).hexdigest()
		return guess_hash[:4] == "0000"
	
	@property
	# The property is used to replace getter and setter in our class
	def last_block(self):
		"""
		Return the last block of the chain. If the index of the dictionnary 
		is -1, the block is the end of the blockchain.
		"""
		return self.chain[-1]
	
	def putting_block(self,block):
		"""
		Put a block inside the waiting list of blocks. 
		PARAMETER :
		- block : the added block
		"""
		self.waiting_blocks.append(block)

### --------------------- TEST --------------------- ###
##new_block_chain = Blockchain()
##new_block_chain.create_genesis_block(0)
##
##lastBlock = new_block_chain.last_block
##amount = 18
##t0 = time.clock()
##new_proof = new_block_chain.proof_of_work(lastBlock)
##t1 = time.clock()
##block1 = new_block_chain.new_block(amount, new_proof, t1-t0, lastBlock['hash'])
##print(block1)
##lastBlock = new_block_chain.last_block
##amount = 24
##t0 = time.clock()
##new_proof = new_block_chain.proof_of_work(lastBlock)
##t1 = time.clock()
##block2 = new_block_chain.new_block(amount, new_proof, t1-t0, lastBlock['hash'])
##print(block2)
##lastBlock = new_block_chain.last_block
##amount = 24
##t0 = time.clock()
##new_proof = new_block_chain.proof_of_work(lastBlock)
##t1 = time.clock()
##block3 = new_block_chain.new_block(amount, new_proof, t1-t0, lastBlock['hash'])
##print(block3)
##new_block_chain.choosing_block()
##
##lastBlock = new_block_chain.last_block
##print(lastBlock)
