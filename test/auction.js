var Auction = artifacts.require('auction');
chai = require('chai');
expect = chai.expect;
contract('Testing Auction contract', function (accounts) {
	describe("Deploy Auction contract",function(){
			it('catch the instance of contract',function(){
			return Auction.new(19,10,1000).then(function(instance){
					auctioninstance = instance;	
				});
			});
		});
	describe('check contract functions',function(){
		
			it('notary-1 registers',function(){
			return auctioninstance.notaryRegister({from:accounts[1]}).then(function(res){
					expect(res).to.not.be.an("error");
					});
			});
			it('notary-2 registers',function(){
			return auctioninstance.notaryRegister({from:accounts[2]}).then(function(res){
					expect(res).to.not.be.an("error");
					});
			});
			it('notary-3 registers',function(){
			return auctioninstance.notaryRegister({from:accounts[3]}).then(function(res){
					expect(res).to.not.be.an("error");
					});
			});
			it('notary-4 registers',function(){
			return auctioninstance.notaryRegister({from:accounts[4]}).then(function(res){
					expect(res).to.not.be.an("error");
					});
			});

		});

	});
