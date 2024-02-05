import "./base/ionPool.spec";
import "./dependencies/erc20.spec";

use builtin rule sanity;

/////////////////// METHODS ///////////////////////

methods {
}

///////////////// DEFINITIONS /////////////////////

////////////////// FUNCTIONS //////////////////////

///////////////// GHOSTS & HOOKS //////////////////

///////////////// PROPERTIES //////////////////////

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

    assert(to_mathint(debtUnaccrued()) == ghostDebt);
    assert(to_mathint(weth()) == ghostWeth);
    assert(to_mathint(totalUnbackedDebt()) == ghostTotalUnbackedDebt);
    assert(interestRateModule() == ghostInterestRateModule);
    assert(whitelist() == ghostWhitelist);
}

rule testUpdateIlkDebtCeiling(env e) {
    assert(require_uint256(ghostIlksDebtCeiling[1]) == debtCeiling(1));
}

rule testTotalNormalizedDebt(env e) {
    assert(totalNormalizedDebt(1) != 4);
}

rule testSpot(env e) {
    assert(spot(4) != 4);
}

rule testDust(env e) {
    assert(dust(0) != 4);
}