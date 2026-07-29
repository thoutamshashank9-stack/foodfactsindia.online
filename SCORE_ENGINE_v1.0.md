# FoodLens AI — Scoring Engine Contract v1.0.0

**Version:** 1.0.0  
**Engine Type:** Pure Deterministic Mathematical Rule Engine (Zero Non-Deterministic LLM Math)  
**Primary Unit Basis:** Per 100g / 100ml Standardized Baseline  
**Output Contract:**

```ts
SCORE_ENGINE_VERSION = "1.0.0";

interface Input {
  nutrition_per_100g: NutritionFacts;
  nutrition_per_serving: NutritionFacts;
  ingredients: Ingredient[];
}

interface Output {
  score: number; // 0 to 100 (Internal rating metric)
  grade: 'A+' | 'A' | 'B' | 'C' | 'D' | 'F';
  breakdown: ScoreBreakdownItem[];
  issues: ScoreBreakdownItem[]; // Filtered deductions (user-facing primary output)
  confidence: number; // 0 to 100%
}
```

---

## 1. Mathematical Rules Summary

| Factor | Baseline Condition (Per 100g/ml) | Point Deduction / Addition | Authority Rationale Source |
|--------|----------------------------------|----------------------------|----------------------------|
| **Base Starting Score** | Default starting constant | **+100 pts** | Standardized baseline |
| **Added Sugar** | > 5.0g per 100g | **−2 pts** per gram over 5g (capped at −20 pts) | WHO & FSSAI Dietary Limits |
| **Sodium** | > 300mg per 100g | **−1 pt** per 50mg over 300mg (capped at −10 pts) | FSSAI & US FDA Guidance |
| **Saturated Fat** | > 3.0g per 100g | **−1 pt** per gram over 3g (capped at −10 pts) | ICMR-NIN Guidelines |
| **Trans Fat** | > 0.0g per 100g | **−10 pts** flat penalty | WHO REPLACE Strategy |
| **Global Market Ban** | Banned in ≥1 major market (IN, EU, US, JP) | **−15 pts** per banned additive (capped at −40 pts) | Regulatory Intelligence DB |
| **High Concern Additive** | Restricted / Southampton Dye / 4-MEI | **−10 pts** per additive | EFSA & FDA Advisories |
| **Moderate Concern Additive** | Highly synthetic / ADI limits | **−5 pts** per additive | JECFA Toxicological Review |
| **Fiber Bonus** | ≥ 3.0g dietary fiber | **+5 pts** bonus | Dietary Fiber Guidelines |
| **Protein Bonus** | ≥ 10.0g protein | **+5 pts** bonus | ICMR Dietary Guidelines |
| **Clean Label Bonus** | ≤ 5 ingredients, 0 NOVA 4 additives | **+5 pts** bonus | NOVA Classification System |

---

## 2. Invariant Safety Constraints

1. **Deterministic Reproducibility**: Given identical input JSON parameters, the Scoring Engine MUST yield the exact same integer deductions and issues array across all runtime environments.
2. **Score Range Boundaries**: The calculated score is strictly bounded between `0` and `100`.
3. **No LLM Math Intervention**: LLMs are strictly forbidden from modifying or generating numerical deductions. All deductions MUST be calculated in pure TypeScript code.
