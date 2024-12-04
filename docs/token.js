// Token details
const TOKEN_CONFIG = {
    tokenAddress: '0x314hash...', // Replace with actual token contract address
    tokenSymbol: 'MEPI',
    tokenDecimals: 18,
    tokenImage: 'https://gateway.pinata.cloud/ipfs/QmeTKApmA3xpAVR5YVU6tEVaw76Hc5uAcTo1Wg7bwhueF3',
    // DEX Configuration
    dexRouter: '0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D', // Uniswap V2 Router
    wethAddress: '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2', // WETH on Ethereum mainnet
    buySlippage: 0.5, // 0.5% slippage tolerance
    gasLimit: 300000 // Default gas limit for swap
};

// Function to add token to MetaMask
async function addTokenToMetaMask() {
    if (typeof window.ethereum === 'undefined') {
        window.open('https://metamask.io/download/', '_blank');
        return;
    }

    try {
        // Request account access
        await window.ethereum.request({ method: 'eth_requestAccounts' });

        // Add token
        const wasAdded = await window.ethereum.request({
            method: 'wallet_watchAsset',
            params: {
                type: 'ERC20',
                options: {
                    address: TOKEN_CONFIG.tokenAddress,
                    symbol: TOKEN_CONFIG.tokenSymbol,
                    decimals: TOKEN_CONFIG.tokenDecimals,
                    image: TOKEN_CONFIG.tokenImage,
                },
            },
        });

        if (wasAdded) {
            showTokenAddedNotification();
        }
    } catch (error) {
        console.error(error);
        showTokenAddError(error.message);
    }
}

// Function to show success notification
function showTokenAddedNotification() {
    const notification = document.createElement('div');
    notification.className = 'fixed top-4 right-4 p-4 bg-green-500 text-white rounded-lg shadow-lg z-50';
    notification.innerHTML = `
        <div class="flex items-center space-x-2">
            <i class="fas fa-check-circle"></i>
            <div>
                <h4 class="font-bold">Success!</h4>
                <p class="text-sm">MEPI Token was added to your MetaMask wallet</p>
            </div>
        </div>
    `;
    document.body.appendChild(notification);
    setTimeout(() => notification.remove(), 3000);
}

// Function to show error notification
function showTokenAddError(message) {
    const notification = document.createElement('div');
    notification.className = 'fixed top-4 right-4 p-4 bg-red-500 text-white rounded-lg shadow-lg z-50';
    notification.innerHTML = `
        <div class="flex items-center space-x-2">
            <i class="fas fa-exclamation-circle"></i>
            <div>
                <h4 class="font-bold">Error</h4>
                <p class="text-sm">Failed to add token: ${message}</p>
            </div>
        </div>
    `;
    document.body.appendChild(notification);
    setTimeout(() => notification.remove(), 3000);
}

// Function to copy token address
function copyTokenAddress() {
    navigator.clipboard.writeText(TOKEN_CONFIG.tokenAddress)
        .then(() => {
            const notification = document.createElement('div');
            notification.className = 'fixed top-4 right-4 p-4 bg-blue-500 text-white rounded-lg shadow-lg z-50';
            notification.innerHTML = `
                <div class="flex items-center space-x-2">
                    <i class="fas fa-copy"></i>
                    <div>
                        <h4 class="font-bold">Copied!</h4>
                        <p class="text-sm">Token address copied to clipboard</p>
                    </div>
                </div>
            `;
            document.body.appendChild(notification);
            setTimeout(() => notification.remove(), 3000);
        })
        .catch(err => console.error('Failed to copy:', err));
}

// Function to buy tokens
async function buyTokens(ethAmount) {
    if (typeof window.ethereum === 'undefined') {
        window.open('https://metamask.io/download/', '_blank');
        return;
    }

    try {
        // Request account access
        const accounts = await window.ethereum.request({ method: 'eth_requestAccounts' });
        const userAddress = accounts[0];

        // Create Web3 instance
        const web3 = new Web3(window.ethereum);
        
        // Initialize router contract
        const routerAbi = [
            'function swapExactETHForTokens(uint amountOutMin, address[] calldata path, address to, uint deadline) external payable returns (uint[] memory amounts)',
            'function getAmountsOut(uint amountIn, address[] calldata path) external view returns (uint[] memory amounts)'
        ];
        const router = new web3.eth.Contract(routerAbi, TOKEN_CONFIG.dexRouter);

        // Calculate minimum tokens to receive
        const path = [TOKEN_CONFIG.wethAddress, TOKEN_CONFIG.tokenAddress];
        const weiAmount = web3.utils.toWei(ethAmount.toString(), 'ether');
        const amounts = await router.methods.getAmountsOut(weiAmount, path).call();
        const minTokens = web3.utils.toBN(amounts[1])
            .mul(web3.utils.toBN(1000 - TOKEN_CONFIG.buySlippage * 10))
            .div(web3.utils.toBN(1000));

        // Prepare transaction
        const deadline = Math.floor(Date.now() / 1000) + 300; // 5 minutes deadline
        const tx = router.methods.swapExactETHForTokens(
            minTokens,
            path,
            userAddress,
            deadline
        );

        // Send transaction
        const gasPrice = await web3.eth.getGasPrice();
        await tx.send({
            from: userAddress,
            value: weiAmount,
            gasLimit: TOKEN_CONFIG.gasLimit,
            gasPrice: gasPrice
        });

        showBuySuccessNotification(ethAmount);
    } catch (error) {
        console.error(error);
        showBuyError(error.message);
    }
}

// Function to show buy success notification
function showBuySuccessNotification(amount) {
    const notification = document.createElement('div');
    notification.className = 'fixed top-4 right-4 p-4 bg-green-500 text-white rounded-lg shadow-lg z-50';
    notification.innerHTML = `
        <div class="flex items-center space-x-2">
            <i class="fas fa-check-circle"></i>
            <div>
                <h4 class="font-bold">Success!</h4>
                <p class="text-sm">Successfully bought MEPI tokens for ${amount} ETH</p>
            </div>
        </div>
    `;
    document.body.appendChild(notification);
    setTimeout(() => notification.remove(), 3000);
}

// Function to show buy error notification
function showBuyError(message) {
    const notification = document.createElement('div');
    notification.className = 'fixed top-4 right-4 p-4 bg-red-500 text-white rounded-lg shadow-lg z-50';
    notification.innerHTML = `
        <div class="flex items-center space-x-2">
            <i class="fas fa-exclamation-circle"></i>
            <div>
                <h4 class="font-bold">Error</h4>
                <p class="text-sm">Failed to buy tokens: ${message}</p>
            </div>
        </div>
    `;
    document.body.appendChild(notification);
    setTimeout(() => notification.remove(), 3000);
}
