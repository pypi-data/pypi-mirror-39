import numpy as np
from scipy.stats import poisson, binom
import msprime

def simulate(genome,
    msprime_args,
    indel_rate=0.01,
    pcr_opts=None):

    assert type(genome) == dict
    assert type(msprime_args) == dict
    pass

# def sim_chroms(...)
# def extract_loci(...)
# def sim_reads(...)
