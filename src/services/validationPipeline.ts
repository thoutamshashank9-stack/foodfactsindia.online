import { z } from "zod";

// --- ZOD SCHEMAS ---

export const IngredientTokenSchema = z.object({
  raw: z.string().min(1),
  normalized: z.string().min(1),
  confidence: z.number().min(0).max(1),
  sourceSpanId: z.string().optional(),
  anomalyFlags: z.array(z.string()).default([]),
});

export const AdditiveMappingSchema = z.object({
  raw: z.string().min(1),
  extractedCodes: z.array(z.string()).default([]),
  resolved: z.array(z.object({
    code: z.string(),
    name: z.string(),
    confidence: z.number().min(0).max(1),
  })).default([]),
  ambiguous: z.boolean().default(false),
});

export const NutritionSchema = z.object({
  energyKcal: z.number().nonnegative().nullable(),
  proteinG: z.number().nonnegative().nullable(),
  totalFatG: z.number().nonnegative().nullable(),
  saturatedFatG: z.number().nonnegative().nullable(),
  transFatG: z.number().nonnegative().nullable(),
  carbohydrateG: z.number().nonnegative().nullable(),
  totalSugarsG: z.number().nonnegative().nullable(),
  addedSugarsG: z.number().nonnegative().nullable(),
  sodiumMg: z.number().nonnegative().nullable(),
  fiberG: z.number().nonnegative().nullable(),
  basis: z.enum(["per_100g", "per_100ml", "per_serving"]),
  servingSizeGml: z.number().positive().nullable().optional(),
});

export const FinalReportCandidateSchema = z.object({
  productId: z.string(),
  validationPassed: z.boolean(),
  reviewRequired: z.boolean().default(false),
  ingredients: z.array(IngredientTokenSchema),
  additiveMappings: z.array(AdditiveMappingSchema).default([]),
  nutrition: NutritionSchema,
  score: z.number().min(0).max(100).nullable().optional(),
  findings: z.array(z.object({
    type: z.string(),
    severity: z.enum(["low", "medium", "high"]),
    message: z.string(),
  })).default([]),
  ocrAnomalies: z.array(z.string()).default([]),
  normalizationAnomalies: z.array(z.string()).default([]),
  mappingConflicts: z.array(z.string()).default([]),
  nutritionMathFailures: z.array(z.string()).default([]),
  displayContradictions: z.array(z.string()).default([]),
});

export type FinalReportCandidate = z.infer<typeof FinalReportCandidateSchema>;

export type PublishDecision = 
  | { ok: true } 
  | { ok: false; code: string; reasons: string[] };

// --- HEURISTICS & ANOMALY DETECTORS ---

const BAD_TOKEN_PATTERNS = [
  /\bglute\b/i,
  /\blodised\b/i,
  /\bcoco\b/i,
  /\bvitamins\s+raising\s+agent\b/i,
  /\b[a-z]{2,}\s+[a-z]{2,}\s+liquid glucose\b/i,
];

const PLACEHOLDERS = [
  "declared ingredients list",
  "ingredients list",
  "see pack for details",
  "n/a",
  "unknown",
];

export function detectOcrIngredientAnomalies(tokens: z.infer<typeof IngredientTokenSchema>[]): string[] {
  const anomalies: string[] = [];

  for (const token of tokens) {
    const raw = token.raw.trim().toLowerCase();
    if (!raw) anomalies.push("EMPTY_INGREDIENT_TOKEN");
    if (PLACEHOLDERS.includes(raw)) anomalies.push(`PLACEHOLDER_TOKEN:${raw}`);
    if (BAD_TOKEN_PATTERNS.some((rx) => rx.test(raw))) anomalies.push(`SUSPICIOUS_TOKEN:${raw}`);
    if (raw.length < 3) anomalies.push(`TOO_SHORT_TOKEN:${raw}`);
  }

  const joined = tokens.map(t => t.raw).join(" | ").toLowerCase();
  if (joined.includes("ingredients:") && tokens.length < 2) {
    anomalies.push("INGREDIENTS_HEADER_WITHOUT_CONTENT");
  }

  return [...new Set(anomalies)];
}

export function validateAdditiveMappings(mappings: z.infer<typeof AdditiveMappingSchema>[]): string[] {
  const issues: string[] = [];

  for (const item of mappings) {
    const uniqueCodes = new Set(item.extractedCodes.map(c => c.toUpperCase()));
    const resolvedCodes = new Set(item.resolved.map(r => r.code.toUpperCase()));

    if (uniqueCodes.size !== resolvedCodes.size) {
      issues.push(`CODE_COUNT_MISMATCH:${item.raw}`);
    }
    if (item.ambiguous) {
      issues.push(`AMBIGUOUS_MAPPING:${item.raw}`);
    }

    const duplicateResolved = new Set<string>();
    for (const r of item.resolved) {
      const key = `${r.code}:${r.name}`.toLowerCase();
      if (duplicateResolved.has(key)) {
        issues.push(`DUPLICATE_RESOLUTION:${item.raw}`);
      }
      duplicateResolved.add(key);
    }

    for (const r of item.resolved) {
      if (r.confidence < 0.85) {
        issues.push(`LOW_MAPPING_CONFIDENCE:${item.raw}:${r.code}`);
      }
    }
  }

  return issues;
}

export function validateNutritionMath(n: z.infer<typeof NutritionSchema>): string[] {
  const issues: string[] = [];

  if (n.saturatedFatG != null && n.totalFatG != null && n.saturatedFatG > n.totalFatG) {
    issues.push("SATURATED_FAT_GT_TOTAL_FAT");
  }
  if (n.totalSugarsG != null && n.carbohydrateG != null && n.totalSugarsG > n.carbohydrateG) {
    issues.push("TOTAL_SUGARS_GT_CARBOHYDRATE");
  }
  if (n.addedSugarsG != null && n.totalSugarsG != null && n.addedSugarsG > n.totalSugarsG) {
    issues.push("ADDED_SUGARS_GT_TOTAL_SUGARS");
  }
  if (n.addedSugarsG != null && n.totalSugarsG == null) {
    issues.push("ADDED_SUGARS_DECLARED_WITHOUT_TOTAL_SUGARS");
  }

  return issues;
}

export function detectDisplayContradictions(input: FinalReportCandidate): string[] {
  const issues: string[] = [];
  const n = input.nutrition;
  const findingText = input.findings.map(f => `${f.type} ${f.message}`.toLowerCase()).join(" | ");

  if ((n.totalSugarsG ?? 0) === 0 && findingText.includes("sugar")) {
    issues.push("SUGAR_FINDING_WITH_ZERO_SUGAR_DISPLAY");
  }
  if ((n.sodiumMg ?? 0) === 0 && findingText.includes("sodium")) {
    issues.push("SODIUM_FINDING_WITH_ZERO_SODIUM_DISPLAY");
  }
  if ((n.saturatedFatG ?? 0) === 0 && findingText.includes("saturated fat")) {
    issues.push("SAT_FAT_FINDING_WITH_ZERO_SAT_FAT_DISPLAY");
  }
  if (input.score != null && input.score >= 80 && input.findings.some(f => f.severity === "high")) {
    issues.push("HIGH_SCORE_WITH_HIGH_SEVERITY_FINDINGS");
  }

  return issues;
}

// --- PUBLISH GATE ---

export function canPublishReport(candidate: FinalReportCandidate): PublishDecision {
  const reasons = [
    ...candidate.ocrAnomalies,
    ...candidate.normalizationAnomalies,
    ...candidate.mappingConflicts,
    ...candidate.nutritionMathFailures,
    ...candidate.displayContradictions,
  ];

  if (!candidate.validationPassed) reasons.push("VALIDATION_NOT_PASSED");
  if (candidate.reviewRequired) reasons.push("MANUAL_REVIEW_REQUIRED");

  return reasons.length === 0 ? { ok: true } : { ok: false, code: "REPORT_BLOCKED", reasons };
}

// --- FINAL CANDIDATE PIPELINE ENTRYPOINT ---

export function validateFinalCandidate(input: unknown) {
  const parsed = FinalReportCandidateSchema.safeParse(input);
  if (!parsed.success) {
    return {
      valid: false,
      state: "needs_review" as const,
      reasons: parsed.error.issues.map(i => `${i.path.join(".")}:${i.message}`),
    };
  }

  const candidate = parsed.data;
  const ocrAnomalies = detectOcrIngredientAnomalies(candidate.ingredients);
  const mappingConflicts = validateAdditiveMappings(candidate.additiveMappings);
  const nutritionMathFailures = validateNutritionMath(candidate.nutrition);
  const displayContradictions = detectDisplayContradictions(candidate);

  const fullCandidate: FinalReportCandidate = {
    ...candidate,
    ocrAnomalies: [...candidate.ocrAnomalies, ...ocrAnomalies],
    mappingConflicts: [...candidate.mappingConflicts, ...mappingConflicts],
    nutritionMathFailures: [...candidate.nutritionMathFailures, ...nutritionMathFailures],
    displayContradictions: [...candidate.displayContradictions, ...displayContradictions],
  };

  const decision = canPublishReport(fullCandidate);

  if (!decision.ok) {
    return {
      valid: false,
      state: "needs_review" as const,
      reasons: decision.reasons,
    };
  }

  return {
    valid: true,
    state: "verified_published" as const,
    reasons: [],
  };
}
