#!/usr/bin/env python3
"""Aplica ortografia brasileira em textos .md pt-BR exportados sem acentos."""
from __future__ import annotations

import re
from pathlib import Path

DOCS = Path(__file__).resolve().parents[1] / "docs"
FILES = ["WHITEPAPER.pt-BR.md", "LITEPAPER.pt-BR.md"]

# Frases / palavras de alta confiança
PHRASE_FIXES = [
    (re.compile(r" e uma\b"), " é uma"),
    (re.compile(r" e um\b"), " é um"),
    (re.compile(r" e o\b"), " é o"),
    (re.compile(r" e criada\b"), " é criada"),
    (re.compile(r" e mais\b"), " é mais"),
    (re.compile(r" não e\b"), " não é"),
    (re.compile(r" Não e\b"), " Não é"),
    (re.compile(r"^E uma\b", re.M), "É uma"),
    (re.compile(r"^E um\b", re.M), "É um"),
    (re.compile(r"^E o\b", re.M), "É o"),
    (re.compile(r"(?<=[.!?])\s+E uma\b"), " É uma"),
    (re.compile(r"(?<=[.!?])\s+E um\b"), " É um"),
    (re.compile(r"\bque e\b"), "que é"),
    (re.compile(r"\bQue e\b"), "Que é"),
    (re.compile(r"\bquando e\b"), "quando é"),
    (re.compile(r" — e linguagem\b"), " — é linguagem"),
    (re.compile(r"\breputação e conquistada pelo\b"), "reputação é conquistada pelo"),
    (re.compile(r"\breputação e conquistada\b"), "reputação é conquistada"),
    (re.compile(r"\bMarco 2026\b"), "Março 2026"),
]

WORD_FIXES = [
    (re.compile(r"\bnao\b"), "não"),
    (re.compile(r"\bNao\b"), "Não"),
    (re.compile(r"\bja\b"), "já"),
    (re.compile(r"\bJa\b"), "Já"),
    (re.compile(r"\bate\b"), "até"),
    (re.compile(r"\bAte\b"), "Até"),
    (re.compile(r"\bha\b"), "há"),
    (re.compile(r"\bHa\b"), "Há"),
    (re.compile(r"\bvoce\b"), "você"),
    (re.compile(r"\bVoce\b"), "Você"),
    (re.compile(r"\bvoces\b"), "vocês"),
    (re.compile(r"\bVoces\b"), "Vocês"),
    (re.compile(r"\busuario\b"), "usuário"),
    (re.compile(r"\bUsuario\b"), "Usuário"),
    (re.compile(r"\busuarios\b"), "usuários"),
    (re.compile(r"\bUsuarios\b"), "Usuários"),
    (re.compile(r"\btambem\b"), "também"),
    (re.compile(r"\bTambem\b"), "Também"),
    (re.compile(r"\balem\b"), "além"),
    (re.compile(r"\bAlem\b"), "Além"),
    (re.compile(r"\bfaca\b"), "faça"),
    (re.compile(r"\bFaca\b"), "Faça"),
    (re.compile(r"\bestao\b"), "estão"),
    (re.compile(r"\bEstao\b"), "Estão"),
    (re.compile(r"\bentao\b"), "então"),
    (re.compile(r"\bEntao\b"), "Então"),
    (re.compile(r"\bporem\b"), "porém"),
    (re.compile(r"\bPorem\b"), "Porém"),
    (re.compile(r"\bsera\b"), "será"),
    (re.compile(r"\bSera\b"), "Será"),
    (re.compile(r"\bserao\b"), "serão"),
    (re.compile(r"\bSerao\b"), "Serão"),
    (re.compile(r"\bpoderao\b"), "poderão"),
    (re.compile(r"\bPoderao\b"), "Poderão"),
    (re.compile(r"\bhavera\b"), "haverá"),
    (re.compile(r"\bsao\b"), "são"),
    (re.compile(r"\bSao\b"), "São"),
]


def _preserve_case(original: str, new_lower: str) -> str:
    if original.isupper():
        return new_lower.upper()
    if original[:1].isupper():
        return new_lower[:1].upper() + new_lower[1:]
    return new_lower


def fix_coes(m: re.Match[str]) -> str:
    g = m.group(1)
    base = g[:-1] + "ções" if g.endswith("c") else g + "ções"
    return _preserve_case(m.group(0), base)


def fix_cao(m: re.Match[str]) -> str:
    g = m.group(1)
    base = g + "ção"
    return _preserve_case(m.group(0), base)


def fix_sao(m: re.Match[str]) -> str:
    g = m.group(1)
    base = g + "são"
    return _preserve_case(m.group(0), base)


def fix_hoes(m: re.Match[str]) -> str:
    g = m.group(1)
    base = g + "ões"
    return _preserve_case(m.group(0), base)


def fix_hao(m: re.Match[str]) -> str:
    g = m.group(1)
    base = g + "hão"
    return _preserve_case(m.group(0), base)


def process(text: str) -> str:
    for rx, rep in PHRASE_FIXES:
        text = rx.sub(rep, text)
    for rx, rep in WORD_FIXES:
        text = rx.sub(rep, text)
    # informacoes -> informações (remove c antes de ções quando ...coes)
    text = re.sub(r"\b([A-Za-zÀ-ÿ]+)coes\b", fix_coes, text)
    # informacao -> informação
    text = re.sub(r"\b([A-Za-zÀ-ÿ]+)cao\b", fix_cao, text)
    # versao, missao -> versão, missão (não terminam em ...cao)
    text = re.sub(r"\b([A-Za-zÀ-ÿ]+)sao\b", fix_sao, text)
    text = re.sub(r"\b([A-Za-zÀ-ÿ]+h)oes\b", fix_hoes, text)
    text = re.sub(r"\b([A-Za-zÀ-ÿ]+)hao\b", fix_hao, text)
    return text


def main() -> None:
    for name in FILES:
        path = DOCS / name
        raw = path.read_text(encoding="utf-8")
        path.write_text(process(raw), encoding="utf-8")
        print("updated", path.name)


if __name__ == "__main__":
    main()
