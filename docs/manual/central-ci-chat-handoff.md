# Forge CAD-library ecosystem handoff

Copy the text block below into a new chat when continuing work on Forge and its supporting ecosystem.

~~~text
Je werkt verder aan Forge als centrale CAD-library en aan de repositories die die library ondersteunen en consumeren.

Belangrijkste repositories:

- `lib.py.solidcraft.forge` — centrale Forge CAD-library: publieke API, compiler/lowering, modellering en Forge-eigen verificatievoorbeelden
- `lib.py.cad.ci` — generieke CAD-CI-logica
- `tool.cad.ci` — dunne CLI/reusable workflows
- `tool.cad.ci.test` — externe test van released CAD-CI
- `lib.py.cad.verification` — generieke CAD-verificatie
- `docker.cad.solidcraft` — immutable SolidCraft runtime/container
- `tool.py.lib.ci` — generieke Python-library CI
- `tool.py.lib.ci.test` — externe test daarvan

Gebruik deze handoff alleen als ingang. Bepaal de actuele werkzaamheden altijd
uit GitHub en de repositoryplannen.

Voor iedere actieve repo:

1. Lees eerst actuele issues, PR's en branches.
2. Lees `AGENTS.md` en `docs/plan.md`.
3. Behandel `docs/plan.md` als source of truth voor onafgemaakt werk.
4. Maak een issue als de wijziging nog geen issue heeft.
5. Update `docs/plan.md` vóór implementatie en beoordeel alle open issues
   opnieuw als `now`, `next`, `later`, `blocked`,
   `probably obsolete` of `effectively complete but still open`.
6. Update `docs/requirements.md` en `docs/design.md` als gedrag of
   architectuur verandert.
7. Daarna pas code.
8. Eén logische wijziging = één issue, branch en PR.
9. Na merge/release het plan opnieuw actualiseren.

Werk niet onnodig serieel:

- `dev-cad` en `dev-ci` zijn onafhankelijke werkstromen en mogen parallel
  vooruitgaan;
- wacht alleen op een workflow als de volgende stap werkelijk van die uitslag
  afhangt;
- werk ondertussen door in de andere lane wanneer daar onafhankelijk werk ligt;
- gedeelde dependency-releases en echte architectuurgates blijven
  synchronisatiepunten;
- repositorybrede governance mag via een korte branch rechtstreeks naar
  `main`.

Merge-regel:

- kies de merge-methode niet handmatig; gebruik na #598 alleen de `/merge`
  policy-workflow;
- korte feature/fix-PR's naar `dev-cad` of `dev-ci` worden squash-merged;
- exact `dev-cad -> main` en `dev-ci -> main` krijgen een normale
  mergecommit;
- alle andere PR's naar `main`, waaronder governance en `promote/*`, worden
  squash-merged;
- tijdelijke merged branches worden alleen via de expliciete cleanup-allow-list
  verwijderd; permanente/generated/backup refs nooit.

Repositorygrenzen:

- Generieke CAD-CI-logica hoort in `lib.py.cad.ci`.
- `tool.cad.ci` blijft dun; externe acceptatie hoort in `tool.cad.ci.test`.
- Generieke CAD/model-verificatie hoort in `lib.py.cad.verification`.
- De SolidCraft runtime, dependency-pins en containerrelease horen in
  `docker.cad.solidcraft`; consumers gebruiken alleen een immutable image tag.
- Forge bezit de herbruikbare CAD-API, compiler/lowering, modellering, Forge-eigen voorbeelden en model-specifieke verwachtingen.
- Product-CAD repositories bezitten hun eigen productmodellen, modelregistratie/catalogus, varianten, dependencies en presentatie-metadata.
- Generieke CAD-CI-, verificatie- en runtime-infrastructuur ondersteunt Forge en andere consumers, maar vormt niet het architecturale middelpunt.
- Gewone Python-library CI hoort in `tool.py.lib.ci`; externe acceptatie
  daarvan in `tool.py.lib.ci.test`.

Als Forge of een andere consumer een ontbrekende generieke CAD-CI-, verificatie- of runtimefunctie blootlegt, leg de behoefte bij de juiste eigenaar neer, test en release die daar, en adopteer daarna de release. Maak geen consumer-lokale workaround.

Begin nu met `lib.py.solidcraft.forge`: inspecteer de actuele toestand en lees
`AGENTS.md` en `docs/plan.md`. Volg daarna de actuele werkvolgorde uit het
plan en de relevante plannen van de andere repositories.
~~~
