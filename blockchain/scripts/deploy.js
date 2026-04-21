const hre = require("hardhat");

async function main() {
  console.log("Deploying Payment contract...");

  const Payment = await hre.ethers.getContractFactory("Payment");
  const payment = await Payment.deploy();

  await payment.waitForDeployment();
  const address = await payment.getAddress();

  console.log(`Payment contract deployed to: ${address}`);
  console.log(`Network: ${hre.network.name}`);

  if (hre.network.name !== "hardhat" && hre.network.name !== "localhost") {
    console.log("\nVerifying contract on Polygon...");
    try {
      await hre.run("verify:verify", {
        address: address,
        constructorArguments: []
      });
      console.log("Contract verified successfully!");
    } catch (error) {
      console.log("Verification failed:", error.message);
    }
  }

  return address;
}

main()
  .then((address) => {
    console.log(`\nDeployment successful!`);
    console.log(`Contract Address: ${address}`);
    console.log(`\nTo interact with the contract, use:`);
    console.log(`npx hardhat run scripts/interact.js --network ${hre.network.name}`);
  })
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });