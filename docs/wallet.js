// Wallet connection functionality
const walletConnectors = {
    metamask: {
        name: 'MetaMask',
        icon: 'fa-fox',
        checkAvailability: () => typeof window.ethereum !== 'undefined' && window.ethereum.isMetaMask,
        connect: async () => {
            try {
                const accounts = await window.ethereum.request({ method: 'eth_requestAccounts' });
                return accounts[0];
            } catch (error) {
                throw new Error('MetaMask connection failed');
            }
        }
    },
    binance: {
        name: 'Binance Wallet',
        icon: 'fa-coins',
        checkAvailability: () => typeof window.BinanceChain !== 'undefined',
        connect: async () => {
            try {
                const accounts = await window.BinanceChain.request({ method: 'eth_requestAccounts' });
                return accounts[0];
            } catch (error) {
                throw new Error('Binance Wallet connection failed');
            }
        }
    },
    okx: {
        name: 'OKX Wallet',
        icon: 'fa-wallet',
        checkAvailability: () => typeof window.okxwallet !== 'undefined',
        connect: async () => {
            try {
                const accounts = await window.okxwallet.request({ method: 'eth_requestAccounts' });
                return accounts[0];
            } catch (error) {
                throw new Error('OKX Wallet connection failed');
            }
        }
    }
};

let currentWalletAddress = null;

async function connectWallet(walletType) {
    try {
        const wallet = walletConnectors[walletType];
        if (!wallet) {
            throw new Error('Unsupported wallet type');
        }

        if (!wallet.checkAvailability()) {
            window.open(getWalletInstallUrl(walletType), '_blank');
            return;
        }

        const address = await wallet.connect();
        currentWalletAddress = address;
        updateWalletUI(address, walletType);
        
        // Show success message
        showNotification('Wallet Connected!', `Connected to ${wallet.name}`, 'success');
        
        // Update all wallet buttons
        updateAllWalletButtons();
        
    } catch (error) {
        showNotification('Connection Failed', error.message, 'error');
    }
}

function getWalletInstallUrl(walletType) {
    const urls = {
        metamask: 'https://metamask.io/download/',
        binance: 'https://www.bnbchain.org/en/wallet-direct',
        okx: 'https://www.okx.com/web3'
    };
    return urls[walletType] || '';
}

function updateWalletUI(address, walletType) {
    const walletInfo = document.getElementById('wallet-info');
    const shortAddress = `${address.substring(0, 6)}...${address.substring(address.length - 4)}`;
    
    walletInfo.innerHTML = `
        <div class="flex items-center space-x-2">
            <i class="fas ${walletConnectors[walletType].icon}"></i>
            <span>${shortAddress}</span>
            <button onclick="disconnectWallet()" class="text-sm text-red-400 hover:text-red-300">
                <i class="fas fa-sign-out-alt"></i>
            </button>
        </div>
    `;
}

function updateAllWalletButtons() {
    const walletButtons = document.querySelectorAll('.wallet-connect-btn');
    walletButtons.forEach(button => {
        if (currentWalletAddress) {
            button.disabled = true;
            button.classList.add('opacity-50', 'cursor-not-allowed');
        } else {
            button.disabled = false;
            button.classList.remove('opacity-50', 'cursor-not-allowed');
        }
    });
}

function disconnectWallet() {
    currentWalletAddress = null;
    const walletInfo = document.getElementById('wallet-info');
    walletInfo.innerHTML = '';
    updateAllWalletButtons();
    showNotification('Wallet Disconnected', 'Your wallet has been disconnected', 'info');
}

function showNotification(title, message, type) {
    const notification = document.createElement('div');
    notification.className = `fixed top-4 right-4 p-4 rounded-lg shadow-lg z-50 ${
        type === 'success' ? 'bg-green-500' :
        type === 'error' ? 'bg-red-500' :
        'bg-blue-500'
    }`;
    
    notification.innerHTML = `
        <div class="flex items-center space-x-2">
            <i class="fas ${
                type === 'success' ? 'fa-check-circle' :
                type === 'error' ? 'fa-exclamation-circle' :
                'fa-info-circle'
            }"></i>
            <div>
                <h4 class="font-bold">${title}</h4>
                <p class="text-sm">${message}</p>
            </div>
        </div>
    `;
    
    document.body.appendChild(notification);
    setTimeout(() => {
        notification.remove();
    }, 3000);
}
