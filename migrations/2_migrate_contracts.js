var NameRegistry = artifacts.require("name_registry");

module.exports = function(deployer) {
	deployer.deploy(NameRegistry);
};
