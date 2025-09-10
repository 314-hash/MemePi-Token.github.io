// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

/// @title MemePi NFT with Metadata (Max 5 Supply)
/// @notice A collection of max 5 NFTs that can only be minted by MEPI holders.
///         Each 10,000 MEPI tokens held = 1 mintable NFT.
///         Each NFT has unique metadata (IPFS/Arweave/Server-hosted).
contract MemePiNFTWithMetadata is ERC721URIStorage, Ownable {
    IERC20 public immutable mepi;
    uint256 private _nextId;
    string private _baseTokenURI;

    uint256 public constant MAX_SUPPLY = 5; // 🔒 hard cap

    mapping(address => uint256) public mintedCount;

    constructor(address initialOwner)
        ERC721("MemePi NFT", "MPNFT")
        Ownable(initialOwner)
    {
        _nextId = 1;
        // ✅ MemePi token address (checksummed)
        mepi = IERC20(0x746F0F67a6FB3c7362De547ce3249F37a138A128);
    }

    /// @notice Mint NFTs based on MEPI token holdings (up to MAX_SUPPLY)
    /// @param amount number of NFTs to mint
    function mintByHolding(uint256 amount) external {
        require(amount > 0, "Must mint at least one NFT");

        uint256 eligible = mepi.balanceOf(msg.sender) / 10_000 ether;
        require(eligible > 0, "Not enough MEPI to mint");

        require(
            mintedCount[msg.sender] + amount <= eligible,
            "Exceeds mintable NFTs based on MEPI balance"
        );

        require(
            _nextId + amount - 1 <= MAX_SUPPLY,
            "Exceeds max NFT supply"
        );

        for (uint256 i = 0; i < amount; i++) {
            uint256 tokenId = _nextId;
            _safeMint(msg.sender, tokenId);

            // Assign unique metadata URI (baseURI + tokenId.json)
            string memory tokenURI_ = string(
                abi.encodePacked(_baseTokenURI, _toString(tokenId), ".json")
            );
            _setTokenURI(tokenId, tokenURI_);

            _nextId++;
        }

        mintedCount[msg.sender] += amount;
    }

    /// @notice Returns how many NFTs a user can still mint (bounded by MAX_SUPPLY)
    function remainingMints(address user) external view returns (uint256) {
        uint256 eligible = mepi.balanceOf(user) / 10_000 ether;
        uint256 available = eligible - mintedCount[user];
        uint256 remainingSupply = MAX_SUPPLY - (_nextId - 1);
        return available < remainingSupply ? available : remainingSupply;
    }

    /// @notice Set base URI for metadata (e.g. "ipfs://QmFolderHash/")
    function setBaseURI(string memory baseURI) external onlyOwner {
        _baseTokenURI = baseURI;
    }

    /// @dev Converts uint256 to string (for tokenId URIs)
    function _toString(uint256 value) internal pure returns (string memory) {
        if (value == 0) return "0";
        uint256 temp = value;
        uint256 digits;
        while (temp != 0) {
            digits++;
            temp /= 10;
        }
        bytes memory buffer = new bytes(digits);
        while (value != 0) {
            digits -= 1;
            buffer[digits] = bytes1(uint8(48 + uint256(value % 10)));
            value /= 10;
        }
        return string(buffer);
    }
}
