import { Networks } from "@stellar/stellar-sdk";

export const STELLAR_NETWORKS = {
  mainnet: {
    name: "Mainnet",
    networkPassphrase: Networks.PUBLIC,
    horizonUrl: "https://horizon.stellar.org",
    sorobanRpcUrl: "https://soroban.stellar.org",
    explorerUrl: "https://stellar.expert/explorer/public",
  },
  testnet: {
    name: "Testnet",
    networkPassphrase: Networks.TESTNET,
    horizonUrl: "https://horizon-testnet.stellar.org",
    sorobanRpcUrl: "https://soroban-testnet.stellar.org",
    explorerUrl: "https://stellar.expert/explorer/testnet",
  },
} as const;

export type StellarNetworkName = keyof typeof STELLAR_NETWORKS;

export const DEFAULT_NETWORK: StellarNetworkName = "testnet";

export const CONTRACT_ID = ""; // Soroban contract ID (deploy pending)

export const MODULE_NAME = "profile";
export const FUNCTION_CREATE_PROFILE = "create_profile";
export const FUNCTION_REGISTER_TREATMENT = "register_treatment";
export const FUNCTION_REGISTER_EVENT = "register_event";

export function getNetwork(name?: StellarNetworkName) {
  return STELLAR_NETWORKS[name ?? DEFAULT_NETWORK];
}

export function getExplorerAccountUrl(address: string, network?: StellarNetworkName) {
  const net = getNetwork(network);
  return `${net.explorerUrl}/account/${address}`;
}

export function getExplorerTxUrl(hash: string, network?: StellarNetworkName) {
  const net = getNetwork(network);
  return `${net.explorerUrl}/tx/${hash}`;
}
