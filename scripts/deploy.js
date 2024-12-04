const hre = require("hardhat");

async function main() {
  try {
    console.log("Starting deployment process...");
    
    // Get the contract factory
    console.log("Getting contract factory...");
    const MemePiToken = await hre.ethers.getContractFactory("MemePiToken");
    
    // Get the deployer's address
    const [deployer] = await hre.ethers.getSigners();
    console.log("Deploying contracts with account:", deployer.address);
    
    // Get account balance
    const balance = await hre.ethers.provider.getBalance(deployer.address);
    console.log("Account balance:", balance.toString());
    
    // Get marketing wallet from env
    const marketingWallet = process.env.MARKETING_WALLET_ADDRESS;
    console.log("Marketing wallet address:", marketingWallet);
    
    // Deploy the contract
    console.log("Deploying MemePiToken...");
    const token = await MemePiToken.deploy(marketingWallet);
    console.log("Waiting for deployment transaction...");
    
    // Wait for deployment
    await token.waitForDeployment();
    const deployedAddress = await token.getAddress();
    console.log("MemePiToken deployed to:", deployedAddress);
    
    // Wait for block confirmations
    const receipt = await token.deploymentTransaction().wait(6);
    console.log("Deployment confirmed in block:", receipt.blockNumber);
    
    // Verify contract
    console.log("Verifying contract on Optimistic Etherscan...");
    try {
      await hre.run("verify:verify", {
        address: deployedAddress,
        constructorArguments: [marketingWallet],
        network: "optimism"
      });
      console.log("Contract verified successfully!");
    } catch (verifyError) {
      console.log("Verification error:", verifyError.message);
      if (verifyError.message.includes("Already Verified")) {
        console.log("Contract was already verified!");
      } else {
        throw verifyError;
      }
    }
    
    // Final deployment info
    console.log("\nDeployment Summary:");
    console.log("-------------------");
    console.log("Token Address:", deployedAddress);
    console.log("Marketing Wallet:", marketingWallet);
    console.log("Deployer Address:", deployer.address);
    console.log("Transaction Hash:", token.deploymentTransaction().hash);
    console.log("Network:", hre.network.name);
    
  } catch (error) {
    console.error("\nDeployment failed!");
    console.error("Error details:", error);
    process.exit(1);
  }
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
