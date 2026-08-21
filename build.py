#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gerador estático do site currículo.

    python build.py

Entrada:  data.py (conteúdo) + static/ (css, ícones, imagens)
Saída:    dist/ — pronto para publicar, é o que o GitHub Pages serve

Tudo em dist/ é gerado. Nada ali é editado à mão nem versionado.
Só stdlib — nada pra instalar.

O site em si é HTML + CSS puro: nenhum JavaScript é gerado ou usado.
Toda a animação (chuva digital, boot digitado, reveal no scroll, glow)
é feita com CSS.
"""

from __future__ import annotations

import argparse
import random
import re
import shutil
import sys
from html import escape
from pathlib import Path

import data

ROOT = Path(__file__).parent
STATIC = ROOT / "static"          # copiado verbatim para dist/
IMG = STATIC / "img"
LOGOS = IMG / "logos"
CSS = STATIC / "css" / "style.css"
DIST = ROOT / "dist"              # saída, no .gitignore
OUT = DIST / "index.html"
PREVIEW = DIST / "preview.html"

# Aviso no topo do HTML gerado. Sem ele, é fácil editar o dist/index.html
# por engano e perder o trabalho no build seguinte.
GENERATED_BANNER = """<!--
  ARQUIVO GERADO por `python build.py` — não edite à mão.
  O conteúdo vive em data.py e o estilo em static/css/style.css.
  Qualquer alteração feita aqui é perdida no próximo build.
-->"""

# extensões aceitas para foto e logos, em ordem de preferência
EXTS = (".png", ".svg", ".webp", ".jpg", ".jpeg")

# velocidade do efeito de máquina de escrever do boot.
# Mantido curto de propósito: o nome só aparece depois do boot, e ninguém
# espera 5 segundos por um currículo.
MS_PER_CHAR = 30
PAUSE_BETWEEN_LINES = 130
BOOT_START = 200


# ------------------------------------------------------------------ helpers

def esc(text: str) -> str:
    """Escapa texto para uso seguro em HTML."""
    return escape(str(text), quote=True)


def find_asset(directory: Path, stem: str) -> str | None:
    """
    Caminho web do primeiro `stem.<ext>` que existir, relativo a static/ —
    que é a raiz do site em dist/. Ex.: static/img/profile.jpeg -> img/profile.jpeg
    """
    for ext in EXTS:
        candidate = directory / f"{stem}{ext}"
        if candidate.exists():
            return candidate.relative_to(STATIC).as_posix()
    return None


def initials(company: str) -> str:
    """Iniciais da empresa, para o placeholder de logo faltante."""
    words = re.findall(r"[A-Za-zÀ-ÿ]+", company)
    if not words:
        return "??"
    if len(words) == 1:
        return words[0][:2].upper()
    return (words[0][0] + words[1][0]).upper()


def indent(html: str, level: int) -> str:
    pad = " " * level
    return "\n".join(pad + line if line.strip() else line for line in html.splitlines())


# ------------------------------------------------------------------ chuva digital

def render_rain() -> str:
    """
    Monta as colunas da chuva de código.

    Cada coluna é um <span> com katakana de meia largura empilhado
    verticalmente (writing-mode), com posição, duração, delay, tamanho e
    opacidade sorteados. O último glifo é a "cabeça" da coluna e recebe
    brilho mais forte, como no filme. Seed fixa pra o build ser
    reprodutível e o diff do index.html ficar limpo.
    """
    rnd = random.Random(data.RAIN_SEED)
    total = data.RAIN_COLUMNS
    step = 100 / total
    columns = []

    for i in range(total):
        length = rnd.randint(14, 32)
        glyphs = "".join(rnd.choice(data.RAIN_GLYPHS) for _ in range(length))
        left = round(i * step + rnd.uniform(-1.0, 1.0), 2)
        duration = round(rnd.uniform(7.5, 19.0), 2)
        delay = round(-rnd.uniform(0, duration), 2)
        size = rnd.choice((13, 14, 15, 16, 18, 20))
        opacity = round(rnd.uniform(0.30, 0.72), 2)
        # Posição estática usada quando o visitante pediu menos movimento:
        # a chuva continua na tela, só não cai.
        static_y = round(rnd.uniform(-20, 80), 1)
        style = (
            f"--x:{left}%;--dur:{duration}s;--delay:{delay}s;"
            f"--fs:{size}px;--op:{opacity};--y:{static_y}vh"
        )
        # Três níveis de brilho, como no filme: rastro escuro, alguns glifos em
        # verde cheio e a cabeça quase branca.
        columns.append(
            f'<span class="rain-col" style="{style}">'
            f"{esc(glyphs[:-4])}"
            f"<i>{esc(glyphs[-4:-1])}</i>"
            f"<b>{esc(glyphs[-1])}</b></span>"
        )

    return (
        '<div class="rain" aria-hidden="true">\n'
        + "\n".join(indent(c, 2) for c in columns)
        + "\n</div>"
    )


# ------------------------------------------------------------------ seções

def render_boot() -> str:
    """
    Sequência de boot digitada linha a linha.

    Sem JS: cada linha é um bloco com overflow escondido cuja largura vai de
    0 a 100% em `steps(n)`, n = número de caracteres. O Python acumula os
    delays pra uma linha só começar quando a anterior terminou.
    """
    lines = []
    elapsed = BOOT_START
    last_duration = 0
    for kind, text in data.BOOT_LINES:
        chars = len(text)
        duration = chars * MS_PER_CHAR
        style = (
            f"--chars:{chars};--type-dur:{duration}ms;--type-delay:{elapsed}ms"
        )
        prompt = '<span class="boot-sign">leo@matrix:~$</span> ' if kind == "cmd" else ""
        lines.append(
            f'<p class="boot-line boot-line--{kind}" style="{style}">'
            f'{prompt}<span class="boot-text">{esc(text)}</span></p>'
        )
        elapsed += duration + PAUSE_BETWEEN_LINES
        last_duration = duration

    # O nome entra sobrepondo o fim da última linha (~55% dela digitada) —
    # sem essa sobreposição a espera fica longa demais.
    reveal_delay = max(0, elapsed - PAUSE_BETWEEN_LINES - int(last_duration * 0.45))
    return "\n".join(lines), reveal_delay


def render_links() -> str:
    out = []
    for link in data.LINKS:
        cls = "btn btn--primary" if link.get("primary") else "btn"
        external = "" if link["url"].startswith("mailto:") else ' target="_blank" rel="noopener"'
        out.append(
            f'<a class="{cls}" href="{esc(link["url"])}"{external}>'
            f'<span class="btn-bracket">[</span>{esc(link["label"])}'
            f'<span class="btn-bracket">]</span></a>'
        )
    return "\n".join(out)


def render_nav() -> str:
    return "\n".join(
        f'<a href="#{esc(anchor)}">{esc(label)}</a>' for anchor, label in data.NAV
    )


def render_logo(exp: dict) -> tuple[str, bool]:
    """Devolve (html do logo, achou_arquivo)."""
    slug = exp.get("logo")
    path = find_asset(LOGOS, slug) if slug else None
    if path:
        return (
            f'<img class="xp-logo" src="{esc(path)}" '
            f'alt="{esc(exp["company"])}" width="72" height="72" loading="lazy">'
        ), True
    return (
        f'<span class="xp-logo xp-logo--empty" role="img" '
        f'aria-label="{esc(exp["company"])}">{esc(initials(exp["company"]))}</span>'
    ), False


def render_experiences() -> tuple[str, list[str]]:
    items, missing = [], []
    for exp in data.EXPERIENCES:
        logo_html, found = render_logo(exp)
        if not found and exp.get("logo"):
            missing.append(exp["logo"])

        badge = (
            '<span class="xp-badge">atual</span>' if exp.get("current") else ""
        )
        tags = ""
        if exp.get("tags"):
            chips = "".join(f"<li>{esc(t)}</li>" for t in exp["tags"])
            tags = f'<ul class="xp-tags">{chips}</ul>'

        bullets = "\n".join(
            indent(f"<li>{esc(b)}</li>", 12) for b in exp["bullets"]
        )

        items.append(f"""      <li class="xp reveal">
        <span class="xp-node" aria-hidden="true"></span>
        <article class="xp-card">
          <header class="xp-head">
            {logo_html}
            <div class="xp-ident">
              <h3 class="xp-role">{esc(exp["role"])}{badge}</h3>
              <p class="xp-org">
                <span class="xp-company">{esc(exp["company"])}</span>
                <span class="xp-slash">//</span>
                <time class="xp-period">{esc(exp["period"])}</time>
              </p>
            </div>
          </header>
          <ul class="xp-bullets">
{bullets}
          </ul>
          {tags}
        </article>
      </li>""")

    return "\n".join(items), missing


def render_stack() -> str:
    groups = []
    for group in data.STACK:
        chips = "\n".join(
            indent(f'<li class="chip">{esc(item)}</li>', 12)
            for item in group["items"]
        )
        groups.append(f"""      <div class="stack-group reveal">
        <h3 class="stack-dir">{esc(group["dir"])}</h3>
        <ul class="stack-list">
{chips}
        </ul>
      </div>""")
    return "\n".join(groups)


def render_education() -> str:
    out = []
    for edu in data.EDUCATION:
        out.append(f"""      <article class="edu-card reveal">
        <h3 class="edu-degree">{esc(edu["degree"])}</h3>
        <p class="edu-school">{esc(edu["school"])}</p>
        <p class="edu-period">{esc(edu["period"])}</p>
      </article>""")
    return "\n".join(out)


def render_certs() -> str:
    return "\n".join(
        indent(f'<li class="cert">{esc(c)}</li>', 8)
        for c in data.CERTIFICATIONS
    )


def render_about() -> str:
    return "\n".join(
        indent(f"<p>{esc(p)}</p>", 8) for p in data.ABOUT
    )


# ------------------------------------------------------------------ página

def build() -> str:
    boot, reveal_delay = render_boot()
    experiences, missing_logos = render_experiences()

    photo = find_asset(IMG, "profile")
    photo_pending = photo is None
    if photo_pending:
        photo = "img/profile.jpg"  # caminho esperado; o aviso sai no final

    name = esc(data.PROFILE["name"])
    role = esc(data.PROFILE["role"])
    role_full = esc(data.PROFILE["role_full"])
    description = (
        f'{data.PROFILE["name"]} — {data.PROFILE["role"]} '
        f'({data.PROFILE["role_full"]}). Currículo e trajetória.'
    )

    # Crawlers de rede social (LinkedIn, WhatsApp, Slack) não resolvem caminho
    # relativo em og:image — tem que ser URL absoluta, senão o link não gera
    # preview nenhum.
    site = data.SITE_URL.rstrip("/") + "/"
    og_image = f"{site}{photo}"

    html = f"""<!DOCTYPE html>
{GENERATED_BANNER}
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{name} — {role}</title>
  <meta name="description" content="{esc(description)}">
  <meta name="author" content="{name}">
  <meta name="theme-color" content="#0D0208">
  <link rel="canonical" href="{esc(site)}">
  <meta property="og:type" content="profile">
  <meta property="og:url" content="{esc(site)}">
  <meta property="og:title" content="{name} — {role}">
  <meta property="og:description" content="{esc(description)}">
  <meta property="og:image" content="{esc(og_image)}">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="icon" href="icons/favicon.ico" sizes="32x32">
  <link rel="icon" href="icons/favicon.svg" type="image/svg+xml">
  <link rel="apple-touch-icon" href="icons/apple-touch-icon.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@300;400;500;600&amp;family=Share+Tech+Mono&amp;display=swap" rel="stylesheet">
  <link rel="stylesheet" href="css/style.css">
</head>
<body>

{indent(render_rain(), 0)}
  <div class="crt" aria-hidden="true"></div>

  <a class="skip" href="#home">Pular para o conteúdo</a>

  <header class="topbar">
    <a class="brand" href="#home">
      <span class="brand-mark">&gt;_</span>
      <span class="brand-name">{name}</span>
    </a>
    <input type="checkbox" id="nav-toggle" class="nav-toggle">
    <label for="nav-toggle" class="burger" aria-label="Abrir menu">
      <span></span><span></span><span></span>
    </label>
    <nav class="nav">
{indent(render_nav(), 6)}
    </nav>
  </header>

  <main>

    <!-- ---------------------------------------------------------- home -->
    <section id="home" class="hero">
      <div class="hero-copy">
        <div class="boot">
{indent(boot, 10)}
        </div>

        <div class="hero-reveal" style="--reveal-delay:{reveal_delay}ms">
          <h1 class="hero-name">{name}</h1>
          <p class="hero-role">
            <span class="hero-role-main">{role}</span>
            <span class="hero-role-sub">{role_full}</span>
          </p>
          <p class="hero-loc">{esc(data.PROFILE["location"])}</p>
          <div class="hero-links">
{indent(render_links(), 12)}
          </div>
        </div>
      </div>

      <div class="hero-photo hero-reveal" style="--reveal-delay:{reveal_delay + 200}ms">
        <div class="photo-frame">
          <img src="{esc(photo)}" alt="{esc(data.PROFILE["photo_alt"])}" width="320" height="320">
        </div>
      </div>

      <a class="scroll-hint" href="#sobre" aria-label="Descer para a próxima seção">
        <span></span>
      </a>
    </section>

    <!-- --------------------------------------------------------- sobre -->
    <section id="sobre" class="section">
      <header class="sec-head reveal">
        <p class="prompt"><span class="prompt-sign">leo@matrix:~$</span> whoami</p>
        <h2>Sobre</h2>
      </header>
      <div class="about reveal">
{render_about()}
      </div>
    </section>

    <!-- ---------------------------------------------------- trajetória -->
    <section id="trajetoria" class="section">
      <header class="sec-head reveal">
        <p class="prompt"><span class="prompt-sign">leo@matrix:~$</span> cat trajetoria.log</p>
        <h2>Trajetória</h2>
      </header>
      <ol class="timeline">
{experiences}
      </ol>
    </section>

    <!-- --------------------------------------------------------- stack -->
    <section id="stack" class="section">
      <header class="sec-head reveal">
        <p class="prompt"><span class="prompt-sign">leo@matrix:~$</span> ls skills/</p>
        <h2>Stack</h2>
      </header>
      <div class="stack">
{render_stack()}
      </div>
    </section>

    <!-- ------------------------------------------------------ formação -->
    <section id="formacao" class="section">
      <header class="sec-head reveal">
        <p class="prompt"><span class="prompt-sign">leo@matrix:~$</span> cat formacao.txt</p>
        <h2>Formação</h2>
      </header>
      <div class="formacao">
{render_education()}
        <div class="certs reveal">
          <h3 class="certs-title">Certificações</h3>
          <ul class="certs-list">
{render_certs()}
          </ul>
        </div>
      </div>
    </section>

  </main>

  <footer class="foot">
    <p class="prompt"><span class="prompt-sign">leo@matrix:~$</span> exit</p>
    <p class="foot-note">Feito com 💚 por Leo — Python, HTML e CSS puro. Zero JavaScript.</p>
    <p class="foot-egg">
      <a href="https://github.com/LeoPianowski" target="_blank" rel="noopener">Follow the white rabbit</a>
    </p>
  </footer>

</body>
</html>
"""
    return html, missing_logos, photo_pending


# ------------------------------------------------------------------ preview
#
# Quem tem os efeitos visuais do Windows desligados (ou "reduzir movimento" no
# macOS/Linux) faz o browser reportar `prefers-reduced-motion: reduce`, e o
# site — corretamente — congela as animações. Isso é o comportamento certo pro
# visitante, mas impede o autor de avaliar o próprio design.
#
# `--preview` gera um preview.html com o CSS já resolvido pro estado COM
# movimento, sem tocar em configuração de sistema nenhuma.

def strip_reduced_motion(css: str) -> str:
    """Remove o bloco @media (prefers-reduced-motion: reduce) inteiro."""
    marker = "@media (prefers-reduced-motion: reduce)"
    start = css.find(marker)
    if start == -1:
        return css
    depth = 0
    for i in range(css.index("{", start), len(css)):
        if css[i] == "{":
            depth += 1
        elif css[i] == "}":
            depth -= 1
            if depth == 0:
                return css[:start] + css[i + 1:]
    return css


def build_preview(html: str) -> str:
    """
    HTML de preview: CSS inline, bloco de reduced-motion removido e os blocos
    `no-preference` promovidos a `all` (senão o browser continuaria pulando
    eles, já que ele ainda reporta `reduce`).
    """
    css = strip_reduced_motion(CSS.read_text(encoding="utf-8"))
    css = css.replace("(prefers-reduced-motion: no-preference)", "all")
    banner = (
        "<!-- ARQUIVO GERADO por `python build.py --preview`. Nao publicar: o "
        "CSS aqui ignora prefers-reduced-motion de proposito, so pra "
        "visualizacao local. O site de verdade e o index.html. -->\n"
    )
    html = html.replace(
        '<link rel="stylesheet" href="css/style.css">',
        f"<style>\n{css}\n</style>",
    )
    return banner + html


def write_dist(html: str) -> None:
    """
    Monta o dist/ do zero: copia static/ verbatim, escreve o index.html e
    põe o .nojekyll.

    O .nojekyll desliga o Jekyll, que o GitHub Pages roda por padrão. Hoje o
    site não tem arquivos com prefixo `_` (que o Jekyll ignoraria), mas é uma
    armadilha silenciosa esperando — e o deploy fica mais rápido sem ele.
    """
    shutil.rmtree(DIST, ignore_errors=True)  # sem sobras de builds antigos
    shutil.copytree(STATIC, DIST)
    OUT.write_text(html, encoding="utf-8")
    (DIST / ".nojekyll").write_text("", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Gera o site em dist/ a partir de data.py e static/."
    )
    parser.add_argument(
        "--preview",
        action="store_true",
        help="gera também dist/preview.html com as animações forçadas, para "
             "quem tem 'reduzir movimento' ativo no sistema",
    )
    args = parser.parse_args()

    html, missing_logos, photo_pending = build()
    write_dist(html)

    files = sum(1 for p in DIST.rglob("*") if p.is_file())
    lines = len(html.splitlines())
    print(f"[ok] dist/ montado — {files} arquivos")
    print(f"[ok] index.html — {lines} linhas, {len(html) / 1024:.1f} KB")
    print(f"[ok] {len(data.EXPERIENCES)} experiências, "
          f"{sum(len(g['items']) for g in data.STACK)} itens de stack, "
          f"{data.RAIN_COLUMNS} colunas de chuva")

    if args.preview:
        PREVIEW.write_text(build_preview(html), encoding="utf-8")
        print("[ok] dist/preview.html — animações forçadas, ignora "
              "prefers-reduced-motion")

    if missing_logos:
        print("\n[pendente] logos faltando — jogue os arquivos em static/img/logos/:")
        for slug in dict.fromkeys(missing_logos):
            print(f"           static/img/logos/{slug}.png   (ou .svg .webp .jpg .jpeg)")
        print("           até chegarem, entra um bloco com as iniciais no lugar.")

    if photo_pending:
        print("\n[ATENÇÃO] nenhuma foto em static/img/profile.(png|svg|webp|jpg|jpeg)")
        print("          o <img> do hero vai ficar quebrado até você colocar uma.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
