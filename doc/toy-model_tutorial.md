# Monday afternoon session tutorial: start simple, with a "toy model" (of a unique country Unit Commitment model)

This **session exercise consists in**:
* **Adapting both scripts** *my_toy_ex_italy.py* and associated *long_term_uc/toy_model_params/italy_parameters.py*
* **To model in PyPSA a simple 1-country (the one you are responsible for) *Unit Commitment* (UC) problem**. N.B. Tuesday's theoretical session will explain this UC problem in more details; for now take it as answering to the question "how to satisfy electricity demand at minimal cost by optimizing production decisions of available generation assets?"

You can **proceed in order**:
1. **Read the two example scripts above**, following comments in them to understand the main stages when writing a PyPSA model
2. **Copy/paste the two following scripts and rename them** *my_toy_ex_{country}.py* and *long_term_uc/toy_model_params/{country}_parameters.py* - with "country" the name of your country (or create two new ones with same names)
2. **Considering installed generation assets data from file** *data/generation_capas/generation-capa_{year}_{country}.csv* - with "year" the one considered in this simulation, update values list of generator (dictionaries) in list of function *get_generators* in script *{country}_parameters.py*. This mainly consists in: (i) Extracting from Italy case the assets that are also present in your country, and only adapt "p_nom" value based on *generation-capa_{year}_{country}.csv* file; (ii) Complement the obtained list with assets in *generation-capa_{year}_{country}.csv* and not in Italy ex. - looking at file *long_term_uc/toy_model_params/ex_italy-complem_parameters.py* - again setting "p_nom" based on values in generation capas csv file.

Note that **technology names do not directly coincide between the "level" used in this exercise** (see XXX JSON file) **and data found in csv files** (here, the one with generation capacities). For some cases an aggregation from names in csv files to the ones in PyPSA will be needed; the correspondence to be used for that is provided at the very beginning of *my_toy_ex_italy.py" script (see global constant AGG_PROD_TYPES_DEF).

Based on the **two following websites**:

* PyPSA documentation: https://pypsa.readthedocs.io/en/latest/
* ERAA documentation (2023.2 will be used): https://www.entsoe.eu/outlooks/eraa/

and an **"extract" of the first one regarding generator objects given below** you may be able to build your own country "Unit Commitment" model.

**Main parameters to define PyPSA generator objects** - that could be sufficient in this course:
* (required) **bus** -> to which the generator is attached. **Format**: str
* (required) **name** -> of your generation asset (used as id). In the proposed piece of code format {technology type}_{country name} is used (ex: "coal_poland"). **Format**: str
* (optional) **carrier** -> mainly primary energy carriers. Can be also used to model CO2eq. emissions. **Format**: str
* (optional) **committable** -> with "dynamics constraints" accounted for? **Format**: boolean. **Default**: False
* (optional) **efficiency** -> of your generator - as a % (related to losses in "generation process"). **Format**: float. **Default**: 1
* (optional) **marginal_cost**. **Format**: float
* (optional) **"p_nom"** -> capacity (a power, in MW). **Format**: int. **Default**: 0
* (optional) **p_min_pu** -> minimal power level - as % of capacity ("pu" stands for "per unit"), set to 0 to start simple. **Format**: float or vector (list or NumPy array). **Default**: 0
* (optional) **p_max_pu** -> idem, maximal power. Can integrate "Capacity Factors" (or maintenance); in this case it can be variable in time. **Format**: float or vector (list or NumPy array). **Default**: 1

TODO: available values in JSON file xxx