// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/token/ERC20/extensions/ERC20Burnable.sol";
import "@openzeppelin/contracts/security/Pausable.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

/**
 * @title MemePi Token
 * @dev Implementation of the MemePi Token
 * @custom:security-contact security@memepi.io
 */
contract MemePiToken is ERC20, ERC20Burnable, Pausable, Ownable {
    // Constants
    uint256 public constant MAX_SUPPLY = 314_159_265 * 10**18; // π hundred million tokens
    uint256 public constant BURN_RATE = 200; // 2% burn rate
    uint256 public constant MARKETING_RATE = 100; // 1% marketing fee
    
    // State variables
    address public marketingWallet;
    mapping(address => bool) public isExcludedFromFees;
    
    // Events
    event MarketingWalletUpdated(address indexed previousWallet, address indexed newWallet);
    event ExcludedFromFees(address indexed account, bool isExcluded);
    event TokensBurned(address indexed from, uint256 amount);
    event MarketingFeeCollected(address indexed from, address indexed to, uint256 amount);

    /**
     * @dev Constructor that gives msg.sender all of initial supply.
     * @param _marketingWallet Address where marketing fees will be sent
     */
    constructor(address _marketingWallet) ERC20("MemePi Token", "MEPI") {
        require(_marketingWallet != address(0), "Marketing wallet cannot be zero address");
        marketingWallet = _marketingWallet;
        
        // Mint initial supply to deployer
        _mint(msg.sender, MAX_SUPPLY);
        
        // Exclude owner and this contract from fees
        isExcludedFromFees[owner()] = true;
        isExcludedFromFees[address(this)] = true;
    }

    /**
     * @dev Updates the marketing wallet address.
     * @param newWallet New address for the marketing wallet
     */
    function setMarketingWallet(address newWallet) external onlyOwner {
        require(newWallet != address(0), "New wallet cannot be zero address");
        emit MarketingWalletUpdated(marketingWallet, newWallet);
        marketingWallet = newWallet;
    }

    /**
     * @dev Excludes an account from paying fees.
     * @param account Address to be excluded/included
     * @param excluded Boolean indicating if the account should be excluded
     */
    function setExcludedFromFees(address account, bool excluded) external onlyOwner {
        require(account != address(0), "Cannot set zero address");
        isExcludedFromFees[account] = excluded;
        emit ExcludedFromFees(account, excluded);
    }

    /**
     * @dev Pauses all token transfers.
     * Can only be called by the contract owner.
     */
    function pause() public onlyOwner {
        _pause();
    }

    /**
     * @dev Unpauses all token transfers.
     * Can only be called by the contract owner.
     */
    function unpause() public onlyOwner {
        _unpause();
    }

    /**
     * @dev Hook that is called before any transfer of tokens.
     * Implements the burn and marketing fee logic.
     */
    function _beforeTokenTransfer(
        address from,
        address to,
        uint256 amount
    ) internal virtual override {
        super._beforeTokenTransfer(from, to, amount);
        require(!paused(), "Token transfer while paused");
    }

    /**
     * @dev Hook that is called after any transfer of tokens.
     * Implements the burn and marketing fee logic.
     */
    function _afterTokenTransfer(
        address from,
        address to,
        uint256 amount
    ) internal virtual override {
        super._afterTokenTransfer(from, to, amount);

        // Skip fees for excluded accounts or minting/burning
        if (isExcludedFromFees[from] || isExcludedFromFees[to] || 
            from == address(0) || to == address(0)) {
            return;
        }

        // Calculate fees
        uint256 burnAmount = (amount * BURN_RATE) / 10000;
        uint256 marketingAmount = (amount * MARKETING_RATE) / 10000;

        // Burn tokens
        if (burnAmount > 0) {
            _burn(to, burnAmount);
            emit TokensBurned(to, burnAmount);
        }

        // Transfer marketing fee
        if (marketingAmount > 0) {
            _transfer(to, marketingWallet, marketingAmount);
            emit MarketingFeeCollected(to, marketingWallet, marketingAmount);
        }
    }
}
