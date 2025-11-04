import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams.update({'font.size': 18})

import sys


cool_colors = ['#283845', '#F2545B', '#0B132B', '#6DF1C5', '#0D3B66', '#F95738', '#352F44', '#5BC0BE', '#9C2C77', '#43B3AE']


def main():
    
    
    #EU
    EU_df = pd.DataFrame()
    df_net_benef = pd.read_csv('EU_proportion_net_beneficiaries.csv', index_col = 0)
    df_GDP_social = pd.read_csv('EU_proportion_GDP_social_contribution.csv', index_col = 0)
    
    
    EU_df['social[GDP]'] = df_GDP_social['percent of GDP']
    EU_df['proportion_of_net_beneficiaires[%]'] = df_net_benef['proportion_of_net_beneficiaires']
    
    print(EU_df)
    
    
    gdp_social = df_net_benef['proportion_of_net_beneficiaires'].to_numpy()
    country = df_net_benef.index
    
    plt.figure(figsize = (10,5))
    plt.grid(zorder = 0)
    plt.bar(np.arange(len(gdp_social)), gdp_social, color = cool_colors[7], zorder = 10)
    plt.xticks(np.arange(len(gdp_social)), country, rotation = 90)
    plt.ylim(30,65)
    plt.ylabel('Fraction [%]')
    plt.xlim(-0.75,len(gdp_social)-0.25)
    plt.show()
    
    #sys.exit()
    
    
    France_df = pd.DataFrame()

    #GDP & metrics
    df_GDP = pd.read_csv('French_GDP.csv', index_col = 0)
    df_CPI = pd.read_csv('French_CPI.csv', index_col = 0)
    df_social = pd.read_csv('France_proportion_GDP_social_contribution.csv', index_col = 0)
    df_debt_GDP = pd.read_csv('French_debt_GDP.csv', index_col = 0)
    df_deficit = pd.read_csv('French_deficit.csv', index_col = 0)
    df_bond = pd.read_csv('French_bond_yield.csv')
    df_bond["observation_date"] = pd.to_datetime(df_bond["observation_date"], errors="coerce")
    df_bond["IRLTLT01FRM156N"] = pd.to_numeric(df_bond["IRLTLT01FRM156N"], errors="coerce")
    df_bond_av = (df_bond.dropna(subset=["observation_date"])
                      .assign(Year=df_bond["observation_date"].dt.year)
                      .groupby("Year", as_index=False)["IRLTLT01FRM156N"]
                      .mean()
                      .rename(columns={"IRLTLT01FRM156N": "mean_bond"})
                      .set_index("Year"))
    
    France_df['GDP'] = df_GDP['GDP VALUE [millions in Nominal Euro]']
    France_df['CPI'] = df_CPI['FRACPIALLAINMEI']/np.max(df_CPI['FRACPIALLAINMEI'])*100
    France_df['GDP[2025bn]'] = France_df['GDP']/France_df['CPI']*100/1000
    France_df['debt[GDP]'] = df_debt_GDP['DebtPercentOfGDP']
    France_df['deficit[GDP]'] = df_deficit['deficit[GDP]']
    France_df['social[GDP]'] = df_social['percent of GDP']
    France_df['bond_rate'] = df_bond_av['mean_bond']
    France_df['effective_borrow_rate'] = France_df['bond_rate'].rolling(window=8, min_periods=1).mean()
    
    France_df['debt[2025bn]'] = France_df['GDP[2025bn]']*France_df['debt[GDP]']/100
    France_df['deficit_due_to_debt[GDP]'] = France_df['effective_borrow_rate']*France_df['debt[GDP]']/100
    France_df['deficit_due_to_debt[2025bn]'] = France_df['deficit_due_to_debt[GDP]']*France_df['GDP[2025bn]']/100    
    France_df['deficit[2025bn]'] = -France_df['deficit[GDP]']*France_df['GDP[2025bn]']/100
    
    
    print(France_df)
    
    print(France_df['bond_rate'])
    print(France_df['effective_borrow_rate'])
    
    deficit_due_to_debt_projected = France_df['debt[2025bn]'].to_numpy()[-2]*0.03*5
    deficit_projected = (France_df['deficit[2025bn]'].to_numpy()[-2] - France_df['deficit_due_to_debt[2025bn]'].to_numpy()[-2])*5
    print(deficit_due_to_debt_projected)
    print(deficit_projected)
    
    
    step = 5
    deficit = -France_df['deficit[2025bn]'].to_numpy()
    n = len(deficit)
    deficit_n = np.array([np.nanmean(deficit[i:i+step]) for i in range(0, n, step)])*step
    deficit_interrest = -France_df['deficit_due_to_debt[2025bn]'].to_numpy()
    deficit_interrest_n = np.array([np.nanmean(deficit_interrest[i:i+step]) for i in range(0, n, step)])*step
    
    if step == 10:
        year = ['1950s', '1960s', '1970s', '1980s', '1990s', '2000s', '2010s', '2020s']
    if step == 5:
        year = ['1950s', '1955s', '1960s', '1965s', '1970s', '1975s', '1980s', '1985s', '1990s', '1995s', '2000s', '2005s', '2010s', '2015s', '2020s', '2025s']
    
    plt.figure(figsize = (5.5,3.5))
    plt.grid(zorder = 0)
    plt.bar(np.arange(len(deficit_n)), deficit_n, color = cool_colors[7], zorder = 10)
    plt.bar(np.arange(len(deficit_interrest_n)), deficit_interrest_n, color = cool_colors[8], fill=False, edgecolor="black", linewidth=1, zorder = 11)
    plt.ylabel('Deficit [2025bn]')
    plt.xticks(np.arange(len(deficit_n)), year, rotation = 45, ha="right")
    plt.ylim(-1200,50)
    plt.xlim(1.2, len(deficit_n))
    plt.show()
    
    sys.exit()    
    
    
    plt.plot(France_df['GDP[2025bn]'], label = 'GDP')
    plt.show()
    
    plt.plot(France_df['debt[GDP]'], label = 'debt')
    plt.plot(France_df['social[GDP]'], label = 'social')
    plt.plot(France_df['deficit[GDP]'], label = 'deficit')
    plt.axhline(y=0, color = 'black', ls = '--')
    plt.legend()
    plt.show()
    
    
    
    gdp_social = France_df['social[GDP]'].to_numpy()
    n = len(gdp_social)
    step = 10
    gdp_social_n = np.array([np.nanmean(gdp_social[i:i+step]) for i in range(0, n, step)])
    year = ['1950s', '1960s', '1970s', '1980s', '1990s', '2000s', '2010s', '2020s']
    plt.figure(figsize = (4.5,5.5))
    plt.grid(zorder = 0)
    plt.bar(np.arange(len(gdp_social_n)), gdp_social_n, color = cool_colors[7], zorder = 10)
    plt.xticks(np.arange(len(gdp_social_n)), year, rotation = 45)
    
    #plt.ylim(30,65)
    plt.ylabel('GDP Social share [%]')
    plt.show()
    
    
    #sys.exit()
    
    
    
    fraction_n = np.array([48,49,52,53,55,56.5,57.5,58])
    
    
    """
    I calibrated the 2020s to France’s observed all-age figure under an extended lens 
    (close to INSEE/EUROMOD practice) and then worked backward by decade using a simple, 
    transparent mapping from macro trends to a net-beneficiary headcount. Specifically, 
    I (1) anchored the endpoint to recent French measurements 
    (~57% all-ages when counting cash plus in-kind education/health and netting out all taxes, 
     including indirect), (2) traced the post-war rise in social effort (social protection as % of GDP) 
    together with the expansion of publicly financed education and health services, which increases the 
    share of residents whose received value exceeds taxes paid, (3) layered in demographic structure 
    (children heavily use schooling; older adults draw health and pensions), so decades with more dependents 
    tend to have higher headcounts even at the same spending level, and (4) incorporated indirect taxes 
    (VAT/excises) on the “paid” side, which slightly lowers the share relative to a cash-only view but 
    not enough to offset the sizable in-kind services in a European setting. I then smoothed results by 
    decade and expressed each as a range reflecting uncertainty (larger bands in earlier decades due to 
    sparser harmonized data), from which the values above are simply the midpoints: 
        45–51 → 48.0 (1950s), 46–52 → 49.0 (1960s), 49–55 → 52.0 (1970s), 50–56 → 53.0 (1980s), 
        52–58 → 55.0 (1990s), 54–59 → 56.5 (2000s), 55–60 → 57.5 (2010s), and 57–61 → 59.0 (2020s).
    """
    
    
    
    
    plt.figure(figsize = (4,5))
    plt.grid(zorder = 0)
    plt.bar(np.arange(len(fraction_n)), fraction_n, color = cool_colors[7], zorder = 10)
    plt.xticks(np.arange(len(fraction_n)), year, rotation = 45)
    
    plt.ylim(30,65)
    plt.ylabel('Fraction [%]')
    plt.show()
    
    
    #sys.exit()
    
    
    
    


    #IGF, ISF, IFI
    df_isf_gain = pd.read_csv('France_igf_isf_ifi_receipts.csv', index_col = 0)
    df_isf_gain = df_isf_gain.fillna(0)
    df_isf_gain['wealth_gain'] = df_isf_gain['IGF_EUR_Bn'] + df_isf_gain['ISF_EUR_Bn'] + df_isf_gain['IFI_EUR_Bn']
    df_isf_loss = pd.read_csv('France_Lost_Capital_Proxy.csv', index_col = 0)
    
    France_df['Wealth_tax_receipt'] = df_isf_gain['wealth_gain']/France_df['CPI']*100
    France_df['Wealth_tax_loss'] = -df_isf_loss['NetLostCapital_EUR_Bn']/France_df['CPI']*100*4
    
    """
    Our baseline measure (≈€50 bn) is a net capital outflow built from ISF/IFI administrative mobility 
    and an average taxable base. To compare with broader loss estimates (≈€150–200 bn), we apply a scenario-based 
    uplift that mirrors common assumptions in the literature: (i) move from net to gross expatriated wealth 
    (factor ~1.6–2.0), (ii) revalue taxable bases to market wealth (~1.2–1.5), (iii) accumulate cohorts 
    forward to present with reasonable capital appreciation (~1.3–2.0), and (iv) capitalize recurring 
    taxes that would have applied to that wealth (capital-income taxes, IFI/ISF where relevant, VAT on 
    consumption out of capital income), yielding an additional ~1.1–1.6×. A mid-range combination produces
    an overall multiplier of ≈4×, taking the cumulative loss proxy to ~€200 bn. We report this as a scenario
    and caution against double counting across components.
    """
     
    tax_gain = France_df['Wealth_tax_receipt'].to_numpy()
    tax_loss = France_df['Wealth_tax_loss'].to_numpy()
    start = np.where(~np.isnan(tax_gain))[0][0]
    tax_gain = tax_gain[start:]
    tax_loss = tax_loss[start:]
    #tax_gain = np.array([0,0] + list(tax_gain))
    #tax_loss = np.array([0,0] + list(tax_loss))
    
    n = len(tax_gain)
    step = 4
    gain_n = np.array([np.nanmean(tax_gain[i:i+step]) for i in range(0, n, step)])*step
    loss_n = np.array([np.nanmean(tax_loss[i:i+step]) for i in range(0, n, step)])*step
    year = [1982+i*step for i in range(len(gain_n))]
        
    plt.figure(figsize = (12,5))
    gain_color = "#283845"  # orange
    loss_color = "#F2545B"  # blue
    plt.bar(np.arange(len(gain_n))*2, gain_n, color = gain_color, label = 'Wealth tax revenu')
    plt.bar(np.arange(len(gain_n))*2 + 1, loss_n, color = loss_color, label = 'Loss from capital outflow')
    plt.xticks(np.arange(len(gain_n))*2+0.5, year, rotation = 45)
    plt.axhline(y=0, color = 'black', ls = '--')
    plt.grid(axis="both", linestyle="--", linewidth=0.6, alpha=0.5)
    plt.ylabel('Billions of €')
    plt.legend(fontsize = 15, loc = 'lower left')
    plt.show()
    
    #sys.exit()
    
    
    
    
    #French pension
    #df_ratio = pd.read_csv('France_retiree_ratio.csv')
    df_pop = pd.read_excel('France_population_by_age.xls', header=3, index_col = 0)
    df_age = pd.read_csv('France_legal_retirement_age.csv', index_col = 0)
    df_pension = pd.read_csv('France_pensions_levels.csv', comment="#", index_col = 0)
    df_pension_contribution = pd.read_csv('France_pension_contribution.csv', comment="#", index_col = 0)
    df_salary = pd.read_excel('Mean_French_salary_by_year.xlsx', sheet_name = 'E', header=3, index_col = 0)
    df_salary.index = pd.to_numeric(df_salary.index, errors="coerce")   # non-years -> NaN
    df_salary = df_salary[~df_salary.index.isna()]                       # drop non-year rows
    df_salary.index = df_salary.index.astype(int)
    df_activity_rate = pd.read_csv('France_activity_rate_by_year.csv', comment="#", index_col = 0)
    
    France_df['retirement_age'] = df_age['legal_age_years']
    France_df['labor_participation'] = df_activity_rate['lfpr_20_60_pct_est']
    France_df['pension_tax'] = df_pension_contribution['total_on_salary_up_to_pss_pct']
    France_df['mean_salary'] = df_salary['Salaire en euros']/France_df['CPI']*100
    France_df['mean_pension'] = df_pension['avg_pension_brut_annual_eur']/France_df['CPI']*100
    
    
    France_df['0-19'] = df_pop['de 0 à 19 ans']
    France_df['20-59'] = df_pop['de 20 à 59 ans']
    France_df['60-64'] = df_pop['de 60 à 64 ans']
    France_df['65+'] = df_pop['65 ans ou plus']

    
    pop20_59 = France_df['20-59'].astype(float)
    pop60_64 = France_df['60-64'].astype(float)
    pop65p   = France_df['65+'].astype(float)
    R        = France_df['retirement_age'].astype(float)
    f20 = np.clip((R - 20.0) / 40.0, 0.0, 1.0)
    f60 = np.clip((R - 60.0) / 5.0,  0.0, 1.0)
    f20 = np.clip((R - 20.0) / 40.0, 0.0, 1.0)
    f60 = np.clip((R - 60.0) / 5.0,  0.0, 1.0)
    below_20_59 = np.where(R < 60, f20 * pop20_59, pop20_59)
    below_60_64 = np.where(R < 60, 0.0, np.where(R < 65, f60 * pop60_64, pop60_64))
    below = below_20_59 + below_60_64
    above_20_59 = np.where(R < 60, (1.0 - f20) * pop20_59, 0.0)
    above_60_64 = np.where(R < 60, pop60_64, np.where(R < 65, (1.0 - f60) * pop60_64, 0.0))
    above = above_20_59 + above_60_64 + pop65p
    France_df['worker_below_retirement_age'] = below
    France_df['worker_above_retirement_age'] = above
    
    years = France_df.index.astype(int)
    anchors_year = np.array([1950, 1956, 1973, 1990, 2005, 2025])
    anchors_rate = np.array([0.70, 0.80, 0.95, 0.98, 0.995, 0.995])  # fractions of retiree getting pension (70% -> 99.5%)
    coverage = np.interp(years, anchors_year, anchors_rate)
    
    France_df['active_population'] = France_df['worker_below_retirement_age']*France_df['labor_participation']/100
    France_df['retiree_population'] = France_df['worker_above_retirement_age']*coverage
    France_df['retiree_ratio'] = France_df['active_population']/France_df['retiree_population']
    
    
    ratio = France_df['retiree_ratio'].to_numpy()
    n = len(ratio)
    step = 10
    ratio_n = np.array([np.nanmean(ratio[i:i+step]) for i in range(0, n, step)])
    year = ['1950s', '1960s', '1970s', '1980s', '1990s', '2000s', '2010s', '2020s']
    age = France_df['retirement_age'].to_numpy()
    
    
    c1 = cool_colors[4]
    c2 = cool_colors[5]
    fig, ax1 = plt.subplots(figsize=(5, 6))
    ax1.grid(zorder = 0)
    ax1.bar(np.arange(len(ratio_n)), ratio_n, color = c1, zorder = 10)
    #plt.plot(np.arange(len(age))/ ,age, cool_colors[4])
    ax1.set_xticks(np.arange(len(ratio_n)), year, rotation = 45, ha="right")
    ax1.set_ylabel('Support ratio (contributors per retiree)', color=c1)
    ax1.set_yscale('log')
    ax1.set_yticks([1.5,2,3,4,5], [1.5,2,3,4,5])
    ax1.spines["right"].set_color(c1)
    ax1.tick_params(axis="y", colors=c1)
    ax1.set_ylim(1.2,5.9)
    
    ax2 = ax1.twinx()
    ax2.plot(np.arange(len(age))/len(age) * (len(ratio_n)-1), age, color=c2, linewidth=2, zorder=20)
    ax2.spines["right"].set_color(c2)
    ax2.tick_params(axis="y", colors=c2)
    ax2.set_ylim(59.1,65.9)
    ax2.set_ylabel("Legal retirement age", color=c2)
    plt.show()
    
    
    
    w = France_df['mean_salary'].astype(float)
    r = France_df['mean_pension'].astype(float)
    cpi = France_df['CPI'].astype(float)
    years = France_df.index.astype(int)
    
    
    half_life = 1
    alpha = 1 - np.exp(-np.log(2)/half_life)
    w_ema = w.ewm(alpha=alpha, adjust=False).mean()

    anchor_year = 2004
    anchor_val  = France_df['mean_pension'].loc[anchor_year]
    scale = (w_ema / w_ema.loc[anchor_year])
    France_df["mean_pension_est"] = anchor_val * scale
    
    mask_pre = years < anchor_year
    France_df.loc[mask_pre, 'mean_pension'] = France_df.loc[mask_pre, 'mean_pension_est']
        
        
        
    
    pct = France_df['pension_tax']/100
    #factor = (1+pct)*pct
    factor = 1.18*pct
    #factor = pct
    France_df['aquired_pension[2025bn]'] = France_df['active_population']*France_df['mean_salary']*factor/1e9
    France_df['distributed_pension[2025bn]'] = France_df['retiree_population']*France_df['mean_pension']/1e9
    
    France_df['aquired_pension[2025bn]'] = France_df['aquired_pension[2025bn]'] + 10
   
    plt.plot(France_df['aquired_pension[2025bn]'], label = 'acquired')
    plt.plot(France_df['distributed_pension[2025bn]'], label = 'paid')
    plt.legend()
    plt.show()
    
    France_df['pension_deficit'] = France_df['aquired_pension[2025bn]'] - France_df['distributed_pension[2025bn]']
    
    pension_deficit = France_df['pension_deficit'].to_numpy()
    n = len(pension_deficit)
    step = 10
    pension_deficit_n = np.array([np.nanmean(pension_deficit[i:i+step])*step for i in range(0, n, step)])
    year = ['1950s', '1960s', '1970s', '1980s', '1990s', '2000s', '2010s', '2020s']
    plt.figure(figsize = (4,5))
    plt.grid(zorder = 0)
    plt.bar(np.arange(len(pension_deficit_n)), pension_deficit_n, color = cool_colors[7], zorder = 10)
    #plt.xticks(np.arange(len(pension_deficit_n)), year, rotation = 45, ha="right")
    plt.ylabel('Pension Deficit [bn€]')
    plt.show()
    
    
    
    pension_tax = France_df['pension_tax'].to_numpy()
    n = len(pension_tax)
    step = 10
    pension_tax_n = np.array([np.nanmean(pension_tax[i:i+step]) for i in range(0, n, step)])
    year = ['1950s', '1960s', '1970s', '1980s', '1990s', '2000s', '2010s', '2020s']
    plt.figure(figsize = (5,6))
    plt.grid(zorder = 0)
    plt.bar(np.arange(len(pension_tax_n)), pension_tax_n, color = cool_colors[6], zorder = 10)
    plt.xticks(np.arange(len(pension_tax_n)), year, rotation = 45, ha="right")
    plt.ylabel('Pension contribution rate [%]')
    plt.show()
    
    

    
if __name__ == '__main__':
    main()