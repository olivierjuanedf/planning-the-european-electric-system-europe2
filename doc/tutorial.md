# To start with: some general documentation

* **PyPSA documentation**: https://pypsa.readthedocs.io/en/latest/ -> normally no more really needed as a lower "layer" of code is here proposed making the connection with PyPSA framework 
* **On ERAA (European Resource Adequacy Assessment)** (2023.2 will be used): https://www.entsoe.eu/outlooks/eraa/ -> to get some informations about the collection, preparation and limitations of data. N.B. (i) **ERAA is a dataset** yearly collected, "built" and made available by ENTSO-E, but also a long-term planning model (and study) to assess... European Resource Adequacy! (ii) **Only an extract of these data is available here**: 2 "Target Years" (2025, 2033) over 4 provided in ERAA2023.2 edition considered here, 6 climatic years over 35 ones available (1982-2016 historical period)

# Tutorial - Long-Term Unit Commitment part

## Tuesday afternoon session: get started with a more robust coding environment

### Running a 1-country (European) UC model by... only playing with 2 JSON files

Now you will be able to **run a Unit Commitment by simply modifying the values in the 2 following files**:
1) *input/long_term_uc/elec-europe_params_to-be-modif.json* -> contain some default values and global parameters (e.g., temporal ones). See appendix for a detailed description
2) *input/long_term_uc/countries/{country}.json* with "country" the name of your considered country -> the values used in this file will overwrite values of preceding file. N.B. In this file not only your own country parameters can be defined, but also the ones of the other countries - typically neighbouring ones. With a specific behaviour whether "solo" or "Europe" mode be considered - as defined in file functional_params/usage_params.json, field "mode" xxx-check-xxx:
- if mode is "solo", all country parameters (for your own country, but also for the rest of them) will be read from your own file {country}.json
- if mode is "Europe", parameters of each country will be extracted from file {country}.json; the rest of the values in this file will not be accounted for. 

Obtained results - in output/ xxx

### Start preparing the "design" of your country/Europe system by playing with this UC tool

Considering different:
* seasons -> by changing **uc_period_start* in file *input/long_term_uc/elec-europe_params_to-be-modif.json*
* xxx


2) **Change values in *elec-europe_params_to-be-modif.json* parameter file** -> you can prepare different European electricity system configurations. Save them under different names; then copy-paste content into *elec-europe_params_to-be-modif.json* to...
3) **Test that execution of *tutorial_long_term_uc\my_little_eur_long_term_uc.py* run properly**: you should get a log "THE END...". If not, the "checkers" should have indicated you some aspects to be corrected in your - modified - parametrization.

**Real runs** (UC model creation and resolution) will come this afternoon! (and after if you are motivated)

## Wednesday morning/afternoon session: on Investment Planning part

# Appendices

## Input data description

**Preliminary remarks**: (i) JSON files used to store dict-like infos. (ii) Must start "directly" with "{" and end with "}". (iii) "null" is used for None in these JSON files. (iv) '.' not allowed in JSON files; use "." instead. (v) Tuples (.) not allowed; use rather lists [.]. 

The ones in folder *input\long_term_uc*; **file by file description**:
- **[NOT TO BE MODIFIED during this practical class]** *elec-europe_eraa-available-values.json*: containing values available in the ERAA extract provided in folder *data/*: 
    - "climatic_years": past historical years weather conditions that are 'projected' on ERAA "target year"
    - "countries": your seven (meta-)countries
    - "aggreg_prod_types": two-level dictionary in format {country name: {(target) year: list of aggregated production types available in the extract of ERAA data}}. N.B. As "aggregated production types" are only used here to simplify the considered model (diminishing its size), availability of such a type means that at least one of the corresponding - more detailed - ERAA production types is available in data
    - "target_years": list of years available here (2025, 2033; identically to the toy example)
    - "intercos": list of interconnection with available data. N.B. Obtained by simple aggregation of ERAA data when multiple sub-zones are present in our (meta-)countries 
- **[NOT TO BE MODIFIED]** *elec-europe_params_fixed.json*: containing parameters... 
    - "aggreg_prod_types_def": **correspondence between "aggregate" production type (the ones that will be used in this class) and the ones - more detailed - in ERAA data**. It will be used in the data reading phase; to simplify (diminish size!) of the used data in this UC exercise
    - "available_climatic_years", "available countries", "available_target_years" (or simply years; "target year" is the used terminology in ERAA): **available values for the dimensions of provided extract of ERAA data**
    - "gps_coordinates": the ones of the capitals excepting meta-countries with coordinates of Rotterdam for "benelux", Madrid for "iberian-peninsula", and Stockholm for "scandinavia". N.B. Only for plotting - very schematic - representation of the "network" associated to your UC model
    - "eraa_edition": edition of ERAA data used - 2023.2 (one/two ERAA editions per year from 2021)

- *elec-europe_params_to-be-modif.json*: containing parameters... **you can play with during this practical class**
    - "selected_climatic_year": to **choose climatic year" considered for UC model (unique deterministic scenario)
    - "selected_countries": to **choose countries** that you would like to be part of your European - copper-plate - long-term UC model. N.B. Following yesterday's toy model test, only Italy is completed at first
    - "selected_agg_prod_types": **per country selection of the (generation unit) aggregate production types** to be part of your model. N.B. (i) Using aggregate production types, i.e. the ones of field "available_aggreg_prod_types" in file *elec-europe_params_fixed.json* (a two-level dictionary, providing per country and year available fields). (ii) Setting a value to "["all"]" will use all aggregate production types corresponding to ERAA data for current run
    - "uc_period_start": **date from which UC optimization period starts; under format "1900/%M/%d"**. Ex.: "1900/1/1" to start from beginning of the year. N.B. "1900" to clearly indicate that a "fictive calendar" (modelling one) be used in ERAA data, with 364 days (to get 52 full weeks... an important granularity for some unit optim., as discussed in class)
    - (optional) "uc_period_end": idem, **end of period; same format**. Default value: period of 9 days starting from "uc_period_start". 

- *input/long_term_uc/countries/{country}.json* XXX
