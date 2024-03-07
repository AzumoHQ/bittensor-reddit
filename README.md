<div align="center">

# **Reddit Scrapper with Bittensor POC** <!-- omit in toc -->
</div>

- [Introduction](#introduction)
    - [Project scope](#project-scope)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
  - [Before you proceed](#before-you-proceed)
- [License](#license)

---

## Introduction

**IMPORTANT**: If you are new to Bittensor subnets, read this section before proceeding to [Installation](#installation) section. 

The Bittensor blockchain hosts multiple self-contained incentive mechanisms called **subnets**. Subnets are playing fields in which:
- Subnet miners who produce value, and
- Subnet validators who produce consensus

determine together the proper distribution of TAO for the purpose of incentivizing the creation of value, i.e., generating digital commodities, such as intelligence or data. 

Each subnet consists of:
- Subnet miners and subnet validators.
- A protocol using which the subnet miners and subnet validators interact with one another. This protocol is part of the incentive mechanism.
- The Bittensor API using which the subnet miners and subnet validators interact with Bittensor's onchain consensus engine [Yuma Consensus](https://bittensor.com/documentation/validating/yuma-consensus). The Yuma Consensus is designed to drive these actors: subnet validators and subnet miners, into agreement on who is creating value and what that value is worth. 

This project is split into three primary files. These files are:
1. `template/protocol.py`: Contains the definition of the protocol used by subnet miners and subnet validators.
2. `neurons/miner.py`: Script that defines the subnet miner's behavior, i.e., how the subnet miner responds to requests from subnet validators.
3. `neurons/validator.py`: This script defines the subnet validator's behavior, i.e., how the subnet validator requests information from the subnet miners and determines the scores.

### Project scope
This project is intended to be a POC of a Reddit scrapper service on Bittensor, so it's function and features are limited to only search and return metadata of subreddits posts and some top level comments for each post.

While this POC lacks the capability to search keywords for specific posts you may specify which subreddit to obtain the results from when running the  `template/client.py` script with the `--subreddit` flag and the number of posts may vary but a max amount can be specified with the `--limit` flag, aditionally you may filter the category the results are coming from using the `--category` flag (category options are limited to `hot`, `new`, `rising` and `random_rising`).

## Prerequisites

Before proceeding further, make sure that you have installed Bittensor. See the below instructions:

- [Install `bittensor`](https://github.com/opentensor/bittensor#install).

After installing `bittensor`, proceed as below:

### 1. Install Substrate dependencies

Begin by installing the required dependencies for running a Substrate node.

Update your system packages:

```bash
sudo apt update 
```

Install additional required libraries and tools

```bash
sudo apt install --assume-yes make build-essential git clang curl libssl-dev llvm libudev-dev protobuf-compiler
```

### 2. Install Rust and Cargo

Rust is the programming language used in Substrate development. Cargo is Rust package manager.

Install rust and cargo:

```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

Update your shell's source to include Cargo's path:

```bash
source "$HOME/.cargo/env"
```

### 3. Clone the subtensor repository

This step fetches the subtensor codebase to your local machine.

```bash
git clone https://github.com/opentensor/subtensor.git
```

### 4. Setup Rust

This step ensures that you have the nightly toolchain and the WebAssembly (wasm) compilation target. Note that this step will run the subtensor chain on your terminal directly, hence we advise that you run this as a background process using PM2 or other software.

Update to the nightly version of Rust:

```bash
./subtensor/scripts/init.sh
```

### 5. Initialize 

These steps initialize your local subtensor chain in development mode. These commands will set up and run a local subtensor.

Build the binary with the faucet feature enabled:

```bash
cargo build --release --features pow-faucet
```

**NOTE**: The `--features pow-faucet` option in the above is required if we want to use the command `btcli wallet faucet` [See the below Mint tokens step](#8-mint-tokens-from-faucet).

Next, run the localnet script and turn off the attempt to build the binary (as we have already done this above):

```bash
BUILD_BINARY=0 ./scripts/localnet.sh 
```

**NOTE**: Watch for any build or initialization outputs in this step. If you are building the project for the first time, this step will take a while to finish building, depending on your hardware.

## Installation

### Before you proceed
Before you proceed with the installation of the subnet, note the following: 

- This project is a proof of concept, is limited to only scrape information of subreddit posts and comments using `praw` to interact with reddit's API, aditional features may be added in the future.
- Use these instructions to run your subnet locally for your development and testing.
- **IMPORTANT**: We **strongly recommend** that you first run your subnet locally and complete your development and testing before running the subnet on Bittensor testnet. Furthermore, make sure that you run your subnet on Bittensor testnet before running it on the Bittensor mainnet.
- You can run your subnet either as a subnet owner, or as a subnet validator or as a subnet miner. 
- **IMPORTANT:** Make sure you are aware of the minimum compute requirements for your subnet. See the [Minimum compute YAML configuration](./min_compute.yml).
- Note that installation instructions differ based on your situation: For example, installing for local development and testing will require a few additional steps compared to installing for testnet. Similarly, installation instructions differ for a subnet owner vs a validator or a miner.
- This project was tested on WSL2 with Ubuntu and Bittensor version 6.8.2.

---
### 1. Set up environment variables

Set up the following variables with the corresponding values from your reddit application:
```bash
CLIENT_ID
CLIENT_SECRET
```

To create a reddit app, follow the instructions [here https://reddit.com/prefs/apps/](https://www.reddit.com/prefs/apps/)


### 2. Set up wallets

You will need wallets for the different roles, i.e., subnet owner, subnet validator and subnet miner, in the subnet. 

- The owner wallet creates and controls the subnet. 
- The validator and miner will be registered to the subnet created by the owner. This ensures that the validator and miner can run the respective validator and miner scripts.

Create a coldkey for the owner role:

```bash
btcli wallet new_coldkey --wallet.name owner
```

Set up the miner's wallets:

```bash
btcli wallet new_coldkey --wallet.name miner
```

```bash
btcli wallet new_hotkey --wallet.name miner --wallet.hotkey default
```

Set up the validator's wallets:

```bash
btcli wallet new_coldkey --wallet.name validator
```
```bash
btcli wallet new_hotkey --wallet.name validator --wallet.hotkey default
```

### 3. Mint tokens from faucet

You will need tokens to initialize the intentive mechanism on the chain as well as for registering the subnet. 

Run the following commands to mint faucet tokens for the owner and for the validator.

Mint faucet tokens for the owner (you need at least 1000 this may take multiple tries):

```bash
btcli wallet faucet --wallet.name owner --subtensor.chain_endpoint ws://127.0.0.1:9946 
```

You will see:

```bash
>> Balance: τ0.000000000 ➡ τ100.000000000
```

Mint tokens for the validator:

```bash
btcli wallet faucet --wallet.name validator --subtensor.chain_endpoint ws://127.0.0.1:9946 
```

You will see:

```bash
>> Balance: τ0.000000000 ➡ τ100.000000000
```

Mint tokens for the miner:

```bash
btcli wallet faucet --wallet.name miner --subtensor.chain_endpoint ws://127.0.0.1:9946 
```

You will see:

```bash
>> Balance: τ0.000000000 ➡ τ100.000000000
```

### 4. Create a subnet

The below commands establish a new subnet on the local chain. The cost will be exactly τ1000.000000000 for the first subnet you create and you'll have to run the faucet several times to get enough tokens.

```bash
btcli subnet create --wallet.name owner --subtensor.chain_endpoint ws://127.0.0.1:9946 
```

You will see:

```bash
>> Your balance is: τ200.000000000
>> Do you want to register a subnet for τ1000.000000000? [y/n]: 
>> Enter password to unlock key: [YOUR_PASSWORD]
>> ✅ Registered subnetwork with netuid: 1
```

**NOTE**: The local chain will now have a default `netuid` of 1. The second registration will create a `netuid` 2 and so on, until you reach the subnet limit of 8. If you register more than 8 subnets, then a subnet with the least staked TAO will be replaced by the 9th subnet you register.

### 5. Register keys

Register your subnet validator and subnet miner on the subnet. This gives your two keys unique slots on the subnet. The subnet has a current limit of 128 slots.

Register the subnet miner:

```bash
btcli subnet register --wallet.name miner --wallet.hotkey default --subtensor.chain_endpoint ws://127.0.0.1:9946
```

Follow the below prompts:

```bash
>> Enter netuid [1] (1): 1
>> Continue Registration? [y/n]: y
>> ✅ Registered
```

Register the subnet validator:

```bash

btcli subnet register --wallet.name validator --wallet.hotkey default --subtensor.chain_endpoint ws://127.0.0.1:9946
```

Follow the below prompts:

```
>> Enter netuid [1] (1): 1
>> Continue Registration? [y/n]: y
>> ✅ Registered
```

### 6. Add stake 

This step bootstraps the incentives on your new subnet by adding stake into its incentive mechanism.

```bash
btcli stake add --wallet.name validator --wallet.hotkey default --subtensor.chain_endpoint ws://127.0.0.1:9946
```

Follow the below prompts:

```bash
>> Stake all Tao from account: 'validator'? [y/n]: y
>> Stake:
    τ0.000000000 ➡ τ100.000000000
```

### 7. Run subnet miner and subnet validator

Run the subnet miner and subnet validator. Make sure to specify your subnet parameters.

Run the subnet miner:

```bash
python neurons/miner.py --netuid 1 --subtensor.chain_endpoint ws://127.0.0.1:9946 --wallet.name miner --wallet.hotkey default --logging.debug
```

Run the subnet validator:

```bash
python neurons/validator.py --netuid 1 --subtensor.chain_endpoint ws://127.0.0.1:9946 --wallet.name validator --wallet.hotkey default --logging.debug
```

### 8. Run client

You may modify the client parameters to test and obtain diferent results:

```bash
python template/client.py --subreddit test --category new --limit 10 --netuid 1 --wallet_name miner --hotkey default --network ws://127.0.0.1:9946 --uid 1
```

This will search the subreddit `test` on the category `new` and it will bring a maximum of 10 results, the result will be printed on the console. A breakdown of the output can be found on `neurons/reddit_data.py` on the functions `comment_to_dict` and `submission_to_dict`

---

## License
This repository is licensed under the MIT License and BSD 3-Clause License.
```text
# The MIT License (MIT)
# Copyright © 2023 Yuma Rao

# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
# documentation files (the “Software”), to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all copies or substantial portions of
# the Software.

# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
# THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.
```

```text
# BSD 3-Clause License
# Copyright 2024 Azumo LLC

# Redistribution and use in source and binary forms, with or without modification, are permitted
# provided that the following conditions are met:

#     1. Redistributions of source code must retain the above copyright notice, this list of
#     conditions and the following disclaimer.
#     2. Redistributions in binary form must reproduce the above copyright notice, this list of
#     conditions and the following disclaimer in the documentation and/or other materials
#     provided with the distribution.
#     3. Neither the name of the copyright holder nor the names of its contributors may be used to
#     endorse or promote products derived from this software without specific prior written
#     permission.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
# IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
```