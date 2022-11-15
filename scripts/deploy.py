from brownie import FundMe, accounts, network, config, MockV3Aggregator
from scripts.helpfulScripts import getAcc, deployMocks, LOCAL_ENV
from web3 import Web3


def deployFundMe():
    acc = getAcc()

    if network.show_active() not in LOCAL_ENV:
        print(network.show_active())
        priceFeedAddr = config["networks"][network.show_active()]["eth_usd_priceFeed"]
    else:
        deployMocks()
        priceFeedAddr = MockV3Aggregator[-1].address

    fundMe = FundMe.deploy(
        priceFeedAddr,
        {"from": acc},
        publish_source=config["networks"][network.show_active()].get("verify"),
    )
    print(f"Contract deployed to {fundMe.address}")
    return fundMe


def main():
    deployFundMe()
