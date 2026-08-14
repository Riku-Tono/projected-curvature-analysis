# Projected Curvature: Second-Order Read-Only Analysis

**Config ID:** `STAGE0_V3_PROJECTED_CURVATURE_SECOND_ORDER_READONLY_V1`
**Status:** `COMPLETE`
**Classification:** `PARTIALLY_EXPLAINED`
**Follow-up diagnostic:** `RANK1_FACE_GEOMETRY_CONFIRMED_DRIFT_LINK_NOT_ROBUST`
**Source support solves:** 38 &nbsp;·&nbsp; **New solver runs:** 0

---

## 1. Executive conclusion

Two independent finite-window fits — one taken along the 90-degree axis (the upper cap) and one along the 270-degree axis (the cone-apex side) — return projected radii that agree to roughly four parts in a thousand:

| Quantity | Value |
| --- | --- |
| 90-degree fitted radius | `47.13790398372574` |
| 270-degree fitted radius | `47.34266132851574` |
| Observed relative difference | `0.004334380178893083` (≈ 0.4334%) |

This analysis asks where that shared scale near 47 comes from, and answers it in two parts.

**What is explained.** The common scale is *not* an empirical coincidence and *not* a reflection of the large raw `z0` coefficient. It is a coordinate-invariant identity of the frozen linear map: the ell=0 imaginary-amplitude map together with unitarity-disk geometry and the exact projection structure predicts

```text
rho = 1 / (4 * kappa_sigma) = 47.34582205692646
```

*before* either fitted radius is consulted. This universal value reproduces the 270-degree fit to a relative radius residual of `-6.675833840030787e-05` (about −0.0067%), which is far below one percent.

**What is not explained.** The 90-degree result lands within `+0.44108%` (in fitted quadratic coefficient) of the same base scale only after a large cross-ell cancellation among the ell=0, ell=2, and ell=4 groups. That cancellation is measured with high precision, but no identity was found in the saved artifacts that *forces* it. The saved solve records contain no conic dual multipliers, and the previously tested full-complement map is infeasible, so an exact full-feasible-set involution could not be established.

Hence the overall classification is `PARTIALLY_EXPLAINED`: a structurally derived base scale plus an isolated, quantified, unexplained upper-cap residual.

Subsequent adversarial read-only analyses sharpened the unresolved side without changing that classification. The 90-degree correction is confined to a narrow, nearly zero-sum cross-ell direction close to `(1,-2,1)`, but its small in-plane drift is not robustly attributable to a fixed active-block pair or even to a face-level demand coordinate across all admissible drift definitions. The strongest surviving follow-up result is therefore geometric rather than causal:

```text
90-degree correction: narrow near-zero-sum cross-ell direction
ell=0 face demand:     extremely stable rank-1 redistribution mode
link between the two:  suggestive in ranks, not robust across definitions
```

The preregistered read-only stopping rule was reached. The saved primal artifacts identify the geometry but do not determine why the optimizer selects it; resolving that question would require a new experiment that records dual/KKT information. Section 6 gives the complete audit trail.

![Projected curvature decomposition: universal scale versus fits, the 90-degree cross-ell cancellation, and the 90-degree active-constraint demand ranking](projected_curvature_decomposition.png)

*Left: the universal ell=0 sigma scale beside the two fitted radii. Center: the ell=0 / ell=2 / ell=4 contributions to `b2` on each axis, showing the large signed cancellation at 90 degrees and its near-absence at 270 degrees. Right: the unweighted disk-demand shares of the 90-degree active blocks.*

---

## 2. Frozen scope and provenance

This is a **sealed-artifact-only, read-only** analysis. Every number reported here was derived from 38 previously saved support solves. **No new solver run, additional support solve, parameter refinement, ell refinement, or full run was performed** — these operations are explicitly prohibited by `ANALYSIS_SCOPE.json`, and `new_solver_runs` is `0` in every provenance record in the package.

| Scope parameter | Value |
| --- | --- |
| Analysis type | Sealed-artifact-only read-only second-order response analysis |
| Axes analyzed | 90.0°, 270.0° |
| Projection fit offsets (degrees) | `0.0439453125`, `0.02197265625`, `0.010986328125`, `0.0054931640625` |
| Representative response offset | `0.010986328125` degrees |
| Response sensitivity offsets | `0.02197265625`, `0.010986328125`, `0.0054931640625` |
| Source solve count | 38 |
| New solver runs | 0 |
| `source_artifacts_unchanged` | `true` |

**Authoritative claim boundary**, quoted from `projected_curvature_result.json` and `ANALYSIS_SCOPE.json`:

> The analysis decomposes the saved finite-grid response and identifies coordinate-invariant identities of the frozen linear map. It does not infer continuum-limit curvature, assign KKT dual weights that were not saved, or prove an exact full-feasible-set involution.

`PROVENANCE_SHA256.json` records the SHA-256 hash of every upstream artifact consulted, including the frozen solve result, the recovered coefficient array, the core implementation module, the gate-2 runner, and the face-microscope package with its own manifest and verification record.

---

## 3. Where the number 47 comes from

This is the central derivation. It is short, and it is the reason the shared scale is called *structural* rather than *coincidental*.

Let `B0` be the ell=0 imaginary-amplitude map on the saved grid. The saved map represents the boundary function `sigma(s)` exactly to numerical precision:

```text
B0 c_sigma = sigma(s)
```

| Reconstruction diagnostic | Value |
| --- | --- |
| Relative residual | `1.3177829497399766e-14` |
| Max absolute residual | `4.085620730620576e-14` |
| Rank of `B0` | 5 |

Define the projected sigma-mode scale as the second projection functional applied to the representing coefficients:

```text
kappa_sigma = q2_ell0^T c_sigma = 0.005280296954172882
```

The unitarity-disk expansion together with the exact projection structure then gives, in order:

```text
y2 = (sigma / 2) * x1^2          disk expansion
x1 = 2 * a1                      projection structure
b2 = 2 * kappa_sigma * a1^2      substituting
rho = a1^2 / (2 * |b2|)
    = 1 / (4 * kappa_sigma)
    = 47.34582205692646
```

The `a1^2` cancels. **The predicted radius is independent of the path amplitude**, which is precisely why the same value can appear on two different axes with different `a1`. The corresponding universal quadratic coefficient is

```text
2 * kappa_sigma = 0.010560593908345763
```

Three points about interpretation:

- This is a **coordinate-invariant disk/basis/projection scale**. It is a property of the frozen map, the disk geometry, and the projection — not of any particular solve, offset, or fitting window.
- It is **not** a consequence of the large raw `z0` coefficient. Section 5 shows that `z0` contributes exactly zero projected curvature.
- Raw coefficient norms are **not** a measure of physical mode importance. All mode-importance statements in this document use physical-amplitude-space or coordinate-invariant quantities. This distinction is material: at 90 degrees the `z0` group carries a first-order physical amplitude norm larger than the full path norm (ratio `1.1080417826762037`) while contributing nothing at all to curvature.

---

## 4. Projected Taylor and curvature decomposition

### 4.1 Finite-window quadratic fits

Both axes were fitted with a parabola over the four saved projection-fit offsets.

| Quantity | 90 degrees | 270 degrees | Universal prediction |
| --- | --- | --- | --- |
| Quadratic coefficient `C` | `0.010607175070249705` | `0.01056129896311589` | `0.010560593908345763` |
| Coefficient / universal | `1.0044108468054178` | `1.0000667627953737` | 1 |
| Fitted radius | `47.13790398372574` | `47.34266132851574` | `47.34582205692646` |
| Radius / universal | `0.995608523325443` | `0.9999332416615997` | 1 |
| Signed curvature | `0.02121435014049941` | `0.02112259792623178` | — |
| Fit RMS residual | `2.7137147538766843e-07` | `3.058183752714136e-08` | — |
| Fit max abs residual | `6.164637657796334e-07` | `5.990749596028785e-08` | — |

In percentage terms: the 270-degree radius sits `-0.00668%` from the universal value, and the 90-degree fitted quadratic coefficient sits `+0.44108%` above the universal coefficient (equivalently, its radius sits `-0.43915%` below). The observed 90/270 fitted-radius difference is `0.433438%`.

### 4.2 Resolution caveat — read this before quoting the 0.43% figure

**The quoted 0.43% agreement is a property of a finite-window parabolic fit, not a demonstrated asymptotic statement.** `taylor_coefficients.csv` records direct Taylor estimates at seven offsets per axis, and the representative direct parametric radii show visible scale sensitivity:

| Offset (degrees) | 90° parametric radius | 270° parametric radius |
| --- | --- | --- |
| `0.087890625` | `45.01612187420047` | `47.37232198196386` |
| `0.0439453125` | `46.91771913837343` | `47.341158251547924` |
| `0.02197265625` | `47.647060657711876` | `47.34091989554357` |
| `0.010986328125` | `47.85190498775318` | `47.28467898852568` |
| `0.0054931640625` | `48.03219449107583` | `46.76543415204345` |
| `0.00274658203125` | `47.69101266321992` | `45.07118457004089` |
| `0.001373291015625` | `48.74916292628686` | `40.6877372208299` |

The smallest offsets are visibly contaminated by finite-precision differencing of the saved grid. Consequently:

- **Exact asymptotic curvature equality between the two axes is not established.**
- No continuum-limit, differentiability, or exact-symmetry conclusion may be drawn from these finite-grid values. The evidence supports a numerical statement about the saved response, and nothing stronger.

### 4.3 Mode-group decomposition at the representative offset

All group quantities below are evaluated at the representative saved offset `0.010986328125` degrees. Contributions to `b1` and `b2` are additive across groups.

**90 degrees** (`a1 = -47.770863870657976`, `a2 = 3693.805124456793`, `b1 = 9.405568783527052e-05`, `b2 = -23.852252706408095`):

| Group | `b1` contribution | `b2` contribution | Signed curvature `2b2/a1^2` | First-order physical amplitude norm | Share of full |
| --- | --- | --- | --- | --- | --- |
| `z0` | `0.0` | `0.0` | `0.0` | `523.3035946693585` | `1.1080417826762037` |
| `ell0_spectral` | `0.06307625605520417` | `17.47054612371266` | `0.015311237278601505` | `239.3906062120376` | `0.5068850983733839` |
| `ell2` | `-0.1904223630651677` | `-77.65338328346152` | `-0.06805565026530491` | `131.49780706780933` | `0.27843314291293664` |
| `ell4` | `0.12744016269779912` | `36.33058445334078` | `0.0318402295552945` | `19.123282575677717` | `0.0404915928948719` |

**270 degrees** (`a1 = 47.22984500175838`, `a2 = 1291.830638283183`, `b1 = 1.5662900860059252e-05`, `b2 = 23.5879657134319`):

| Group | `b1` contribution | `b2` contribution | Signed curvature `2b2/a1^2` | First-order physical amplitude norm | Share of full |
| --- | --- | --- | --- | --- | --- |
| `z0` | `0.0` | `0.0` | `0.0` | `517.3770298987137` | `1.0000161028333538` |
| `ell0_spectral` | `2.1317834215819618e-05` | `23.564676969297835` | `0.02112800279951677` | `0.019415594361973522` | `3.752757831528591e-05` |
| `ell2` | `-2.9358949453223984e-06` | `0.011734827090482791` | `1.0521402858294875e-05` | `0.0009948535212718163` | `1.9229101481893104e-06` |
| `ell4` | `-2.7190384104379625e-06` | `0.01155391704357727` | `1.0359199574860922e-05` | `0.0019439919978747578` | `3.7574596267532794e-06` |

The two axes reach comparable curvature by structurally different routes. At 270 degrees the ell=0 spectral group supplies essentially all of `b2` directly, with ell=2 and ell=4 contributing at the `0.01` level. At 90 degrees the individual group contributions are three to four times the net result and carry opposing signs — the subject of the next section.

---

## 5. Why `z0`-only is insufficient, and how the upper-cap rest modes cancel

### 5.1 The `z0`-only path has zero projected curvature

Because `q2[0] = 0`, the `z0` direction is annihilated by the second projection functional. A strict `z0`-only projected path therefore has

```text
b1 = 0,  b2 = 0,  projected curvature = 0,  projected radius = INFINITE
```

on **both** axes. This is recorded explicitly in the result JSON as `z0_only_projected_radius: "INFINITE"` for 90 and 270 alike.

The consequence is structural, and it is the reason Section 3 insists on the distinction between coefficient magnitude and curvature relevance: **all finite projected curvature is supplied by rest modes.** The dominant raw `z0` coefficient supplies none of it, however large its amplitude norm.

### 5.2 The 90-degree cancellation

At the representative offset `0.010986328125` degrees, the 90-degree `b2` contributions are:

```text
ell=0 spectral: +17.47054612371266
ell=2:          -77.65338328346152
ell=4:          +36.33058445334078
-----------------------------------
net:            -23.852252706408095
```

The gross magnitude of these contributions is roughly `131.45`; the net is roughly `-23.85`. Three cancellation diagnostics are saved:

| Diagnostic | 90 degrees | 270 degrees |
| --- | --- | --- |
| First-order `q2` cancellation | `0.9997530950054853` (99.9753%) | `0.4193068687336866` (41.93%) |
| Second-order gross-to-net cancellation | `0.8185512843498286` (81.8551%) | `-2.220446049250313e-16` (≈ 0%) |
| Cancellation of group deviations from the universal baseline | `0.9984082220825932` (99.8408%) | `0.0` |

The third row is the most informative. Evaluating the universal identity `b2 = 2 * kappa_sigma * a1^2` at the saved 90-degree `a1`, and applying the reflection appropriate to that axis, gives a **reflected universal `b2` prediction of `-24.09986072482907`**. The saved value is `-23.852252706408095`, so:

| Quantity (90 degrees, representative offset) | Value |
| --- | --- |
| Reflected universal `b2` prediction | `-24.09986072482907` |
| Actual `b2` | `-23.852252706408095` |
| Actual minus universal | `+0.24760801842097635` |
| Relative | `0.010274251011163572` |

Measured against that universal baseline, the individual group deviations are large and opposed:

```text
ell=0 spectral - universal baseline: +41.57040684854173
ell=2:                              -77.65338328346152
ell=4:                              +36.33058445334078
```

These deviations cancel to `99.8408%`, leaving the small residual above. For contrast, at 270 degrees the same accounting shows deviations of `+0.007600948861661294`, `+0.011734827090482791`, and `+0.011553917043577270` — all small, all the same sign, with a saved baseline-delta cancellation fraction of exactly `0.0`. The 270-degree axis simply does not need a cancellation; the 90-degree axis does, and gets one.

### 5.3 What this does and does not establish

This is **strong quantitative compensation toward the common scale**: three group contributions, individually several times the net, conspire to land within one percent of a baseline derived independently of them.

It is **not a proof**. No exact identity over the full feasible set was found that forces this cancellation. The saved solve records contain no conic dual multipliers, and the previously tested full-complement map is infeasible, so the candidate symmetry that would have explained the cancellation was rejected rather than confirmed. The compensation is reported here as a measured fact about the saved response, and the residual `+0.24760801842097635` is left explicitly on the unexplained side of the ledger.

---

## 6. Follow-up audit of the 90-degree near-null geometry

All analyses in this section reuse the same 38 saved primal solves. They perform no additional support solve, parameter refinement, or optimizer run. Each inferential step was placed in a separate output package, and the later adversarial audits govern the interpretation of the earlier exploratory candidate.

### 6.1 The cancellation selects a narrow near-zero-sum direction

For each of the five stable differencing widths, define the actual-minus-universal group response

```text
Delta(h) = (Delta_ell0, Delta_ell2, Delta_ell4).
```

At the representative width, the components are

```text
(+41.57040684854174, -77.65338328346150, +36.33058445334078),
```

with cancellation fraction `0.9984082220825929`. Across the full five-width stable window:

| Diagnostic | Saved result |
| --- | ---: |
| Cancellation fraction | `0.9974076450485962` to `0.9993025274414703` |
| Minimum cosine to `(1,-2,1)` | `0.9989309387181827` |
| Maximum angle to `(1,-2,1)` | `2.6495836119518867` degrees |
| Three-group leading uncentered energy fraction | `0.999958236968428` |

A blind PCA constrained only to the zero-sum plane returns

```text
d_zero = (+0.4337285565, -0.8159549679, +0.3822264114),
```

which is `2.0870314575` degrees from normalized `(1,-2,1)` and captures `0.9999623707345359` of the zero-sum projection energy. The 270-degree representative control has three small same-sign deviations and zero cancellation, so this near-null geometry is specific to the 90-degree route within the saved data.

This establishes a narrow empirical direction, not an exact stencil law. Writing the zero-sum component in the orthogonal basis

```text
s = (1,-2,1),  a = (1,0,-1),  n = (1,1,1),
```

shows that the best aggregate direction can be written approximately as

```text
d_star proportional to (1.0631164788, -2, 0.9368835212).
```

However, the fitted in-plane coefficient ratio `lambda = B/A` varies from `0.0511741` to `0.0800424`; its maximum relative deviation from the aggregate value is `0.2681688852`. The strict fixed-`lambda` hypothesis therefore fails even though the zero-sum plane and narrow cone are confirmed.

### 6.2 A provisional active-demand association

The direction was decomposed as

```text
Delta(h) = alpha(h) d_zero + eta(h) d_perp + epsilon(h) n,
r_eta = eta/alpha,  r_epsilon = epsilon/alpha.
```

An initial preregistered comparison separated the in-plane drift from observable leakage:

| Five-scale diagnostic | Normalized LOOCV SSE |
| --- | ---: |
| `r_eta ~ h^2` | `4.940203292987409` |
| `r_eta ~ p_D` for fixed blocks `(0,29)` and `(0,24)` | `0.2894104030993035` |
| 270-degree `r_eta ~ p_D` control | `5.6489178654789525` |
| 90-degree `r_epsilon ~ h^2` | `0.07879180758138568` |
| 90-degree `r_epsilon ~ p_D` | `2.2969901737346796` |

Here `p_D` is a normalized quadratic-demand balance constructed from the odd first response. The fixed pair carries between `95.71%` and `95.94%` of the active demand over these widths, and the original `r_eta` association has absolute Spearman correlation `0.90`. This justified the provisional label `ACTIVE_DEMAND_CANDIDATE`, but not a causal or KKT interpretation.

### 6.3 Adversarial audit rejects the pair-specific mechanism

The candidate was then tested without changing or reselecting the fixed pair.

| Audit component | Result |
| --- | --- |
| Exact five-point permutation | `2/120 = 0.0166667`; PASS |
| Leave-one-scale-out | slope sign `5/5`, absolute Spearman at least `0.8` in `5/5`, demand beats width in `4/5`; PASS |
| Algebraic self-coupling robustness | frozen baseline tail `8/120`, but raw-even direction reverses slope and ranks `119/120`; FAIL |
| All active ell=0 competitor pairs | canonical pair ranks `4/6`; all `6/6` pairs lie within 10% of its LOOCV statistic |

The canonical pair was never replaced by a better-looking competitor. The correct adversarial decision is

```text
DOES_NOT_SURVIVE
ELL0_FACE_LEVEL_NOT_PAIR_SPECIFIC
```

The failure does not show that the shared odd-response term mechanically manufactures the association: that universal shared term alone has exact tail `99/120 = 0.825`, while the unratioed raw-even `eta` retains the original sign with tail `8/120 = 0.0666667`. It shows instead that the claimed *direction-level, pair-specific* mechanism is not robust.

### 6.4 Regression-free face geometry

The four center-boundary ell=0 blocks were next treated as a single normalized demand vector

```text
p(h) = (p_11, p_12, p_24, p_29),  sum_i p_i = 1,
```

with no regression of drift on face coordinates. Centered PCA gives:

| Geometry diagnostic | 90 degrees |
| --- | ---: |
| PC1 centered energy fraction | `0.9999736204908275` |
| Minimum four-point training PC1 fraction | `0.999977311449773` |
| Maximum leave-one-scale-out PC1 angle | `0.5321827389967885` degrees |
| Mean face proportions `(s11,s12,s24,s29)` | `(0.0240076, 0.0158375, 0.2631050, 0.6970499)` |
| Oriented PC1 loadings | `(-0.3235915, -0.2704150, -0.2712143, +0.8652208)` |

Thus the face-demand variation is genuinely rank-1, but its mode is predominantly `s29` against the pooled other three blocks rather than a special `s29-s24` exchange. This also explains why all six pairwise demand coordinates performed similarly in the competitor scan.

For each held-out width, the PCA direction and mean were estimated from the other four widths only. The resulting cross-fitted score was compared with four drift definitions using ranks and signs, without fitting a regression line:

| Drift definition | Spearman with cross-fitted face score | Positive centered-sign matches | Preregistered relation |
| --- | ---: | ---: | --- |
| Original `r_eta` | `0.90` | `3/5` | FAIL |
| Frozen-baseline `r_eta` | `0.80` | `5/5` | PASS |
| Raw-even `eta` | `0.80` | `5/5` | PASS |
| Raw-even `eta/alpha` | `-0.30` | `4/5` | FAIL |

The original rank ordering is uncommon under the 120 scale assignments (`5/120 = 0.0416667` one-sided), but it fails the preregistered all-five sign condition. The varying positive denominator `alpha` reverses `6/10` pairwise raw-`eta` orderings. This documents normalization sensitivity; it does not prove that `alpha` is a nuisance or that the reversal is an artifact.

The matched four-coordinate 270-degree control is also strongly rank-1 (`0.9975978110332967` PC1 fraction), as is the native 29-block ell=0 face (`0.9963579652925423`). Rank-1 demand variation alone is therefore not a 90-degree-specific signature. What does not reproduce at 270 degrees is the original drift correspondence: matched-coordinate Spearman is `-0.60` with only `2/5` positive centered-sign matches.

### 6.5 Final follow-up classification and stopping point

The follow-up evidence separates a firm geometric result from an unsupported mechanism claim:

```text
RANK1_FACE_GEOMETRY_CONFIRMED_DRIFT_LINK_NOT_ROBUST
FACE_LEVEL_NOT_SUPPORTED
```

The narrow 90-degree near-zero-sum direction, the small observable leakage, and the rank-1 ell=0 face redistribution are reproducible facts about the saved five-scale window. The identity of the optimizer-level mechanism selecting that direction is not recoverable robustly from the saved primal responses. Under the preregistered stopping rule, the read-only mechanism search ends here. A further causal test would require new solves that save conic dual multipliers, slacks, and active-threshold information, with its decision rule sealed before execution.

The exact permutation fractions above describe only the ordering of five saved scales. They are not population p-values and do not authorize causal, KKT, dual, continuum, or intervention claims.

### 6.6 Authoritative follow-up artifacts

| Stage | Authoritative result | Role |
| --- | --- | --- |
| Near-null identification | `near_null_result.json` | Identifies the narrow projected direction and rejects a simple active-disk column-dependence explanation |
| Fixed-direction validation | `fixed_direction_result.json` | Confirms the zero-sum plane; rejects strict offset-independent `lambda` |
| Initial drift separation | `drift_origin_result.json` | Records the provisional `ACTIVE_DEMAND_CANDIDATE` |
| Adversarial candidate audit | `adversarial_audit_result.json` | Governing rejection of pair specificity and strict self-coupling robustness |
| Regression-free face geometry | `face_geometry_result.json` | Governing final classification and read-only stopping decision |

Every stage has its own scope, provenance record, preflight record, and SHA-256 manifest. Later negative audits narrow the claims of earlier exploratory stages; they do not retroactively alter the saved results.

---

## 7. Disk-level and active-constraint findings

`active_disk_quadratic_demand.csv` records, per active boundary block, the physical disk-level quadratic demand `sigma * (x1^2 + y1^2)`, the corresponding `z0`-only demand, the second-order supply, and the resulting supply/demand accounting.

> **Ranking boundary (authoritative, from the result JSON).** Ranks use unweighted physical disk quadratic demand `sigma*(x1^2+y1^2)`, not absent KKT dual weights; they are kinematic stress ranks, not unique causal curvature allocations. Nothing in this section may be read as a KKT-weighted causal attribution — conic dual multipliers were never saved.

### 7.1 The 90-degree cap is effectively low rank

Thirteen boundary blocks are active, but the unweighted demand is concentrated in a handful:

| Rank | Block | Unweighted demand share | Cumulative |
| --- | --- | --- | --- |
| 1 | ell=0, s = `12.0` | `0.6955178353209` (69.55%) | 69.55% |
| 2 | ell=0, s = `9.479222948870392` | `0.2625409821623596` (26.25%) | `0.9580588174832595` (95.81%) |
| 3 | ell=0, s = `5.151096313912009` | `0.023968415567122946` | 98.20% |
| 4 | ell=0, s = `5.369880737217597` | `0.015808359133050693` | `0.9978355921834331` (99.7836%) |

| Summary | Value |
| --- | --- |
| Boundary block count | 13 |
| Leading two blocks together | `0.9580588174832595` (95.81%) |
| All four ell=0 boundary blocks | `0.9978355921834331` (99.7836%) |
| Effective participation count | `1.8066802556828403` |
| Total unweighted full quadratic demand | `28777.24418787053` |
| Total unweighted `z0`-only quadratic demand | `23318.742563346408` |
| Full / `z0`-only demand ratio | `1.2340821598632883` |

An effective participation count of `1.8067` against 13 active blocks is the quantitative statement of "effectively low rank." The full-over-`z0`-only ratio of `1.234` is a second, independent sign that the rest modes matter here: the true demand exceeds what the `z0` direction alone would generate by roughly 23%.

Demand by ell at 90 degrees: `0` → `28714.95849561105`, `2` → `62.28548520077859`, `4` → `0.0002070587022949553`; the ell=0 share is `0.9978355921834331`.

### 7.2 The 270-degree cone-apex side is broad but overwhelmingly ell=0

| Summary | Value |
| --- | --- |
| Boundary block count | 89 |
| ell=0 share of first-order quadratic disk demand | `0.99999999999959` (99.999999999959%) |
| Leading two blocks together | `0.10528879184208709` (10.53%) |
| Effective participation count | `24.391381797941015` |
| Total unweighted full quadratic demand | `137554.43514206423` |
| Total unweighted `z0`-only quadratic demand | `137562.3617097971` |
| Full / `z0`-only demand ratio | `0.9999423783683682` |

Demand by ell at 270 degrees: `0` → `137554.43514200783`, `2` → `5.6142181336861233e-08`, `4` → `2.6268109124899874e-10`.

The apex side is the mirror image of the cap in structure. Far more blocks are active (89 versus 13) and demand is spread across roughly 24 of them, yet the ell=2 and ell=4 apex blocks — while genuinely boundary blocks — carry **negligible first-order curvature demand**, some ten orders of magnitude below the ell=0 total. This is the disk-level counterpart of the mode-group table in Section 4.3, where the 270-degree ell=2 and ell=4 `b2` contributions were likewise negligible, and it is why no cancellation is required on that axis.

---

## 8. What is structurally explained versus what remains unexplained

### Explained

| Item | Value |
| --- | --- |
| Structurally explained base scale | `47.34582205692646` |
| Mechanism | Frozen ell=0 imaginary-amplitude map plus unitarity-disk geometry and exact projection structure; `rho = 1/(4*kappa_sigma)` |
| Character | Coordinate-invariant; independent of path amplitude `a1`; derived before either fitted radius was consulted |
| 270-degree unexplained relative radius residual | `-6.675833840030787e-05` (about −0.0067%) |

Also established, and structural rather than numerical: the `z0` direction contributes exactly zero projected curvature on both axes because `q2[0] = 0`, so the entire projected curvature is a rest-mode phenomenon.

### Unexplained

| Item | Value |
| --- | --- |
| 90-degree coefficient correction to universal | `0.004410846805417812` (`+0.44108%`) |
| 90-degree unexplained relative radius residual | `-0.004391476674556971` (about −0.4391%) |
| Residual `b2` at the representative offset | `+0.24760801842097635` |

The reasoning behind the `PARTIALLY_EXPLAINED` label, in the words of the result JSON:

- **Why not a numerical coincidence.** A coordinate-invariant disk/basis identity predicts the shared scale before using either fitted radius and reproduces the lower result to far below one percent; the upper residual is explicitly isolated.
- **Why not fully structurally explained.** The common `47.3458` scale is exact for the frozen ell=0 sigma mode and explains the lower cap. The upper cap lands within 0.44 percent only after a large cross-ell cancellation. Saved artifacts contain no conic dual multipliers and the previously tested full complement map is infeasible, so no identity was found that forces that cancellation.

The follow-up audits add two statements to this ledger:

- **Geometrically explained.** The 90-degree correction lies in an exceptionally narrow near-zero-sum cross-ell cone, and the four-block ell=0 face demand varies along an exceptionally stable rank-1 mode.
- **Mechanistically unexplained.** Neither a strict fixed cross-ell direction, the dominant `(0,29)-(0,24)` pair, nor the face PC1 score provides a drift explanation robust to the preregistered alternative response definitions. These negative results are why the classification remains `PARTIALLY_EXPLAINED`.

### Standing claim boundaries

These are limits on interpretation, not open questions to be resolved by rereading the data:

1. **No continuum limit.** The finite-grid numerical evidence here does not support a continuum-limit, differentiability, or exact-symmetry theorem. Section 4.2 shows the direct Taylor estimates are scale-sensitive.
2. **No causal attribution from rankings.** The active-block rankings are unweighted kinematic disk-demand ranks. Conic dual multipliers were not saved, so no KKT-weighted causal curvature allocation exists in this package and none may be inferred from it.
3. **No mode importance from raw coefficients.** Use physical-amplitude-space or coordinate-invariant quantities. The `z0` group is the standing counterexample: dominant in raw norm, exactly zero in curvature.
4. **No exact symmetry claim for the upper cap.** The 90-degree closeness to the common scale is measured, not proven to be forced.
5. **No additional solves.** This analysis consumed 38 sealed solves and performed zero solver runs. Nothing in this document should be read as implying otherwise.
6. **No further mechanism selection from the five saved scales.** Pair scans, exact permutations, cross-fitted PCA, and normalization audits have exhausted the preregistered read-only route. Selecting another block contrast or drift normalization from these same five points would reopen post-selection bias rather than resolve the mechanism.

---

## 9. Reproducibility and file guide

### Verification record

The original handoff records below verify the base projected-curvature package. The five follow-up analyses in Section 6 are separate sealed read-only packages with their own manifests; they are referenced here but are not silently added to the original 12-file handoff manifest.

| Record | Result |
| --- | --- |
| Handoff verification | `PASS` — 12 included files, `source_solve_count=38`, `new_solver_runs=0`, no failures |
| Underlying package verification | `PASS` — 11 manifest entries, `source_solve_count=38`, `new_solver_runs=0`, `failures=[]` |
| Follow-up read-only packages | `PASS` — five staged analyses, each using the same 38 saved solves and `new_solver_runs=0` |
| Source artifacts unchanged | `true` |

Every file in this handoff is hash-listed in `HANDOFF_MANIFEST_SHA256.txt`, and every upstream artifact consumed by the analysis is hash-listed in `PROVENANCE_SHA256.json`. To confirm integrity:

```bash
sha256sum -c HANDOFF_MANIFEST_SHA256.txt
```

The upstream package's own record is preserved verbatim in `MANIFEST_SHA256_SOURCE.txt` and `PACKAGE_VERIFICATION_SOURCE.txt`. Note that the source manifest lists two files not carried into this handoff — `analyze_projected_curvature.py` and `read_only_preflight.json` — along with the source package's own `README.md`, which appears here under the name `README_SOURCE.md` with an unchanged hash.

### File guide

| File | Role |
| --- | --- |
| `projected_curvature_result.json` | **Authoritative machine-readable result.** Fits, mode decomposition, cancellation fractions, demand summaries, classification, claim boundary. Where this README and the JSON appear to differ, the JSON governs. |
| `mode_group_curvature_contributions.csv` | Additive `b1`, `b2`, signed-curvature, and physical-amplitude group diagnostics per axis (Section 4.3). |
| `active_disk_quadratic_demand.csv` | Per-block disk-level demand, `z0`-only demand, second-order supply, supply/demand ratios, and the unweighted ranking (Section 7). 102 data rows: 13 for the 90-degree axis, 89 for the 270-degree axis. |
| `taylor_coefficients.csv` | Direct finite-offset Taylor coefficients and parametric radii at seven offsets per axis. Retains the numerical-resolution caveat of Section 4.2. |
| `projected_curvature_decomposition.png` | Three-panel summary figure embedded in Section 1. |
| `ANALYSIS_SCOPE.json` | Frozen scope, offsets, classification labels, prohibited operations, claim boundary. |
| `PROVENANCE_SHA256.json` | SHA-256 hashes of every upstream source artifact. |
| `PACKAGE_VERIFICATION_SOURCE.txt`, `MANIFEST_SHA256_SOURCE.txt` | Verification record and manifest of the underlying read-only analysis package. |
| `HANDOFF_VERIFICATION.txt`, `HANDOFF_MANIFEST_SHA256.txt` | Verification record and manifest for this handoff. |
| `README_SOURCE.md` | Compact source narrative. Useful as background; **not** more authoritative than the JSON. |
| `CLAUDE_REQUEST.md`, `FILE_GUIDE.md` | Writing request and reading order for this README. |

The 38 individual solve JSON files and the analysis source code are intentionally omitted from the original handoff. All README-relevant base values are present in its JSON and CSV artifacts; the later near-null and face-geometry values are governed by the separately manifested result files listed in Section 6.6.

---

*All numerical result artifacts referenced here are frozen and read-only. This README synthesizes the original package and the subsequent manifested audits without modifying their saved values.*
