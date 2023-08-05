
cdef extern from "snp_hwe.h":
    double SNPHWE(long, long, long)

def snphwe(obs_hets, obs_hom1, obs_hom2):
    return SNPHWE(obs_hets, obs_hom1, obs_hom2)
