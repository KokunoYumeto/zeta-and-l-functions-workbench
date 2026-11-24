# A finite arithmetic test for simplicity of the Riemann zeros, after Suzuki

WB-0009, version 1. Permanent record: <https://github.com/KokunoYumeto/mathematics-workbenches/blob/main/works/WB-0009.md>.

Under the Riemann hypothesis, now a theorem of L. Alpöge, M. Suzuki's compressions C_N of the inverse of a
differentiation operator to windows of Weil's quadratic form converge in Hilbert–Schmidt norm and see each distinct
zero once. This work compares their even trace powers with the Taylor moments S_k of log ξ(1/2+iz), which count
multiplicity. The defect D_{N,k} = S_k − tr C_N^{2k} satisfies D_{N,k} ≥ 2E(T)/T^{2k}, where E(T) is the
multiplicity excess up to height T, and sup_{N,k}(2/D_{N,k})^{1/(2k)} is the first multiple ordinate. So simplicity
up to a height is one finite arithmetic inequality.
- **Integer form:** the zeros up to T are simple iff ind_+(T H_N − G_N) ≥ n(T) for some N.
- **Certificate:** every zero with 0 < Im ρ ≤ 97.632 is simple, computed from prime powers below e^12 in ball
  arithmetic, with no zero as input.
- **Explicit constants:** m_γ < (3/4) log γ.
- **Size bound:** a certificate at height T needs a window of dimension at least 2n(T).
- **Heat flow:** in the backward de Bruijn–Newman heat flow, a·j_*(−a) → γ_*²/2.

**Who produced and checked it.**
- **Produced:** the results were produced by GPT-6 Astra (ChatGPT Pro mode), with a first computation of the
  certificate.
- **Checked and written up:** Claude Opus 5.5 at effort high checked every proof, wrote the note, and wrote an
  independent rigorous enclosure program. It also opened Suzuki's Hilbert–Schmidt convergence and the explicit formula
  at their sources.
- **Re-proved:** a separate Claude Opus 5.5 at effort high re-proved Theorems 1–2 independently and checked
  Proposition 10.
- **Main session:** Claude Opus 5.5 at effort max read the note and checked Propositions 4 and 8.

No human has checked the proofs.

**Files:**
- the paper: `finite_arithmetic_simplicity_test.tex`, and its PDF;
- `STATEMENTS.tsv`, `CHECK_EVENTS.tsv`, `SOURCES.tsv`;
- `CHECKS.md`;
- `checks/`: the enclosure program and two floating-point replays, each with its output.

Our text and programs are dedicated to the public domain under CC0 1.0.
