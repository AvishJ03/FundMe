from scripts.helpfulScripts import getAcc, LOCAL_ENV
from scripts.deploy import deployFundMe
from brownie import network, accounts, exceptions
import pytest


def test_fundandWithdraw():
    acc = getAcc()
    fundMe = deployFundMe()
    entranceFee = 50000000000000000
    txn = fundMe.fund({"from": acc, "value": entranceFee})
    txn.wait(1)
    assert fundMe.addressToAmt(acc.address) == entranceFee
    txn2 = fundMe.withdraw({"from": acc})
    txn2.wait(1)
    assert fundMe.addressToAmt(acc.address) == 0


def testOwner():
    if network.show_active() not in LOCAL_ENV:
        pytest.skip("Only for local testing")
    fundMe = deployFundMe()
    badAcc = accounts.add()
    with pytest.raises(exceptions.VirtualMachineError):
        fundMe.withdraw({"from": badAcc})
