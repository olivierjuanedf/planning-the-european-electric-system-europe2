[Toy ex, Mon afternoon]
1) Doc doc/... pour clarifier les choses + baba utilisation codespace en dehors du repot ?
2) my_toy_ex_italy.py
* voir "XXX" (notamment les coding tricks)
* conserver FUEL_SOURCES ou bien trop compliqué pour les étudiants ?
* voir si certains warning sont de notre fait... même si en ligne il semble que PyPSA en génère pas mal - notamment en lien avec Linopy
* Robust end of run when infeasible... not crashing after resolution
* doc/toy-model_tutorial.md to be completed/improved
2bis) Cleaner italy_parameters.py
4) Hydraulic storages... cf. CS student code
5) Scripts avec qques exemples de base Python ? "[coding tricks]"
6) Usage param auto fulfill interco capa missing
7) / by efficiency in FuelSources and not * for primary cost?
8) Remplir long_term_uc/toy_model_params/ex_italy-complem_parameters.py avec des exs complémentaires au cas italien (hydrau, batteries)

[Tue-...]
1) Set dates as values in plots (and not obscure idx)


[If time allows...]
0) Finish and connect type checker for JSON file values -> using map(func, [val]) and all([true])
-> OK excepting UsageParameters
1) Set available aggreg. prod type PER COUNTRY - to facilitate exercise
2) Add possibility to set Stock (additional to ERAA data) in JSON tb modif input file
5) Add possibility to provide additional fatal demand -> for iterations between UC and imperfect disaggreg..
6) Check multiple links between two zones possible. Cf. ger-scandinavia AC+DC in CentraleSupélec students hypothesis
And types ok? Q2Emmanuel NEAU and Jean-Yves BOURMAUD
7) Add plot functions to get demand/cf/capas values for the selected values of params (and selected period)
8) Q2oj Sous-partie git avec accès différencié élèves / ta pour docs et données diff ?

[Next year]
1) Iberian-peninsula -> Iberia