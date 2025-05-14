# Guia de Estilos (Style Guide) - Auge Invest

## 1. Introdução

Este Guia de Estilos documenta as diretrizes de design visual e de interface para a plataforma "Auge Invest". O objetivo é garantir consistência, usabilidade e uma identidade visual coesa em todas as partes do aplicativo. Este é um documento vivo e será atualizado conforme o projeto evolui.

## 2. Filosofia de Design

*   **Moderno e Limpo:** Interfaces com design contemporâneo, sem excesso de elementos, focando na clareza e facilidade de uso.
*   **Interativo:** Elementos de interface que respondem de forma intuitiva às ações do usuário, proporcionando feedback claro.
*   **Profissional:** Transmitir confiança e seriedade, adequadas a uma plataforma do mercado financeiro.
*   **Acessível:** Considerar as diretrizes de acessibilidade (WCAG) para garantir que a plataforma possa ser utilizada pelo maior número de pessoas possível.

## 3. Branding

*   **Nome da Plataforma:** Auge Invest
*   **Logo:** Conceito de uma montanha em formato de "A". (O arquivo do logo será fornecido pelo usuário e integrado aqui).
    *   **Aplicações do Logo:** Cabeçalhos, e-mails, material de marketing.
    *   **Variações:** Versões para fundos claros e escuros.

## 4. Paleta de Cores

(Esta seção será preenchida com as cores exatas após definição ou recebimento dos assets visuais do usuário. Exemplo inicial abaixo, a ser refinado.)

### 4.1. Cores Primárias

*   **Azul Auge Principal:** `#0052CC` (Exemplo - um azul corporativo, confiável)
*   **Verde Auge Destaque:** `#00875A` (Exemplo - para calls-to-action positivos, indicadores de alta)

### 4.2. Cores Secundárias

*   **Cinza Escuro (Texto Principal):** `#172B4D` (Exemplo)
*   **Cinza Médio (Texto Secundário, Bordas):** `#5E6C84` (Exemplo)
*   **Cinza Claro (Fundos de Seção, Divisores):** `#F4F5F7` (Exemplo)

### 4.3. Cores de Feedback e Alerta

*   **Sucesso (Verde):** `#36B37E` (Exemplo)
*   **Atenção (Amarelo):** `#FFAB00` (Exemplo)
*   **Erro (Vermelho):** `#FF5630` (Exemplo - para indicadores de baixa, alertas negativos)
*   **Informação (Azul Claro):** `#00B8D9` (Exemplo)

### 4.4. Cores para Modos Light e Dark

*   **Modo Light (Padrão):**
    *   Fundo Principal: `#FFFFFF`
    *   Fundo de Cards/Seções: `#F4F5F7` ou `#FFFFFF` com sombras suaves.
    *   Texto Principal: Cinza Escuro (`#172B4D`)
    *   Texto Secundário: Cinza Médio (`#5E6C84`)
*   **Modo Dark:**
    *   Fundo Principal: `#0D1117` (Exemplo - um cinza bem escuro, quase preto)
    *   Fundo de Cards/Seções: `#161B22` (Exemplo - um cinza um pouco mais claro que o fundo)
    *   Texto Principal: `#C9D1D9` (Exemplo - um cinza claro)
    *   Texto Secundário: `#8B949E` (Exemplo - um cinza médio-claro)
    *   Cores primárias e de alerta podem precisar de ajustes de tonalidade/saturação para manter o contraste no modo dark.

## 5. Tipografia

(Sugestão inicial, a ser confirmada/ajustada. Priorizar fontes legíveis e com boa renderização web.)

*   **Fonte Principal (Títulos, Cabeçalhos):** Inter (Sans-serif)
    *   Pesos: Bold (700), Semi-Bold (600)
*   **Fonte Secundária (Corpo de Texto, Labels):** Inter (Sans-serif)
    *   Pesos: Regular (400), Medium (500)

*   **Hierarquia de Tamanhos (Exemplo Responsivo - base 16px):**
    *   H1 (Título Principal da Página): 32px (2rem) - Bold
    *   H2 (Título de Seção): 24px (1.5rem) - Semi-Bold
    *   H3 (Subtítulo de Seção): 20px (1.25rem) - Semi-Bold
    *   Corpo de Texto Principal: 16px (1rem) - Regular
    *   Texto Secundário/Labels: 14px (0.875rem) - Regular
    *   Microtexto/Legendas: 12px (0.75rem) - Regular

*   **Altura da Linha:** 1.5 para corpo de texto, 1.2-1.3 para títulos.

## 6. Espaçamento e Layout

*   **Sistema de Grid:** Utilizar um sistema de grid flexível (ex: grid de 12 colunas) para alinhar os elementos e garantir responsividade.
*   **Unidade de Espaçamento Base:** 8px (ou múltiplos: 4px, 8px, 12px, 16px, 24px, 32px, etc.) para margens, paddings e espaçamento entre elementos.
*   **Consistência:** Manter o espaçamento consistente em toda a plataforma.

## 7. Componentes de UI (Exemplos Iniciais)

(Esta seção será expandida com especificações detalhadas para cada componente reutilizável. Storybook será usado para documentar e visualizar os componentes.)

*   **Botões:**
    *   Primário (Azul Auge Principal)
    *   Secundário (Borda Azul Auge, fundo transparente)
    *   Destrutivo (Vermelho Erro)
    *   Estados: Normal, Hover, Focus, Active, Disabled.
    *   Tamanhos: Pequeno, Médio, Grande.
*   **Inputs de Formulário:**
    *   Campos de texto, selects, checkboxes, radio buttons.
    *   Labels claras, mensagens de erro/validação.
    *   Estados: Normal, Focus, Error, Disabled.
*   **Cards:**
    *   Usados para exibir indicadores, resumos de ativos, etc.
    *   Sombra suave no modo light, bordas sutis no modo dark.
    *   Padding interno consistente.
*   **Tabelas:**
    *   Para exibir dados como histórico de transações, listas de ativos.
    *   Linhas zebradas (opcional), cabeçalhos claros.
*   **Gráficos:**
    *   Cores consistentes com a paleta da plataforma.
    *   Tooltips informativos, legendas claras.
    *   Interatividade (zoom, pan, seleção de período).
*   **Navegação:**
    *   Menu principal, breadcrumbs, abas.
*   **Modais e Pop-ups:**
    *   Para confirmações, formulários rápidos, alertas.

## 8. Iconografia

*   **Estilo:** Ícones limpos, modernos e facilmente reconhecíveis.
*   **Biblioteca Sugerida:** Feather Icons, Heroicons, ou Material Symbols (escolher uma e manter a consistência).
*   **Tamanhos:** Padrões (ex: 16px, 20px, 24px).
*   **Cor:** Geralmente cor do texto secundário, ou cor primária para ícones em destaque.

## 9. Imagens e Ilustrações

*   **Fundos de Página:** (Serão fornecidos pelo usuário).
*   **Ilustrações:** Se usadas (ex: para onboarding, seções vazias), devem seguir um estilo coeso e profissional, alinhado com a identidade visual da "Auge Invest".

## 10. Tom de Voz e Linguagem

*   **Tom:** Profissional, confiável, claro, educativo e encorajador.
*   **Linguagem:** Evitar jargões excessivos sem explicação. Textos devem ser concisos e diretos.
*   **Público Alvo:** Investidores brasileiros de diferentes níveis de experiência.

## 11. Acessibilidade (Princípios)

*   **Contraste de Cores:** Garantir contraste suficiente entre texto e fundo.
*   **Navegação por Teclado:** Todos os elementos interativos devem ser acessíveis via teclado.
*   **Texto Alternativo para Imagens:** Fornecer `alt text` descritivo para imagens significativas.
*   **Semântica HTML:** Usar tags HTML de forma semântica.
*   **ARIA Attributes:** Utilizar atributos ARIA quando necessário para melhorar a acessibilidade de componentes dinâmicos.

---

*Este Guia de Estilos será a referência principal para o design e desenvolvimento da interface da "Auge Invest".*

