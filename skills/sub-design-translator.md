---
name: biomimicry-design-translator
description: Translates the top-ranked biological analogies into production-engineering specifications — material analogues, geometric parameters, manufacturing routes, patent landscape, and Life's Principles compliance scores.
---

## Purpose

Bridge the gap between "this is what biology does" and "this is how an engineer builds it." This sub-skill takes the top 3 biological analogies from sub-analogy-mapper and produces a concrete Engineering Design Specification for each — including the key geometric parameters derived from biology literature, the synthetic material analogue, the applicable manufacturing process, existing products and patents that implement the strategy, and a Life's Principles compliance evaluation. The output is a draft specification ready for inclusion in the final Biomimicry Design Brief.

---

## Inputs

- **Top 3 Biological Analogies** from sub-analogy-mapper (organism, mechanism summary, ranked scores)
- **Structured Problem Profile** from sub-profile-intake (manufacturing process available, material constraints, scale, performance KPIs)

---

## Natural-to-Synthetic Material Analogue Reference Table

Use this table as a starting mapping. Always verify with a literature or patent search before specifying.

| Biological Material | Natural Function | Synthetic Analogue | Engineering Application |
|--------------------|-----------------|--------------------|------------------------|
| Chitin (insect exoskeleton) | Lightweight structural armor | Carbon fiber reinforced polymer (CFRP), Nylon-based composites | Structural panels, impact-resistant shells |
| Keratin (feathers, hair, nails) | Lightweight flexible-to-rigid gradient | Thermoplastic elastomers (TPE), polyimides | Flexible structural elements, gradient-stiffness joints |
| Silk (spider, silkworm) | High tensile strength, toughness, lightweight | Ultra-high molecular weight polyethylene (UHMWPE), Dyneema, Kevlar analogs | Fibers, ropes, armor, biomedical scaffolds |
| Nacre (abalone shell) | High fracture toughness via layered tablet-matrix | Alumina platelet-epoxy composites, ceramic-polymer laminates | Body armor, cutting tools, wear-resistant surfaces |
| Bone (cortical) | Hierarchical load-bearing composite | Carbon fiber/resin with gradient density, metal foams | Structural bones, aerospace frames, crash structures |
| Cellulose (plant cell walls) | Lightweight tensile structural fiber | Nanocellulose composites, glass fiber, bamboo-GFRP | Panels, containers, packaging |
| Collagen/elastin (tendons) | High-cycle fatigue resistant fiber | Polyurethane elastomers, PTFE | Flexible connectors, seals, vascular grafts |
| Melanin (cephalopod chromatophores) | Active coloration / light absorption | Electrochromic polymers, liquid crystal displays | Smart coatings, variable-absorption surfaces |
| Calcium carbonate (echinoderm ossicles) | Perforated strong-but-lightweight structure | Ceramic foams, 3D-printed lattice structures | Lightweight structural lattices |
| Wax crystals (lotus leaf) | Superhydrophobic nano-roughness | Fluoropolymer coatings (PTFE/PVDF) with micro-texture | Anti-icing, anti-fouling, self-cleaning coatings |
| Setal arrays (gecko foot) | Dry reversible adhesion via van der Waals | Carbon nanotube (CNT) arrays, PDMS pillar arrays | Dry adhesives, climbing robots |
| Mussel adhesion proteins (DOPA) | Wet adhesion on any surface | Polydopamine, catechol-functionalized polymers | Underwater adhesives, surgical glues |
| Structural color (butterfly wing lamellae) | Iridescent color without pigment | Nanoimprinted polymer gratings, photonic crystals, colloidal assemblies | Cosmetics, anti-counterfeiting, display films |
| Exocuticle (beetle elytra) | Sandwich structure with rigid face sheets + porous core | Aluminum honeycomb sandwich, carbon fiber sandwich panels | Aerospace panels, vehicle hoods |

---

## Manufacturing Route Reference

| Required Feature | Biological Analogy | Manufacturing Route |
|-----------------|-------------------|---------------------|
| Nano-scale surface texture (50–500nm) | Gecko setae, lotus wax crystals | Two-photon lithography, nanoimprint lithography (NIL), atomic layer deposition (ALD) |
| Micro-scale riblets or denticles (1–100μm) | Shark denticles, moth-eye | Soft lithography (PDMS casting), laser ablation, injection molding with textured tooling |
| Hierarchical porous structure | Bone trabecular, wood cross-section | Selective laser sintering (SLS), 3D printing (FFF/SLA), freeze-casting (ice templating) |
| High-aspect-ratio fibers | Spider silk, carbon nanotubes | Electrospinning, wet spinning, CVD nanotube growth |
| Gradient stiffness | Tendon-to-bone insertion, tree trunk cross-section | Multi-material 3D printing (Stratasys PolyJet), functionally graded casting |
| Self-assembling microstructure | Cell membrane, viral capsid | DNA origami (research-stage), block copolymer self-assembly, colloidal self-assembly |
| Hollow sealed chambers | Bird bone pneumaticity, grass stem | Blow molding, extrusion with internal mandrel, foam-core sandwich |
| Branching fluid network | Leaf venation, cardiovascular | 3D printing (resin), investment casting with sacrificial template, PDMS microfluidics |
| Reversible interlocking | Velcro (bur hooks) | Injection molded hook-and-loop fasteners, 3D printed hook arrays |
| Iridescent surface | Morpho butterfly lamellae | Colloidal photonic crystal deposition, reactive ion etching, vacuum-deposited thin films |

---

## Workflow

### Step 1 — Deep Dive: Biological Mechanism Parameters

For each of the top 3 analogies, search the source citation (and related papers) to extract quantitative geometric parameters:
- Spatial dimensions: feature size, spacing, aspect ratio, hierarchy levels
- Material composition: reported modulus, tensile strength, fracture toughness, density
- Functional performance: adhesion force per area, drag coefficient, R-value, filtration efficiency, etc.
- Key references: additional papers cited within the primary source that report quantitative data

WebFetch the DOI or AskNature page to retrieve these details. If not available in the primary source, do a targeted search:
```
WebSearch: "[organism] [mechanism] geometry parameters measurement [journal]"
```

### Step 2 — Map to Synthetic Material Analogue

Using the Natural-to-Synthetic Material Analogue Reference Table (above) and the Problem Profile's material constraints:
1. Identify the primary biological material driving the mechanism
2. Select the best synthetic analogue that:
   - Is allowed by the Problem Profile material constraints
   - Is commercially available at the budget tier specified
   - Can be processed by the available manufacturing methods
3. Record any material performance gap: how different is the synthetic analogue from the biological original? (e.g., "CFRP has similar specific stiffness to bone but lower fracture toughness")

### Step 3 — Select Manufacturing Route

Using the Manufacturing Route Reference Table (above) and the Problem Profile's manufacturing constraints:
1. Identify the feature type that the mechanism requires (surface texture, porous structure, fiber, gradient, etc.)
2. Match to the appropriate manufacturing route
3. Verify the route is compatible with the selected synthetic material
4. Estimate minimum feature size achievable with the route vs. what is biologically required — flag if a gap exists

### Step 4 — Patent and Existing Product Search

Search for existing bio-inspired implementations of this strategy:
```
WebSearch: "[organism] inspired [engineering function] patent
WebSearch: "[biological mechanism name] synthetic [material]" product
WebSearch: USPTO "bio-inspired" "[function keyword]"
```

Document:
- Existing commercial products that implement the same biological strategy
- Relevant patents (patent number, assignee, year, key claim)
- Research prototypes demonstrated in literature (paper + DOI)

This search confirms the strategy is technically feasible and identifies prior art to work around.

### Step 5 — Life's Principles Compliance Evaluation

Evaluate the proposed engineering specification against all 6 of Janine Benyus's Life's Principles categories:

```
Life's Principles Compliance Matrix
╔══════════════════════════════════════╦═════════════════╦═══════════════════════════════════╗
║ Principle Category                   ║ Assessment       ║ Notes                             ║
╠══════════════════════════════════════╬═════════════════╬═══════════════════════════════════╣
║ 1. Evolve to Survive                 ║ [Aligns/Part./No]║ ...                               ║
║ 2. Adapt to Changing Conditions      ║ [Aligns/Part./No]║ ...                               ║
║ 3. Be Locally Attuned & Responsive   ║ [Aligns/Part./No]║ ...                               ║
║ 4. Use Life-Friendly Chemistry       ║ [Aligns/Part./No]║ ...                               ║
║ 5. Be Resource-Efficient             ║ [Aligns/Part./No]║ ...                               ║
║ 6. Integrate Development with Growth ║ [Aligns/Part./No]║ ...                               ║
╚══════════════════════════════════════╩═════════════════╩═══════════════════════════════════╝
Life's Principles Score: [X/6 Aligns, Y/6 Partially Aligns, Z/6 Does Not Align]
```

For any "Does Not Align" category, document what design modification would move it to "Partially Aligns."

### Step 6 — Failure Mode & Risk Analysis

For each proposed specification, document:
1. **Top 3 engineering failure modes** when translating this biological mechanism to a product (e.g., "gecko setal arrays degrade with particulate contamination")
2. **Key translation assumptions** most likely to fail (e.g., "assumes feature replication at 200nm — requires NIL at scale, which is costly")
3. **Comparison to conventional solution** — what is the conventional engineering approach to this problem, and why does the bio-inspired spec win (or not)?
4. **Depth of biomimicry** — is this deep principle extraction (e.g., understanding the physical principle of van der Waals setal adhesion) or surface-level copying (e.g., just making something look like a gecko foot)?

### Step 7 — Estimate Implementation Effort

| Effort Level | Criteria |
|-------------|---------|
| **Low** | Uses commercially available materials and standard manufacturing; achievable in <6 months without new R&D |
| **Medium** | Requires material adaptation or process modification; 6–18 months development; some new tooling |
| **High** | Requires novel materials, new manufacturing capability, or multi-year R&D program |

### Step 8 — Compile Engineering Design Specification

For each of the top 3 analogies, produce:

```
ENGINEERING DESIGN SPECIFICATION
Analogy Rank: [1/2/3]
Biological Analogy: [Organism — Mechanism Name]
Analogy Score: [Weighted Total from sub-analogy-mapper]
TRIZ Principle: [if applicable]

BIOLOGICAL MECHANISM
  Organism: [Scientific name (common name)]
  Mechanism: [2–3 sentence description]
  Key Geometric Parameters:
    - Feature size: [e.g., setal tip radius 100nm]
    - Spacing: [e.g., 200μm between setae]
    - Aspect ratio: [e.g., 10:1]
    - Hierarchy levels: [e.g., 2 — setae on lamellae]
  Biological Performance: [e.g., adhesion = 10 N/cm²]
  Evidence Tier: [Peer-Reviewed]
  Primary Citation: [Author (Year), Journal, DOI]

ENGINEERING TRANSLATION
  Material Analogue: [e.g., PDMS pillar array on polyimide substrate]
  Material Performance Gap: [e.g., "PDMS setae give ~60% of gecko adhesion per area"]
  Manufacturing Route: [e.g., soft lithography — PDMS cast from Si master wafer]
  Key Manufacturing Parameters:
    - Feature resolution: [e.g., 500nm minimum — achievable by NIL]
    - Process temperature: [e.g., ambient cure at 70°C, 4h]
    - Unit cost estimate: [e.g., $12/m² at pilot scale]
  Estimated Performance: [e.g., adhesion ~6 N/cm², 10,000 cycles]

EXISTING IMPLEMENTATIONS
  Products: [e.g., Geckskin (UMass Amherst), Draper Lab climbing robot adhesive]
  Patents: [e.g., US8398909B2 — Gecko-inspired dry adhesive (Maeno et al., 2013)]
  Research: [DOI of key demonstration papers]

LIFE'S PRINCIPLES COMPLIANCE
  [6-row compliance matrix as defined in Step 5]
  Overall: [X/6 Aligns]

FAILURE MODES & RISKS
  1. [Top failure mode]
  2. [Second failure mode]
  3. [Third failure mode]
  Key Translation Risk: [most likely assumption to fail]
  vs. Conventional Solution: [comparison]
  Biomimicry Depth: [Surface / Principle / Ecosystem level]

IMPLEMENTATION EFFORT: [Low / Medium / High]
RECOMMENDED NEXT STEP: [e.g., "Fabricate PDMS pillar array test coupon using standard photolithography; test adhesion per ASTM D4541"]
```

---

## Outputs

- **Engineering Design Specification** for each of the 3 top-ranked biological analogies
- **Life's Principles Compliance Matrix** for each specification
- **Patent & Existing Product Landscape** for each analogy
- **Failure Mode Analysis** for each specification
- **Implementation Effort Rating** for each specification

---

## Quality Gate

Before passing specifications to the main harness for final synthesis:

- [ ] Quantitative biological parameters are cited from literature (not estimated)
- [ ] Material analogue is compatible with the Problem Profile's material constraints
- [ ] Manufacturing route is compatible with the Problem Profile's manufacturing constraints
- [ ] At least one existing product or patent is documented for each specification
- [ ] Life's Principles compliance matrix is completed for all 6 categories (no blanks)
- [ ] At least 3 failure modes are documented for each specification
- [ ] Implementation effort is rated (Low/Medium/High) for each specification
- [ ] The biomimicry depth assessment (Surface / Principle / Ecosystem) is recorded

**Failure action:** If quantitative biological parameters cannot be found in the primary source, do a targeted literature search before defaulting to estimated ranges. If no existing product or patent is found, document "No prior art found — confirm with comprehensive patent search" rather than leaving the field blank.
