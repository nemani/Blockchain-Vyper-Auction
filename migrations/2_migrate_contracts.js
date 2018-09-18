var NameRegistry = artifacts.require("name_registry");

module.exports = function(deployer) {
	deployer.deploy(NameRegistry,19,10,1000);
};
