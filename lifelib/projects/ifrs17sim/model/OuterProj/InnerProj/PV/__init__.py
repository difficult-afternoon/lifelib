"""Present values of cashflows

This Space is a child Space of :mod:`~ifrs17sim.model.OuterProj.InnerProj`,
and calculates present values of cashflows.

This Space is parameterized with ``t_rate``, which indicates that
the discount rates at time ``t_rate`` are used for discounting.

.. blockdiag::

   blockdiag {
     default_node_color="#D5E8D4";
     default_linecolor="#628E47";
     ifrs17sim [shape=roundedbox, linecolor="#7B99C5", color="#D4E8FC", width=96]
     ifrs17sim <- "OuterProj\n[PolicyID, ScenID=1]" <- "InnerProj[t0]" [hstyle=composition];
     "OuterProj\n[PolicyID, ScenID=1]" [stacked];
     "InnerProj[t0]" [stacked];
     "PV[t_rate]" [stacked];
     "InnerProj[t0]" <- "PV[t_rate]" [hstyle=composition]
   }

"""

from modelx.serialize.jsonvalues import *

def _formula(t_rate):
    refs = {'last_t': _space.parent.last_t,
            'InsurIF_Beg1': _space.parent.InsurIF_Beg1,
            'InsurIF_End': _space.parent.InsurIF_End,
            'PremIncome': _space.parent.PremIncome,
            'BenefitSurr': _space.parent.BenefitSurr,
            'BenefitDeath': _space.parent.BenefitDeath,
            'BenefitTotal': _space.parent.BenefitTotal,
            'ExpsCommTotal': _space.parent.ExpsCommTotal,
            'ExpsAcq': _space.parent.ExpsAcq,
            'ExpsMaint': _space.parent.ExpsMaint,
            'ExpsTotal': _space.parent.ExpsTotal,
            'DiscRate': _space.parent.parent[t_rate].DiscRate}

    return {'refs': refs}


_bases = []

_allow_none = None

_spaces = []

# ---------------------------------------------------------------------------
# Cells

def InterestNetCF(t):
    """Interest accreted on pv of net cashflows"""
    if t > last_t():
        return 0
    else:
        return (PV_NetCashflow(t)
                - PremIncome(t)
                + ExpsTotal(t)) * DiscRate(t)


def PV_BenefitDeath(t):
    """Present value of death benefits"""
    if t > last_t():
        return 0
    else:
        return (-BenefitDeath(t) + PV_BenefitDeath(t+1)) / (1 + DiscRate(t))


def PV_BenefitMat(t):
    """Present value of matuirty benefits"""
    if t > last_t():
        return 0
    else:
        return (-BenefitMat(t) + PV_BenefitMat(t+1)) / (1 + DiscRate(t))


def PV_BenefitSurr(t):
    """Present value of surrender benefits"""
    if t > last_t():
        return 0
    else:
        return (-BenefitSurr(t) + PV_BenefitSurr(t+1)) / (1 + DiscRate(t))


def PV_BenefitTotal(t):
    """Present value of total benefits"""
    if t > last_t():
        return 0
    else:
        return (-BenefitTotal(t) + PV_BenefitTotal(t+1)) / (1 + DiscRate(t))


def PV_Check(t):
    return PV_NetCashflow(t) - PV_NetCashflowForCheck(t)


def PV_ExpsAcq(t):
    """Present value of acquisition expenses"""
    if t > last_t():
        return 0
    else:
        return - ExpsAcq(t) + PV_ExpsAcq(t+1) / (1 + DiscRate(t))


def PV_ExpsCommTotal(t):
    """Present value of commission expenses"""
    if t > last_t():
        return 0
    else:
        return - ExpsCommTotal(t) + PV_ExpsCommTotal(t+1) / (1 + DiscRate(t))


def PV_ExpsMaint(t):
    """Present value of maintenance expenses"""
    if t > last_t():
        return 0
    else:
        return - ExpsMaint(t) + PV_ExpsMaint(t+1) / (1 + DiscRate(t))


def PV_ExpsTotal(t):
    """Present value of total expenses"""
    if t > last_t():
        return 0
    else:
        return - ExpsTotal(t) + PV_ExpsTotal(t+1) / (1 + DiscRate(t))


def PV_NetCashflow(t):
    """Present value of net cashflow"""
    return (PV_PremIncome(t)
            + PV_ExpsTotal(t)
            + PV_BenefitTotal(t))


def PV_NetCashflowForCheck(t):
    """Present value of net cashflow"""
    if t > last_t():
        return 0
    else:
        return (PremIncome(t)
                - ExpsTotal(t)
                - BenefitTotal(t) / (1 + DiscRate(t))
                + PV_NetCashflow(t+1) / (1 + DiscRate(t)))


def PV_PremIncome(t):
    """Present value of premium income"""
    if t > last_t():
        return 0
    else:
        return PremIncome(t) + PV_PremIncome(t+1) / (1 + DiscRate(t))


def PV_SumInsurIF(t):
    """Present value of insurance in-force"""
    if t > last_t():
        return 0
    else:
        return InsurIF_Beg1(t) + PV_SumInsurIF(t+1) / (1 + DiscRate(t))


# ---------------------------------------------------------------------------
# References

scen = ("Interface", ("....", "Economic"), "auto")