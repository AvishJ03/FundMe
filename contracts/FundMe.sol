//SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "./PriceConverter.sol";

error NotOwner(); //Custom Error

contract FundMe {
    using PriceConverter for uint256;
    // constant and immutable are gas savers
    uint256 public constant MIN_USD = 50 * 1e18;
    address public immutable owner;
    AggregatorV3Interface public priceFeed;

    address[] public funders;
    mapping(address => uint256) public addressToAmt;

    constructor(address _priceFeed) {
        priceFeed = AggregatorV3Interface(_priceFeed);
        owner = msg.sender;
    }

    function fund() public payable {
        require(
            msg.value.getConversionRate(priceFeed) >= MIN_USD,
            "Didnt send enough"
        ); //1e18 = 1*10^18 = 1ETH
        funders.push(msg.sender);
        addressToAmt[msg.sender] = msg.value;
        // 18 decimals
    }

    function withdraw() public onlyOwner {
        // For loop
        for (uint256 i = 0; i < funders.length; i++) {
            address funder = funders[i];
            addressToAmt[funder] = 0;
        }
        // reset an array
        funders = new address[](0);

        // withdraw eth

        // 1. transfer
        // msg.sender => address
        // payable(msg.sender) => payable address
        // payable(msg.sender).transfer(address(this).balance);

        // 2. send
        // bool sendSuccess = payable(msg.sender).send(address(this).balance);
        // require(sendSuccess, "Send Failed");

        // 3. call
        (bool callSuccess, ) = payable(msg.sender).call{
            value: address(this).balance
        }("");
        require(callSuccess, "Call Failed");
    }

    modifier onlyOwner() {
        // require(msg.sender == owner, "Not the owner");
        if (msg.sender != owner) {
            revert NotOwner();
        }
        _;
    }

    receive() external payable {
        fund();
    }

    fallback() external payable {
        fund();
    }
}
// 0xD4a33860578De61DBAbDc8BFdb98FD742fA7028e
