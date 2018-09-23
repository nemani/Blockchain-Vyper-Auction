#events 
Payment: event({amount: uint256(wei), arg2: indexed(address)})
NotaryRegister : event({_from:address})
BidderRegister : event({_from:address})
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
notaries_size: public(int128)
#number of bidders registered
bidders_size : public(int128)
#Allocating this notary to bidder
notary_num: public(int128)

bidders: public({
        bidder: address,
        notary: address,
        num_items : uint256,
        isValid : bool
    }[int128])


notaries : public({
        notary : address,
        bidder:address,
        bid_input : uint256[100][2],
        bid_value : uint256[2],
        isValid : bool
    }[int128])


winners : int128[100]

@public
def __init__(_q: uint256, _M: uint256, _bidding_time: timedelta):
    assert _M > 0 and _q > 0

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
    assert not self.notaries[self.notaries_size].isValid and not msg.sender == self.auctioner
    self.notaries[self.notaries_size].notary = msg.sender
    self.notaries[self.notaries_size].isValid = True
    self.notaries_size = self.notaries_size + 1
    log.NotaryRegister(msg.sender)  


#Next bidders register and assigned a notary based on notary_num value (Not random)
@public
@payable
def bidderRegister(_bid_input:uint256[100][2], _bid_value:uint256[2], _num_items:uint256):
    assert self.notary_num < self.notaries_size
    assert not self.auctioner == msg.sender
    assert not self.bidders[self.notary_num].isValid and not self.notaries[self.notary_num].isValid
    assert _num_items > 0 and _num_items <= self.M

    self.bidders[self.bidders_size].bidder = msg.sender
    self.bidders_size = self.bidders_size + 1

    #Assign notary
    self.notaries[self.notary_num].bidder = msg.sender
    self.bidders[self.notary_num].notary = self.notaries[self.notary_num].notary
    self.bidders[self.notary_num].isValid = True

    #send items and value to notary
    self.bidders[self.notary_num].num_items = _num_items
    self.notaries[self.notary_num].bid_input = _bid_input
    self.notaries[self.notary_num].bid_value = _bid_value
    self.notary_num = self.notary_num + 1
    
    log.BidderRegister(msg.sender)  


@public
def compareIndex(j : int128, k : int128) -> bool:
    Au : uint256 = self.notaries[j].bid_value[0]
    Av : uint256 = self.notaries[j].bid_value[1]
    Bu : uint256 = self.notaries[k].bid_value[0]
    Bv : uint256 = self.notaries[k].bid_value[1]

    val1 : uint256 = (Au - Bu) 
    val2 : uint256 = (Av - Bv)
    
    if val1 + val2 < self.q / 2:
        return True

    return False

@public
def swapBidders(j : int128, k : int128) -> bool:
    temp : uint256[2]  = self.notaries[j].bid_value
    self.notaries[j].bid_value = self.notaries[j + 1].bid_value
    self.notaries[j + 1].bid_value = temp
    return True

@public    
def checkNotEqual(j : int128, i : int128,k : int128, l : int128) ->bool:
    Au : uint256 = self.notaries[j].bid_input[k][0]
    Av : uint256 = self.notaries[j].bid_input[k][1]
    Bu : uint256 = self.notaries[i].bid_input[l][0]
    Bv : uint256 = self.notaries[i].bid_input[l][1]

    val1 : uint256 = (Au - Bu)
    val2 : uint256 = (Av - Bv)
    
    if val1 + val2 == 0:
        return False
    return True

@public
def winnerDetermine():
    assert self.auctioner == msg.sender
    #step 1
    for i in range(100):
        if i >= self.bidders_size:
            return
        for j in range(100):
            if j >= self.bidders_size - i - 1:
                break

            if self.compareIndex(j, j + 1):
                self.swapBidders(j, j + 1)
    
    #step 2
    index : int128 = 0
    for i in range(100):
        if i == 0:
            self.winners[index] = i
            index = index + 1
            continue

        for j in range(100):
            if j >= i:
                break

            for k in range(100):
                if k >= convert(self.bidders[j].num_items,'int128'):
                    break

                for l in range(100):
                    if l >= convert(self.bidders[i].num_items,'int128'):
                        break

                    if(self.checkNotEqual(j,i,k,l)):
                        self.winners[index] = i
                        index = index + 1


