using IonPoolHarness as _IonPool;

/////////////////// METHODS ///////////////////////

methods {
    function _IonPool.initialize(
        address _underlying,
        address _treasury,
        uint8 decimals_,
        string name_,
        string symbol_,
        address initialDefaultAdmin,
        address _interestRateModule,
        address _whitelist
    ) external;
    // ION
    function _IonPool.initializeIlk(address ilkAddress) external;
    function _IonPool.updateIlkSpot(uint8 ilkIndex, address newSpot) external;
    function _IonPool.updateIlkDebtCeiling(uint8 ilkIndex, uint256 newCeiling) external;
    function _IonPool.updateIlkDust(uint8 ilkIndex, uint256 newDust) external;
    function _IonPool.updateSupplyCap(uint256 newSupplyCap) external;
    function _IonPool.updateInterestRateModule(address _interestRateModule) external;
    function _IonPool.updateWhitelist(address _whitelist) external;
    function _IonPool.pause() external;
    function _IonPool.unpause() external;
    // Interest Calculations
    function _IonPool.accrueInterest() external returns (uint256);
    function _IonPool.calculateRewardAndDebtDistribution() external returns (uint256, uint256, uint104[], uint256, uint48[]);
    function _IonPool.calculateRewardAndDebtDistributionForIlk(uint8 ilkIndex) external returns (uint104, uint48);
    // Lender Operations
    function _IonPool.withdraw(address receiverOfUnderlying, uint256 amount) external;
    function _IonPool.supply(address user, uint256 amount, bytes32[] calldata proof) external;
    // Borrower Operations
    function _IonPool.borrow(uint8 ilkIndex, address user, address recipient, uint256 amountOfNormalizedDebt, bytes32[] proof) external;
    function _IonPool.repay(uint8 ilkIndex, address user, address payer, uint256 amountOfNormalizedDebt) external;
    function _IonPool.withdrawCollateral(uint8 ilkIndex, address user, address recipient, uint256 amount) external;
    function _IonPool.depositCollateral(uint8 ilkIndex, address user, address depositor, uint256 amount,bytes32[] proof) external;
    // Settlement
    function _IonPool.repayBadDebt(address user, uint256 rad) external;
    // CDP Confiscation
    function _IonPool.confiscateVault(uint8 ilkIndex, address u, address v, address w, int256 changeInCollateral, int256 changeInNormalizedDebt) external;
    // Fungibility
    function _IonPool.mintAndBurnGem(uint8 ilkIndex, address usr, int256 wad) external;
    function _IonPool.transferGem(uint8 ilkIndex, address src, address dst, uint256 wad) external;
    // Getters
    function _IonPool.ilkCount() external returns (uint256) envfree;
    function _IonPool.getIlkIndex(address ilkAddress) external returns (uint8) envfree;
    function _IonPool.getIlkAddress(uint256 ilkIndex) external returns (address) envfree;
    function _IonPool.addressContains(address ilk) external returns (bool) envfree;
    function _IonPool.totalNormalizedDebt(uint8 ilkIndex) external returns (uint256) envfree;
    function _IonPool.rateUnaccrued(uint8 ilkIndex) external returns (uint256) envfree;
    function _IonPool.rate(uint8 ilkIndex) external returns (uint256) envfree;
    function _IonPool.lastRateUpdate(uint8 ilkIndex) external returns (uint256) envfree;
    function _IonPool.spot(uint8 ilkIndex) external returns (address) envfree;
    function _IonPool.debtCeiling(uint8 ilkIndex) external returns (uint256) envfree;
    function _IonPool.dust(uint8 ilkIndex) external returns (uint256) envfree;
    function _IonPool.collateral(uint8 ilkIndex, address user) external returns (uint256) envfree;
    function _IonPool.normalizedDebt(uint8 ilkIndex, address user) external returns (uint256) envfree;
    function _IonPool.vault(uint8 ilkIndex, address user) external returns (uint256, uint256) envfree;
    function _IonPool.gem(uint8 ilkIndex, address user) external returns (uint256) envfree;
    function _IonPool.unbackedDebt(address user) external returns (uint256) envfree;
    function _IonPool.isOperator(address user, address operator) external returns (bool) envfree;
    function _IonPool.isAllowed(address user, address operator) external returns (bool) envfree;
    function _IonPool.debtUnaccrued() external returns (uint256) envfree;
    function _IonPool.debt() external returns (uint256);
    function _IonPool.totalUnbackedDebt() external returns (uint256) envfree;
    function _IonPool.interestRateModule() external returns (address) envfree;
    function _IonPool.whitelist() external returns (address) envfree;
    function _IonPool.weth() external returns (uint256) envfree;
    function _IonPool.getCurrentBorrowRate(uint8 ilkIndex) external returns (uint256, uint256);
    function _IonPool.implementation() external returns (address) envfree;
    // Auth
    function _IonPool.addOperator(address operator) external;
    function _IonPool.removeOperator(address operator) external;    
}   

///////////////// DEFINITIONS /////////////////////

////////////////// FUNCTIONS //////////////////////

///////////////// GHOSTS & HOOKS //////////////////

///////////////// PROPERTIES //////////////////////
