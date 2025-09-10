// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

interface IERC20 {
    function balanceOf(address account) external view returns (uint256);
}

contract MemePiNFTFlexibleMetadata is ERC721URIStorage, Ownable {
    uint256 private _nextId;
    mapping(address => bool) public minters;
    mapping(address => uint256) public mintedCount;

    IERC20 public immutable mepi;
    uint256 public constant UNIT = 10_000 ether; // 10,000 MEPI = 1 NFT

    event MinterUpdated(address indexed account, bool allowed);

    constructor()
        ERC721("MemePi NFT", "MPNFT")
        Ownable(0xd6bd8e730b4aeF3D2AdAf282623341E9B99D6AdB) // your wallet
    {
        _nextId = 1;
        mepi = IERC20(0x746F0F67a6FB3c7362De547ce3249F37a138A128); // ✅ Checksummed
    }

    modifier onlyMinter() {
        require(minters[msg.sender] || owner() == msg.sender, "not minter");
        _;
    }

    function setMinter(address account, bool allowed) external onlyOwner {
        minters[account] = allowed;
        emit MinterUpdated(account, allowed);
    }

    /// @notice Mint NFTs by holding MEPI (choose amount) with unique metadata
    /// @param amount Number of NFTs to mint
    /// @param uris Array of IPFS/Arweave URIs for each NFT
    function mintByHolding(uint256 amount, string[] memory uris) external {
        require(amount > 0, "Amount must be > 0");
        require(uris.length == amount, "URIs length mismatch");

        uint256 balance = mepi.balanceOf(msg.sender);
        uint256 eligible = balance / UNIT;
        uint256 alreadyMinted = mintedCount[msg.sender];

        require(alreadyMinted + amount <= eligible, "Mint exceeds entitlement");

        for (uint256 i = 0; i < amount; i++) {
            uint256 id = _nextId++;
            _safeMint(msg.sender, id);
            _setTokenURI(id, uris[i]);
        }

        mintedCount[msg.sender] += amount;
    }

    /// @notice Controlled mint (for rewards, staking, etc.)
    function mintReward(address to, string memory uri) external onlyMinter {
        uint256 id = _nextId++;
        _safeMint(to, id);
        _setTokenURI(id, uri);
    }

    /// @notice Owner mint with custom metadata
    function ownerMint(address to, string memory uri) external onlyOwner {
        uint256 id = _nextId++;
        _safeMint(to, id);
        _setTokenURI(id, uri);
    }
}
