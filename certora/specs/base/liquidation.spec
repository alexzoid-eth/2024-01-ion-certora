using LiquidationHarness as _Liquidation;

/////////////////// METHODS ///////////////////////

methods {
    function _Liquidation.getRepayAmt(uint8 ilkIndex, address vault) external returns (uint256);
    function _Liquidation.liquidate(uint8 ilkIndex, address vault, address kpr) external returns (uint256, uint256);
}

///////////////// DEFINITIONS /////////////////////

////////////////// FUNCTIONS //////////////////////

///////////////// GHOSTS & HOOKS //////////////////

///////////////// PROPERTIES //////////////////////
