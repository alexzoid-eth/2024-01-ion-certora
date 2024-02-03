// SPDX-License-Identifier: BUSL-1.1
pragma solidity 0.8.21;

import "../../src/InterestRate.sol";

contract InterestRateHarness is InterestRate {   
    constructor(IlkData[] memory ilkDataList, IYieldOracle _yieldOracle) InterestRate(ilkDataList, _yieldOracle) { }
}