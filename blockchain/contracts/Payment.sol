// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "@openzeppelin/contracts/security/ReentrancyGuard.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract Payment is ReentrancyGuard, Ownable {
    struct PaymentRecord {
        address sender;
        address recipient;
        uint256 amount;
        uint256 timestamp;
        bool completed;
    }

    mapping(bytes32 => PaymentRecord) public payments;
    mapping(address => bool) public merchants;
    mapping(address => uint256) public balances;

    event PaymentCreated(
        bytes32 indexed paymentId,
        address indexed sender,
        address indexed recipient,
        uint256 amount
    );
    event PaymentCompleted(
        bytes32 indexed paymentId,
        address indexed recipient,
        uint256 amount
    );
    event MerchantRegistered(address indexed merchant);

    modifier onlyMerchant() {
        require(merchants[msg.sender], "Caller is not a merchant");
        _;
    }

    constructor() Ownable(msg.sender) {
        merchants[msg.sender] = true;
    }

    function sendPayment(address payable to, uint256 amount)
        external
        payable
        nonReentrant
        onlyMerchant
    {
        require(to != address(0), "Invalid recipient address");
        require(amount > 0, "Amount must be greater than zero");
        require(msg.value >= amount, "Insufficient Native Token balance");

        bytes32 paymentId = keccak256(
            abi.encodePacked(msg.sender, to, amount, block.timestamp)
        );

        payments[paymentId] = PaymentRecord({
            sender: msg.sender,
            recipient: to,
            amount: amount,
            timestamp: block.timestamp,
            completed: true
        });

        (bool success, ) = to.call{value: amount}("");
        require(success, "Transfer failed");

        emit PaymentCreated(paymentId, msg.sender, to, amount);
        emit PaymentCompleted(paymentId, to, amount);
    }

    function getPaymentDetails(bytes32 paymentId)
        external
        view
        returns (
            address sender,
            address recipient,
            uint256 amount,
            uint256 timestamp,
            bool completed
        )
    {
        PaymentRecord memory payment = payments[paymentId];
        return (
            payment.sender,
            payment.recipient,
            payment.amount,
            payment.timestamp,
            payment.completed
        );
    }

    function registerMerchant(address merchant) external onlyOwner {
        require(merchant != address(0), "Invalid merchant address");
        merchants[merchant] = true;
        emit MerchantRegistered(merchant);
    }

    function removeMerchant(address merchant) external onlyOwner {
        merchants[merchant] = false;
    }

    function getContractBalance() external view returns (uint256) {
        return address(this).balance;
    }

    receive() external payable {}
}