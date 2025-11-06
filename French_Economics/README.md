
### This repository supports the Medium article

### [The Tyranny of the Median Voter: France's Democratic Road to Stagnation](https://medium.com/p/0a81466cc2dc)


&nbsp;


# French and EU Economics

All the data used for the article is in the `Data` folder. 
To reproduce the figures and the analysis, run `Data/Make_Figures.py`

### EU and OCED statistics
- Public Social Spending in OECD Countries: https://www.oecd.org/en/publications/public-social-spending-is-high-in-many-oecd-countries_c9a15b71-en.html
- Historical Public Social Spending in OECD Countries: https://ourworldindata.org/grapher/social-spending-oecd-longrun
- Net Fiscal Contributions in the EU: https://onlinelibrary.wiley.com/doi/10.1111/kykl.70009
- 2025 International Tax competitiveness Ranking: https://taxfoundation.org/research/all/global/2025-international-tax-competitiveness-index/
- 2025 Global Innovation Index rankings: https://www.wipo.int/web-publications/global-innovation-index-2025/en/index.html
- 2025 Millionaires migration: https://www.henleyglobal.com/publications/henley-private-wealth-migration-report-2025
- Well-Being Index across OECD: https://www.oecd.org/en/data/tools/oecd-better-life-index.html
- Sustainability of PAYG pension systems in the EU: https://www.oecd.org/en/publications/2025/04/oecd-economic-surveys-luxembourg-2025_3eb782b5.html
- Luxembourg Income Study Database: https://www.lisdatacenter.org/our-data/lis-database/

### French GDP and Debt
- French GDP since 1950: https://fred.stlouisfed.org/data/NGDPXDCFRA
- French CPI since 1955: https://fred.stlouisfed.org/series/FRACPIALLAINMEI
-	French net yearly deficit since 1959: 
https://db.nomics.world/AMECO/UBLG/FRA.1.0.319.0.UBLG
-	French debt since 1959: https://www.imf.org/external/datamapper/DEBT1@DEBT/FRA
-	10 years French bonds rate since 1960:
https://fred.stlouisfed.org/series/IRLTLT01FRM156N
(The effective cost of the debt was computed with a 8 years rolling average, which is roughly the average maturity of the french bonds)

### French Retirement Pensions
- Age statistics of the french population since 1950: https://www.ined.fr/fr/tout-savoir-population/chiffres/france/structure-population/population-ages/
- Used this to estimate the ratio of contributors per retiree (Also accounting for the legal retirement age), and cross checked with https://www.insee.fr/fr/statistiques/2415121
- Average net salary of workers since 1950: https://www.insee.fr/fr/statistiques/6662214
- Labor force participation rate: https://www.insee.fr/fr/statistiques/8242345
- Pension levels: https://www.insee.fr/fr/statistiques/3303437

### Wealth Tax (IGF, ISF, IFI)
- Recettes fiscales: https://fr.wikipedia.org/wiki/Imp%C3%B4t_de_solidarit%C3%A9_sur_la_fortune
- Cross-checked with: https://www.ifrap.org/budget-et-fiscalite/ce-que-lisf-fait-perdre-la-france
- Cross-checked with: https://www.rexecode.fr/media/documents/document-de-travail/2017/document-de-travail-n-63-les-consequences-economiques-des-expatriations-dues-aux-ecarts-de-fiscalite-entre-la-france-et-les-autres-pays

## Additional Ressources:
- The Macro-History Database: https://www.macrohistory.net/database/
- Wealth-Income Ratios in Rich Countries 1700-2010: https://gabriel-zucman.eu/files/PikettyZucman2014Databook.pdf

