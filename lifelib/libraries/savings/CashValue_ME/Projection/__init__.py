"""The main Space in the :mod:`~basiclife.BasicTerm_ME` model.

:mod:`~basiclife.BasicTerm_ME.Projection` is the only Space defined
in the :mod:`~basiclife.BasicTerm_ME` model, and it contains
all the logic and data used in the model.

.. rubric:: Parameters and References

(In all the sample code below,
the global variable ``Projection`` refers to the
:mod:`~basiclife.BasicTerm_ME.Projection` Space.)

Attributes:

    model_point_table: All model points as a DataFrame.
        The sample model point data was generated by
        *generate_model_points_with_duration.ipynb* included in the library.
        By default, :func:`model_point` returns this
        entire :attr:`model_point_table`.
        The DataFrame has an index named ``point_id``,
        and has the following columns:

            * ``age_at_entry``
            * ``sex``
            * ``policy_term``
            * ``policy_count``
            * ``sum_assured``
            * ``duration_mth``

        Cells defined in :mod:`~basiclife.BasicTerm_SE.Projection`
        with the same names as these columns return
        the corresponding columns.


        .. code-block::

            >>> Projection.model_poit_table
                       age_at_entry sex  ...  sum_assured  duration_mth
            policy_id                    ...
            1                    47   M  ...       622000             1
            2                    29   M  ...       752000           210
            3                    51   F  ...       799000            15
            4                    32   F  ...       422000           125
            5                    28   M  ...       605000            55
                            ...  ..  ...          ...           ...
            9996                 47   M  ...       827000           157
            9997                 30   M  ...       826000           168
            9998                 45   F  ...       783000           146
            9999                 39   M  ...       302000            11
            10000                22   F  ...       576000           166

            [10000 rows x 6 columns]

        The DataFrame is saved in the Excel file *model_point_table.xlsx*
        placed in the model folder.
        :attr:`model_point_table` is created by
        Projection's `new_pandas`_ method,
        so that the DataFrame is saved in the separate file.
        The DataFrame has the injected attribute
        of ``_mx_dataclident``::

            >>> Projection.model_point_table._mx_dataclient
            <PandasData path='model_point_table.xlsx' filetype='excel'>

        .. seealso::

           * :func:`model_point`
           * :func:`age_at_entry`
           * :func:`sex`
           * :func:`policy_term`
           * :func:`pols_if_init`
           * :func:`sum_assured`
           * :func:`duration_mth`

    premium_table: Premium rate table by entry age and duration as a Series.
        The table is created using :mod:`~basiclife.BasicTerm_M`
        as demonstrated in *create_premium_table.ipynb*.
        The table is stored in *premium_table.xlsx* in the model folder.

        .. code-block::

            >>> Projection.premium_table
            age_at_entry  policy_term
            20            10             0.000046
                          15             0.000052
                          20             0.000057
            21            10             0.000048
                          15             0.000054
                                           ...
            58            15             0.000433
                          20             0.000557
            59            10             0.000362
                          15             0.000471
                          20             0.000609
            Name: premium_rate, Length: 120, dtype: float64

    disc_rate_ann: Annual discount rates by duration as a pandas Series.

        .. code-block::

            >>> Projection.disc_rate_ann
            year
            0      0.00000
            1      0.00555
            2      0.00684
            3      0.00788
            4      0.00866

            146    0.03025
            147    0.03033
            148    0.03041
            149    0.03049
            150    0.03056
            Name: disc_rate_ann, Length: 151, dtype: float64

        The Series is saved in the Excel file *disc_rate_ann.xlsx*
        placed in the model folder.
        :attr:`disc_rate_ann` is created by
        Projection's `new_pandas`_ method,
        so that the Series is saved in the separate file.
        The Series has the injected attribute
        of ``_mx_dataclident``::

            >>> Projection.disc_rate_ann._mx_dataclient
            <PandasData path='disc_rate_ann.xlsx' filetype='excel'>

        .. seealso::

           * :func:`disc_rate_mth`
           * :func:`disc_factors`

    mort_table: Mortality table by age and duration as a DataFrame.
        See *basic_term_sample.xlsx* included in this library
        for how the sample mortality rates are created.

        .. code-block::

            >>> Projection.mort_table
                        0         1         2         3         4         5
            Age
            18   0.000231  0.000254  0.000280  0.000308  0.000338  0.000372
            19   0.000235  0.000259  0.000285  0.000313  0.000345  0.000379
            20   0.000240  0.000264  0.000290  0.000319  0.000351  0.000386
            21   0.000245  0.000269  0.000296  0.000326  0.000359  0.000394
            22   0.000250  0.000275  0.000303  0.000333  0.000367  0.000403
            ..        ...       ...       ...       ...       ...       ...
            116  1.000000  1.000000  1.000000  1.000000  1.000000  1.000000
            117  1.000000  1.000000  1.000000  1.000000  1.000000  1.000000
            118  1.000000  1.000000  1.000000  1.000000  1.000000  1.000000
            119  1.000000  1.000000  1.000000  1.000000  1.000000  1.000000
            120  1.000000  1.000000  1.000000  1.000000  1.000000  1.000000

            [103 rows x 6 columns]

        The DataFrame is saved in the Excel file *mort_table.xlsx*
        placed in the model folder.
        :attr:`mort_table` is created by
        Projection's `new_pandas`_ method,
        so that the DataFrame is saved in the separate file.
        The DataFrame has the injected attribute
        of ``_mx_dataclident``::

            >>> Projection.mort_table._mx_dataclient
            <PandasData path='mort_table.xlsx' filetype='excel'>

        .. seealso::

           * :func:`mort_rate`
           * :func:`mort_rate_mth`

    np: The `numpy`_ module.
    pd: The `pandas`_ module.

.. _numpy:
   https://numpy.org/

.. _pandas:
   https://pandas.pydata.org/

.. _new_pandas:
   https://docs.modelx.io/en/latest/reference/space/generated/modelx.core.space.UserSpace.new_pandas.html

"""

from modelx.serialize.jsonvalues import *

_formula = None

_bases = []

_allow_none = None

_spaces = []

# ---------------------------------------------------------------------------
# Cells

def accum_prem_init_pp():
    return model_point()['accum_prem_init_pp']


def accum_prem_pp(t):
    if t == 0:
        prev = accum_prem_init_pp()

    else:
        prev = accum_prem_pp(t-1)

    return  prev + premium_pp(t)


def age(t):
    """The attained age at time t.

    Defined as::

        age_at_entry() + duration(t)

    .. seealso::

        * :func:`age_at_entry`
        * :func:`duration`

    """
    return age_at_entry() + duration(t)


def age_at_entry():
    """The age at entry of the model points

    The ``age_at_entry`` column of the DataFrame returned by
    :func:`model_point`.
    """
    return model_point()["age_at_entry"]


def av_at(t, timing):
    """Number of policies in-force

    :func:`pols_if_at(t, timing)<pols_if_at>` calculates
    the number of policies in-force at time ``t``.
    The second parameter ``timing`` takes a string value to
    indicate the timing of in-force,
    which is either
    ``"BEF_MAT"``, ``"BEF_NB"`` or ``"BEF_DECR"``.

    .. rubric:: BEF_MAT

    The number of policies in-force before maturity after lapse and death.
    At time 0, the value is read from :func:`pols_if_init`.
    For time > 0, defined as::

        pols_if_at(t-1, "BEF_DECR") - pols_lapse(t-1) - pols_death(t-1)

    .. rubric:: BEF_NB

    The number of policies in-force before new business after maturity.
    Defined as::

        pols_if_at(t, "BEF_MAT") - pols_maturity(t)

    .. rubric:: BEF_DECR

    The number of policies in-force before lapse and death after new business.
    Defined as::

        pols_if_at(t, "BEF_NB") + pols_new_biz(t)

    .. seealso::
        * :func:`pols_if_init`
        * :func:`pols_lapse`
        * :func:`pols_death`
        * :func:`pols_maturity`
        * :func:`pols_new_biz`
        * :func:`pols_if`

    """
    if timing == "BEF_MAT":
        return av_pp_at(t, "BEF_PREM") * pols_if_at(t, "BEF_MAT")

    elif timing == "BEF_NB":
        return av_pp_at(t, "BEF_PREM") * pols_if_at(t, "BEF_NB")

    elif timing == "BEF_FEE":
        return av_pp_at(t, "BEF_FEE") * pols_if_at(t, "BEF_DECR")

    else:
        raise ValueError("invalid timing")


def av_change(t):
    return av_at(t+1, 'BEF_MAT') - av_at(t, 'BEF_MAT')


def av_pp_at(t, timing):
    """Number of policies in-force



    .. rubric:: BEF_INV

    .. rubric:: BEF_FEE


    """
    if timing == "BEF_PREM":
        if t == 0:
            return av_pp_init()
        else:
            return av_pp_at(t-1, "BEF_INV") + inv_income_pp(t-1)

    elif timing == "BEF_FEE":
        return av_pp_at(t, "BEF_PREM") + prem_to_av_pp(t)

    elif timing == "BEF_INV":
        return av_pp_at(t, "BEF_FEE") - maint_fee_pp(t) - coi_pp(t)

    elif timing == "MID_MTH":
        return av_pp_at(t, "BEF_INV") + 0.5 * inv_income_pp(t)

    else:
        raise ValueError("invalid timing")


def av_pp_init():
    return model_point()["av_pp_init"]


def check_av_roll_fwd(t):

    av = (av_at(t, "BEF_NB")
          + prem_to_av(t)
          - maint_fee(t) 
          - coi(t)
          + inv_income(t)
          - claims_from_av(t, "DEATH") 
          - claims_from_av(t, "LAPSE")
          - claims_from_av(t, "MATURITY"))

    return av_at(t+1, "BEF_NB") - av


def check_margin(t):

    return net_cf(t) - margin_expense(t) - margin_mortality(t)


def check_pv_net_cf():
    """Check present value summation

    Check if the present value of :func:`net_cf` matches the
    sum of the present values each cashflows.
    Returns the check result as :obj:`True` or :obj:`False`.

     .. seealso::

        * :func:`net_cf`
        * :func:`pv_net_cf`

    """

    import math
    res = sum(list(net_cf(t) for t in range(proj_len())) * disc_factors()[:proj_len()])

    return math.isclose(res, pv_net_cf())


def claim_pp(t, kind):
    """Claim per policy

    The claim amount per plicy. Defaults to :func:`sum_assured`.
    """

    if kind == "DEATH":
        return np.maximum(sum_assured(), av_pp_at(t, "MID_MTH"))

    elif kind == "LAPSE":
        return av_pp_at(t, "MID_MTH")

    elif kind == "MATURITY":
        return av_pp_at(t, "BEF_PREM")

    else:
        raise ValueError("invalid kind")


def claims(t, kind=None):
    """Claims

    Claims during the period from ``t`` to ``t+1`` defined as::

        claim_pp(t) * pols_death(t)

    .. seealso::

        * :func:`claim_pp`
        * :func:`pols_death`

    """
    if kind == "DEATH":
        return claim_pp(t, "DEATH") * pols_death(t)

    elif kind == "LAPSE":
        return claims_from_av(t, "LAPSE") - surr_charge(t)

    elif kind == "MATURITY":
        return claims_from_av(t, "MATURITY")

    elif kind is None:
        return sum(claims[t, k] for k in ["DEATH", "LAPSE", "MATURITY"])

    else:
        raise ValueError("invalid kind")


def claims_from_av(t, kind):

    if kind == "DEATH":
        return av_pp_at(t, "MID_MTH") * pols_death(t)

    elif kind == "LAPSE":
        return av_pp_at(t, "MID_MTH") * pols_lapse(t)

    elif kind == "MATURITY":
        return av_pp_at(t, "BEF_PREM") * pols_maturity(t)

    else:
        raise ValueError("invalid kind")


def claims_over_av(t):
    return (claim_pp(t, "DEATH") - av_pp_at(t, "MID_MTH")) * pols_death(t)


def coi(t):
    return coi_pp(t) * pols_if_at(t, "BEF_DECR")


def coi_av(t):
    return 1.1 * mort_rate_mth(t)


def coi_pp(t):
    return coi_av(t) * net_amt_at_risk(t)


def commissions(t):
    """Commissions

    By default, 100% premiums for the first year, 0 otherwise.

    .. seealso::

        * :func:`premiums`
        * :func:`duration`

    """
    return 0.05 * premiums(t)


def disc_factors():
    """Discount factors.

    Vector of the discount factors as a Numpy array. Used for calculating
    the present values of cashflows.

    .. seealso::

        :func:`disc_rate_mth`
    """
    return np.array(list((1 + disc_rate_mth()[t])**(-t) for t in range(max_proj_len())))


def disc_rate_mth():
    """Monthly discount rate

    Nummpy array of monthly discount rates from time 0 to :func:`max_proj_len` - 1
    defined as::

        (1 + disc_rate_ann)**(1/12) - 1

    .. seealso::

        :func:`disc_rate_ann`

    """
    return np.array(list((1 + disc_rate_ann[t//12])**(1/12) - 1 for t in range(max_proj_len())))


def duration(t):
    """Duration of model points at ``t`` in years

    .. seealso:: :func:`duration_mth`

    """
    return duration_mth(t) //12


def duration_mth(t):
    """Duration of model points at ``t`` in months

    Indicates how many months the policies have been in-force at ``t``.
    The initial values at time 0 are read from the ``duration_mth`` column in
    :attr:`model_point_table` through :func:`model_point`.
    Increments by 1 as ``t`` increments.
    Negative values of :func:`duration_mth` indicate future new business
    policies. For example, If the :func:`duration_mth` is
    -15 at time 0, the model point is issued at ``t=15``.

    .. seealso:: :func:`model_point`

    """

    if t == 0:
        return model_point()['duration_mth']
    else:
        return duration_mth(t-1) + 1


def expense_acq():
    """Acquisition expense per policy

    ``300`` by default.
    """
    return 5000


def expense_maint():
    """Annual maintenance expense per policy

    ``60`` by default.
    """
    return 500


def expenses(t):
    """Expenses

    Expenses during the period from ``t`` to ``t+1``
    defined as the sum of acquisition expenses and maintenance expenses.
    The acquisition expenses are modeled as :func:`expense_acq`
    times :func:`pols_new_biz`.
    The maintenance expenses are modeled as :func:`expense_maint`
    times :func:`inflation_factor` times :func:`pols_if_at` before
    decrement.

    .. seealso::

        * :func:`expense_acq`
        * :func:`expense_maint`
        * :func:`inflation_factor`
        * :func:`pols_new_biz`
        * :func:`pols_if_at`
    """

    return expense_acq() * pols_new_biz(t) \
        + pols_if_at(t, "BEF_DECR") * expense_maint()/12 * inflation_factor(t)


def has_surr_charge():
    return model_point()['has_surr_charge']


def inflation_factor(t):
    """The inflation factor at time t

    .. seealso::

        * :func:`inflation_rate`

    """
    return (1 + inflation_rate())**(t/12)


def inflation_rate():
    """Inflation rate"""
    return 0.01


def inv_income(t):
    return (inv_income_pp(t) * pols_if_at(t+1, "BEF_MAT")
            + 0.5 * inv_income_pp(t) * (pols_death(t) + pols_lapse(t)))


def inv_income_pp(t):
    return inv_return_mth(t) * av_pp_at(t, "BEF_INV")


def inv_return_mth(t):
    return inv_return_table()[scen_id, t]


def inv_return_table():
    return np.exp(0.02 * 1/12 + 0.03 * (1/12)**0.5 * std_norm_rand) - 1


def is_wl():
    return model_point()['is_wl']


def lapse_rate(t):
    """Lapse rate

    By default, the lapse rate assumption is defined by duration as::

        max(0.1 - 0.02 * duration(t), 0.02)

    .. seealso::

        :func:`duration`

    """
    return np.maximum(0.1 - 0.02 * duration(t), 0.02)


def load_prem_rate():
    """Loading per premium

    .. note::
       This cells is not used by default.

    ``0.5`` by default.

    .. seealso::

        * :func:`premium_pp`

    """
    return model_point()['load_prem_rate']


def loading_prem():
    """Loading per premium

    .. note::
       This cells is not used by default.

    ``0.5`` by default.

    .. seealso::

        * :func:`premium_pp`

    """
    return 0.5


def maint_fee(t):
    return maint_fee_pp(t) * pols_if_at(t, "BEF_DECR")


def maint_fee_av():
    """Maintenance fee per account value
    """
    return 0.01 / 12


def maint_fee_pp(t):
    return maint_fee_av() * av_pp_at(t, "BEF_FEE")


def margin_expense(t):

    return (load_prem_rate()* premium_pp(t) * pols_if_at(t, "BEF_DECR")
            + surr_charge(t)
            + maint_fee(t)
            - commissions(t)
            - expenses(t))


def margin_mortality(t):
    return coi(t) - claims_over_av(t)


max_proj_len = lambda: max(proj_len())
"""The max of all projection lengths

Defined as ``max(proj_len())``

.. seealso::
    :func:`proj_len`
"""

def model_point():
    """Target model points

    Returns as a DataFrame the model points to be in the scope of calculation.
    By default, this Cells returns the entire :attr:`model_point_table`
    without change.
    To select model points, change this formula so that this
    Cells returns a DataFrame that contains only the selected model points.

    Examples:
        To select only the model point 1::

            def model_point():
                return model_point_table.loc[1:1]

        To select model points whose ages at entry are 40 or greater::

            def model_point():
                return model_point_table[model_point_table["age_at_entry"] >= 40]

    Note that the shape of the returned DataFrame must be the
    same as the original DataFrame, i.e. :attr:`model_point_table`.

    When selecting only one model point, make sure the
    returned object is a DataFrame, not a Series, as seen in the example
    above where ``model_point_table.loc[1:1]`` is specified
    instead of ``model_point_table.loc[1]``.

    Be careful not to accidentally change the original table.
    """
    return model_point_table_ext() #.loc[1:5000]


def model_point_table_ext():
    return model_point_table.join(product_spec_table, on='spec_id')


def mort_rate(t):
    """Mortality rate to be applied at time t

    Returns a Series of the mortality rates to be applied at time t.
    The index of the Series is ``point_id``,
    copied from :func:`model_point`.

    .. seealso::

       * :func:`mort_table_reindexed`
       * :func:`mort_rate_mth`
       * :func:`model_point`

    """

    # mi is a MultiIndex whose values are
    # pairs of age at t and duration at t capped at 5 for all the model points.

    # ``mort_table_reindexed().reindex(mi, fill_value=0)`` returns
    # a Series of mortality rates whose indexes match the MultiIndex values.
    # The ``set_axis`` method replace the MultiIndex with ``point_id``

    mi = pd.MultiIndex.from_arrays([age(t), np.minimum(duration(t), 5)])
    return mort_table_reindexed().reindex(
        mi, fill_value=0).set_axis(model_point().index, inplace=False)


def mort_rate_mth(t):
    """Monthly mortality rate to be applied at time t

    .. seealso::

       * :attr:`mort_table`
       * :func:`mort_rate`

    """
    return 1-(1- mort_rate(t))**(1/12)


def mort_table_last_age():

    for i in mort_table.index:
        mort_i = mort_table.loc[i]
        if (mort_i == 1).all():
            return i

    return i


def mort_table_reindexed():
    """MultiIndexed mortality table

    Returns a Series of mortlity rates reshaped from :attr:`mort_table`.
    The returned Series is indexed by age and duration capped at 5.

    """
    result = []
    for col in mort_table.columns:
        df = mort_table[[col]]
        df = df.assign(Duration=int(col)).set_index('Duration', append=True)[col]
        result.append(df)

    return pd.concat(result)


def net_amt_at_risk(t):
    return np.maximum(sum_assured() - av_pp_at(t, 'BEF_FEE'), 0)


def net_cf(t):
    """Net cashflow

    Net cashflow for the period from ``t`` to ``t+1`` defined as::

        premiums(t) - claims(t) - expenses(t) - commissions(t)

    .. seealso::

        * :func:`premiums`
        * :func:`claims`
        * :func:`expenses`
        * :func:`commissions`

    """
    return premiums(t) - claims(t) - expenses(t) - commissions(t)


def net_premium_pp():
    """Net premium per policy

    .. note::
       This cells is not used by default.

    The net premium per policy is defined so that
    the present value of net premiums equates to the present value of
    claims::

        pv_claims() / pv_pols_if()

    .. seealso::

        * :func:`pv_claims`
        * :func:`pv_pols_if`

    """
    with np.errstate(divide='ignore', invalid='ignore'):
        return np.nan_to_num(pv_claims() / pv_pols_if())


def policy_term():
    """The policy term of the model points.

    The ``policy_term`` column of the DataFrame returned by
    :func:`model_point`.
    """

    return (is_wl() * (mort_table_last_age() - age_at_entry()) 
            + (is_wl() == False) * model_point()["policy_term"])


def pols_death(t):
    """Number of death occurring at time t"""
    return pols_if_at(t, "BEF_DECR") * mort_rate_mth(t)


def pols_if(t):
    """Number of policies in-force

    :func:`pols_if(t)<pols_if>` is an alias
    for :func:`pols_if_at(t, "BEF_MAT")<pols_if_at>`.

    .. seealso::
        * :func:`pols_if_at`

    """
    return pols_if_at(t, "BEF_MAT")


def pols_if_at(t, timing):
    """Number of policies in-force

    :func:`pols_if_at(t, timing)<pols_if_at>` calculates
    the number of policies in-force at time ``t``.
    The second parameter ``timing`` takes a string value to
    indicate the timing of in-force,
    which is either
    ``"BEF_MAT"``, ``"BEF_NB"`` or ``"BEF_DECR"``.

    .. rubric:: BEF_MAT

    The number of policies in-force before maturity after lapse and death.
    At time 0, the value is read from :func:`pols_if_init`.
    For time > 0, defined as::

        pols_if_at(t-1, "BEF_DECR") - pols_lapse(t-1) - pols_death(t-1)

    .. rubric:: BEF_NB

    The number of policies in-force before new business after maturity.
    Defined as::

        pols_if_at(t, "BEF_MAT") - pols_maturity(t)

    .. rubric:: BEF_DECR

    The number of policies in-force before lapse and death after new business.
    Defined as::

        pols_if_at(t, "BEF_NB") + pols_new_biz(t)

    .. seealso::
        * :func:`pols_if_init`
        * :func:`pols_lapse`
        * :func:`pols_death`
        * :func:`pols_maturity`
        * :func:`pols_new_biz`
        * :func:`pols_if`

    """
    if timing == "BEF_MAT":

        if t == 0:
            return pols_if_init()
        else:
            return pols_if_at(t-1, "BEF_DECR") - pols_lapse(t-1) - pols_death(t-1)

    elif timing == "BEF_NB":

        return pols_if_at(t, "BEF_MAT") - pols_maturity(t)

    elif timing == "BEF_DECR":

        return pols_if_at(t, "BEF_NB") + pols_new_biz(t)

    else:
        raise ValueError("invalid timing")


def pols_if_init():
    """Initial number of policies in-force

    Number of in-force policies at time 0 referenced from
    :func:`pols_if_at(0, "BEF_MAT")<pols_if_at>`.
    """
    return model_point()["policy_count"].where(duration_mth(0) > 0, other=0)


def pols_lapse(t):
    """Number of lapse occurring at time t

    .. seealso::
        * :func:`pols_if_at`
        * :func:`lapse_rate`

    """
    return (pols_if_at(t, "BEF_DECR") - pols_death(t)) * (1-(1 - lapse_rate(t))**(1/12))


def pols_maturity(t):
    """Number of maturing policies

    The policy maturity occurs when
    :func:`duration_mth` equals 12 times :func:`policy_term`.
    The amount is equal to :func:`pols_if_at(t, "BEF_MAT")<pols_if_at>`.

    otherwise ``0``.
    """
    return (duration_mth(t) == policy_term() * 12) * pols_if_at(t, "BEF_MAT")


def pols_new_biz(t):
    """Number of new business policies

    The number of new business policies.
    The value :func:`duration_mth(0)<duration_mth>`
    for the selected model point is read from the ``policy_count`` column in
    :func:`model_point`. If the value is 0 or negative,
    the model point is new business at t=0 or at t when
    :func:`duration_mth(t)<duration_mth>` is 0, and the
    :func:`pols_new_biz(t)<pols_new_biz>` is read from the ``policy_count``
    in :func:`model_point`.

    .. seealso::
        * :func:`model_point`

    """
    return model_point()['policy_count'].where(duration_mth(t) == 0, other=0)


def prem_to_av(t):

    return (1 - load_prem_rate()) * premium_pp(t) * pols_if_at(t, "BEF_DECR")


def prem_to_av_pp(t):
    return (1 - load_prem_rate()) * premium_pp(t)


def premium_pp(t):
    """Monthly premium per policy

    A Series of monthly premiums per policy for all the model points,
    calculated as::

        np.around(sum_assured() * prem_rates, 2)

    where the ``prem_rates`` is a Series of premium rates
    retrieved from :attr:`premium_table`.

    .. seealso::

        * :attr:`premium_table`
        * :func:`model_point`
        * :func:`age_at_entry`
        * :func:`policy_term`

    """


    # mi is a MultiIndex whose values are
    # pairs of issue ages and policy terms for all the model points.

    # ``premium_table.reindex(mi)`` returns
    # a Series of premium rates whose indexes match the MultiIndex values.
    # The ``set_axis`` method replace the MultiIndex with ``point_id``

    # mi = pd.MultiIndex.from_arrays([age_at_entry(), policy_term()])
    # prem_rates = premium_table.reindex(mi).set_axis(
    #     model_point().index, inplace=False)
    # return np.around(sum_assured() * prem_rates, 2)


    sp = (premium_type() == 'SINGLE') * (duration_mth(t) == 0) * model_point()['premium_pp']
    lp = (premium_type() == 'LEVEL') * (duration_mth(t) < 12 * policy_term()) * model_point()['premium_pp']
    return sp + lp


def premium_type():
    return model_point()['premium_type']


def premiums(t):
    """Premium income

    Premium income during the period from ``t`` to ``t+1`` defined as::

        premium_pp() * pols_if_at(t, "BEF_DECR")

    .. seealso::

        * :func:`premium_pp`
        * :func:`pols_if_at`

    """
    return premium_pp(t) * pols_if_at(t, "BEF_DECR")


def proj_len():
    """Projection length in months

    :func:`proj_len` returns how many months the projection
    for each model point should be carried out
    for all the model point. Defined as::

        np.maximum(12 * policy_term() - duration_mth(0) + 1, 0)

    Since this model carries out projections for all the model points
    simultaneously, the projections are actually carried out
    from 0 to :attr:`max_proj_len` for all the model points.

    .. seealso::

        * :func:`policy_term`
        * :func:`duration_mth`
        * :attr:`max_proj_len`

    """
    return np.maximum(12 * policy_term() - duration_mth(0) + 1, 0)


def pv_av_change():
    """Present value of claims

    .. seealso::

        * :func:`claims`

    """
    result = np.array(list(av_change(t) for t in range(max_proj_len()))).transpose()

    return result @ disc_factors()[:max_proj_len()]


def pv_claims(kind=None):
    """Present value of claims

    .. seealso::

        * :func:`claims`

    """
    cl = np.array(list(claims(t, kind) for t in range(max_proj_len()))).transpose()

    return cl @ disc_factors()[:max_proj_len()]


def pv_commissions():
    """Present value of commissions

    .. seealso::

        * :func:`expenses`

    """
    result = np.array(list(commissions(t) for t in range(max_proj_len()))).transpose()

    return result @ disc_factors()[:max_proj_len()]


def pv_expenses():
    """Present value of expenses

    .. seealso::

        * :func:`expenses`

    """
    result = np.array(list(expenses(t) for t in range(max_proj_len()))).transpose()

    return result @ disc_factors()[:max_proj_len()]


def pv_inv_income():
    """Present value of policies in-force

    .. note::
       This cells is not used by default.

    The discounted sum of the number of in-force policies at each month.
    It is used as the annuity factor for calculating :func:`net_premium_pp`.

    """
    result = np.array(list(inv_income(t) for t in range(max_proj_len()))).transpose()

    return result @ disc_factors()[:max_proj_len()]


def pv_net_cf():
    """Present value of net cashflows.

    Defined as::

        pv_premiums() - pv_claims() - pv_expenses() - pv_commissions()

    .. seealso::

        * :func:`pv_premiums`
        * :func:`pv_claims`
        * :func:`pv_expenses`
        * :func:`pv_commissions`

    """
    return (pv_premiums() 
            + pv_inv_income() 
            - pv_claims() 
            - pv_expenses() 
            - pv_commissions() 
            - pv_av_change())


def pv_pols_if():
    """Present value of policies in-force

    .. note::
       This cells is not used by default.

    The discounted sum of the number of in-force policies at each month.
    It is used as the annuity factor for calculating :func:`net_premium_pp`.

    """
    result = np.array(list(pols_if_at(t, "BEF_DECR") for t in range(max_proj_len()))).transpose()

    return result @ disc_factors()[:max_proj_len()]


def pv_premiums():
    """Present value of premiums

    .. seealso::

        * :func:`premiums`

    """
    result = np.array(list(premiums(t) for t in range(max_proj_len()))).transpose()

    return result @ disc_factors()[:max_proj_len()]


def result_cf():
    """Result table of cashflows

    .. seealso::

       * :func:`premiums`
       * :func:`claims`
       * :func:`expenses`
       * :func:`commissions`
       * :func:`net_cf`

    """

    t_len = range(max_proj_len())

    data = {
        "Premiums": [sum(premiums(t)) for t in t_len],
        "Claims": [sum(claims(t)) for t in t_len],
        "Expenses": [sum(expenses(t)) for t in t_len],
        "Commissions": [sum(commissions(t)) for t in t_len],
        "Net Cashflow": [sum(net_cf(t)) for t in t_len]
    }

    return pd.DataFrame(data, index=t_len)


def result_pols():
    """Result table of policy decrement

    .. seealso::

       * :func:`pols_if`
       * :func:`pols_maturity`
       * :func:`pols_new_biz`
       * :func:`pols_death`
       * :func:`pols_lapse`

    """

    t_len = range(max_proj_len())

    data = {
        "pols_if": [sum(pols_if(t)) for t in t_len],
        "pols_maturity": [sum(pols_maturity(t)) for t in t_len],
        "pols_new_biz": [sum(pols_new_biz(t)) for t in t_len],
        "pols_death": [sum(pols_death(t)) for t in t_len],
        "pols_lapse": [sum(pols_lapse(t)) for t in t_len]
    }

    return pd.DataFrame(data, index=t_len)


def result_pv():
    """Result table of present value of cashflows

    .. seealso::

       * :func:`pv_premiums`
       * :func:`pv_claims`
       * :func:`pv_expenses`
       * :func:`pv_commissions`
       * :func:`pv_net_cf`

    """

    data = {
            "Premiums": pv_premiums(), 
            "Death": pv_claims("DEATH"),
            "Surrender": pv_claims("LAPSE"),
            "Maturity": pv_claims("MATURITY"),
            "Expenses": pv_expenses(), 
            "Commissions": pv_commissions(), 
            "Investment Income": pv_inv_income(),
            "Change in AV": pv_av_change(),
            "Net Cashflow": pv_net_cf()
        }

    return pd.DataFrame.from_dict(data)


def sex():
    """The sex of the model points

    .. note::
       This cells is not used by default.

    The ``sex`` column of the DataFrame returned by
    :func:`model_point`.
    """
    return model_point()["sex"]


def sum_assured():
    """The sum assured of the model points

    The ``sum_assured`` column of the DataFrame returned by
    :func:`model_point`.
    """
    return model_point()['sum_assured']


def surr_charge(t):
    return surr_charge_av(t) * av_pp_at(t, "MID_MTH") * pols_lapse(t)


def surr_charge_av(t):
    # if has_surr_charge():

    #     surr_rates = surr_charge_table[surr_charge_id()]
    #     max_idx = max(surr_rates.index)
    #     idx = duration(t) if duration(t) <= max_idx else max_idx
    #     return surr_rates[idx]

    # else:
    #     return 0

    idx = pd.MultiIndex.from_arrays(
        [has_surr_charge() * surr_charge_id(),
         np.minimum(duration(t), surr_charge_max_idx())])

    return surr_charge_table_stacked().reindex(idx, fill_value=0).set_axis(
        model_point().index, inplace=False)


def surr_charge_id():
    return model_point()['surr_charge_id']


def surr_charge_table_stacked():
    return surr_charge_table.stack().reorder_levels([1, 0]).sort_index()


def surr_charge_max_idx():
    return max(surr_charge_table.index)


# ---------------------------------------------------------------------------
# References

disc_rate_ann = ("DataClient", 2387125989680)

mort_table = ("DataClient", 2387126202864)

np = ("Module", "numpy")

pd = ("Module", "pandas")

std_norm_rand = ("DataClient", 2387147354272)

surr_charge_table = ("DataClient", 2387147861632)

product_spec_table = ("DataClient", 2387123660304)

model_point_samples = ("DataClient", 2387125990880)

model_point_all = ("DataClient", 2387126154384)

scen_id = 1

model_point_table = ("DataClient", 2387125990880)