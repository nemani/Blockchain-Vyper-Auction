var Auction = artifacts.require('auction');
contract('auction', accounts => {
	const owner = accounts[0];
	describe('constructor', () => {
		describe('success case', () => {
			it('should deploy this contract', async () => {
				try {
				const instance = await Auction.new(19,10,1000, { from: owner });
				} catch (err) {
				assert.isUndefined(err.message,'revert with valid arguments');
				}
			});
		});
		describe('Fail case', () => {
			it('should revert on invalid arguments', async () => {
				try {
				const instance = await Auction.new(19,10,1000, { from: accounts[1] });
				assert.isUndefined(instance, 'contract should be created from owner');
				} catch (err) {
				assert.isUndefined(err.message,'revert with valid arguments');
				}
			});
		});
	});
	describe('Notary Register', () => {
		let instance;	
		beforeEach(async () => {
			instance = await Auction.new(19,10,1000, { from: owner });
		});
		describe('Fail case', () => {
			it('notary should register with valid address', async () => {
				try {
				await instance.notaryRegister({ from: accounts[0] });
				} catch (err) {
				assert.isUndefined(err.message,'revert from valid address');
				}
			});
		});
		describe('success case', () => {
			it('successfully register with this address', async () => {
				try {
				await instance.notaryRegister({ from: accounts[1] });
				await instance.notaryRegister({ from: accounts[2] });
				await instance.notaryRegister({ from: accounts[3] });
				await instance.notaryRegister({ from: accounts[4] });
				} catch (err) {
				assert.isUndefined(err.message,'revert from valid address');
				}
			});
		});
		describe('success case', () => {
			it('should return notary num', async () => {
				try {
				await instance.notaryRegister({ from: accounts[1] });
				await instance.notaryRegister({ from: accounts[2] });
				await instance.notaryRegister({ from: accounts[3] });
				await instance.notaryRegister({ from: accounts[4] });
				assert.equal(await instance.notaries_size.call(),4,'num of notaries should be 4');
				} catch (err) {
				assert.isUndefined(err.message,'wrong number of notaries');
				}
			});
		});
	});
	describe('Bidder Register', () => {
		let instance;	
		beforeEach(async () => {
			instance = await Auction.new(19,10,1000, { from: owner });
			await instance.notaryRegister({ from: accounts[1] });
			await instance.notaryRegister({ from: accounts[2] });
			await instance.notaryRegister({ from: accounts[3] });
			await instance.notaryRegister({ from: accounts[4] });
		});
		describe('Fail case', () => {
			it('bidder should register with valid address', async () => {
				try {
				await instance.bidderRegister([[12,8],[12,9]],[5,6],2,{ from: accounts[2] });
				} catch (err) {
				assert.isUndefined(err.message,'revert from valid address');
				}
			});
		});
		describe('success case', () => {
			it('bidder successfully registers with this address', async () => {
				try {
				await instance.bidderRegister([[12,8],[12,9]],[5,6],2,{ from: accounts[5]});
				} catch (err) {
				assert.isUndefined(err.message,'revert from valid address');
				}
			});
		});
	});

});

