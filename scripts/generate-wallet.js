const ethers = require('ethers');

async function main() {
    // Generate a new random wallet
    const wallet = ethers.Wallet.createRandom();
    
    console.log("\n=== IMPORTANT: SAVE THIS INFORMATION SECURELY ===");
    console.log("\nNew Wallet Generated:");
    console.log("Address:", wallet.address);
    console.log("Private Key:", wallet.privateKey);
    console.log("Mnemonic:", wallet.mnemonic.phrase);
    
    console.log("\n⚠️  SECURITY INSTRUCTIONS ⚠️");
    console.log("1. Save the mnemonic phrase in a secure location (NOT on your computer)");
    console.log("2. Never share your private key or mnemonic with anyone");
    console.log("3. Send only the required ETH to this address for deployment");
    console.log("4. After deployment, transfer any remaining ETH to a secure wallet");
}

main()
    .then(() => process.exit(0))
    .catch((error) => {
        console.error(error);
        process.exit(1);
    });
