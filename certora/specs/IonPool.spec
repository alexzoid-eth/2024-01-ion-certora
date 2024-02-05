import "./base/ionPool.spec";
import "./dependencies/erc20.spec"; 

use builtin rule sanity;

/////////////////// METHODS ///////////////////////

methods {
    function hasRole(bytes32 role, address account) external returns (bool) envfree;
    function GEM_JOIN_ROLE() external returns (bytes32) envfree;
    function LIQUIDATOR_ROLE() external returns (bytes32) envfree;

    // Interest rate model
    function _.calculateInterestRate(uint256, uint256, uint256) external => DISPATCHER(true);
    function _.COLLATERAL_COUNT() external => collateralCountCVL() expect uint256;

    // Spot oracle
    function _.getSpot() external => getSpotCVL() expect uint256;

    // Whitelist
    function _.isWhitelistedBorrower(uint8 ilkIndex, address poolCaller, address addr, bytes32[] proof) external => getWhitelistBorrowerCVL(poolCaller) expect bool;
    function _.isWhitelistedLender(address poolCaller, address addr, bytes32[] proof) external => getWhitelistLenderCVL(poolCaller) expect bool;

    // Chainlink
    function _.latestRoundData() external => latestRoundDataCVL() expect (uint80, int256, uint256, uint256, uint80);

    function _.getStETHByWstETH(uint256 amount) external => getStETHByWstETHCVL(amount) expect (uint256);

    // mulDiv summary for better run time
    function _.mulDiv(uint x, uint y, uint denominator) internal => mulDivCVL(x,y,denominator) expect uint;
}

///////////////// DEFINITIONS /////////////////////

definition PAUSABLE_FUNCTIONS(method f) returns bool = 
    f.selector == sig:accrueInterest().selector
    || f.selector == sig:withdraw(address, uint256).selector
    || f.selector == sig:supply(address, uint256, bytes32[]).selector
    || f.selector == sig:borrow(uint8, address,address, uint256, bytes32[]).selector
    || f.selector == sig:repay(uint8, address, address, uint256).selector
    || f.selector == sig:withdrawCollateral(uint8, address, address, uint256).selector
    || f.selector == sig:depositCollateral(uint8, address, address, uint256, bytes32[]).selector
    || f.selector == sig:repayBadDebt(address, uint256).selector
    || f.selector == sig:confiscateVault(uint8, address, address, address, int256, int256).selector
    || f.selector == sig:transferGem(uint8, address, address, uint256).selector;

definition ONLY_WHITELISTED_BORROWERS_FUNCTIONS(method f) returns bool = 
    f.selector == sig:borrow(uint8, address,address, uint256, bytes32[]).selector
    || f.selector == sig:depositCollateral(uint8, address, address, uint256, bytes32[]).selector;

definition ONLY_WHITELISTED_LENDERS_FUNCTIONS(method f) returns bool = 
    f.selector == sig:supply(address, uint256, bytes32[]).selector;

definition ROLE_ION() returns bytes32 = to_bytes32(0x5ab1a5ffb29c47d95dec8c5f9ad49a551754822b51a3359ed1c21e2be24beefa); // keccak256("ION");
definition ONLY_ROLE_ION_FUNCTIONS(method f) returns bool = 
    f.selector == sig:initializeIlk(address).selector
    || f.selector == sig:updateIlkSpot(uint8, address).selector
    || f.selector == sig:updateIlkDebtCeiling(uint8, uint256).selector
    || f.selector == sig:updateIlkDust(uint8, uint256).selector
    || f.selector == sig:updateSupplyCap(uint256).selector
    || f.selector == sig:updateInterestRateModule(address).selector
    || f.selector == sig:updateWhitelist(address).selector
    || f.selector == sig:pause().selector
    || f.selector == sig:unpause().selector
    || f.selector == sig:initializeIlk(address).selector;

definition ONLY_ROLE_LIQUIDATOR_FUNCTIONS(method f) returns bool = 
    f.selector == sig:confiscateVault(uint8, address, address, address, int256, int256).selector;

definition ONLY_ROLE_GEM_JOIN_FUNCTIONS(method f) returns bool = 
    f.selector == sig:mintAndBurnGem(uint8, address, int256).selector;

definition ACCRUE_INTEREST_FUNCTIONS(method f) returns bool = 
    f.selector == sig:accrueInterest().selector
    || f.selector == sig:pause().selector
    || f.selector == sig:withdraw(address, uint256).selector
    || f.selector == sig:supply(address, uint256, bytes32[]).selector
    || f.selector == sig:borrow(uint8, address,address, uint256, bytes32[]).selector
    || f.selector == sig:repay(uint8, address, address, uint256).selector
    || f.selector == sig:withdrawCollateral(uint8, address, address, uint256).selector
    || f.selector == sig:depositCollateral(uint8, address, address, uint256, bytes32[]).selector
    || f.selector == sig:confiscateVault(uint8, address, address, address, int256, int256).selector;

definition PURE_VIEW_FUNCTIONS(method f) returns bool = f.isView || f.isPure;

////////////////// FUNCTIONS //////////////////////

function collateralCountCVL() returns uint256 {
    return require_uint256(ghostCollateralCount);
}

function latestRoundDataCVL() returns (uint80, int256, uint256, uint256, uint80) {
    return (roundId, answer, startedAt, updatedAt, answeredInRound);
}

function getSpotCVL() returns uint256 {
    return spot;
}

function getWhitelistBorrowerCVL(address user) returns bool {
    return ghostIsWhitelistedBorrower[user];
}

function getWhitelistLenderCVL(address user) returns bool {
    return ghostIsWhitelistedLender[user];
}

function getStETHByWstETHCVL(uint256 amount) returns uint256 {
    return getStETHByWstETH_Ghost[amount];
}

function mulDivCVL(uint x, uint y, uint denominator) returns uint {
    require(denominator != 0);
    return require_uint256(x*y/denominator);
}

///////////////// GHOSTS & HOOKS //////////////////

ghost mapping(uint256 => uint256) getStETHByWstETH_Ghost;
ghost mapping(address => bool) ghostIsWhitelistedBorrower;
ghost mapping(address => bool) ghostIsWhitelistedLender;

ghost uint256 spot;
ghost uint80 roundId;
ghost int256 answer;
ghost uint256 startedAt;
ghost uint256 updatedAt;
ghost uint80 answeredInRound;

ghost mathint ghostCollateralCount;

ghost bool ghostMadeCall;
hook CALL(uint g, address addr, uint value, uint argsOffset, uint argsLength, uint retOffset, uint retLength) uint rc {
    ghostMadeCall = true;
}

///////////////// PROPERTIES //////////////////////

use invariant ilkAddressesLengthSolvency;
use invariant ilkMaxLength;

rule initializeCouldBeExecutedOnce(env e, calldataarg args) {

    setUpEnv(e);

    initialize(e, args);

    initialize@withrevert(e, args);
    bool reverted = lastReverted;

    assert(reverted);
}

rule onlyRoleIonIntegrity(env e, method f, calldataarg args) 
    filtered { f -> ONLY_ROLE_ION_FUNCTIONS(f) } {
    
    setUpEnv(e);

    f@withrevert(e, args);
    bool reverted = lastReverted;

    assert(!hasRole(ROLE_ION(), e.msg.sender) => reverted);
}

rule onlyRoleLiquidatorIntegrity(env e, method f, calldataarg args) 
    filtered { f -> ONLY_ROLE_LIQUIDATOR_FUNCTIONS(f) } {
    
    setUpEnv(e);

    f@withrevert(e, args);
    bool reverted = lastReverted;

    assert(!hasRole(LIQUIDATOR_ROLE(), e.msg.sender) => reverted);
}

rule onlyRoleGemJoinIntegrity(env e, method f, calldataarg args) 
    filtered { f -> ONLY_ROLE_GEM_JOIN_FUNCTIONS(f) } {
    
    setUpEnv(e);

    f@withrevert(e, args);
    bool reverted = lastReverted;

    assert(!hasRole(GEM_JOIN_ROLE(), e.msg.sender) => reverted);
}

rule modifyStoragePossibility(env e, method f, calldataarg args) 
    filtered { f -> !PURE_VIEW_FUNCTIONS(f) } {
    
    storage before = lastStorage;

    f(e, args);

    storage after = lastStorage;

    satisfy(before[currentContract] != after[currentContract]);
}

rule pauseableIntegrity(env e, method f, calldataarg args) 
    filtered { f -> PAUSABLE_FUNCTIONS(f) } {
    
    setUpEnv(e);

    f@withrevert(e, args);
    bool reverted = lastReverted;

    assert(ghostPaused != 0 => reverted);
}

rule accrueInterestNotMissed(env e, method f, calldataarg args) 
    filtered { f -> ACCRUE_INTEREST_FUNCTIONS(f) } {
    
    mathint debtBefore = ghostDebt;

    f(e, args);

    mathint debtAfter = ghostDebt;

    satisfy(debtBefore != debtAfter);
}

rule onlyWhitelistedBorrowersIntegrity(env e, method f, calldataarg args) 
    filtered { f -> ONLY_WHITELISTED_BORROWERS_FUNCTIONS(f) } {
    
    setUpEnv(e);

    f@withrevert(e, args);
    bool reverted = lastReverted;

    assert(!ghostIsWhitelistedBorrower[e.msg.sender] => reverted);
}

rule onlyWhitelistedLendersIntegrity(env e, method f, calldataarg args) 
    filtered { f -> ONLY_WHITELISTED_LENDERS_FUNCTIONS(f) } {
    
    setUpEnv(e);

    f@withrevert(e, args);
    bool reverted = lastReverted;

    assert(!ghostIsWhitelistedLender[e.msg.sender] => reverted);
}

rule pauseIntegrity(env e) {

    pause(e);

    assert(ghostPaused != 0);
}

rule unpauseIntegrity(env e) {

    setUp();

    mathint n;
    require(n >= 0 && n < ghostIlksLength);

    unpause(e);

    assert(ghostPaused == 0);
    assert(require_uint48(ghostIlksLastRateUpdate[n]) == require_uint48(e.block.timestamp));
}

rule gettersIntegrity() {

    setUp();

    mathint n;
    require(n >= 0 && n < ghostIlksLength);

    assert(to_mathint(ilkCount()) == ghostIlksLength);
    assert(to_mathint(totalNormalizedDebt(require_uint8(n))) == ghostIlksTotalNormalizedDebt[n]);
    assert(to_mathint(rateUnaccrued(require_uint8(n))) == ghostIlksRate[n]);
    assert(to_mathint(lastRateUpdate(require_uint8(n))) == ghostIlksLastRateUpdate[n]);
    assert(spot(require_uint8(n)) == ghostIlksSpot[n]);
    assert(to_mathint(debtCeiling(require_uint8(n))) == ghostIlksDebtCeiling[n]);
    assert(to_mathint(dust(require_uint8(n))) == ghostIlksDust[n]);

    // assert(getIlkAddress(require_uint256(n)) == require_address(ghostAddressSetValues[n]));

    assert(to_mathint(debtUnaccrued()) == ghostDebt);
    assert(to_mathint(weth()) == ghostWeth);
    assert(to_mathint(totalUnbackedDebt()) == ghostTotalUnbackedDebt);
    assert(interestRateModule() == ghostInterestRateModule);
    assert(whitelist() == ghostWhitelist);
}

rule updateIlkSpotIntegrity(env e, uint8 ilkIndex, address newSpot) {

    setUp();
    require(to_mathint(ilkIndex) < STORAGE_ILKS_MAX_LENGTH());
    
    updateIlkSpot(e, ilkIndex, newSpot);

    assert(newSpot == ghostIlksSpot[ilkIndex]);
}

rule updateIlkDebtCeilingIntegrity(env e, uint8 ilkIndex, uint256 newCeiling) {

    setUp();
    require(to_mathint(ilkIndex) < STORAGE_ILKS_MAX_LENGTH());
    
    updateIlkDebtCeiling(e, ilkIndex, newCeiling);

    assert(to_mathint(newCeiling) == ghostIlksDebtCeiling[ilkIndex]);
}

rule updateIlkDustIntegrity(env e, uint8 ilkIndex, uint256 newDust) {

    setUp();
    require(to_mathint(ilkIndex) < STORAGE_ILKS_MAX_LENGTH());
    
    updateIlkDust(e, ilkIndex, newDust);

    assert(to_mathint(newDust) == ghostIlksDust[ilkIndex]);
}

rule updateSupplyCapIntegrity(env e, uint256 newSupplyCap) {
    
    updateSupplyCap(e, newSupplyCap);

    assert(to_mathint(newSupplyCap) == ghostWethSupplyCap);
}

rule updateInterestRateModuleIntegrity(env e, address _interestRateModule) {
    
    setUpEnv(e);

    updateInterestRateModule@withrevert(e, _interestRateModule);
    bool reverted = lastReverted;

    assert(!reverted => _interestRateModule == ghostInterestRateModule);
    assert(_interestRateModule == 0 => reverted);
    assert(ghostCollateralCount != ghostIlksLength => reverted);
}

rule updateWhitelistIntegrity(env e, address _whitelist) {
    
    setUpEnv(e);

    updateWhitelist@withrevert(e, _whitelist);
    bool reverted = lastReverted;

    assert(!reverted => _whitelist == ghostWhitelist);
    assert(_whitelist == 0 => reverted);
}

rule addOperatorIntegrity(env e, address operator) {

    addOperator(e, operator);

    assert(isOperator(e.msg.sender, operator));
}

rule removeOperatorIntegrity(env e, address operator) {

    removeOperator(e, operator);

    assert(!isOperator(e.msg.sender, operator));
}

rule withdrawCollateralSetRecepientGem(env e, uint8 ilkIndex, address user, address recipient, uint256 amount) {

    uint256 gemBefore = gem(ilkIndex, recipient);

    withdrawCollateral(e, ilkIndex, user, recipient, amount);

    uint256 gemAfter = gem(ilkIndex, recipient);

    satisfy(gemBefore != gemAfter);
}