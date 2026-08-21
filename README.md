# resumewebsite

Site currículo do Leonardo Pianowski, com tema visual inspirado em
**The Matrix (1999)** — analogia ao trabalho com IA.

🔗 **https://leopianowski.github.io/resumewebsite/**

## Stack

| Camada | O que é |
|---|---|
| **Python** | Gerador estático (`build.py` + `data.py`) |
| **HTML** | Gerado, nunca editado à mão |
| **CSS** | `static/css/style.css` — tema, layout responsivo e **todas** as animações |
| **JavaScript** | Nenhum. Zero. |

## Estrutura

```
├── data.py                     conteúdo — a fonte de verdade
├── build.py                    gerador: data.py + static/ -> dist/
├── make_favicon.py             ferramenta de asset (roda raramente)
├── static/                     copiado verbatim para dist/
│   ├── css/style.css
│   ├── icons/                  favicon.svg (fonte) + .ico e .png gerados
│   └── img/                    profile.jpeg + logos/
├── dist/                       SAÍDA — gerada, no .gitignore
└── .github/workflows/deploy.yml
```

Nada em `dist/` é versionado. O site é sempre construído a partir de `data.py`,
então é impossível publicar HTML desatualizado.

## Como mexer

Todo o conteúdo vive em [`data.py`](data.py). Edite lá e rode:

```bash
python build.py
```

Abra `dist/index.html`. Sem dependências — só a stdlib do Python 3.

### Preview das animações

Se o seu sistema tem "reduzir movimento" ativo (no Windows: efeitos visuais
desligados), o browser reporta `prefers-reduced-motion: reduce` e o site
congela as animações — corretamente. Para conseguir avaliar o design mesmo
assim:

```bash
python build.py --preview   # gera dist/preview.html
```

O `preview.html` remove o bloco `@media (prefers-reduced-motion: reduce)` e
promove os blocos `no-preference` a `all`. É só visualização local, nunca vai
para produção.

## Deploy

Push na `main` → o GitHub Actions roda o `build.py` e publica o `dist/`.

Pré-requisito, uma vez só: **Settings → Pages → Source = "GitHub Actions"**.

O workflow falha de propósito se a foto de perfil estiver faltando — melhor
quebrar o deploy do que publicar um `<img>` quebrado.

## Animação sem JavaScript

Tudo em CSS, com o Python fazendo o trabalho repetitivo no build:

- **Chuva digital** — o `build.py` gera 34 colunas de katakana de meia largura
  (U+FF71–U+FF9D, os mesmos glifos da fonte do filme) com posição, duração,
  delay, tamanho e opacidade sorteados. `random` com seed fixa (1999), então o
  HTML não muda entre builds sem motivo. Três níveis de brilho: rastro escuro,
  alguns glifos em verde cheio, cabeça quase branca — o rastro é escuro de
  propósito, porque rastro claro camufla o texto do site.
- **Boot digitado** — máquina de escrever com `width` + `steps()`. Como a fonte
  é monospace, o alvo é `chars × 1ch`, o que crava o cursor no fim do texto em
  qualquer tamanho de fonte. O Python calcula o delay acumulado de cada linha.
- **Reveal no scroll** — `animation-timeline: view()`, dentro de `@supports`;
  em browser sem suporte o conteúdo aparece normalmente.
- **Menu mobile** — `<input type="checkbox">` escondido + seletor irmão.

Com `prefers-reduced-motion`, a chuva **congela** em vez de desaparecer (o
Python sorteia uma posição estática por coluna). A pessoa pediu menos
movimento, não menos design. Também tem folha de impressão para virar currículo
em papel.

## Favicon

O ícone é o mesmo `>_` do topbar. A fonte de verdade é
[`static/icons/favicon.svg`](static/icons/favicon.svg) — formas geométricas,
sem `<text>`, então não depende de nenhuma fonte estar disponível.

```bash
python make_favicon.py
```

Rasteriza com o Chrome/Edge instalado e monta o `.ico` (16/32/48 px, payloads
PNG) com `struct` da stdlib. Gera também o `apple-touch-icon.png` de 180 px com
fundo quadrado e opaco, porque o iOS aplica a própria máscara e ignora o alpha.

Os rasterizados são versionados de propósito: rasterizar exige um browser, e
depender disso no CI seria frágil.

## Assets pendentes

**Logos das empresas** → `static/img/logos/<slug>.png` (aceita `.svg`,
`.webp`, `.jpg`, `.jpeg`). O `build.py` detecta sozinho; enquanto o arquivo não
existir, entra um bloco com as iniciais da empresa. Rode `python build.py` para
ver o que falta.

**Foto de perfil** → `static/img/profile.jpeg`.

## Domínio próprio

Troque `SITE_URL` em [`data.py`](data.py) e crie um `static/CNAME` com o
domínio dentro. O `SITE_URL` alimenta `og:image`, `og:url` e `canonical` — e
`og:image` **tem** que ser URL absoluta, senão LinkedIn e WhatsApp não geram
preview do link.

## Paleta

`#0D0208` · `#003B00` · `#008F11` · `#00FF41` — o "Matrix code green" canônico.
Tipografia: [Share Tech Mono](https://fonts.google.com/specimen/Share+Tech+Mono)
(display) e [IBM Plex Mono](https://fonts.google.com/specimen/IBM+Plex+Mono) (texto).
