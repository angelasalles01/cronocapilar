"""
Merge ang3la.xyz/papers into docs/ (whitepapers from agent-tools cache; litepapers via HTTP).
Run from cronocapilar/: python scripts/sync_papers_from_ang3la.py
"""
import re
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
AGENT = Path(
    r"C:\Users\cesilva\.cursor\projects\c-Users-cesilva-OneDrive-Protheus-TDS-Pessoal-Stellar-CronoCapilar\agent-tools"
)


def read_agent(name: str) -> str:
    return (AGENT / name).read_text(encoding="utf-8")


def strip_wp_title_block(text: str) -> str:
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if line.strip() == "---" and i >= 6:
            return "\n".join(lines[i:])
    return text


def strip_lp_title_block(text: str) -> str:
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if line.strip() == "---" and i >= 4:
            return "\n".join(lines[i:])
    return text


FOOT_WP_EN = """<p align="center">
  <strong>Built with care on <a href="https://stellar.org/">Stellar</a></strong>
</p>

<p align="center">
  <a href="WHITEPAPER.md">English</a> ·
  <a href="WHITEPAPER.pt-BR.md">Português</a> ·
  <a href="WHITEPAPER.es-ES.md">Español</a>
</p>

<p align="center">
  <a href="LITEPAPER.md">Read the Litepaper</a>
</p>
"""

FOOT_WP_PT = """<p align="center">
  <strong>Feito com cuidado na <a href="https://stellar.org/">Stellar</a></strong>
</p>

<p align="center">
  <a href="WHITEPAPER.md">English</a> ·
  <a href="WHITEPAPER.pt-BR.md">Português</a> ·
  <a href="WHITEPAPER.es-ES.md">Español</a>
</p>

<p align="center">
  <a href="LITEPAPER.pt-BR.md">Leia o Litepaper</a>
</p>
"""

FOOT_WP_ES = """<p align="center">
  <strong>Hecho con cuidado en <a href="https://stellar.org/">Stellar</a></strong>
</p>

<p align="center">
  <a href="WHITEPAPER.md">English</a> ·
  <a href="WHITEPAPER.pt-BR.md">Português</a> ·
  <a href="WHITEPAPER.es-ES.md">Español</a>
</p>

<p align="center">
  <a href="LITEPAPER.es-ES.md">Lee el Litepaper</a>
</p>
"""

FOOT_LP_EN = """<p align="center">
  <strong>Built with care on <a href="https://stellar.org/">Stellar</a></strong>
</p>

<p align="center">
  <a href="LITEPAPER.md">English</a> ·
  <a href="LITEPAPER.pt-BR.md">Português</a> ·
  <a href="LITEPAPER.es-ES.md">Español</a>
</p>

<p align="center">
  <a href="WHITEPAPER.md">Read the full Whitepaper</a>
</p>
"""

FOOT_LP_PT = """<p align="center">
  <strong>Feito com cuidado na <a href="https://stellar.org/">Stellar</a></strong>
</p>

<p align="center">
  <a href="LITEPAPER.md">English</a> ·
  <a href="LITEPAPER.pt-BR.md">Português</a> ·
  <a href="LITEPAPER.es-ES.md">Español</a>
</p>

<p align="center">
  <a href="WHITEPAPER.pt-BR.md">Leia o Whitepaper completo</a>
</p>
"""

FOOT_LP_ES = """<p align="center">
  <strong>Hecho con cuidado en <a href="https://stellar.org/">Stellar</a></strong>
</p>

<p align="center">
  <a href="LITEPAPER.md">English</a> ·
  <a href="LITEPAPER.pt-BR.md">Português</a> ·
  <a href="LITEPAPER.es-ES.md">Español</a>
</p>

<p align="center">
  <a href="WHITEPAPER.es-ES.md">Lee el Whitepaper completo</a>
</p>
"""

HEAD_WP_EN = """<p align="center">
  <img src="https://img.shields.io/badge/Stellar-Built%20on%20Stellar-blue?style=for-the-badge&logo=stellar&logoColor=white" alt="Built on Stellar" />
</p>

<h1 align="center">CronoCapilar — Whitepaper</h1>
<h3 align="center">Proof of Care: A Decentralized Reputation Protocol for Natural Hair Care</h3>

<p align="center">
  <strong>Version 1.0 | March 2026</strong><br/>
  Angela Salles — <a href="https://ang3la.xyz">Ang3la.xyz</a>
</p>

"""

HEAD_WP_PT = """<p align="center">
  <img src="https://img.shields.io/badge/Stellar-Built%20on%20Stellar-blue?style=for-the-badge&logo=stellar&logoColor=white" alt="Built on Stellar" />
</p>

<h1 align="center">CronoCapilar — Whitepaper</h1>
<h3 align="center">Proof of Care: Um Protocolo de Reputacao Descentralizada para Cuidados Capilares Naturais</h3>

<p align="center">
  <strong>Versao 1.0 | Marco 2026</strong><br/>
  Angela Salles — <a href="https://ang3la.xyz">Ang3la.xyz</a>
</p>

"""

HEAD_WP_ES = """<p align="center">
  <img src="https://img.shields.io/badge/Stellar-Built%20on%20Stellar-blue?style=for-the-badge&logo=stellar&logoColor=white" alt="Built on Stellar" />
</p>

<h1 align="center">CronoCapilar — Whitepaper</h1>
<h3 align="center">Proof of Care: Un Protocolo de Reputacion Descentralizada para el Cuidado Capilar Natural</h3>

<p align="center">
  <strong>Version 1.0 | Marzo 2026</strong><br/>
  Angela Salles — <a href="https://ang3la.xyz">Ang3la.xyz</a>
</p>

"""

HEAD_LP_EN = """<p align="center">
  <img src="https://img.shields.io/badge/Stellar-Built%20on%20Stellar-blue?style=for-the-badge&logo=stellar&logoColor=white" alt="Built on Stellar" />
</p>

<h1 align="center">CronoCapilar — Litepaper</h1>
<h3 align="center">Proof of Care: Decentralized Reputation for Natural Hair Care</h3>

<p align="center">
  <strong>Version 1.0 | March 2026</strong><br/>
  Angela Salles — <a href="https://ang3la.xyz">Ang3la.xyz</a>
</p>

"""

HEAD_LP_PT = """<p align="center">
  <img src="https://img.shields.io/badge/Stellar-Built%20on%20Stellar-blue?style=for-the-badge&logo=stellar&logoColor=white" alt="Built on Stellar" />
</p>

<h1 align="center">CronoCapilar — Litepaper</h1>
<h3 align="center">Proof of Care: Reputacao Descentralizada para Cuidados Capilares Naturais</h3>

<p align="center">
  <strong>Versao 1.0 | Marco 2026</strong><br/>
  Angela Salles — <a href="https://ang3la.xyz">Ang3la.xyz</a>
</p>

"""

HEAD_LP_ES = """<p align="center">
  <img src="https://img.shields.io/badge/Stellar-Built%20on%20Stellar-blue?style=for-the-badge&logo=stellar&logoColor=white" alt="Built on Stellar" />
</p>

<h1 align="center">CronoCapilar — Litepaper</h1>
<h3 align="center">Proof of Care: Reputacion Descentralizada para el Cuidado Capilar Natural</h3>

<p align="center">
  <strong>Version 1.0 | Marzo 2026</strong><br/>
  Angela Salles — <a href="https://ang3la.xyz">Ang3la.xyz</a>
</p>

"""


def replace_wp_footer(body: str, lang: str) -> str:
    if lang == "en":
        return re.sub(
            r"\n---\n\nBuilt with care on \[Stellar\]\(https://stellar\.org/\)\n\n\[Read the Litepaper\]\([^\)]*\)\s*$",
            "\n\n" + FOOT_WP_EN,
            body,
            flags=re.MULTILINE,
        )
    if lang == "pt":
        return re.sub(
            r"\n---\n\nFeito com cuidado na \[Stellar\]\(https://stellar\.org/\)\n\n\[Leia o Whitepaper completo\]\([^\)]+\)\s*$",
            "\n\n" + FOOT_WP_PT,
            body,
            flags=re.MULTILINE,
        )
    if lang == "es":
        return re.sub(
            r"\n---\n\nHecho con cuidado en \[Stellar\]\(https://stellar\.org/\)\n\n\[Lee el Whitepaper completo\]\([^\)]+\)\s*$",
            "\n\n" + FOOT_WP_ES,
            body,
            flags=re.MULTILINE,
        )
    raise ValueError(lang)


def replace_lp_footer(body: str, lang: str) -> str:
    if lang == "en":
        return re.sub(
            r"\n---\n\nBuilt with care on \[Stellar\]\(https://stellar\.org/\)\n\n\[Read the full Whitepaper\]\([^\)]+\)\s*$",
            "\n\n" + FOOT_LP_EN,
            body,
            flags=re.MULTILINE,
        )
    if lang == "pt":
        return re.sub(
            r"\n---\n\nFeito com cuidado na \[Stellar\]\(https://stellar\.org/\)\n\n\[Leia o Whitepaper completo\]\([^\)]+\)\s*$",
            "\n\n" + FOOT_LP_PT,
            body,
            flags=re.MULTILINE,
        )
    if lang == "es":
        return re.sub(
            r"\n---\n\nHecho con cuidado en \[Stellar\]\(https://stellar\.org/\)\n\n\[Lee el Whitepaper completo\]\([^\)]+\)\s*$",
            "\n\n" + FOOT_LP_ES,
            body,
            flags=re.MULTILINE,
        )
    raise ValueError(lang)


def main() -> None:
    for out_name, src, toc_pat, lang, head, fixes in [
        (
            "WHITEPAPER.md",
            "0b587ff7-45a9-4962-88cc-9add1f534780.txt",
            r"\(https://www\.ang3la\.xyz/papers/WHITEPAPER\.md#",
            "en",
            HEAD_WP_EN,
            [
                (
                    "Check in daily with treatments: H ydration, N utrition, or R econstruction",
                    "Check in daily with treatments: Hydration (H), Nutrition (N), or Reconstruction (R)",
                )
            ],
        ),
        (
            "WHITEPAPER.pt-BR.md",
            "7978bb94-ea51-46d0-a9ea-e10196c7f85b.txt",
            r"\(https://www\.ang3la\.xyz/papers/WHITEPAPER\.pt-BR\.md#",
            "pt",
            HEAD_WP_PT,
            [
                (
                    "Faca check-in diario com tratamentos: H idratacao, N utricao ou R econstrucao",
                    "Faca check-in diario com tratamentos: Hidratacao (H), Nutricao (N) ou Reconstrucao (R)",
                )
            ],
        ),
        (
            "WHITEPAPER.es-ES.md",
            "fb538a5b-8092-437f-b294-cb4d8af36819.txt",
            r"\(https://www\.ang3la\.xyz/papers/WHITEPAPER\.es-ES\.md#",
            "es",
            HEAD_WP_ES,
            [
                (
                    "Haz check-in diario con tratamientos: H idratacion, N utricion o R econstruccion",
                    "Haz check-in diario con tratamientos: Hidratacion (H), Nutricion (N) o Reconstruccion (R)",
                )
            ],
        ),
    ]:
        body = strip_wp_title_block(read_agent(src))
        body = re.sub(toc_pat, "(#", body)
        for old, new in fixes:
            body = body.replace(old, new)
        body = replace_wp_footer(body, lang)
        (DOCS / out_name).write_text(head.rstrip() + "\n\n" + body, encoding="utf-8")
        print("wrote", out_name)

    base = "https://www.ang3la.xyz/papers/"
    for path, lang, head in [
        ("LITEPAPER.md", "en", HEAD_LP_EN),
        ("LITEPAPER.pt-BR.md", "pt", HEAD_LP_PT),
        ("LITEPAPER.es-ES.md", "es", HEAD_LP_ES),
    ]:
        with urllib.request.urlopen(base + path, timeout=60) as r:
            raw = r.read().decode("utf-8")
        body = strip_lp_title_block(raw)
        body = replace_lp_footer(body, lang)
        (DOCS / path).write_text(head.rstrip() + "\n\n" + body, encoding="utf-8")
        print("wrote", path, "(fetched)")


if __name__ == "__main__":
    main()
