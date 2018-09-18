var Auction = artifacts.require('name_registry');
contract('Testing Auction contract', function (accounts) {
	describe("Deploy Auction contract",function(){
			it('catch the instance of contract',function(){
			return Auction.new(19,10,1000).then(function(instance){
					auctioninstance = instance;	
				});
			});
		});

	});
