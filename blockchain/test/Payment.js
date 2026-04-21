const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("Payment Contract", function () {
  let payment;
  let owner, merchant, user1, user2;

  beforeEach(async function () {
    [owner, merchant, user1, user2] = await ethers.getSigners();

    const Payment = await ethers.getContractFactory("Payment");
    payment = await Payment.deploy();
    await payment.waitForDeployment();
  });

  describe("Deployment", function () {
    it("should set the correct owner", async function () {
      expect(await payment.owner()).to.equal(owner.address);
    });

    it("should register owner as merchant", async function () {
      expect(await payment.merchants(owner.address)).to.be.true;
    });
  });

  describe("Payments", function () {
    it("should send payment successfully", async function () {
      const amount = ethers.parseEther("0.1");

      const initialBalance = await ethers.provider.getBalance(user1.address);

      const tx = await payment.sendPayment(user1.address, amount, {
        value: amount
      });
      await tx.wait();

      const finalBalance = await ethers.provider.getBalance(user1.address);
      expect(finalBalance - initialBalance).to.equal(amount);
    });

    it("should fail with invalid recipient", async function () {
      await expect(
        payment.sendPayment(ethers.ZeroAddress, ethers.parseEther("0.1"), {
          value: ethers.parseEther("0.1")
        })
      ).to.be.revertedWith("Invalid recipient address");
    });

    it("should fail with zero amount", async function () {
      await expect(
        payment.sendPayment(user1.address, 0, { value: 0 })
      ).to.be.revertedWith("Amount must be greater than zero");
    });
  });

  describe("Merchant Management", function () {
    it("should register new merchant", async function () {
      await payment.registerMerchant(merchant.address);
      expect(await payment.merchants(merchant.address)).to.be.true;
    });

    it("should remove merchant", async function () {
      await payment.registerMerchant(merchant.address);
      await payment.removeMerchant(merchant.address);
      expect(await payment.merchants(merchant.address)).to.be.false;
    });

    it("should prevent non-owner from registering merchant", async function () {
      await expect(
        payment.connect(user1).registerMerchant(user2.address)
      ).to.be.revertedWith("Ownable: caller is not the owner");
    });
  });

  describe("Payment Records", function () {
    it("should store payment records", async function () {
      const amount = ethers.parseEther("0.1");
      const tx = await payment.sendPayment(user1.address, amount, {
        value: amount
      });
      const receipt = await tx.wait();

      const paymentEvent = receipt.logs.find(
        (log) => log.fragment && log.fragment.name === "PaymentCreated"
      );

      const paymentId = paymentEvent.args.paymentId;
      const details = await payment.getPaymentDetails(paymentId);

      expect(details.sender).to.equal(owner.address);
      expect(details.recipient).to.equal(user1.address);
      expect(details.amount).to.equal(amount);
      expect(details.completed).to.be.true;
    });
  });
});