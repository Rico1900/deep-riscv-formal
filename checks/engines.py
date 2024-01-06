bools = ['true', "false"]

def space(s):
    if s == "":
        return ""
    else:
        return s + " "

# it seems that current sby does not support yices configurations
# requires further investigation
def generate_yices_configs():
    return {"yices"}

def generate_boolector_configs():
    configs = set()
    boolector = "boolector"
    for rtl in range(4):
        rewrite_level = f"--rewrite-level={rtl}"
        for sp in range(2):
            sp_cfg = f"--skeleton-preproc={sp}"
            # for ack in range(2):
            #     ack_cfg = f"--ackermannize={ack}"
            #     for br in ["none", "fun", "all"]:
            #         br_cfg = f"--beta-reduce={br}"
            #         for es in range(2):
            #             es_cfg = f"--eliminate-slices={es}"
            #             for vs in range(2):
            #                 vs_cfg = f"--var-subst={vs}"
            #                 for uc in range(2):
            #                     uc_cfg = f"--ucopt={uc}"
            #                     for ml in range(2):
            #                         ml_cfg = f"--merge-lambdas={ml}"
            #                         for xl in range(2):
            #                             xl_cfg = f"--extract-lambdas={xl}"
            #                             for norm in range(2):
            #                                 norm_cfg = f"--normalize={norm}"
            #                                 for fj in range(2):
            #                                     fj_cfg = f"--fun-just={fj}"
            for fjh in ["left", "applies", "depth"]:
                fjh_cfg = f"--fun-just-heuristic={fjh}"
                for lazy in range(2):
                    lazy_cfg = f"--fun-lazy-synthesize={lazy}"
                    for el in ["none", "conf", "all"]:
                        el_cfg = f"--fun-eager-lemmas={el}"
                        for fsl in range(2):
                            fsl_cfg = f"--fun-store-lambdas={fsl}"
                            configs.add(
                                space(boolector) +
                                space(rewrite_level) +
                                space(sp_cfg) +
                                # space(ack_cfg) +
                                # space(br_cfg) +
                                # space(es_cfg) +
                                # space(vs_cfg) +
                                # space(uc_cfg) +
                                # space(ml_cfg) +
                                # space(xl_cfg) +
                                # space(norm_cfg) +
                                # space(fj_cfg) +
                                space(fjh_cfg) +
                                space(lazy_cfg) +
                                space(el_cfg) +
                                space(fsl_cfg))                                                              
    return configs

def generate_bitwuzla_configs():
    configs = set()
    bitwuzla = "bitwuzla"
    for sat_eng in ["cadical", "lingeling", "kissat", "gimsatul"]:
        sat_eng_cfg = f"--sat-engine={sat_eng}"
        for rtl in range(4):
            rewrite_level = f"--rewrite-level={rtl}"
            configs.add(
                space(bitwuzla) +
                space(sat_eng_cfg) +
                space(rewrite_level)
            )
    return configs

def generate_z3_configs():
    configs = set()
    z3 = "z3"
    # select rewrite options
    for is_cache in bools:
        cache_cfg = f"rewriter.cache_all={is_cache}"
        for is_blast_distinct in bools:
            blast_distinct_cfg = f"rewriter.blast_distinct={is_blast_distinct}"
            configs.add(
                space(z3) + 
                space(cache_cfg) + 
                space(blast_distinct_cfg)
            )
    return configs

def generate_mathsat_configs():
    configs = set()
    mathsat = "mathsat"
    for seed in range(5):
        seed_cfg = f"-random_seed={seed}"
        configs.add(
            space(mathsat) +
            space(seed_cfg)
        )
    return configs

def generate_cvc5_configs():
    configs = set()
    cvc5 = "cvc5"
    for prop in ["--bv-propagate", ""]:
        for decision in ["internal", "justification", "stoponly"]:
            configs.add(
                space(cvc5) +
                space(prop) +
                space(f"--decision={decision}")
            )
    return configs

def generate_solver_configs():
    yices_configs = generate_yices_configs()
    boolector_configs = generate_boolector_configs()
    bitwuzla_configs = generate_bitwuzla_configs()
    z3_configs = generate_z3_configs()
    mathsat_configs = generate_mathsat_configs()
    cvc5_configs = generate_cvc5_configs()
    return (yices_configs |
            boolector_configs |
            bitwuzla_configs |
            z3_configs |
            mathsat_configs |
            cvc5_configs)

def generate_engines():
    engines = set()
    engines.add("abc bmc3")
    engines.add("btor btormc")
    engines.add("btor pono")
    smt_engine = "smtbmc"
    for mem_representation in ["--nomem", ""]:
        for is_syn in ["--syn", ""]:
            for is_big_vec in ["--stbv", ""]:
                for is_presat in ["--nopresat", ""]:
                    for is_unroll in ["--unroll", "--nounroll"]:
                        for solver_cfg in generate_solver_configs():
                            engines.add(
                                space(smt_engine) +
                                space(mem_representation) +
                                space(is_syn) +
                                space(is_big_vec) +
                                space(is_presat) +
                                space(is_unroll) +
                                space(solver_cfg))
    return engines

def print_engine_number():
    print(len(generate_engines()))

print_engine_number()