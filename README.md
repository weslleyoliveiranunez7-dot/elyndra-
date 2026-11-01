# ELYNDRA

RPG de escolhas em pixel art, feito para celular (paisagem). Fan game sem fins lucrativos, inspirado em Undertale, com história e personagens originais.
Criado por **Weslley Nunes**. Versão **1.8**: Prólogo e Capítulos 1 a 8, 7 rotas/finais e Modo Genocide (abre ao terminar o final de Sacrifício).

## Jogar
- Abra `www/index.html` por um servidor local (ex.: `npx serve www`) ou use o GitHub Pages (Actions > "Publicar no GitHub Pages" > Run workflow).
- Use fones de ouvido: o jogo avisa na abertura.

## Baixar APK e EXE prontos
- **Automático:** a cada push na `main` (ou em *Actions > Run workflow*) saem `ELYNDRA-apk` (Android) e `ELYNDRA-exe` (Windows, portátil, sem instalar) em *Artifacts*.
- **Release:** crie uma tag, ex.: `git tag v1.8 && git push origin v1.8`; o APK e o EXE aparecem na aba *Releases* para qualquer pessoa baixar.
- No Windows, F11 alterna tela cheia. O EXE não é assinado: o SmartScreen pode avisar ("Mais informações > Executar assim mesmo").

## Gerar o APK (GitHub Actions)
1. Suba esta pasta para um repositório no GitHub (branch `main`).
2. Aba **Actions** > **Gerar APK** (roda sozinho a cada push, ou clique em *Run workflow*).
3. Ao terminar, baixe `ELYNDRA-apk` em *Artifacts* e instale o `app-debug.apk` no celular (permita fontes desconhecidas).
O workflow não foi testado por mim; se falhar, mande o log da aba Actions.

## Áudio
- `www/audio/sfx`: 141 efeitos, ambientes, passos e vozes originais (sintetizados).
- `www/audio/sint`: músicas originais sintéticas, uma para cada slot do jogo (toca quando não há música em `audio/musica`).
- `www/audio/musica`: coloque aqui as suas músicas (veja `ELYNDRA_Musicas_Organizadas.zip`); têm prioridade sobre as sintéticas. **Não vão no repositório público** (direitos autorais). Para APK pessoal com repositório privado, apague `www/audio/musica/` do `.gitignore`.

## Sprites e texturas (v1.6)
- `www/img/`: `prot.png` (protagonista, 4 direções), `faces.png` (rostos de diálogo de todos os personagens), `jordana*.png` (Jordana: andar, retratos, batalha), `npc.png` (moradores), `floris.png` (Floris) e `tiles.png` (chão e parede de cada capítulo).
- `tools/build_assets.py` refaz tudo a partir da pasta EXPLOIT (que não vai no repositório): `python3 tools/build_assets.py EXPLOIT www/img www/index.html`.
- Sem a imagem, o jogo volta ao desenho antigo (retângulos); nada quebra.

## Licença
Código, áudio sintético e texturas de chão/parede: de Weslley Nunes. Os sprites do protagonista, de Floris e dos moradores (recolorizados) vêm de sprites de Undertale (Toby Fox); a Jordana é arte do próprio autor. Projeto de fã, sem monetização.
