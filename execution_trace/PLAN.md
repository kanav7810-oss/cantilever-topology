# Plan: Computational Topology Optimization of Cantilever Beam Geometries

## Summary
Execute all 6 phases of the hyperprompt as a single reproducible pipeline: (1) literature-grounded hypotheses, (2) analytical + numerical simulation of 38 geometries × 13 load cases = 494 rows, (3) statistical analysis and 7 SVG figures, (4) 4500+ word research paper, (5) single-file interactive web interface, (6) handoff file. All deliverables saved to the results folder with the exact filenames in the checklist.

## Explicit assumptions (delegated decisions)
1. **Combined load cases**: 3 cases — 500 N + 50 N/mm; 1000 N + 50 N/mm; 1000 N + 100 N/mm. Total load cases = 4 point + 3 UDL + 3 triangular + 3 combined = 13. Dataset = 38 × 13 = 494 rows (≥200 required).
2. **SIMP freeform geometries**: 2D plan-view topology optimization of a 500×100 mm cantilever domain (Sigmund 88-line style, p=3, volume fraction 0.4, density filter rmin=1.5 elements, OC update, ~100 iterations, Q4 plane-stress FEA). Optimized topologies are evaluated directly from their FEA solution; out-of-plane thickness is scaled so total volume = 100 cm³ (t = V / plan area), making comparison with analytical sections fair. 10 variants: 4 load types × mesh/filter variations + seed variations. Von Mises and tip deflection scale as 1/t from the unit-thickness solve.
3. **Material efficiency index (MEI)**: computed exactly as specified (SF ÷ area). Because iso-volume (100 cm³) + fixed length (500 mm) forces area = 200 mm² and mass = 785 g for every analytical section, the paper will state explicitly that MEI ∝ safety factor under this constraint; discrimination therefore comes from safety factor, deflection, and stress uniformity. SIMP sections get their own effective area (plan area × t / L = 200 mm² by construction).

## Design by subsystem

### Geometry engine (Python, /workspace/beamopt/)
- All analytical sections sized to area A = 200 mm² exactly (closed-form solve per family):
  - Solid rectangle: b/h ∈ {0.5, 1.0, 1.5, 2.0, 2.5} (5)
  - I-beam: bf/h ∈ {0.3, 0.5, 0.7, 1.0}, tf = 0.15h, tw = 0.1h, area-solved (4)
  - Hollow rectangle: t/h ∈ {0.1, 0.2, 0.3, 0.4}, outer b/h = 1 (4)
  - T-section: 5 flange/web proportion variants (5)
  - Trapezoidal: 5 top/bottom width-ratio variants (5)
  - Circular hollow: D/t ∈ {5, 8, 12, 20, 30} (5)
  - SIMP freeform: 10 (above)
- Section properties (I about neutral axis, c_max, Q, shear stress) computed analytically where closed forms exist and verified numerically by polygon integration (shapely-free; custom Green's-theorem integrator) — cross-check |I_analytic − I_numeric| < 1%.

### Loads & metrics (Euler-Bernoulli + thin-walled shear)
- Tip deflection: PL³/3EI (point), wL⁴/8EI (UDL), w₀L⁴/30EI (triangular max-at-root), superposition for combined.
- Max von Mises: max of outer-fiber bending VM (σ = Mc/I at root) and neutral-axis combined VM (√(σ²+3τ²)) with τ = VQ/(I·b) for thin-walled/open sections.
- Metrics per row: max VM stress (MPa), tip deflection (mm), safety factor (250/σ_vm), MEI (SF/A), stress uniformity coefficient (std of outer-fiber bending stress sampled at 51 stations along length), mass (g), I (mm⁴). No missing values; SIMP rows get uniformity from element VM field std.

### Analysis & figures (matplotlib, SVG with editable text, Liberation Sans, colorblind-safe palette)
- Rankings per load type; load-sensitivity slopes (ΔSF per kN); best geometry per load type; SIMP vs hand-designed comparison; Pareto front (deflection vs stress, Pareto-optimal set marked); k-means (k=4, standardized features, k-means++ seed fixed); full descriptive stats.
- Graphs 1–7 exactly as specified, each saved as .svg (+ .png for QC), each passing a media output check before acceptance. Graph 5: beam-elevation stress-gradient strip + cross-section diagram for top 3. Graph 7: ≥5 density snapshots + compliance curve from recorded SIMP iteration history.

### Paper (research_paper.md, ≥4500 words)
- Structure exactly as specified (abstract → appendix B). ≥15 real citations anchored on retrieved literature (Bendsøe & Sigmund SIMP lineage, Sigmund 88-line, Xie & Steven ESO, Ashby shape factors, Sotola et al. cantilever SIMP sensitivity, Ballo et al. I-beam bending optimality, plus beam-theory texts). Every number in the paper traceable to dataset.csv (generated from the same run; key stats injected programmatically where practical).

### Web interface (index.html, single file)
- Vanilla HTML/CSS/JS + Inter (Google Fonts) + Chart.js (cdnjs) only; colors #f8f9fa / #0066cc / #ff6600; dataset embedded as inline JSON; all 11 sections in specified order; sortable/searchable table with red/yellow/green SF cells; dynamic SVG cross-section renderer per geometry family; Chart.js interactive Pareto + SF-vs-load charts; sticky nav with scroll-spy; smooth scroll; responsive.

### Handoff (handoff.md)
- All 8 sections as specified, including the 8 named next-step categories (fabrication, ANSYS/Abaqus validation protocol, 3D TO extension, material variation, 3 named journals, ISEF/Regeneron/TSA, lab collaboration, funding).

## Validation & test cases
- Unit checks: rectangle I = bh³/12 vs numeric integrator; thin-tube I ≈ πR³t limit; cantilever point-load deflection vs textbook value; SIMP compliance decreases monotonically (post-filter) and final volume fraction = 0.40 ± 0.01; SIMP cantilever produces the classic two-diagonal-strut topology (visual QC).
- Dataset audit: 494 rows, 0 NaN, all 7 geometry families present, SF > 0, spot-check 3 rows by hand calculation.
- Figure QC: media output check on every PNG; regenerate if blank/clipped.
- Paper: word count ≥4500 verified programmatically; every table number matches dataset.

## Compute estimate
- Analytical sweep: <1 s. SIMP: 10 runs × ~100 iterations × ~6.4k-DOF sparse solves ≈ 1–3 min total on worker-0 (default machine, no HPC needed). Figures/paper/web: minutes. Total well under one 20-min notebook budget; no extra machines, no background jobs.

## Deliverables (results folder)
dataset.csv, research_paper.md, graph1–7 SVGs (9 files), index.html, handoff.md — exactly matching the hyperprompt checklist.
