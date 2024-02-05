using IonPoolHarness as _IonPool;

/////////////////// METHODS ///////////////////////

methods {
    function _IonPool.initialize(address _underlying, address _treasury, uint8 decimals_, string name_, string symbol_,
        address initialDefaultAdmin, address _interestRateModule, address _whitelist) external;
    // onlyRole(ION)
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
    function _IonPool.rate(uint8 ilkIndex) external returns (uint256);
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

// Slot number of IonPoolStorageLocation
definition ION_POOL_STORAGE_LOCATION() returns uint256 
    = 0xceba3d526b4d5afd91d1b752bf1fd37917c20a6daf576bcb41dd1c57c1f67e00;
 
// Slot number of IonPoolStorage.ilks[] length
definition STORAGE_SLOT_ILKS_LENGTH() returns bytes32 = to_bytes32(ION_POOL_STORAGE_LOCATION());

// Size of IonPoolStorage.ilks in slots
definition ILKS_SIZE_IN_SLOTS() returns mathint = 4;

// Slot number of IonPoolStorage.ilks[0]
definition STORAGE_SLOT_ILKS_0() returns bytes32 
    = keccak256(STORAGE_SLOT_ILKS_LENGTH()); 

// Limit the maximum length of IonPoolStorage.ilks[] from max_uint8 to 2
definition STORAGE_ILKS_MAX_LENGTH() returns mathint = 2;

// Check if slot contains variables of IonPoolStorage.ilks[number]
definition IS_STORAGE_SLOT_ILKS_OFFSET(mathint slot, mathint number, mathint offset) returns bool 
    = to_bytes32(require_uint256(slot - (number * ILKS_SIZE_IN_SLOTS() + offset))) == STORAGE_SLOT_ILKS_0(); 

// Unpack from slot `uint104 totalNormalizedDebt; uint104 rate; uint48 lastRateUpdate;`
// https://docs.certora.com/en/cvl1/docs/confluence/anatomy/hooks.html#manually-unpacking-structs
definition ILKS_SLOT0_TOTAL_NORMALIZED_DEBT(uint256 s) returns uint256 
    = s & 0xffffffffffffffffffffffffff;
definition ILKS_SLOT0_RATE(uint256 s) returns uint256 
    = (s & 0xffffffffffffffffffffffffff00000000000000000000000000) >> 104;
definition ILKS_SLOT0_LAST_RATE_UPDATE(uint256 s) returns uint256 
    = (s & 0xffffffffffff0000000000000000000000000000000000000000000000000000) >> 208;

// Slot number of IonPoolStorage.ilkAddresses._inner._values[] length
definition STORAGE_SLOT_ILKADDRESSES_INNER_VALUES_LENGTH() returns bytes32 
    = keccak256(to_bytes32(require_uint256(ION_POOL_STORAGE_LOCATION() + 1))); 

// Slot number of IonPoolStorage.debt
definition IS_STORAGE_SLOT_DEBT(mathint slot) returns bool 
    = to_bytes32(require_uint256(slot - 7)) == to_bytes32(ION_POOL_STORAGE_LOCATION()); 

// Slot number of IonPoolStorage.weth
definition IS_STORAGE_SLOT_WETH(mathint slot) returns bool 
    = to_bytes32(require_uint256(slot - 8)) == to_bytes32(ION_POOL_STORAGE_LOCATION()); 

// Slot number of IonPoolStorage.wethSupplyCap
definition IS_STORAGE_SLOT_WETH_SUPPLY_CAP(mathint slot) returns bool 
    = to_bytes32(require_uint256(slot - 9)) == to_bytes32(ION_POOL_STORAGE_LOCATION()); 

// Slot number of IonPoolStorage.totalUnbackedDebt
definition IS_STORAGE_SLOT_TOTAL_UNBACKED_DEBT(mathint slot) returns bool 
    = to_bytes32(require_uint256(slot - 10)) == to_bytes32(ION_POOL_STORAGE_LOCATION()); 

// Slot number of IonPoolStorage.interestRateModule
definition IS_STORAGE_SLOT_INTEREST_RATE_MODULE(mathint slot) returns bool 
    = to_bytes32(require_uint256(slot - 11)) == to_bytes32(ION_POOL_STORAGE_LOCATION()); 

// Slot number of IonPoolStorage.whitelist
definition IS_STORAGE_SLOT_WHITELIST(mathint slot) returns bool 
    = to_bytes32(require_uint256(slot - 12)) == to_bytes32(ION_POOL_STORAGE_LOCATION()); 

////////////////// FUNCTIONS //////////////////////

// Setup contract environment
function setUp() {
    require(ghostIlksLength <= STORAGE_ILKS_MAX_LENGTH());
}

// Process hook for IonPoolStorage.ilks[]. Support 2 elements in ilks[] array
function processIlksArrayHook(bool read, uint256 slot, uint256 val) returns bool {
        
    // IonPoolStorage.ilks[] length
    if(to_bytes32(slot) == STORAGE_SLOT_ILKS_LENGTH()) {
        if(read) {
            require(require_uint256(ghostIlksLength) == val);
        } else {
            ghostIlksLength = val;
        }

    // ilks[0].totalNormalizedDebt, ilks[0].rate, ilks[0].lastRateUpdate
    } else if(IS_STORAGE_SLOT_ILKS_OFFSET(slot, 0, 0)) {  
        if(read) {
            require(require_uint256(ghostIlksTotalNormalizedDebt[0]) == ILKS_SLOT0_TOTAL_NORMALIZED_DEBT(val));
            require(require_uint256(ghostIlksRate[0]) == ILKS_SLOT0_RATE(val));
            require(require_uint256(ghostIlksLastRateUpdate[0]) == ILKS_SLOT0_LAST_RATE_UPDATE(val));
        } else {
            ghostIlksTotalNormalizedDebt[0] = ILKS_SLOT0_TOTAL_NORMALIZED_DEBT(val);
            ghostIlksRate[0] = ILKS_SLOT0_RATE(val);
            ghostIlksLastRateUpdate[0] = ILKS_SLOT0_LAST_RATE_UPDATE(val);
        }
    // ilks[0].spot
    } else if(IS_STORAGE_SLOT_ILKS_OFFSET(slot, 0, 1)) {  
        if(read) {
            require(ghostIlksSpot[0] == require_address(to_bytes32(val)));
        } else {
            ghostIlksSpot[0] = require_address(to_bytes32(val));
        }
    // ilks[0].debtCeiling
    } else if(IS_STORAGE_SLOT_ILKS_OFFSET(slot, 0, 2)) {  
        if(read) {
            require(require_uint256(ghostIlksDebtCeiling[0]) == val);
        } else {
            ghostIlksDebtCeiling[0] = val;
        }
    // ilks[0].dust
    } else if(IS_STORAGE_SLOT_ILKS_OFFSET(slot, 0, 3)) {  
        if(read) {
            require(require_uint256(ghostIlksDust[0]) == val);
        } else {
            ghostIlksDust[0] = val;
        }
    }

    // ilks[1].totalNormalizedDebt, ilks[1].rate, ilks[1].lastRateUpdate
    if(IS_STORAGE_SLOT_ILKS_OFFSET(slot, 1, 0)) {  
        if(read) {
            require(require_uint256(ghostIlksTotalNormalizedDebt[1]) == ILKS_SLOT0_TOTAL_NORMALIZED_DEBT(val));
            require(require_uint256(ghostIlksRate[1]) == ILKS_SLOT0_RATE(val));
            require(require_uint256(ghostIlksLastRateUpdate[1]) == ILKS_SLOT0_LAST_RATE_UPDATE(val));
        } else {
            ghostIlksTotalNormalizedDebt[1] = ILKS_SLOT0_TOTAL_NORMALIZED_DEBT(val);
            ghostIlksRate[1] = ILKS_SLOT0_RATE(val);
            ghostIlksLastRateUpdate[1] = ILKS_SLOT0_LAST_RATE_UPDATE(val);
        }
    // ilks[1].spot
    } else if(IS_STORAGE_SLOT_ILKS_OFFSET(slot, 1, 1)) {  
        if(read) {
            require(ghostIlksSpot[1] == require_address(to_bytes32(val)));
        } else {
            ghostIlksSpot[1] = require_address(to_bytes32(val));
        }
    // ilks[1].debtCeiling
    } else if(IS_STORAGE_SLOT_ILKS_OFFSET(slot, 1, 2)) {  
        if(read) {
            require(require_uint256(ghostIlksDebtCeiling[1]) == val);
        } else {
            ghostIlksDebtCeiling[1] = val;
        }
    // ilks[1].dust
    } else if(IS_STORAGE_SLOT_ILKS_OFFSET(slot, 1, 3)) {  
        if(read) {
            require(require_uint256(ghostIlksDust[1]) == val);
        } else {
            ghostIlksDust[1] = val;
        }
    
    } else {
        return false;
    }

    return true;
}

// Process hook for EnumerableSet.AddressSet
function processEnumerableSetHook(bool read, uint256 slot, uint256 val) returns bool {

    return false;
}

// Process hook for regular variables
function processVariablesHook(bool read, uint256 slot, uint256 val) returns bool {
    
    if(IS_STORAGE_SLOT_DEBT(slot)) {
        if(read) {
            require(require_uint256(ghostDebt) == val);
        } else {
            ghostDebt = val;
        }
    // IonPoolStorage.weth
    } else if(IS_STORAGE_SLOT_WETH(slot)) {
        if(read) {
            require(require_uint256(ghostWeth) == val);
        } else {
            ghostWeth = val;
        }
    // IonPoolStorage.wethSupplyCap
    } else if(IS_STORAGE_SLOT_WETH_SUPPLY_CAP(slot)) {
        if(read) {
            require(require_uint256(ghostWethSupplyCap) == val);
        } else {
            ghostWethSupplyCap = val;
        }
    // IonPoolStorage.totalUnbackedDebt
    } else if(IS_STORAGE_SLOT_TOTAL_UNBACKED_DEBT(slot)) {
        if(read) {
            require(require_uint256(ghostTotalUnbackedDebt) == val);
        } else {
            ghostTotalUnbackedDebt = val;
        }
    // IonPoolStorage.interestRateModule
    } else if(IS_STORAGE_SLOT_INTEREST_RATE_MODULE(slot)) {
        if(read) {
            require(ghostInterestRateModule == require_address(to_bytes32(val)));
        } else {
            ghostInterestRateModule = require_address(to_bytes32(val));
        }
    // IonPoolStorage.whitelist
    } else if(IS_STORAGE_SLOT_WHITELIST(slot)) {
        if(read) {
            require(ghostWhitelist == require_address(to_bytes32(val)));
        } else {
            ghostWhitelist = require_address(to_bytes32(val));
        }

    } else {
        return false;
    }

    return true;
}

///////////////// GHOSTS & HOOKS //////////////////

//
// IonPoolStorage.ilks[]
//

// IonPoolStorage.ilks length
ghost mathint ghostIlksLength {
    init_state axiom ghostIlksLength == 0;
}

// IonPoolStorage.ilks[].totalNormalizedDebt
ghost mapping (mathint => mathint) ghostIlksTotalNormalizedDebt {
    init_state axiom forall mathint i. ghostIlksTotalNormalizedDebt[i] == 0;
}

// IonPoolStorage.ilks[].rate
ghost mapping (mathint => mathint) ghostIlksRate {
    init_state axiom forall mathint i. ghostIlksRate[i] == 0;
}

// IonPoolStorage.ilks[].lastRateUpdate
ghost mapping (mathint => mathint) ghostIlksLastRateUpdate {
    init_state axiom forall mathint i. ghostIlksLastRateUpdate[i] == 0;
}

// IonPoolStorage.ilks[].spot
ghost mapping (mathint => address) ghostIlksSpot {
    init_state axiom forall mathint i. ghostIlksSpot[i] == 0;
}

// IonPoolStorage.ilks[].debtCeiling
ghost mapping (mathint => mathint) ghostIlksDebtCeiling {
    init_state axiom forall mathint i. ghostIlksDebtCeiling[i] == 0;
}

// IonPoolStorage.ilks[].dust
ghost mapping (mathint => mathint) ghostIlksDust {
    init_state axiom forall mathint i. ghostIlksDust[i] == 0;
}

//
// IonPoolStorage.debt ... IonPoolStorage.whitelist
//

// IonPoolStorage.debt
ghost mathint ghostDebt {
    init_state axiom ghostDebt == 0;
}

// IonPoolStorage.weth
ghost mathint ghostWeth {
    init_state axiom ghostWeth == 0;
}

// IonPoolStorage.wethSupplyCap
ghost mathint ghostWethSupplyCap {
    init_state axiom ghostWethSupplyCap == 0;
}

// IonPoolStorage.totalUnbackedDebt
ghost mathint ghostTotalUnbackedDebt {
    init_state axiom ghostTotalUnbackedDebt == 0;
}

// IonPoolStorage.interestRateModule
ghost address ghostInterestRateModule {
    init_state axiom ghostInterestRateModule == 0;
}

// IonPoolStorage.whitelist
ghost address ghostWhitelist {
    init_state axiom ghostWhitelist == 0;
}

// Read storage hook
hook ALL_SLOAD(uint256 slot) uint256 val {

    // ilks[]
    if(processIlksArrayHook(true, slot, val)) {

    // ilkAddresses
    } else if(processEnumerableSetHook(true, slot, val)) {

    // debt, weth, wethSupplyCap, totalUnbackedDebt, interestRateModule, whitelist
    } else if(processVariablesHook(true, slot, val)) {
    }
}

// Write storage hook
hook ALL_SSTORE(uint256 slot, uint256 val)  {

    // ilks[]
    if(processIlksArrayHook(false, slot, val)) {
        
    // ilkAddresses
    } else if(processEnumerableSetHook(false, slot, val)) {

    // debt, weth, wethSupplyCap, totalUnbackedDebt, interestRateModule, whitelist
    } else if(processVariablesHook(false, slot, val)) {
    }
}

///////////////// PROPERTIES //////////////////////
