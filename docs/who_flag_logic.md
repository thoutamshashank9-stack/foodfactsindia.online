# FoodFactsIndia AI — Scientific Documentation: WHO Nutrition Flag Logic

## Overview

This document specifies the scientific rationale, mathematical formulas, zero-calorie guard clauses, fallback heuristics, and disclaimer language used by **FoodFactsIndia AI** to generate nutrition benchmark flags.

---

## 1. Core Principles & Scientific Stance

1. **Intake Guidance vs. Per-100g Declared Data**:
   World Health Organization (WHO) guidelines define nutrient limits primarily as daily adult intake limits (e.g. $<2,000\text{ mg}$ sodium/day) or percentages of total daily energy intake (e.g. $<10\%$ total energy from free sugars).
   
2. **Total Sugars vs. Free Sugars Declaration**:
   Open Food Facts and packaged food labels declare **Total Sugars** (`sugars_100g`), which include both naturally occurring sugars (e.g. lactose in milk, fructose in 100% fruit) and added free sugars. FoodFactsIndia AI labels all sugar flags as **"Estimated High Free Sugars (based on total sugars declaration)"** to maintain scientific accuracy.

3. **Zero-Calorie Guard Clause**:
   For zero-calorie or low-calorie products (e.g., diet sodas, seasonings, tea leaves), calculating $\frac{\text{sugar calories}}{\text{total calories}}$ yields `Infinity` or `NaN`. A strict guard clause prevents runtime calculation errors and defaults to a per-100g heuristic.

---

## 2. Nutrient Benchmark Formulas & Logic

### 2.1 Free Sugars Flag

- **WHO Target**: $< 10\%$ of total daily energy intake (WHO Guideline: Sugars Intake for Adults and Children, 2015).
- **Energy-Adjusted Formula** (when `calories` $> 0$):
  \[
  \text{Sugar Energy \%} = \operatorname{round1}\left( \frac{\text{totalSugarG} \times 4\text{ kcal/g}}{\text{calories}} \times 100 \right)
  \]
  - **Threshold**: Triggered if $\text{Sugar Energy \%} > 10.0\%$.
  - **Label**: `Estimated High Free Sugars (X% of Total Calories)`
  - **Benchmark Text**: `< 10% total daily energy intake (WHO Recommended Target)`

- **Zero-Calorie / Missing Calorie Heuristic Fallback** (when `calories` $\le 0$ or missing):
  - **Threshold**: Triggered if $\text{totalSugarG} > 10\text{g} / 100\text{g}$.
  - **Label**: `Estimated High Free Sugars (FoodFactsIndia Heuristic: >10g/100g)`
  - **Benchmark Text**: `FoodFactsIndia Heuristic (>10g/100g); WHO Context: < 10% daily energy intake (Energy data unavailable)`

---

### 2.2 Sodium Flag

- **WHO Target**: $< 2,000\text{ mg}$ sodium per day for adults ($< 5\text{ g}$ salt/day) (WHO Guideline: Sodium Intake for Adults and Children, 2012).
- **Heuristic Threshold**: Triggered if $\text{sodiumMg} > 600\text{ mg} / 100\text{g}$.
- **Label**: `High Sodium per 100g`
- **Benchmark Text**: `FoodFactsIndia Heuristic (> 600 mg/100g); WHO Adult Daily Target: < 2,000 mg/day`

---

### 2.3 Saturated Fat Flag

- **WHO Target**: $< 10\%$ of total daily energy intake (WHO Saturated Fatty Acid Intake Guidelines, 2023).
- **Heuristic Threshold**: Triggered if $\text{saturatedFatG} > 4\text{g} / 100\text{g}$.
- **Label**: `High Saturated Fat per 100g`
- **Benchmark Text**: `FoodFactsIndia Heuristic (> 4g/100g); WHO Context: < 10% total daily energy intake`

---

### 2.4 Trans Fat Flag

- **WHO Target**: $0\text{g} / 100\text{g}$ ($< 1\%$ total daily energy intake) (WHO REPLACE Action Package, 2018).
- **Threshold**: Triggered if $\text{transFatG} > 0\text{g} / 100\text{g}$.
- **Label**: `Contains Industrially Produced Trans Fat`
- **Benchmark Text**: `0 g / 100g (WHO REPLACE Goal: Eliminate Trans Fat, < 1% energy)`

---

## 3. Mandatory Legal & Health Disclaimer

```text
FoodFactsIndia AI provides verified food information and cross-country regulatory comparisons for consumer awareness.
It is not medical advice or legal advice for manufacturers. Regulatory statuses and formulations may change over time.
Always verify against the physical product package label and official regulatory authorities (FSSAI, EFSA, FDA, WHO).
```
