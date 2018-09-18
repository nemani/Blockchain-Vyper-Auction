#address of auctioner
auctioner: public(address)
#auction timestamps
auction_start: public(timestamp)
auction_end: public(timestamp)
#large prime
q: public(uint256)
#number of items
M: public(uint256)
#number of notaries registered
notaries_size: public(uint256)
#number of bidders registered
bidders_size : public(uint256)
#Allocating this notary to bidder
notary_num: public(uint256)

bidders: public({
        notary: address,
        bid_input : uint256[100][1],
        bid_value : uint256[1][1],
    }[address])

bidder_map : address[uint256]

notaries : public({
        bidder:address,
        isAssigned : bool,
        bid_input : uint256[100][1],
        bid_value : uint256[1][1],
    }[address])

notary_map : address[uint256]


@public
def __init__(_q: uint256,_M: uint256, _bidding_time: timedelta):
    self.auctioner = msg.sender
    self.q = _q
    self.M = _M
    self.notaries_size = 0
    self.bidders_size = 0
    self.notary_num = 0
    self.auction_start = block.timestamp
    self.auction_end = self.auction_start + _bidding_time

#First notaries register and their public address stored in map
@public
def notaryRegister():
    self.notary_map[self.notaries_size] = msg.sender
    self.notaries_size = self.notaries_size + 1         

#Next bidders register and assigned a notary based on notary_num value (Not random)
@public
def bidderRegister():
    assert self.notary_num < self.notaries_size
    assert not self.notaries[self.notary_map[self.notary_num]].isAssigned
    self.bidder_map[self.bidders_size] = msg.sender
    self.bidders_size = self.bidders_size + 1
    self.notaries[self.notary_map[self.notary_num]].isAssigned = True
    self.notaries[self.notary_map[self.notary_num]].bidder = msg.sender
    self.bidders[msg.sender].notary = self.notary_map[self.notary_num]
    self.notary_num = self.notary_num + 1 


#Bidder will input tuples which will be items and value of bid as tuple
#This input will be immediately passed to assigned notary

@public
@payable
def bid(_bid_input:uint256[100][1],_bid_value:uint256[1][1]):
    
    self.bidders[msg.sender].bid_input = _bid_input
    self.bidders[msg.sender].bid_value = _bid_value
    self.notaries[self.bidders[msg.sender].notary].bid_input = _bid_input
    self.notaries[self.bidders[msg.sender].notary].bid_value = _bid_value



