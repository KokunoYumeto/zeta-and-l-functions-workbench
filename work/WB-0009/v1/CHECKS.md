# WB-0009, version 1: the checks

Every check is listed by statement in `CHECK_EVENTS.tsv`. In short:

- **November 2026, GPT-6 Astra (ChatGPT Pro mode).** Produced the results and made the first computation of the
  certificate: Arb at 120 digits, rigorous integration, and a preconditioned positive-definiteness test. All six rows
  of Table 1 pass.
- **23 November 2026, Claude Opus 5.5 at effort high.**
  - Followed every step of Theorem 1 and Proposition 4 (the multiplicity bound and the constants), and the size bound
    (Proposition 8).
  - Recomputed rows 1–4 of the certificate in floating point (mpmath). The values agree with the first computation's
    bounds to 9–10 digits.
- **24 November 2026, Claude Opus 5.5 at effort high (checker and writer of the note).**
  - **Theorems 1 and 2:** rewrote the proofs in ℓ²(Γ, m). Proved the density of the dyadic windows (Lemma 6), which
    the original cites from its construction.
  - **The explicit formula (Lemma 9):** derived it for H¹ test functions from Bombieri's form, as recorded in the
    appendix of Connes and Consani, opened at the source.
  - **Suzuki:** opened his Hilbert–Schmidt convergence at the source (arXiv:2610.32704, §2.3 and (4.1)).
  - **Proposition 10:** checked step by step, and opened Borcea–Brändén Theorem 2(b) and Rodgers–Tao §1 at their
    locators.
  - **The certificate:** wrote an independent rigorous program, `checks/enclose_trace_defect.py`, from the note's
    formulas: ball integration, ball power series for S_k, and a rigorous linear solve. All six rows are certified, for
    example D_{6,3} ∈ [2.3092709160972367573e−12 ± 3.9e−32] < 2/97.632⁶. A floating-point replay of all six rows,
    `checks/replay_floating_point_flint.py`, also counts the eigenvalues of C_N above 1/T. It finds n(T) at every
    height (0, 1, 3, 6, 14, 28), which is not rigorous.
  - **Credit:** read Alpöge–Furman (arXiv:2608.13637v2) in §§1–4. They state neither Theorem 1 nor Theorem 2; the
    shared principle and their Lemma 3.1 are credited.
- **24 November 2026, a separate instance of Claude Opus 5.5 at effort high.** Given only the statements and
  Suzuki's paper:
  - re-proved Theorems 1 and 2 and the density lemma independently, then compared with the note. It found no gap and
    made three points: a trapezoid constant, the case of singular G_N, and the basis of V_N. All three are applied,
    and the basis proof is taken from it.
  - then checked Proposition 10 step by step, with both sources opened; it found no error and made two wording
    points, both applied.
- **24 November 2026, Claude Opus 5.5 at effort max.** Read the whole note. Re-derived the digamma bound of
  Proposition 4, and checked the counting step of Proposition 8.

All the programs are in `checks/`, with their outputs. The rigour of the certificate is that of Arb ball arithmetic
and of the programs; it is not formally verified. No human has checked the proofs.
