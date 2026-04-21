const hre = require("hardhat");

const CONTRACT_ADDRESS = process.env.CONTRACT_ADDRESS;

async function main() {
  const [deployer, merchant, user1, user2] = await hre.ethers.getSigners();

  console.log("Interacting with Payment contract...");
  console.log(`Deployer: ${deployer.address}`);

  const payment = await hre.ethers.getContractAt("Payment", CONTRACT_ADDRESS);

  console.log("\n1. Registering merchant...");
  const tx1 = await payment.registerMerchant(user1.address);
  await tx1.wait();
  console.log(`   Merchant registered: ${user1.address}`);

  console.log("\n2. Sending payment...");
  const amountToSend = hre.ethers.parseEther("0.1");
  const tx2 = await payment.sendPayment(user2.address, amountToSend);
  const receipt = await tx2.wait();
  
  const paymentEvent = receipt.logs.find(
    (log) => log.fragment && log.fragment.name === "PaymentCompleted"
  );
  
  if (paymentEvent) {
    console.log(`   Payment sent: ${hre.ethers.formatEther(amountToSend)} MATIC`);
    console.log(`   Recipient: ${user2.address}`);
  }

  console.log("\n3. Checking contract balance...");
  const balance = await payment.getContractBalance();
  console.log(`   Balance: ${hre.ethers.formatEther(balance)} MATIC`);

  console.log("\n4. Getting transaction details...");
  const paymentId = hre.ethers.keccak256(
    hre.ethers.AbiCoder.encode(
      ["address", "address", "uint256", "uint256"],
      [deployer.address, user2.address, amountToSend, receipt.blockNumber]
    )
  );
  
  console.log("\nAll interactions completed!");
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });