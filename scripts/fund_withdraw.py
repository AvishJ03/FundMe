from brownie import FundMe
from scripts.helpfulScripts import getAcc


def fund():
    fundMe = FundMe[-1]
    acc = getAcc()
    print("Funding")

    fundMe.fund({"from": acc, "value": 50000000000000000})


def withdraw():
    fundMe = FundMe[-1]
    acc = getAcc()
    fundMe.withdraw({"from": acc})


def main():
    # fund()
    withdraw()
