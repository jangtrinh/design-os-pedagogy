# DESIGN:OS Pedagogy — Art Direction & Meta-Prompt Specification

> **Style System**: Luminous Layered Precision (Isometric 3D)  
> **Philosophy**: Architectural exploded-view product visualization translating pedagogical mechanics, cognitive load theory, and the human developmental spectrum into tactile, frosted-glass hardware layers with strict 35° isometric perspective, minimal typography, and studio illumination.

---

## 📐 The 4 Core Visual Laws

| Law | Specification | Anti-Pattern to Avoid |
|---|---|---|
| **1. Strict 35° Isometric Grid** | Every UI element (cognitive slots, developmental progression stages, diagnostic gauges, worked-example fading tiers) must be mapped flush onto the 3D surface plane of its glass wafer. | 2D flat text overlays, misaligned skew, floating billboards disconnected from plane |
| **2. Radical Textless Minimization (Strict)** | Aim for 100% textless tactile design. If required, max 1 single glyph, number, or 1-token abbreviation (e.g., `g`, `d`, `80%`, `S1`). NEVER permit phrases, sentences, headers, explanatory text, or floating labels. | Any multi-word phrases, sentences, paragraph blocks, poster headers, cluttered text |
| **3. Tactile Glass & Material Physics** | Thick borosilicate glass wafers with rounded corners, 1px bright specular chamfers, soft caustic refractions, hovering over a brushed frosted aluminum chassis. | Flat opacity boxes, dirty smudge textures, harsh plastic reflections |
| **4. Studio Atmospheric Lighting** | Clean seamless soft lilac studio gradient (`#F5F4FC` → `#ECE7FF`). Diffused royal-violet and electric-cyan subsurface glow radiating from underneath the glass wafers. | Pitch black sci-fi, cyberpunk neon bloom, dark gamer/hacker aesthetics |

---

## 🎨 Design Tokens & Palette

```yaml
Atmosphere:
  canvas_base: "#F5F4FC"      # Clean soft atmospheric lilac
  ambient_lavender: "#ECE7FF" # Subtle secondary depth glow
  fill_daylight: "#DFEDFF"    # Subtle daylight fill

Materials:
  wafer_glass: "Translucent borosilicate glass (90% transmission, refractive index 1.52)"
  edge_bevel: "1px crisp white specular chamfer (#FFFFFF)"
  chassis_base: "Anodized pearl-white & satin-brushed aluminum (#F0EEF8)"
  caustic_shadow: "Soft neutral-violet contact shadows rgba(105, 80, 216, 0.08)"

Luminous Pedagogical Accents:
  royal_violet: "#6950D8"     # Working memory, metacognition, doctoral viva, expert schema
  electric_cyan: "#66CFF5"    # Scaffolding, formative feedback, inquiry, active retrieval
  amber_alert: "#F5A623"      # Cognitive overload barrier, misconception trap, neuromyth warning
  emerald_valid: "#2ECC71"    # Validated evidence (Grade A), mastery convergence
```

---

## 🧬 Reusable Meta-Prompt Schema

```text
High-end 3D architectural exploded isometric product visualization demonstrating {TOPIC_NAME} in a Next-Gen Pedagogical Operating System (DESIGN:OS Pedagogy).
Style: Luminous Layered Precision.
Color palette: Clean soft lilac studio background (#F5F4FC, #ECE7FF), royal violet (#6950D8) and electric cyan (#66CFF5) glowing cognitive learning elements, white translucent frosted borosilicate glass wafers with sharp 1px specular edges.
Composition: 35-degree isometric exploded view with 3 vertically floating translucent glass interface slabs hovering over a solid frosted satin-aluminum chassis slab:
- Base chassis ({TIER_1_NAME}): {TIER_1_ELEMENTS_EMBOSSED_ON_PLANE}.
- Middle slab ({TIER_2_NAME}): {TIER_2_ELEMENTS_EMBOSSED_ON_PLANE}.
- Top slab ({TIER_3_NAME}): {TIER_3_ELEMENTS_EMBOSSED_ON_PLANE}.
Perspective & Affordance: Strict 35-degree isometric alignment. All tactile chips, memory slots, diagnostic gauges, and rubric indicators are surface-mapped directly onto the glass planes with realistic depth, specular highlights, and contact shadows.
Typography: Ultra-minimal. No long sentences, no paragraphs, no canvas titles. Pure tactile iconography, numbers, and short functional chips.
Lighting: Soft studio softbox lighting with delicate caustic reflections, diffused violet-cyan subsurface glow beneath each layer, 8k crisp raytraced industrial product design render.
Avoid: Dark backgrounds, black sci-fi, cyberpunk neon clutter, avatars, human figures, floating 2D billboard text.
```

---

## 🗺️ Master Visual Roadmap for design-os-pedagogy

| ID | Section | Topic | Visual Metaphor |
|---|---|---|---|
| 1 | `README.md` | Hero Overview | Master Pedagogical Console with 4 glass tiers (Stages, Axes, Capabilities, Evidence) |
| 2 | `10-foundations` | Cognitive Load & Working Memory | 4 glowing cyan memory slots with amber overload filter blade and germane schema core |
| 3 | `20-stages` | Life-Stage Spectrum (S0–S7) | Stepped glass progression ladder from prenatal seed to doctoral viva & professor console |
| 4 | `30-pedagogy` | Instructional Design & Rosenshine | 3-tier scaffolding stack with worked-example fading wafers and hinge-question probe lens |
| 5 | `00-navigation` | Triple Graph Architecture | Interconnected floating crystal prisms linking Concept Graph, Evidence Metrics & Clinical Cases |
