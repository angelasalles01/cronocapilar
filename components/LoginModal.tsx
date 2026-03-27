"use client";

import { useState, useEffect } from "react";
import { useStellar, formatAddress } from "@/lib/stellar-provider";
import { useI18n } from "@/lib/i18n";
import { getExplorerAccountUrl } from "@/lib/constants";

interface LoginModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export default function LoginModal({ isOpen, onClose }: LoginModalProps) {
  const { language } = useI18n();
  const { account, isFreighterInstalled, connect, disconnect, networkName } = useStellar();
  const [showSuccess, setShowSuccess] = useState(false);
  const [isConnecting, setIsConnecting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (account && isOpen) {
      setShowSuccess(true);
      const timer = setTimeout(() => {
        setShowSuccess(false);
        onClose();
      }, 2000);
      return () => clearTimeout(timer);
    }
  }, [account, isOpen, onClose]);

  if (!isOpen) return null;

  const handleConnect = async () => {
    setIsConnecting(true);
    setError(null);
    try {
      await connect();
    } catch (err: any) {
      setError(err.message || "Connection failed");
    } finally {
      setIsConnecting(false);
    }
  };

  const handleDisconnect = () => {
    disconnect();
    onClose();
  };

  const t = {
    title: language === "pt-BR" ? "Bem-vindo ao CronoCapilar" : language === "en-US" ? "Welcome to CronoCapilar" : "Bienvenido a CronoCapilar",
    description: language === "pt-BR"
      ? "Conecte sua carteira Stellar para registrar tratamentos capilares on-chain."
      : language === "en-US"
      ? "Connect your Stellar wallet to register hair treatments on-chain."
      : "Conecta tu cartera Stellar para registrar tratamientos capilares on-chain.",
    connected: language === "pt-BR" ? "Conectado" : language === "en-US" ? "Connected" : "Conectado",
    disconnectBtn: language === "pt-BR" ? "Desconectar" : language === "en-US" ? "Disconnect" : "Desconectar",
    connectFreighter: language === "pt-BR" ? "Conectar com Freighter" : language === "en-US" ? "Connect with Freighter" : "Conectar con Freighter",
    connecting: language === "pt-BR" ? "Conectando..." : language === "en-US" ? "Connecting..." : "Conectando...",
    noWallet: language === "pt-BR" ? "Freighter não detectado" : language === "en-US" ? "Freighter not detected" : "Freighter no detectado",
    installMsg: language === "pt-BR"
      ? "Instale a extensão Freighter para conectar sua carteira Stellar."
      : language === "en-US"
      ? "Install the Freighter extension to connect your Stellar wallet."
      : "Instala la extensión Freighter para conectar tu cartera Stellar.",
    installBtn: language === "pt-BR" ? "Instalar Freighter" : language === "en-US" ? "Install Freighter" : "Instalar Freighter",
    viewExplorer: language === "pt-BR" ? "Ver no Stellar Expert" : language === "en-US" ? "View on Stellar Expert" : "Ver en Stellar Expert",
    success: language === "pt-BR" ? "Carteira conectada!" : language === "en-US" ? "Wallet connected!" : "Cartera conectada!",
  };

  return (
    <div
      style={{
        position: "fixed", top: 0, left: 0, right: 0, bottom: 0,
        background: "rgba(0,0,0,0.5)", backdropFilter: "blur(4px)",
        display: "flex", alignItems: "center", justifyContent: "center",
        zIndex: 1000, padding: 20,
      }}
      onClick={onClose}
    >
      <div
        style={{
          background: "linear-gradient(135deg, #ffffff 0%, #fdf4f7 100%)",
          borderRadius: 24, padding: 32, maxWidth: 480, width: "100%",
          boxShadow: "0 20px 60px rgba(0,0,0,0.3)",
          border: "1px solid rgba(255,107,157,0.2)",
        }}
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 24 }}>
          <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
            <span style={{ fontSize: 28 }}>💜</span>
            <div>
              <div style={{ fontSize: 12, color: "#667eea", fontWeight: 700, letterSpacing: 1 }}>STELLAR {networkName.toUpperCase()}</div>
            </div>
          </div>
          <button onClick={onClose} style={{ background: "transparent", border: "none", fontSize: 24, cursor: "pointer", color: "#666", padding: "4px 8px", borderRadius: 8 }}>
            ×
          </button>
        </div>

        <h2 style={{ fontSize: 26, fontWeight: 700, margin: "0 0 8px 0", background: "linear-gradient(135deg, #667eea 0%, #ff6b9d 100%)", WebkitBackgroundClip: "text", WebkitTextFillColor: "transparent" }}>
          {t.title}
        </h2>
        <p style={{ fontSize: 14, color: "#666", margin: "0 0 28px 0", lineHeight: 1.6 }}>{t.description}</p>

        {/* Success */}
        {showSuccess && account && (
          <div style={{ background: "linear-gradient(135deg, #2d6a4f 0%, #667eea 100%)", color: "white", padding: "16px 20px", borderRadius: 16, marginBottom: 24, textAlign: "center", fontSize: 15, fontWeight: 600 }}>
            ✅ {t.success}
            <div style={{ fontSize: 11, marginTop: 8, opacity: 0.9, fontFamily: "monospace" }}>{account.address}</div>
          </div>
        )}

        {/* Error */}
        {error && (
          <div style={{ background: "rgba(255,59,48,0.1)", color: "#ff3b30", padding: "12px 16px", borderRadius: 12, marginBottom: 16, fontSize: 13, border: "1px solid rgba(255,59,48,0.2)" }}>
            {error}
          </div>
        )}

        {/* Connected state */}
        {account ? (
          <div>
            <div style={{ background: "linear-gradient(135deg, #667eea 0%, #764ba2 100%)", color: "white", padding: "20px", borderRadius: 16, marginBottom: 16 }}>
              <div style={{ fontSize: 11, opacity: 0.7, marginBottom: 4, fontWeight: 600, letterSpacing: 1 }}>{t.connected}</div>
              <div style={{ fontSize: 13, fontFamily: "monospace", wordBreak: "break-all", lineHeight: 1.5 }}>{account.address}</div>
              <div style={{ marginTop: 12, fontSize: 12, opacity: 0.8 }}>
                Network: <strong>{account.network}</strong>
              </div>
            </div>
            <a
              href={getExplorerAccountUrl(account.address, account.network)}
              target="_blank" rel="noopener noreferrer"
              style={{ display: "block", textAlign: "center", fontSize: 13, color: "#667eea", marginBottom: 16, textDecoration: "none", fontWeight: 600 }}
            >
              🔗 {t.viewExplorer}
            </a>
            <button onClick={handleDisconnect} style={{ width: "100%", padding: "14px", borderRadius: 16, border: "2px solid rgba(102,126,234,0.3)", background: "white", color: "#667eea", fontSize: 15, fontWeight: 600, cursor: "pointer" }}>
              {t.disconnectBtn}
            </button>
          </div>
        ) : (
          <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
            {isFreighterInstalled ? (
              <button
                onClick={handleConnect}
                disabled={isConnecting}
                style={{
                  width: "100%", padding: "18px 20px", borderRadius: 16,
                  border: "none",
                  background: isConnecting ? "#ccc" : "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                  color: "white", fontSize: 16, fontWeight: 700, cursor: isConnecting ? "not-allowed" : "pointer",
                  display: "flex", alignItems: "center", justifyContent: "center", gap: 12,
                  boxShadow: isConnecting ? "none" : "0 8px 24px rgba(102,126,234,0.4)",
                  transition: "all 0.3s",
                }}
              >
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <circle cx="12" cy="12" r="10" stroke="white" strokeWidth="2"/>
                  <path d="M12 6L12 18M6 12L18 12" stroke="white" strokeWidth="2" strokeLinecap="round"/>
                </svg>
                {isConnecting ? t.connecting : t.connectFreighter}
              </button>
            ) : (
              <div style={{ padding: "28px", borderRadius: 16, background: "rgba(102,126,234,0.06)", border: "2px solid rgba(102,126,234,0.15)", textAlign: "center" }}>
                <div style={{ fontSize: 40, marginBottom: 12 }}>⭐</div>
                <div style={{ fontWeight: 700, marginBottom: 8, fontSize: 16, color: "#333" }}>{t.noWallet}</div>
                <p style={{ fontSize: 13, lineHeight: 1.6, color: "#666", marginBottom: 20 }}>{t.installMsg}</p>
                <a
                  href="https://www.freighter.app/"
                  target="_blank" rel="noopener noreferrer"
                  style={{
                    display: "inline-flex", alignItems: "center", gap: 8,
                    padding: "14px 24px", borderRadius: 14,
                    background: "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                    color: "white", fontWeight: 700, fontSize: 14, textDecoration: "none",
                    boxShadow: "0 4px 16px rgba(102,126,234,0.3)",
                  }}
                >
                  ⭐ {t.installBtn}
                </a>
              </div>
            )}

            <div style={{ padding: "10px 16px", borderRadius: 10, background: "rgba(102,126,234,0.05)", fontSize: 11, textAlign: "center", color: "#999", lineHeight: 1.5 }}>
              {language === "pt-BR"
                ? "Freighter é a carteira oficial da Stellar. Seus dados ficam no seu navegador."
                : language === "en-US"
                ? "Freighter is the official Stellar wallet. Your keys stay in your browser."
                : "Freighter es la cartera oficial de Stellar. Tus claves se quedan en tu navegador."}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
