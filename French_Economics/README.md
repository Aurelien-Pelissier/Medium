
### This repository supports the Medium article

### [The Tyranny of the Median Voter: France's democratic road to Stagnation](https://medium.com/p/0a81466cc2dc)


&nbsp;


# French Economics

Here I provide all the data and code I used for the article. To reproduce the figures and the analysis of the article, run `Data/Make_Figures.py`

### Cumulative government deficit per decades since 1950s
- French GDP since 1950: https://fred.stlouisfed.org/data/NGDPXDCFRA
- French CPI: https://fred.stlouisfed.org/series/FRACPIALLAINMEI
-	French net deficit since 1959: 
https://db.nomics.world/AMECO/UBLG/FRA.1.0.319.0.UBLG
-	French debt since 1959: https://www.imf.org/external/datamapper/DEBT1@DEBT/FRA
-	10 years French bonds rate since 1960:
https://fred.stlouisfed.org/series/IRLTLT01FRM156N
(The effective cost of the debt was computed with a 8 years rolling average, which is the average maturity of the french bond)


### Retirement pensions:
- Collected statistics about french population since 1950: https://www.ined.fr/fr/tout-savoir-population/chiffres/france/structure-population/population-ages/
- Used this to estimate the ratio of worker : retirees (Also accounting for the legal retirement age), and cross checked with https://www.insee.fr/fr/statistiques/2415121
https://www.persee.fr/doc/pop_0032-4663_1989_num_44_6_3525
- Average net alary of workers: https://www.insee.fr/fr/statistiques/6662214
- Labor force participation rate per year: https://www.insee.fr/fr/statistiques/8242345

### Wealth tax (IGF, ISF, IFI):
- Recettes fiscales: https://fr.wikipedia.org/wiki/Imp%C3%B4t_de_solidarit%C3%A9_sur_la_fortune



