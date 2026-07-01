---
name: biomimicry-profile-intake
description: Structured intake sub-skill — captures and validates the 8-field engineering Problem Profile required before any biological search begins.
---

## Purpose

Capture a complete, unambiguous engineering problem description that can be directly fed into the biological research stage. Vague inputs produce vague analogies. This sub-skill forces the user to articulate what the design must DO (function), under what conditions (environment), with what constraints (materials, manufacturing, scale, budget), and against what targets (performance KPIs, sustainability goals).

The output is a structured Problem Profile that acts as the governing specification for all subsequent sub-skills in the harness.

---

## Inputs

- Free-text problem description from the user (may be brief or detailed)
- Optional: existing design documents, CAD drawings, or specifications the user can reference

---

## Workflow

### Step 1 — Extract Initial Fields
Read the user's free-text problem description and attempt to populate the 8 Problem Profile fields:

| Field | What to Extract |
|-------|----------------|
| 1. **Required Function** | What must the design DO? (verb phrase — e.g., "attach reversibly to wet curved surfaces") |
| 2. **Operating Environment** | Temperature range, humidity, pH, pressure, UV exposure, salinity, load frequency, indoors/outdoors |
| 3. **Material Constraints** | Allowed material classes (metals, polymers, ceramics, composites, biologics); forbidden materials (toxicity, regulatory); recyclability requirements |
| 4. **Manufacturing Process** | Available fabrication methods (injection molding, CNC, 3D printing, wet lay-up, electrospinning, casting, weaving); unit volume (prototype/pilot/mass) |
| 5. **Scale** | Physical size of the component/system (micro: <1mm, meso: 1mm–10cm, macro: >10cm); and scale of deployment (single unit, fleet, building-wide) |
| 6. **Performance KPIs** | Quantified targets: strength (MPa), adhesion force (N/cm²), thermal resistance (R-value), drag coefficient, fatigue cycles, cost per unit, etc. |
| 7. **Sustainability Goals** | Recyclability, biodegradability, embodied carbon target, Life Cycle Assessment requirement, regulatory standard (REACH, RoHS, LEED) |
| 8. **Budget Tier** | Research/Prototype (cost not critical), Mid-range (cost matters but not primary), Cost-sensitive (must be competitive with conventional solutions) |

### Step 2 — Validate and Flag Missing Fields
For each field:
- If the field is clearly populated from the user input → accept and move on.
- If the field is ambiguous → generate a single clarifying question and ask the user.
- If the field is missing entirely → ask the user directly.

Batch all clarifying questions into one message (do not ask one at a time for each missing field).

### Step 3 — Translate Function into AskNature Vocabulary
Map the Required Function to AskNature taxonomy language. This translation step ensures the subsequent biological search uses the right functional vocabulary:

| Engineering Language | AskNature Functional Vocabulary |
|---------------------|--------------------------------|
| Stick / Adhere | Attach, Fasten, Bind |
| Hold structure together | Maintain structural integrity, Distribute force |
| Keep dry / repel water | Regulate water, Prevent wetting |
| Ventilate / Cool passively | Regulate temperature, Move fluids |
| Absorb impact / shock | Dampen vibration, Absorb energy |
| Filter / Separate | Separate, Filter, Sort |
| Sense / Detect | Sense, Signal, Transduce |
| Repair damage | Self-repair, Regenerate |
| Collect water from air | Collect, Capture, Harvest |
| Move through fluid efficiently | Reduce drag, Locomote |
| Prevent biological fouling | Protect from biotic threats |

Record both the original engineering phrasing and the AskNature functional translation in the Problem Profile.

### Step 4 — Identify Key Search Constraints
From the 8 fields, extract the 3–4 most constraining factors that will filter biological analogies. For example:
- If Manufacturing Process = "injection molding at scale," then biological structures requiring nano-scale precision may be low-transferability.
- If Operating Environment = "seawater at 30°C with barnacle fouling," then the biological search should focus on marine organisms.
- If Scale = "micro (<1mm)," then only mechanisms that operate at microscale are relevant.

Document these constraint filters in the Problem Profile — they will be used by sub-analogy-mapper as hard filters.

### Step 5 — Output Structured Problem Profile
Format the collected information as a structured Problem Profile:

```
PROBLEM PROFILE
═══════════════════════════════════════════════════════════
Required Function:       [engineering verb phrase]
AskNature Function:      [AskNature vocabulary translation]
Operating Environment:   [temperature, humidity, load type, etc.]
Material Constraints:    [allowed/forbidden materials, standards]
Manufacturing Process:   [available methods, volume]
Scale:                   [physical size + deployment scale]
Performance KPIs:        [quantified targets with units]
Sustainability Goals:    [recyclability, carbon, standards]
Budget Tier:             [Research / Mid-range / Cost-sensitive]
Key Search Constraints:  [top 3-4 filtering factors for biology search]
═══════════════════════════════════════════════════════════
```

---

## Outputs

- **Structured Problem Profile** — formatted as above; passed to sub-biological-researcher
- **AskNature Function Translation** — one or more AskNature functional vocabulary terms that will guide the search
- **Key Search Constraints** — the 3–4 most constraining factors, used as hard filters in sub-analogy-mapper

---

## Quality Gate

Before passing the Problem Profile to the next sub-skill, verify:

- [ ] All 8 fields are populated (no field left blank or marked "unknown")
- [ ] Required Function is phrased as an engineering verb phrase (not a noun; not a technology name)
- [ ] AskNature Function Translation is derived from AskNature vocabulary (not free-form)
- [ ] Performance KPIs include at least one quantified target with units
- [ ] Key Search Constraints are documented (minimum 2, maximum 5)
- [ ] If any field was ambiguous and resolved through clarification, the resolution is recorded

**Failure action:** If any gate fails, return to Step 2 and request clarification before passing the profile forward.


---

## Worked Examples ? Intake (3 sample problem statements)

These three worked demonstrations validate that the 8-field schema and the
AskNature translation table can absorb realistic free-text inputs and produce
a complete, quality-gate-compliant Problem Profile. They are reference
intakes (design-time validation), not live runs.

### Example A ? Gecko dry adhesive (robotics end-of-arm tool)

**Free-text input:**
> "I need a gripper pad that sticks to flat cardboard boxes, releases on command, holds 10 kg per 100 cm?, must not leave residue, works indoors, ~100k cycles, REACH-compliant polymer, injection-molded with micro-texturing, mid-range budget."

**Derived Problem Profile:**
- Required Function: Reversible dry adhesion to flat surfaces under dynamic loading
- AskNature Function: Attach, Fasten (reversibly)
- Operating Environment: Indoor, 15?35 ?C, low humidity, flat/semi-flat surfaces
- Material Constraints: Non-toxic REACH-compliant polymers/elastomers; no exotic materials
- Manufacturing Process: Injection molding + secondary micro-texturing (soft lithography / textured tooling)
- Scale: Meso ? pad area ~100 cm?, feature size 10?500 ?m
- Performance KPIs: ?10 N/cm?, ?100,000 cycles, attach <200 ms, zero residue
- Sustainability Goals: REACH-compliant; recyclable elastomer preferred
- Budget Tier: Mid-range
- Key Search Constraints: feature size 10?500 ?m; REACH-compliant polymer; ?100k cycles; residue-free release

### Example B ? Passive ventilation (hot-arid building)

**Free-text input:**
> "Passive ventilation for a 4-story building in Riyadh (45 ?C peak, 10?15% RH), keep interior ?27 ?C with no powered fans, competitive construction cost."

**Derived Problem Profile:**
- Required Function: Passive thermal regulation and airflow management in hot arid conditions
- AskNature Function: Regulate temperature, Move fluids (air), Maintain homeostasis
- Operating Environment: Hot-arid, up to 45 ?C, 10?15% RH, large diurnal swing, outdoor/semi-outdoor
- Material Constraints: Standard construction materials (concrete, brick, stone, clay, timber); no exotic materials
- Manufacturing Process: Construction methods (cast-in-place, masonry, prefab panels)
- Scale: Macro ? building 30 m ? 40 m; airflow features 0.1?1 m
- Performance KPIs: Interior ?27 ?C at 45 ?C peak; zero mechanical energy input; LCA better than conventional HVAC
- Sustainability Goals: Zero operational energy; local materials; LEED-aligned
- Budget Tier: Cost-sensitive
- Key Search Constraints: no powered fans; hot-arid climate; macro scale; construction-materials only

### Example C ? Anti-drag marine coating

**Free-text input:**
> "Spray-on hull coating for a 50 m ferry that cuts drag ?5% and stops barnacle/algae fouling ?18 months without biocides (EU BPR), seawater 5?25 ?C, mid-range budget."

**Derived Problem Profile:**
- Required Function: Reduce hydrodynamic drag and prevent biofouling simultaneously
- AskNature Function: Reduce drag, Protect from biotic threats
- Operating Environment: Marine, 5?25 ?C seawater, continuous immersion, abrasion, fouling organisms
- Material Constraints: Non-biocidal (EU BPR compliant); spray-applicable; abrasion-resistant
- Manufacturing Process: Spray coating; 18-month dry-dock cycle
- Scale: Macro ? hull ~1000 m?; surface features 1?200 ?m
- Performance KPIs: ?5% drag reduction; ?18 months anti-fouling without biocides; abrasion resistance
- Sustainability Goals: EU BPR-compliant; no biocide release to seawater
- Budget Tier: Mid-range
- Key Search Constraints: EU BPR non-biocidal; spray-applicable; marine immersion; 1?200 ?m feature resolution

**Intake quality-gate validation:** All three examples populate 8/8 fields,
phrase functions as verb phrases, derive AskNature terms from the controlled
vocabulary table, include ?1 quantified KPI with units, and document 2?4 key
search constraints each. ? All three PASS the sub-profile-intake quality gate.
