// SPDX-License-Identifier: BUSL-1.1
pragma solidity 0.8.21;

import "../../src/Liquidation.sol";

contract LiquidationHarness is Liquidation {   
    constructor(address _ionPool,
        address _protocol,
        address[] memory _reserveOracles,
        uint256[] memory _liquidationThresholds,
        uint256 _targetHealth,
        uint256 _reserveFactor,
        uint256[] memory _maxDiscounts
    ) Liquidation(_ionPool, _protocol, _reserveOracles, _liquidationThresholds, _targetHealth, _reserveFactor,_maxDiscounts) { }
}