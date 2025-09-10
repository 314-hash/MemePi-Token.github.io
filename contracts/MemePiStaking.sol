// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

interface IERC20 {
    function transfer(address to, uint256 amount) external returns (bool);
    function transferFrom(address from,address to,uint256 amount) external returns (bool);
    function balanceOf(address account) external view returns (uint256);
    function approve(address spender, uint256 amount) external returns (bool);
}

interface IMemePiNFT {
    function mintReward(address to) external;
}

contract MemePiStaking {
    IERC20 public immutable mepi;
    IMemePiNFT public immutable nftContract;
    address public owner;

    uint256 public rewardRatePerTokenPerSecond; // reward amount (MEPI wei) per 1 token-per-second
    uint256 public totalStaked;
    bool public paused;

    struct UserInfo {
        uint256 staked;
        uint256 rewardDebt; // rewards already accounted for
        uint256 lastUpdate; // timestamp of last update
        uint256 lifetimeStaked; // total ever staked (for NFT thresholds)
    }

    mapping(address => UserInfo) public users;

    // NFT thresholds (lifetime staked amounts) - owner configurable
    uint256[] public nftThresholds;

    event Staked(address indexed user, uint256 amount);
    event Withdrawn(address indexed user, uint256 amount);
    event RewardClaimed(address indexed user, uint256 amount);
    event RewardRateUpdated(uint256 oldRate, uint256 newRate);
    event NFTContractUpdated(address oldAddr, address newAddr);
    event Paused(bool paused);
    event NFTMinted(address indexed to, uint256 threshold);

    modifier onlyOwner() {
        require(msg.sender == owner, "only owner");
        _;
    }

    modifier notPaused() {
        require(!paused, "paused");
        _;
    }

    constructor(address _mepi, address _nftContract, uint256 _rewardRatePerTokenPerSecond) {
        require(_mepi != address(0), "zero mepi");
        owner = msg.sender;
        mepi = IERC20(_mepi);
        nftContract = IMemePiNFT(_nftContract);
        rewardRatePerTokenPerSecond = _rewardRatePerTokenPerSecond;
        // default thresholds example (in wei units of MEPI): 1k, 10k, 100k tokens
        nftThresholds = [1000 ether, 10_000 ether, 100_000 ether];
    }

    // update reward rate (wei per token per second)
    function setRewardRate(uint256 newRate) external onlyOwner {
        emit RewardRateUpdated(rewardRatePerTokenPerSecond, newRate);
        rewardRatePerTokenPerSecond = newRate;
    }

    function setNftThresholds(uint256[] calldata thresholds) external onlyOwner {
        delete nftThresholds;
        for (uint i = 0; i < thresholds.length; ++i) nftThresholds.push(thresholds[i]);
    }

    function pause(bool p) external onlyOwner {
        paused = p;
        emit Paused(p);
    }

    // helper view: pending rewards for user
    function pendingRewards(address userAddr) public view returns (uint256) {
        UserInfo memory u = users[userAddr];
        if (u.staked == 0) return 0;
        uint256 timeDelta = block.timestamp - u.lastUpdate;
        uint256 pending = (u.staked * rewardRatePerTokenPerSecond * timeDelta) / 1 ether;
        return pending;
    }

    // stake MEPI (user must approve mepi -> this contract)
    function stake(uint256 amount) external notPaused {
        require(amount > 0, "zero");
        UserInfo storage u = users[msg.sender];
        // settle pending rewards into rewardDebt (conceptual)
        uint256 pending = pendingRewards(msg.sender);
        if (pending > 0) {
            // send pending rewards immediately in MEPI (funds must exist in contract)
            require(mepi.transfer(msg.sender, pending), "reward transfer failed");
            emit RewardClaimed(msg.sender, pending);
        }
        // transfer staked tokens into contract
        require(mepi.transferFrom(msg.sender, address(this), amount), "transferFrom failed");
        u.staked += amount;
        u.lifetimeStaked += amount;
        u.lastUpdate = block.timestamp;
        totalStaked += amount;
        emit Staked(msg.sender, amount);

        // check NFT thresholds and mint (owner can set nftContract to this staking contract's constructor)
        for (uint i = 0; i < nftThresholds.length; ++i) {
            if (u.lifetimeStaked >= nftThresholds[i]) {
                // Attempt to mint for each threshold once; real implementation should track minted tiers to avoid repeat mints
                // For safety: the NFT contract should handle duplicate prevention or this contract enhanced to mark minted tiers.
                try nftContract.mintReward(msg.sender) {
                    emit NFTMinted(msg.sender, nftThresholds[i]);
                } catch {
                    // If NFT mint fails, do not revert staking
                }
            }
        }
    }

    // withdraw staked tokens and claim rewards
    function withdraw(uint256 amount) external notPaused {
        UserInfo storage u = users[msg.sender];
        require(amount > 0 && u.staked >= amount, "invalid amount");
        uint256 pending = pendingRewards(msg.sender);
        if (pending > 0) {
            require(mepi.transfer(msg.sender, pending), "reward transfer failed");
            emit RewardClaimed(msg.sender, pending);
        }
        u.staked -= amount;
        u.lastUpdate = block.timestamp;
        totalStaked -= amount;
        require(mepi.transfer(msg.sender, amount), "stake return failed");
        emit Withdrawn(msg.sender, amount);
    }

    // claim without withdrawing
    function claim() external notPaused {
        UserInfo storage u = users[msg.sender];
        uint256 pending = pendingRewards(msg.sender);
        require(pending > 0, "no rewards");
        u.lastUpdate = block.timestamp;
        require(mepi.transfer(msg.sender, pending), "reward transfer failed");
        emit RewardClaimed(msg.sender, pending);
    }

    // admin: fund contract with MEPI reward tokens
    function fund(uint256 amount) external onlyOwner {
        require(mepi.transferFrom(msg.sender, address(this), amount), "fund failed");
    }

    // getters used by Governance
    function stakeOf(address account) external view returns (uint256) {
        return users[account].staked;
    }
}

