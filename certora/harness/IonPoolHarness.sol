// SPDX-License-Identifier: BUSL-1.1
pragma solidity 0.8.21;

import "../../src/IonPool.sol";

contract IonPoolHarness is IonPool {   
    constructor() IonPool() { }

    function setTotalNormalizedDebt(uint8 ilkIndex, uint104 value) external {
        IonPoolStorage storage $ = _getIonPoolStorage();
        $.ilks[ilkIndex].totalNormalizedDebt = value;
    }
}