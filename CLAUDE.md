# OCN — Open Chess Naming

This repo holds the **OCN-1 catalogue** (CC-BY-4.0 spec + CSV) and its
Python validator (MIT). Companion to `escacsfigueres/chess-parquet`.

## Comptes externs · Verificació obligatòria abans de tocar Vercel o GitHub

L'Albert manté **3 comptes Vercel** i **3 comptes GitHub** simultàniament. Aquest repo es desplega i es versiona amb comptes específics. Abans d'executar `vercel`, `gh`, o `git push`:

**Comptes correctes per a aquest projecte (`ocn` · OCN-1 catalogue):**
- **GitHub:** `escacsfigueres` ha de ser Active. Verificar amb `gh auth status`. Si no: `gh auth switch -u escacsfigueres` **+ tot seguit** `gh auth setup-git` (sense aquest segon pas, `git push` HTTPS falla amb *"repository not found"* tot i tenir el user correcte; `gh auth switch` no actualitza les credencials del keychain de macOS que `git` consulta).
- **Vercel:** team `escacsfigueres`. **Sempre** fer servir l'alias `vercel-escacs` (definit a `~/.zshrc`, usa `$VERCEL_TOKEN_ESCACS`) en lloc de `vercel` directe. Així el deploy va sempre al compte correcte independentment del CLI login global.
  - Deploy preview: `vercel-escacs`
  - Deploy producció: `vercel-escacs --prod`
  - Mai usar `vercel` (sense `-escacs`) per a aquest repo.

**Mapping de comptes (referència):**
- Team Vercel `escacsfigueres` → `Web`, `backend`, `ocn` (aquest), `parquet`
- Team Vercel `albert` → `source`, `source-next`, `chroma-index`
- Team Vercel `noras` (norasproject) → projectes separats

**Si el compte actiu és incorrecte:** ATURA i avisa l'Albert. NO facis push, NO facis deploy, NO executis cap comanda `gh` o `vercel` que escrigui a remot. Aquest no és un repo personal — la barreja amb comptes personals causaria confusió administrativa.

---

## Promotion de feature branches a `main`

**Promoure una feature a `main` NO és cherry-pick d'un sol commit final.** Una
feature branch normalment porta múltiples commits (catàleg → validador → docs)
i el commit tip depèn dels seus pares: cherry-pickejar només el tip falla
perquè el patch referencia codi introduït per commits previs.

**Promotion checklist (obligatori abans de promoure):**

1. `git fetch origin` — sincronitza refs locals (main pot haver avançat per altres sessions).
2. `git log --oneline origin/main..feat/<name>` — llista TOTS els commits a promoure.
3. `git merge-base feat/<name> origin/main` — confirma punt de divergència.
4. Decidir estratègia:
   - **Range cherry-pick** (default): `git cherry-pick <first>^..<tip>`. Preserva granularitat per bisect/blame.
   - **Squash merge**: 1 commit a main. Linealitza historial; perd granularitat.
   - **Fast-forward merge**: només si main no s'ha mogut des del branch point.
5. Aplicar contra `main` net (working tree clean). Si conflicte **fora del scope esperat** de la feature: STOP i avisa l'Albert abans de tocar res més.
6. Mai promoure el catàleg sense passar el validador + un sample-check sobre el CSV (consistència de codes OCN-1, integritat referencial entre `chess-parquet`).

## Worktree per stream

Múltiples streams concurrents al mateix working tree causen branca-switch
sorpresa, fitxers untracked perduts, scope creep i conflictes de promoció
inesperats. **Cada stream va al seu worktree** quan corren en paral·lel:

```bash
git worktree add ../ocn-catalogue feat/catalogue-update
git worktree add ../ocn-validator feat/validator-x
```

Mai obrir dos streams al mateix WT (`/Users/albertpi/Code/ocn`) si una altra
sessió hi treballa. Si trobes el WT en una branca aliena, treballa des d'un
worktree separat (o demana a l'Albert que coordini).

## Agentic development contract

For OCN-specific agentic work, follow
[`docs/agentic-development-playbook.md`](docs/agentic-development-playbook.md):
Intent, Expectations, Context, Workflow — with explicit GO gates for
apply / push / tag / release / dynamic workflows. It generalises the
account, promotion, and worktree rules above into the full human–agent
loop (task sizing + verification discipline).

**Batch attribution/naming applies — never hand-edit the CSV.** Write an
`ocn.attribution_manifest.v1` JSON and run `tools/apply_attribution_manifest.py`
(dry-run by default; `--apply --out` only under an explicit GO). It enforces
the field-scope, exact-changed-rows, and zero-collateral-diff guardrails. See
[`docs/attribution-batch-engine.md`](docs/attribution-batch-engine.md).

## No middle-dot separator (AI tell)

NEVER use the middle dot `·` (U+00B7) as a separator — e.g. `A · B`, `place · year`, `name · detail`. The interpunct as a separator is a dead giveaway of AI-generated text. Use a comma, a dash (— or -), a slash (/), a line break, or rewrite the phrase. Applies to ALL output: UI copy, editorial content, data labels, code, and comments.
