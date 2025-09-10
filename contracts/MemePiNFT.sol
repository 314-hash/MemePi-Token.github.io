// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

interface IERC20 {
    function balanceOf(address account) external view returns (uint256);
}

contract MemePiNFT is ERC721, Ownable {
    uint256 private _nextId;
    mapping(address => bool) public minters;
    mapping(address => uint256) public mintedCount; // how many NFTs each address minted

    IERC20 public immutable mepi;
    uint256 public constant UNIT = 10_000 ether; // 10,000 MEPI (with 18 decimals)

    event MinterUpdated(address indexed account, bool allowed);

    constructor()
        ERC721("MemePi NFT", "MPNFT")
        Ownable(0xd6bd8e730b4aeF3D2AdAf282623341E9B99D6AdB) // your wallet as contract owner
    {
        _nextId = 1;
        // ✅ Correct checksummed MEPI token address
        mepi = IERC20(0x746F0F67a6FB3c7362De547ce3249F37a138A128);
    }

    modifier onlyMinter() {
        require(minters[msg.sender] || owner() == msg.sender, "not minter");
        _;
    }

    function setMinter(address account, bool allowed) external onlyOwner {
        minters[account] = allowed;
        emit MinterUpdated(account, allowed);
    }

    /// @notice Mint NFTs by holding MEPI
    /// - 1 NFT for every 10,000 MEPI tokens held
    /// - Example: 25,000 MEPI = 2 NFTs max
    function mintByHolding() external {
        uint256 balance = mepi.balanceOf(msg.sender);
        uint256 eligible = balance / UNIT; // total NFTs wallet is entitled to
        uint256 alreadyMinted = mintedCount[msg.sender];

        require(eligible > alreadyMinted, "No more NFTs available to mint");

        uint256 id = _nextId++;
        _safeMint(msg.sender, id);

        mintedCount[msg.sender] += 1;
    }

    /// @notice Controlled mint (for rewards, staking, etc.)
    function mintReward(address to) external onlyMinter {
        uint256 id = _nextId++;
        _safeMint(to, id);
    }

    /// @notice Owner can mint NFTs anytime
    function ownerMint(address to) external onlyOwner {
        uint256 id = _nextId++;
        _safeMint(to, id);
    }
}
