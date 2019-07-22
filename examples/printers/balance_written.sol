pragma solidity ^0.5.9;

contract BalanceWritten {
    uint256 balance;

    constructor() public {
        balance = 1;
    }

    function setBalanceTo2() public {
        balance = 2;
    }

    function setBalanceTo3() external {
        balance = 3;
    }

    function dontSetBalanceExt() external pure {}

    function dontSetBalancePub() public pure {}
}
