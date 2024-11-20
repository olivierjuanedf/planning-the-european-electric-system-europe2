# To start with: some general documentation

* **PyPSA documentation**: https://pypsa.readthedocs.io/en/latest/ -> normally no more really needed as a lower "layer" of code is here proposed making the connection with PyPSA framework 
* **On ERAA (European Resource Adequacy Assessment)** (2023.2 will be used): https://www.entsoe.eu/outlooks/eraa/ -> to get some informations about the collection, preparation and limitations of data. N.B. (i) **ERAA is a dataset** yearly collected, "built" and made available by ENTSO-E, but also a long-term planning model (and study) to assess... European Resource Adequacy! (ii) **Only an extract of these data is available here**: 2 "Target Years" (2025, 2033) over 4 provided in ERAA2023.2 edition considered here, 6 climatic years over 35 ones available (1982-2016 historical period)

# Tutorial - Long-Term Unit Commitment part

## Tuesday afternoon session: get started with a more robust coding environment

### Running a 1-country (European) UC model by... only playing with 2 JSON files

Now you will be able to **run a Unit Commitment by simply modifying the values in the 2 following files**:
1) *input/long_term_uc/elec-europe_params_to-be-modif.json* -> contain **some default values and global parameters** (e.g., temporal ones - with the UC period to be simulated). See appendix for a detailed description of the different fields in this file
2) *input/long_term_uc/countries/{country}.json* with "country" the name of your considered country -> the **values used in this file will overwrite values of preceding file**. This is to make your own country choice. N.B. In this file not only your own country parameters can be defined, but also the ones of the other countries - typically neighbouring ones. **Importantly, note two distinguished behaviours of the code, whether "solo" or "Europe" mode be considered** - as defined in file *input/functional_params/usage_params.json*, field "mode":
- if mode is set to **"solo", all country parameters (for your own country, but also for the rest of them) will be read from your own file *{country}.json***
- if mode is **"europe", parameters of each country will be extracted from file *{country}.json*; the rest of the values in this file being not be accounted for**. 

**Open and run *my_little_eur_long_term_uc.py***: you should get a log "THE END...". If not, the "checkers" should have indicated you some aspects to be corrected in your - modified - parametrization. N.B. The only remaining bug that has been observed in class is when you have assets that can both produce and consume for the cumulated production plot (not possible in this case... will be corrected soon); however the .csv results data will have been saved. Now run stops correctly - with an explicit error message - when optimisation problem solved by PyPSA does not have "optimal" status; in this case no output data (neither figures) are obtained. 

### And directly getting output results for an extended analysis

Obtained data (resp. plotted figures) results are obtained in *output/long_term_uc/data* (resp. *output/long_term_uc/figures*) folders.

In detail, and **except if the resolution of PyPSA optimization model was not successful** (you did not get the "optimal" resolution status; and the execution will be stopped with a log clearly indicating it), it will give you: 
* (*data/* subfolder) optimal production of all generators considered in Europe, in a .csv file. N.B. The suffix of this file is indicating the year, climatic year ("cy") and the date of UC start period
* (*data/* subfolder) "prices" for all countries considered in Europe, in a .csv file. N.B. Idem
* (*figures/* subfolder) a "cumulated vision" of the production, in a .png file
* (*figures/* subfolder) price curves, for the different countries

### Start preparing the "design" of your country/Europe system by playing with this UC tool

Based on the numeric results obtained for each of the simulated configurations you can start "designing" (i.e. sizing the capacities) you own country (if in "solo" mode)/European ("Europe" mode) system. Indeed, considering different:
* **seasons** -> by changing **uc_period_start* in file *input/long_term_uc/elec-europe_params_to-be-modif.json*. **Question**: how would you select a few typical, or extreme, weeks to be considered to size your system? Is it possible to do it *ex-ante*, i.e. only looking at input data (e.g., demand, RES sources CF, installed generation capacities) or do you need some iterative process with UC runs to do that?
* **(target) years** -> using 2025 or 2033
* **climatic years** -> how sensitive are your results to the choice of this parameter? in combination with the ones of the season (associated period)? **Question** how would you choose one/a few scenarios used for your investment planning decision-making?
* **interconnection capacities** -> how are your results sensitive to the limit on the flows that can be exchanged between your 7 countries? N.B. Playing with parameter "interco_capas_updated_values" in file *input/long_term_uc/elec-europe_params_to-be-modif.json* can give you some preliminar insights on this
* (in solo mode) **What if... my neighbouring countries..." -> how are your individual country results sensitive to the decisions made by your neighbours? N.B. In solo mode you can exactly simulate the cases to try answering this question, by testing different configurations for your neighbours - in your own *{country}.json* file

## Wednesday morning/afternoon session: on Investment Planning part

You can start answering the following questions:
* Can you **"progressively" make failure disappear** by investing in your country / Europe? Can be done iteratively by running: (i) A first UC configuration then; (ii) Observing when + how big is failure then; (iii) Adapting investments to make these values decrease; etc. 
* Can you **find an "acceptable" trade-off between level of investment (€) and failure** (total "non-served" energy - to final consumers; or number of hours with failure)?

A lot more that you can discuss in thiese sessions with Jean-Yves BOURMAUD, Alexis LEBEAU, and Cécile ROTTNER.

# Appendices

## Input data description

**Preliminary remarks**: (i) JSON files used to store dict-like infos. (ii) Must start "directly" with "{" and end with "}". (iii) "null" is used for None in these JSON files. (iv) '.' not allowed in JSON files; use "." instead. (v) Tuples (.) not allowed; use rather lists [.]. 

The ones in folder *input\long_term_uc*; **file by file description**:
- **[NOT TO BE MODIFIED during this practical class]** *elec-europe_eraa-available-values.json*: containing values available in the ERAA extract provided in folder *data/*: 
    - "climatic_years": **past historical years weather conditions** that are 'projected' on ERAA "target year" (*list of int* values)
    - "countries": your seven **(meta-)countries**, the only ones for which ERAA data are made available in this code environment (*list of str*)
    - "aggreg_prod_types": **per country and year aggregated production types** (two-level dictionary in format {country name: {(target) year: list of aggregated production types available in the extract of ERAA data}}). N.B. As "aggregated production types" are only used here to simplify the considered model (diminishing its size), availability of such a type means that at least one of the corresponding - more detailed - ERAA production types is available in data
    - "target_years": list of **years available** here - 2025 or 2033 here, identically to the toy example (*list of int*)
    - "intercos": list of **interconnection with available data** (*list of str*, with str under format {origin country}2{destination country}). N.B. Obtained by simple aggregation of ERAA data when multiple sub-zones are present in our (meta-)countries
      
- **[NOT TO BE MODIFIED]** *elec-europe_params_fixed.json*: containing parameters... 
    - "aggreg_prod_types_def": **correspondence between "aggregate" production type (the ones that will be used in this class) and the ones - more detailed - in ERAA data**. It will be used in the data reading phase; to simplify (diminish size!) of the used data in this UC exercise
    - "available_climatic_years", "available countries", "available_target_years" (or simply years; "target year" is the used terminology in ERAA): **available values for the dimensions of provided extract of ERAA data**
    - "gps_coordinates": the ones of the capitals excepting meta-countries with coordinates of Rotterdam for "benelux", Madrid for "iberian-peninsula", and Stockholm for "scandinavia". N.B. Only for plotting - very schematic - representation of the "network" associated to your UC model
    - "eraa_edition": edition of ERAA data used - 2023.2 (one/two ERAA editions per year from 2021)

- *elec-europe_params_to-be-modif.json*: containing parameters... 
    - "selected_climatic_year": to **choose climatic year" considered for UC model (unique deterministic scenario, *int* value)
    - "selected_countries": to **choose countries** that you would like to be part of your European - copper-plate - long-term UC model (*list of string*; that must be in the set of considered countries for this class). N.B. Following yesterday's toy model test, only Italy is completed at first
    - "slected_target_year": to choose the ERAA (target) **year** to be simulated (*int*, either 2025 or 2033)
    - "selected_prod_types": **per country selection of the (generation unit) aggregate production types** to be part of your model. N.B. (i) Using aggregate production types, i.e. the ones of field "available_aggreg_prod_types" in file *elec-europe_params_fixed.json* (a two-level dictionary, providing per country and year available fields). (ii) Setting a value to "["all"]" will use all aggregate production types corresponding to ERAA data for current run
    - "uc_period_start": **date from which UC optimization period starts; under format "1900/%M/%d"**. Ex.: "1900/1/1" to start from beginning of the year. N.B. "1900" to clearly indicate that a "fictive calendar" (modelling one) be used in ERAA data, with 364 days (to get 52 full weeks... an important granularity for some unit optim., as discussed in class)
    - (optional) "uc_period_end": idem, **end of period; same format**. Default value: period of 9 days starting from "uc_period_start".
    -  "failure_power_capa": **capacity of the failure - fictive - asset** considered (*non-negative float*). N.B. Common to all countries
    -  "failure_penalty": **failure asset variable cost**, or more standardly "penalty" (*non-negative float*). N.B. Typically set to a "very big" value, so that this asset be used as a last recourse - i.e. after having used all other production units at maximal power available
    -  "interco_capas_updated_values": **values for the interconnection capacities**; to be used to overwrite - or complete - ERAA data (*dictionary with str keys and on-negative float values*, with keys under format {origin country}2{destination country}). Ex:  {"france2poland": 10, "france2scandinavia": 0, "italy2iberian-peninsula": 0} will set interconnection capacity from France to Poland to 10GW (very fictive!) and from France to both Scandinavia et Iberian-Peninsula to 0GW. Note that regarding the France to Scandinavia link this value will be useless as there is no ERAA data associated to this link; in turn our code already used 0GW as the value. 

- *input/long_term_uc/countries/{country}.json*: containing parameters
    - "team": **name of your team**, i.e. name of the country you are "responsible for" (*str*, that Must be in the set {"benelux", "germany", "iberian-peninsula", "poland", "scandinavia"} - use lower letters)
    - "selected_prod_types": list of **production types - using aggregate classes** defined in *input/long_term_uc/elec-europe_eraa_available-values.json* file/field "aggreg_prod_types" (*dictionary* {country name: list of aggreg. production types to be selected for run}). Ex: {"france": ["nuclear", "failure"], "germany": ["coal", "wind_onshore", "wind_offshore"]} will lead to a run with only nuclear and failure (resp. coal and wind on-/off-shore) units in France (resp. Germany) 
    - "updated_capacities_prod_types": **aggreg. production units for which you want to update the capacities - versus the ones in ERAA data**, and for the considered (target) year (*dictionary* {country: aggreg. prod. type: updated capacity}). Ex: {"france": {"nuclear": 100000, "failure": 100000} will update French nuclear (aggreg.) capacity to 100GW and set a big failure asset of the same capacity. In this exemple, capacities for Germany will be taken as given in ERAA data. 
