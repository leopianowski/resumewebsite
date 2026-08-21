# -*- coding: utf-8 -*-
"""
Fonte única de verdade do currículo.

Para atualizar o site, edite este arquivo e rode:

    python build.py

Nada de conteúdo fica escrito à mão no index.html — ele é gerado.
"""

# ---------------------------------------------------------------- site
#
# URL final publicada. Precisa ser absoluta: crawler de rede social (LinkedIn,
# WhatsApp, Slack) não resolve caminho relativo em og:image, e sem isso o link
# não gera preview nenhum.
#
# Se um dia entrar domínio próprio, troque aqui e crie um arquivo
# static/CNAME com o domínio dentro.

SITE_URL = "https://leopianowski.github.io/resumewebsite/"

# ---------------------------------------------------------------- perfil

PROFILE = {
    "name": "Leonardo Pianowski",
    "role": "AI Engineer",
    "role_full": "Generative AI & LLM Agents",
    "location": "Curitiba, Paraná — Brasil",
    # O build procura images/profile.(png|svg|webp|jpg|jpeg) e usa o primeiro
    # que existir. Trocar de foto = trocar o arquivo e rodar o build.
    "photo_alt": "Leonardo Pianowski",
}

# Linhas do "boot" digitadas uma após a outra no topo da página.
# O build calcula os delays de cada linha a partir do tamanho dela.
BOOT_LINES = [
    ("cmd", "./wake_up.sh"),
    ("out", "Wake up, Leo..."),
    ("out", "The Matrix has you."),
    ("out", "Follow the white rabbit."),
]

ABOUT = [
    "Passei quase cinco anos em Customer Success e CX — suporte, onboarding, "
    "processos, dashboards. Todo esse tempo do outro lado do balcão, traduzindo "
    "dor de cliente para time de produto.",
    "Em 2024 eu troquei de lado. Hoje sou AI Engineer na Monest, onde construo "
    "agentes de IA conversacionais que atendem por WhatsApp e voz — os mesmos "
    "atendimentos que eu fazia na mão, agora em escala.",
    "Essa bagagem é o meu diferencial: eu sei o que quebra numa conversa real, "
    "o que o cliente odeia ouvir e onde um agente perde a confiança do usuário. "
    "Isso vira prompt, vira tool use, vira teste de regressão.",
]

LINKS = [
    {"label": "LinkedIn", "url": "https://www.linkedin.com/in/leonardo-pianowski/", "primary": True},
    {"label": "GitHub", "url": "https://github.com/LeoPianowski", "primary": False},
    {"label": "WhatsApp", "url": "https://api.whatsapp.com/send?phone=5541996270671", "primary": False},
    {"label": "E-mail", "url": "mailto:leopianowski@gmail.com", "primary": False},
]

NAV = [
    ("home", "Home"),
    ("sobre", "Sobre"),
    ("trajetoria", "Trajetória"),
    ("stack", "Stack"),
    ("formacao", "Formação"),
]

# ---------------------------------------------------------------- experiência
#
# `logo` é o slug do arquivo em images/logos/. O build aceita .png, .jpg,
# .jpeg, .svg e .webp — basta jogar o arquivo lá com esse nome e rodar o build
# de novo. Se o arquivo não existir, entra um bloco com as iniciais no lugar.

EXPERIENCES = [
    {
        "role": "AI Engineer | Generative AI & LLM Agents",
        "company": "Monest",
        "logo": "monest",
        "period": "set/2024 — atual",
        "current": True,
        "tags": ["Prompt Engineering", "LLM Agents", "Tool Use", "LLMOps", "Python", "SQL"],
        "bullets": [
            "Projeto e itero system prompts para agentes de IA conversacionais "
            "multicanal (WhatsApp e Voz) que automatizam cobrança, adaptando "
            "estratégia de prompt e modelo por canal para equilibrar precisão, "
            "custo e latência.",
            "Desenho fluxos de tool use / function calling (cálculo de ofertas, "
            "geração de acordos, atualização de status) integrados ao raciocínio "
            "do agente, reduzindo alucinação e garantindo respostas auditáveis.",
            "Crio scripts de automação em Python e skills de IA reutilizáveis "
            "para o time (scaffolding de projetos, validação de prompts, "
            "adaptação de templates), reduzindo trabalho manual repetitivo.",
            "Mantenho pipeline de LLMOps para versionamento e deploy de prompts: "
            "validação e testes de regressão automatizados antes da promoção "
            "para produção via CI/CD.",
            "Uso LangSmith para observability e tracing de conversas em "
            "produção, investigando falhas, loops e regressões de comportamento "
            "do agente.",
            "Construo dashboards e consultas SQL no MetaBase para monitorar "
            "desempenho dos agentes, e mantenho contato ativo com clientes para "
            "transformar feedback em melhorias de prompt.",
        ],
    },
    {
        "role": "Customer Success Manager",
        "company": "Monest",
        "logo": "monest",
        "period": "mar/2024 — set/2024",
        "tags": ["Customer Success", "Relacionamento"],
        "bullets": [
            "Gestão da carteira de clientes e ponte entre a operação de cobrança "
            "e o time de produto — a porta de entrada que virou a transição para "
            "engenharia de IA.",
        ],
    },
    {
        "role": "CS Ops | Customer Success Operations",
        "company": "SuaMEi",
        "logo": "suamei",
        "period": "mai/2023 — mar/2024",
        "tags": ["KPIs", "Looker Studio", "Pipefy", "Processos"],
        "bullets": [
            "Criação e melhoria de processos de CS (onboarding, ongoing e "
            "suporte) junto ao head da área.",
            "Mapeamento e criação de indicadores (KPIs) de todas as frentes.",
            "Centralização de todos os processos internos através da ferramenta "
            "Pipefy.",
            "Criação de dashboards de monitoramento de toda a área no Looker "
            "Studio (antigo Data Studio).",
            "Criação de rotinas de acompanhamento junto ao time de produto, como "
            "processos de report de bug e sugestões de melhoria ao produto.",
            "Mapeamento de oportunidades de upsell e monitoramento de possíveis "
            "churns baseados em dados.",
        ],
    },
    {
        "role": "Customer Success Analyst",
        "company": "Comunica.In",
        "logo": "comunicain",
        "period": "fev/2022 — mar/2023",
        "tags": ["B2B SaaS", "Zendesk", "CSAT"],
        "bullets": [
            "Atendimento a cliente enterprise (grande porte) por meio do Zendesk.",
            "Experiência do cliente B2B em SaaS.",
            "Análise e simulação de cenários para localizar possíveis bugs.",
            "Acompanhamento de métricas como CSAT e tempo de primeira resposta.",
            "Atualização de formulários e configurações do Zendesk.",
            "Treinamento B2B (onboarding para novos clientes).",
        ],
    },
    {
        "role": "Customer Experience Analyst",
        "company": "BEES Bank Brasil",
        "logo": "bees",
        "period": "out/2021 — fev/2022",
        "tags": ["Suporte N2", "SQL", "DataBricks", "Grafana"],
        "bullets": [
            "Atuação no suporte de Nível 2 (N2).",
            "Respondendo dúvidas e resolvendo problemas através de tickets via "
            "Zendesk.",
            "Responsável por demandas da área de banking (TED, PIX, boletos).",
            "Uso de Grafana e DataBricks (SQL) para fazer a análise dos casos.",
        ],
    },
    {
        "role": "Implementation Success Manager",
        "company": "Olist",
        "logo": "olist",
        "period": "jun/2021 — out/2021",
        "bullets": [
            "Contato com a base de lojistas após o ganho, por meio de chat, "
            "telefone e e-mail, dando o suporte necessário.",
            "Objetivo de alavancar as primeiras vendas dos lojistas realizando o "
            "onboarding e primeiros passos.",
            "Análise de informações e dados elaborando estratégias, "
            "identificando e corrigindo possíveis problemas.",
            "Acompanhamento dos primeiros passos do lojista atuando de forma "
            "consultiva, identificando oportunidades de negócio e de melhoria, "
            "além de atuar em reversão ao churn.",
        ],
    },
    {
        "role": "Analista de Relacionamento Junior",
        "company": "Banco Bari",
        "logo": "bari",
        "period": "mar/2021 — jun/2021",
        "bullets": [
            "Responsável por atender dúvidas, problemas e sugestões referentes "
            "ao banco digital.",
            "Atendimento de até 4 chats simultâneos.",
            "Auxílio na criação dos materiais de apoio aos colaboradores e "
            "construção de fluxogramas dos processos da área.",
        ],
    },
    {
        "role": "Customer Success Analyst",
        "company": "EngagED S/A",
        "logo": "engaged",
        "period": "out/2020 — mar/2021",
        "tags": ["MongoDB", "Postman", "Intercom"],
        "bullets": [
            "Responsável pelo suporte via chat (Intercom), respondendo dúvidas "
            "sobre o produto e passando demandas para o time de tecnologia como "
            "bugs e tasks.",
            "Definição e melhoria de processos de suporte.",
            "Extração de dados e relatórios do banco de dados (MongoDB).",
            "Demandas de tecnologia, tais como alteração, sincronização e "
            "criação de dados via endpoint (Postman).",
        ],
    },
    {
        "role": "Customer Support Analyst",
        "company": "aftersale",
        "logo": "aftersale",
        "period": "mai/2020 — out/2020",
        "bullets": [
            "Responsável pelo suporte nível 1.",
            "Garantir que todos os clientes da base tenham um atendimento de "
            "alta qualidade.",
            "Cuidar do processo de demandas de suporte para o time de tecnologia "
            "(nível 2).",
            "Auxílio ao head da área com os dados de usabilidade dos clientes.",
            "Auxílio na implementação da ferramenta de suporte Movidesk.",
        ],
    },
    {
        "role": "Customer Success Intern",
        "company": "aftersale",
        "logo": "aftersale",
        "period": "set/2019 — mai/2020",
        "bullets": [
            "Melhoria de processos na área, como onboarding de clientes, "
            "bloqueio de usuários inadimplentes e atendimento.",
            "Onboarding de clientes SMB, responsável pelo primeiro treinamento "
            "da plataforma e acompanhamento do primeiro mês do parceiro.",
            "Suporte reativo e proativo ao cliente pelo Zendesk, telefone e "
            "e-mail.",
            "Coleta de feedbacks dos clientes a fim de propor melhorias na "
            "plataforma para o time de produto.",
            "Análise do uso da ferramenta pelo cliente com o objetivo de upsell "
            "para um plano maior.",
        ],
    },
    {
        "role": "SDR Intern",
        "company": "NEX Energy",
        "logo": "nex",
        "period": "mai/2019 — set/2019",
        "bullets": [
            "Prospecção de novos clientes para adesão ao modelo de gestão de "
            "energia da Nex, elaboração de propostas de acordo com a simulação "
            "de consumo energético e manutenção da base de cadastro no CRM "
            "conforme o funil de venda.",
        ],
    },
    {
        "role": "Diretor Administrativo",
        "company": "Yapira UFPR",
        "logo": "yapira",
        "period": "jul/2018 — mar/2019",
        "bullets": [
            "Desenvolvimento de processos seletivos, implementação de processos "
            "gerenciais, desenvolvimento de padrões e organização de eventos e "
            "viagens.",
        ],
    },
]

# ---------------------------------------------------------------- stack

STACK = [
    {
        "dir": "ai/",
        "items": [
            "Prompt Engineering", "LLM Agents", "Tool Use", "Function Calling",
            "System Prompts", "LLMOps", "LangSmith", "Observability & Tracing",
        ],
    },
    {
        "dir": "dev/",
        "items": [
            "Python", "SQL", "HTML", "CSS", "JavaScript", "Git", "CI/CD",
            "Postman", "VBA",
        ],
    },
    {
        "dir": "data/",
        "items": [
            "MetaBase", "Looker Studio", "Grafana", "DataBricks", "MongoDB",
            "Excel",
        ],
    },
    {
        "dir": "ops/",
        "items": ["Zendesk", "Movidesk", "Intercom", "Pipefy", "Pipedrive"],
    },
]

# ---------------------------------------------------------------- formação

EDUCATION = [
    {
        "school": "Universidade Federal do Paraná",
        "degree": "Bacharelado em Engenharia de Produção",
        "period": "2017 — 2022",
    },
]

CERTIFICATIONS = [
    "Desenvolvimento Web Básico — HTML, CSS, JavaScript",
    "Bootcamp Customer Success",
    "Customer Experience (CX)",
    "Inteligência Emocional",
]

# ---------------------------------------------------------------- chuva digital
#
# Glifos do código do filme: katakana de meia largura (U+FF71–U+FF9D) +
# dígitos, que é o que mais se aproxima da fonte original.

RAIN_GLYPHS = "".join(chr(c) for c in range(0xFF71, 0xFF9E)) + "0123456789"
RAIN_COLUMNS = 34
RAIN_SEED = 1999  # ano do filme; fixo pra o build ser reprodutível
