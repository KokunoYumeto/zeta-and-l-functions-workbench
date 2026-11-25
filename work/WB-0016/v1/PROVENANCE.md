# Provenance of "Hilbert's Nullstellensatz is in AM from a zero-free half-plane of Dedekind zeta functions, after Koiran" (WB-0016)

## As deposited on Hexagon

The provenance field of the deposit, as it stands on Hexagon:

> Text: AI-authored; none of it was written by a human. The submitter takes responsibility for the veracity of the text.
>
> How it was produced. GPT-6 Astra (OpenAI), in ChatGPT Pro mode, produced the statement that a fixed zero-free half-plane of Dedekind zeta functions suffices for Koiran's theorem, with its proof; GPT-6.2 Astra (OpenAI) at reasoning effort ultra (Codex) edited it; it is Proposition 17.2 of hexagon:2611.00987v1 (24 November 2026). GPT-6 Astra (ChatGPT Pro mode) also produced, under a hypothesis of GRH type, the statements on circuit and homogeneous systems and on homogeneous systems of parameters (November 2026). Claude Opus 5.5 (Anthropic), at effort max, derived Koiran's estimate from B. Hu's Corollary 9.6 and listed the consequences for the dimension problem, the parametric Nullstellensatz and Schubert vanishing (24 November 2026). Claude Fable 5.2 (Anthropic), at effort max, wrote this text on 24 November 2026, derived Sections 3 and 4 again, added the term for the leading coefficient of a non-monic polynomial and the explicit threshold, and opened Koiran's extended report, his erratum of 1997, his paper on the dimension problem, and the papers of Ait El Manssour et al., Pak-Robichaux, Mulmuley and Andrews-Garg-Schost at the cited places.
>
> How it was checked. Claude Opus 5.5, at effort high, checked the derivation and the five consequences on 24 November 2026: it read Koiran's article at the step where GRH enters, re-derived the replacement of his Theorem 9, checked the prime ideal estimate from a half-plane against the explicit formula of Lagarias and Odlyzko as quoted by Rojas, and read the reductions of Ait El Manssour et al. and Pak-Robichaux at the places where GRH is used. On 24 November 2026 the same model, at effort high, checked this text: it recomputed every constant of Sections 3 and 4 and read the sources at the cited places. The half-plane preprints of Cureton-Thorner, Hu and Liu were read at their statements only; their proofs were not checked by us. Lagarias-Odlyzko 1977, Boppana-Hastad-Zachos 1987 and Lackenby 2021 were not opened and are cited as Frei-Sofos-Widmer, Pak-Robichaux and Baldwin-Sivek describe them. Rojas's Theorem 5 and OpenAI's preprint on factorization are no longer used. Literature, arXiv and Hexagon were searched before the note was written. No human has checked the proofs or the text, and nothing is formalized by us.
>
> Version 2 (25 November 2026). After version 1 was posted, Claude Opus 5.5 (Anthropic), at effort high, found two papers that version 1 did not cite: Frei-Sofos-Widmer, arXiv:2610.18491 (13 October 2026), and Baldwin-Sivek, arXiv:2611.06705 (4 November 2026). Claude Fable 5.2 (Anthropic), at effort max, opened both at the cited statements (Theorem 1.1 of the first; Theorems 1.1, 1.3, 2.1 and 3.1, Corollary 3.3, Remark 1.4 and pages 2-3 of the second), credited them in the abstract, Sections 1.4 and 1.5, Proposition 3.1(b) and Remark 3.3, and replaced the proof of Proposition 3.1(b) by the deduction from Frei-Sofos-Widmer's theorem. Kuperberg's and Zentner's papers were opened at the cited theorems; Lackenby's is cited as Baldwin-Sivek describe it. No theorem or corollary of ours changed (the bound in Proposition 3.1(b) is now quoted in Frei-Sofos-Widmer's form), and we claim no result in topology.
>
> Where the records are. https://github.com/KokunoYumeto/mathematics-workbenches
>
> The text and accompanying work are dedicated to the public domain under CC0 1.0.

## Text history

The text was first committed to Hexagon on 24 November 2026 at 23:20 UTC and withdrawn before it was published, because it did not cite two papers that Claude Opus 5.5 at effort high then found: Frei, Sofos and Widmer (arXiv:2610.18491) and Baldwin and Sivek (arXiv:2611.06705). Claude Fable 5.2 at effort max made the corrected text, the one in this folder; Claude Opus 5.5 at effort high checked the new citations; it was committed on 25 November 2026 at 00:33 UTC and published as hexagon:2611.01018 (Hexagon's version identifier is 2611.01018v2, because it counts the withdrawn submission). What changed:

1. Abstract: the sentence on a general half-plane names Frei-Sofos-Widmer and Baldwin-Sivek.
2. Section 1.4: a new paragraph on the estimates from a half-plane (Frei-Sofos-Widmer in October, Baldwin-Sivek in November 2026, before our 2611.00987); the explicit threshold, the route through Hu's Corollary 9.6 and Corollary D are what is new here.
3. Section 1.5: a new paragraph on three-manifold topology, ending "we claim nothing in topology".
4. Section 1.6: Theorem B(b) is called a case of Frei-Sofos-Widmer's theorem.
5. Proposition 3.1(b): inequality (4) is their Theorem 1.1 for the trivial extension; the proof through Lagarias-Odlyzko's explicit formula as quoted by Rojas is gone (a known result is cited, not proved again, when the source has the form needed).
6. Remark 3.3: Baldwin-Sivek's Corollary 3.3 and Theorem 2.1 credited for the monic case and the polynomial-size prime; their Section 5 for the non-monic case.
7. Note on method: the sources not opened are Lagarias-Odlyzko, Boppana-Håstad-Zachos and Lackenby.
8. Bibliography: Baldwin-Sivek, Frei-Sofos-Widmer, Kuperberg, Lackenby and Zentner added; OpenAI's factorization preprint no longer cited.

Unchanged: every statement and constant of Theorems A and B, Corollaries C and D, Propositions 2.1, 3.2 and 5.1 and Theorem 4.1. So the checks made on the first text apply to the deposited one, except those of the proof of Proposition 3.1(b), which the deposited text replaces; their rows in `CHECK_EVENTS.tsv` say so.

## The earlier statement in our own work

The step from a fixed zero-free half-plane to AM is Proposition 17.2 of our paper hexagon:2611.00987v1 (p. 59) and a row of its Table 1; the note cites it and says so in the abstract, Section 1.4 and the note on method. New in the note: the derivation of Koiran's estimate from Hu's Corollary 9.6 (Propositions 3.1(a) and 3.2), the explicit threshold x₀ (Theorem A, Theorem 4.1), Corollary D with the place where each source uses GRH, and the relation to Andrews, Garg and Schost.

## Sources opened, and where

By Claude Fable 5.2 at effort max, the writer; the checker, Claude Opus 5.5 at effort high, read the sources at the cited places again.

| Source | Opened at |
|---|---|
| Koiran, J. Complexity 12 (1996) | whole text; pp. 275-276, 281-282 as page images |
| Koiran, DIMACS TR 96-27 | abstract, §§1-5 (Thm 1, Thm 2 with proof, Thms 4, 5, 7, 8, 9, Cor. 1) |
| Koiran, Erratum, 8 Aug 1997 | whole (page image) |
| Koiran, FOCS 1997 (author's version) | abstract, §1, p. 6 (Thm 4.1), p. 9 (Thm 5.8) |
| Hu, hexagon:2610.00216v2 | abstract, Thm 1.1, Thm 1.2, Cor. 9.6 with proof, "AI provenance" |
| Cureton-Thorner, hexagon:2610.00200v2 | abstract, §1 to Cor. 1.2, §15 |
| Liu, hexagon:2611.00741v1 | abstract, Thm 7.21 (statement) |
| OpenAI, Primitive roots (4 Oct 2026) | introduction, Thm 1.2 |
| OpenAI, factorization over prime fields (4 Oct 2026) | §11 whole (Lemma 11.2 and proof); no longer cited in the deposited text |
| Rojas, arXiv math/0301111v2 | pp. 1-7 (Thm 1, DZH, GIPIT, Thm 5; p. 7 as page image) |
| Ait El Manssour et al., arXiv 2408.13027v3 | abstract, §1, §3.3.1, §3.4 (proof of Thm 1) |
| Pak-Robichaux, arXiv 2504.03004v1 | pp. 1-5, Thm 2.1, §3.1, Lemma 3.2, Thm 3.4 with proof |
| Pak-Robichaux, arXiv 2412.02064v3 | abstract, Thm 1.4, Thms 1.7-1.8, Lemma 1.9, §1.8 |
| Mulmuley, GCT V, arXiv 1209.5993v5 | Thm 2.10, §3 to the remarks after Thm 3.4 |
| Andrews-Garg-Schost, arXiv 2602.17904v1 | abstract page; §§1.1-1.2 through two fetches (summaries, not the full text) |
| hexagon:2611.00987v1 (ours) | Table 1 row, §§17.2-17.3 |
| Frei-Sofos-Widmer, arXiv 2610.18491v2 (v1 of 13 Oct 2026) | abstract; §1, first paragraph; Theorem 1.1, p. 2 (page image read); Corollaries 1.2-1.3 |
| Baldwin-Sivek, arXiv 2611.06705v1 (4 Nov 2026) | abstract; Theorem 1.1 (p. 1); Hypothesis 1.2, Theorem 1.3 and the text after it (p. 2); pp. 2-3 on Cureton-Thorner; Table 1 caption; Remarks 1.4-1.5, AI and IA statements (p. 3); Theorem 2.1 (p. 4); Theorem 3.1 and Corollary 3.3 (p. 7); start of §5; bibliography |
| Kuperberg, arXiv 1112.0845 | Theorem 1.1 (start) and Theorem 3.2 |
| Zentner, arXiv 1605.08530v4 | Theorem 11.2 |

Not opened: Lagarias-Odlyzko 1977 (its Theorem 7.1 as quoted by Rojas, Theorem 5, used in the first text only); Boppana-Håstad-Zachos 1987 (as quoted by Pak-Robichaux, p. 5); Lackenby, Adv. Math. 387 (2021) (as Baldwin and Sivek, Remark 1.4, describe it).

## Literature searches

Before the note was written, arXiv, ECCC, the web and the Hexagon catalogue were searched for the result (24 November 2026). The searches recorded with the note:

- 2026-11-24, Claude Fable 5.2, effort max, agent ae2754d9739e7e166 (HNAM note): Relation to arXiv 2602.17904 (Andrews-Garg-Schost). opened (abs page; HTML sections 1.1-1.2 via fetch summaries): HN in CH, no hypothesis, also finite fields and function fields; PH inside CH so AM is the smaller class; no comparison made there
- 2026-11-24, Claude Fable 5.2, effort max, agent ae2754d9739e7e166 (HNAM note): Earlier statement in our own paper. hexagon:2611.00987v1 Prop 17.2 (p.59) and Table 1 already state HN in AM from a fixed half-plane, accepting Cureton-Thorner; the earlier novelty search missed it; the note cites it
- 2026-11-25, Claude Fable 5.2, effort max, agent ae2754d9739e7e166 (HNAM v2): HNAM v2 credit: Baldwin-Sivek Thm 2.1, Thm 1.3. arXiv 2611.06705v1 opened at Thm 1.1 (p.1), Hyp 1.2 and Thm 1.3 (p.2), pp.2-3, Remark 1.4 (p.3), Thm 2.1 (p.4), Thm 3.1 and Cor 3.3 (p.7), section 5: one-polynomial prime p=poly(d, log||f||) under a uniform half-plane, from FSW; coNP results for 3-manifold recognition; nothing on HN or AM; our Prop 3.2 with Thm 4.1 for one polynomial gives their Thm 2.1 again
- 2026-11-25, Claude Fable 5.2, effort max, agent ae2754d9739e7e166 (HNAM v2): HNAM v2 new bibliography entries. Kuperberg Adv. Math. 256 (2014) 493-506 and Zentner Duke Math. J. 167 (2018) no.9 1643-1712 confirmed on the arXiv journal-reference lines and in Baldwin-Sivek's bibliography; Kuperberg Thm 3.2 and Zentner Thm 11.2 opened; Lackenby Adv. Math. 387 (2021) Paper No. 107796 from Baldwin-Sivek's bibliography only (arXiv 1604.00290 says to appear), paper not opened
