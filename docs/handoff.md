# Forge CAD-library ecosystem handoff

Repository: `brainboxemb/lib.py.solidcraft.forge`.

This is the normal session entrypoint. It is intentionally kept under
`docs/handoff.md` so it is easy to find.

The copy block below is deliberately Dutch because it is intended to be pasted
into the user's Dutch-language ChatGPT session. Repository engineering
documentation remains English.

~~~text
Je werkt verder aan Forge als centrale CAD-library en aan de repositories die
die library ondersteunen en consumeren.

Belangrijkste repositories:

- `meta.cad.solidcraft` — gedeelde, kleine SolidCraft/CAD-conventies en
  documenttemplates;
- `lib.py.solidcraft.forge` — centrale Forge CAD-library: publieke API,
  compiler/lowering, modellering en Forge-eigen verificatievoorbeelden;
- `2026-011-02.cad.solidcraft` — product-CAD modellen en catalogus;
- `lib.py.cad.ci` — generieke CAD-CI-logica;
- `tool.cad.ci` — dunne CLI/reusable workflows;
- `tool.cad.ci.test` — externe acceptatie van released CAD-CI;
- `lib.py.cad.verification` — generieke CAD-verificatie;
- `docker.cad.solidcraft` — immutable SolidCraft runtime/container;
- `tool.py.lib.ci` en `tool.py.lib.ci.test` — generieke Python-library CI
  en externe acceptatie daarvan.

Gebruik deze handoff alleen als ingang. Bepaal de actuele werkzaamheden altijd
opnieuw uit GitHub en de repositoryplannen.

Begin met `lib.py.solidcraft.forge`:

1. inspecteer de actuele issues, PR's en branches;
2. lees `AGENTS.md` en `docs/plan.md`;
3. behandel `docs/plan.md` als source of truth voor onafgemaakt werk;
4. volg de actuele werkvolgorde uit het plan, niet een oude handofftekst;
5. maak een issue voordat je een logische wijziging implementeert als die nog
   geen issue heeft;
6. houd één logische wijziging bij één issue, branch en PR;
7. werk requirements/design bij als gedrag of architectuur verandert;
8. reconcileer het plan na merge of release.

Repositorygrenzen:

- Forge bezit de herbruikbare CAD-API, compiler/lowering, modellering,
  Forge-eigen voorbeelden en model-specifieke verwachtingen.
- Product-CAD repositories bezitten hun eigen productmodellen, varianten,
  dependencies, catalogus en presentatie-metadata.
- Generieke CAD-CI-logica hoort in `lib.py.cad.ci`.
- `tool.cad.ci` blijft dun; externe acceptatie hoort in
  `tool.cad.ci.test`.
- Generieke CAD/model-verificatie hoort in `lib.py.cad.verification`.
- Runtime/container packaging hoort in `docker.cad.solidcraft`.
- Gewone Python-library CI hoort in `tool.py.lib.ci`; externe acceptatie
  daarvan in `tool.py.lib.ci.test`.
- Ontbrekende generieke functionaliteit wordt bij de juiste eigenaar opgelost,
  getest en released; maak geen consumer-lokale workaround.

Werk niet onnodig serieel. Permanente lanes en hun merge/promotion-regels staan
in `AGENTS.md` en `docs/plan.md`; gebruik die actuele documenten in plaats
van ze hier te dupliceren.

Gedeelde documentstructuren staan in `brainboxemb/meta.cad.solidcraft`:
`templates/docs/plan.md` en `templates/docs/handoff.md`.
~~~
