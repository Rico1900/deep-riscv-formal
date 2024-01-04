# Deep Risc-V Formal

This is a fork version of riscv-formal, which is a formal verification framework for RISC-V processors.

## Configuration
`DRF` supports a new `hypermode` section in `checks.cfg`.

### manual
In this hyper mode, `DRF` will only run the checks specified in `checks.cfg`, which is consistent with the original `riscv-formal`.
```cfg
[hypermode]
manual
```

### all
In this hyper mode, `DRF` will generate all kinds of model-checking configurations for a single model checking task, such that the performance of different model-checking configuration can be utilized to train a deep-learning model to select model-checking configuration automatically.
```cfg
[hypermode]
all
```

### auto
In this hyper mode, `DRF` will select the model-checking configuration automatically based on the deep-learing model.
```cfg
[hypermode]
auto
``````