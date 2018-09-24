#events 
Payment: event({amount: uint256(wei), arg2: indexed(address)})
AuctionStarted : event({q: uint256, m: uint256})
NotaryRegister : event({_from:address})
BidderRegister : event({_from:address})

myevent : event({x: uint256, y: uint256})
myevent2 : event({x: int128})
#address of auctioner
auctioner: address

#large prime
q: public(uint256)

#number of items
M: public(uint256)

#number of notaries registered
notaries_size: public(int128)

#number of bidders registered
bidders_size: public(int128)

#Allocating this notary to bidder
notary_num: int128

# Pay for each time notary is used
constantPay: wei_value 

# Bidders struct Array
bidders: {
        bidder: address,
        notary: address,
        notaryIndex: int128,
        Payment : wei_value,
        Payed : wei_value,
    }[int128]

# bidder map 
bidder_map: bool[address]

# Notaries struct Array
notaries : {
        timesused: uint256,
        notary: address,
        bidder: address,
        bidderIndex: int128,
        num_items : uint256,
        bid_input : uint256[100][2],
        bid_value : uint256[2],
        w: int128
    }[int128]

# notary map 
notary_map: bool[address]

winners: int128[100]

@public
def __init__(_q: uint256, _M: uint256):
    self.auctioner = msg.sender
    self.q = _q
    self.M = _M

    self.notaries_size = 0
    self.bidders_size = 0
    self.notary_num = 0
    self.constantPay = 10
    
    log.AuctionStarted(_q, _M)


@public
def sqrt(x: uint256, xx: uint256) -> decimal :
    _val : decimal = convert(xx, 'decimal')
    z : decimal  = (_val + 1.0) / 2.0
    y : decimal  = _val
    for i in range(100):
        if z >= y:
            break
        y = z
        z = (_val / z + z) / 2.0
    
    return y * convert(x, 'decimal')

#First notaries register and their public address stored in map
@public
def notaryRegister():
    assert not self.notary_map[msg.sender] and not msg.sender == self.auctioner
    self.notaries[self.notaries_size].notary = msg.sender
    self.notary_map[msg.sender] = True
    self.notaries_size = self.notaries_size + 1
    log.NotaryRegister(msg.sender)  


#Next bidders register and assigned a notary based on notary_num value (Not random)
@public
@payable
def bidderRegister(_bid_input:uint256[100][2], _bid_value:uint256[2], _num_items:uint256):
    assert self.notary_num < self.notaries_size
    assert not self.auctioner == msg.sender
    assert not self.bidder_map[msg.sender] and not self.notary_map[msg.sender]
    assert _num_items > 0
    assert _num_items <= self.M

    self.bidders[self.bidders_size].bidder = msg.sender

    #Assign notary
    self.notaries[self.notary_num].bidder = msg.sender
    self.bidders[self.notary_num].notary = self.notaries[self.notary_num].notary
    self.bidders[self.notary_num].notaryIndex = self.notary_num
    self.bidder_map[msg.sender]=True

    #send items and value to notary
    self.notaries[self.notary_num].num_items = _num_items
    self.notaries[self.notary_num].bidderIndex = self.notary_num
    self.notaries[self.notary_num].bid_input = _bid_input
    self.notaries[self.notary_num].bid_value = _bid_value
    
    U : uint256 = _bid_value[0]
    V : uint256 = _bid_value[1]
    wi : uint256 = (U + V) % self.q

    assert msg.value > as_wei_value(self.sqrt(wi, _num_items), 'wei')

    self.notaries[self.notary_num].w = convert(wi, 'int128')
    self.bidders[self.notary_num].Payed = msg.value
    log.myevent2(self.notaries[self.notary_num].w)
    log.BidderRegister(msg.sender)
    
    self.notary_num = self.notary_num + 1
    self.bidders_size = self.bidders_size + 1


@public    
def checkEqual(j : int128, i : int128,k : int128, l : int128) -> bool:
    Au : uint256 = self.notaries[j].bid_input[k][0]
    Av : uint256 = self.notaries[j].bid_input[k][1]

    Bu : uint256 = self.notaries[i].bid_input[l][0]
    Bv : uint256 = self.notaries[i].bid_input[l][1]

    val1 : uint256 = (Au - Bu)
    val2 : uint256 = (Av - Bv)
    
    if val1 + val2 == 0:
        return True
    return False


@public    
def checkGreater(j : int128, i : int128) -> bool:
    # Q : int128 = convert(self.q, 'int128')
    # Au : int128 = convert(self.notaries[j].bid_value[0], 'int128')
    # Av : int128 = convert(self.notaries[j].bid_value[1], 'int128')

    # Bu : int128 = convert(self.notaries[i].bid_value[0], 'int128')
    # Bv : int128 = convert(self.notaries[i].bid_value[1], 'int128')

    # val1 : int128 = (Au - Bu) % Q
    # val2 : int128 = (Av - Bv) % Q

    # if (val1 + val2) < (Q/2):
    #     return False
    # else:
    #     return True

    if self.notaries[j].w <= self.notaries[i].w:
        return False
    else:
        return True


@private
def sortNotaries():
    temp: {
        timesused: uint256,
        notary: address,
        bidder: address,
        bidderIndex: int128,
        num_items : uint256,
        bid_input : uint256[100][2],
        bid_value : uint256[2],
        w: int128
    }
    for index in range(1,100):

        if index >= self.bidders_size:
            break
        
        currentvalue : int128 = index
        position : int128 = index
        temp = self.notaries[currentvalue]
        for lol in range(100):
            if position > 0:
                if not self.checkGreater(position - 1, currentvalue):
                    self.notaries[position] = self.notaries[position - 1]
                    position = position - 1
            else:
                break
        self.notaries[position] = temp

@private
def getWinners() -> int128:
    self.winners[0] = 0
    winner_num : int128 = 1

    for i in range(100):
        flag : bool = False
        
        if i >= self.bidders_size:
            break
        
        for j in range(100):
            if flag or j >= winner_num:
                break

            for k in range(100):
                if flag or k >= convert(self.notaries[self.winners[j]].num_items,'int128'):
                    break
                for l in range(100):
                    if l >= convert(self.notaries[i].num_items,'int128'):
                        break
                    # Compare bidder[winners[j]][k] and bidders[i][l]
                    if self.checkEqual(i, self.winners[j], l, k):
                        flag = True
                        break
        
        if flag:
            self.winners[winner_num] = i
            winner_num = winner_num + 1

    return winner_num

@public
def winnerDetermine():
    assert msg.sender == self.auctioner, "Only Auctioner can call this function" 
    # Step 1 Sort the array of Notaries
    self.sortNotaries()

    # # Step 2 Find the winners  
    winners_num: int128 = self.getWinners()

    log.myevent2(winners_num)
    # # Step 3 Calculate Payments for each Bidder
    # for i in range(100):
    #     didwefindaj : bool = False
    #     ourJ : int128 = 0
    #     if i >= winner_num:
    #         break

    #     for j in range(self.winners[i], self.winners[i] + 100):
    #         ijnointersect : bool = True
    #         isthisthej : bool = True
    #         if j >= self.bidders_size:
    #             break

    #         for k in range(0, 100):
    #             if not isthisthej or k >= j:
    #                 break

    #             if k == i:
    #                 if not ijnointersect:
    #                     continue

    #                 for a in range(100):
    #                     if not isthisthej or a >= convert(self.notaries[j].num_items,'int128'):
    #                         break

    #                     for b in range(100):
    #                         if b >= convert(self.notaries[k].num_items,'int128'):
    #                             break

    #                         #  Compare bidder[winners[j]][k] and bidders[i][l]
    #                         if (self.checkEqual(j, i, a, b)):
    #                             ijnointersect = False
    #                             break
    #             else:
    #                 for a in range(100):
    #                     if not isthisthej or a >= convert(self.notaries[j].num_items,'int128'):
    #                         break

    #                     for b in range(100):
    #                         if b >= convert(self.notaries[k].num_items,'int128'):
    #                             break

    #                         #  Compare bidder[j][k] and bidders[i][l]
    #                         if (self.checkEqual(j, k, a, b)):
    #                             isthisthej = False
    #                             break
                
    #         if isthisthej and ijnointersect:
    #             didwefindaj = True
    #             ourJ = j
    #             break

    #     xi : int128 = self.winners[i]
    #     if didwefindaj:
    #         U : uint256 = self.notaries[self.bidders[ourJ].notaryIndex].bid_value[0]
    #         V : uint256 = self.notaries[self.bidders[ourJ].notaryIndex].bid_value[1]
    #         wj : uint256 = (U + V) % self.q
    #         self.bidders[xi].Payment = as_wei_value(self.sqrt(wj, self.notaries[xi].num_items), 'wei')
    #     else:
    #         self.bidders[xi].Payment = 0


    # # Send Money to each Bidder (Money Payed - Payment)
    # for i in range(100):
    #     if i > self.bidders_size:
    #         break
    #     send_addr : address = self.bidders[i].bidder
    #     diff : wei_value = self.bidders[i].Payed - self.bidders[i].Payment
    #     if diff > 0:
    #         send(send_addr, diff)
    
    # # Send Money to each Notary (constantPay * timesused)
    # for i in range(100):
    #     if i > self.notaries_size:
    #         break
    #     send_addr : address = self.notaries[i].notary
    #     val : wei_value = self.constantPay * self.notaries[i].timesused
    #     if val > 0:
    #         send(send_addr, val)
