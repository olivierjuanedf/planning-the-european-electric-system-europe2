# Monday afternoon session tutorial: start simple, with a "toy model" (of a unique country Unit Commitment model)

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