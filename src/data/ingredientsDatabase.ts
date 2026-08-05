import { Ingredient } from '../types';

export const INGREDIENT_DATABASE: Ingredient[] = [
  {
    id: 'ing_e102',
    canonicalName: 'Tartrazine',
    scientificName: 'Trisodium 1-(4-sulfonatophenyl)-4-(4-sulfonatophenylazo)-5-pyrazolone-3-carboxylate',
    synonyms: ['FD&C Yellow No. 5', 'Yellow 5', 'INS 102', 'E102', 'CI 19140'],
    insNumber: '102',
    eNumber: 'E102',
    category: 'ARTIFICIAL_COLOR',
    riskLevel: 'HIGH',
    baseRiskWeight: -15,
    description: 'A synthetic lemon yellow azo dye used as a food coloring. Linked to hyperactivity in children (Southampton study) and allergic reactions in sensitive individuals.',
    processingLevel: 'NOVA_4_ULTRA_PROCESSED',
    regulatoryRecords: [
      {
        countryCode: 'IN',
        countryName: 'India (FSSAI)',
        flagEmoji: '🇮🇳',
        status: 'RESTRICTED',
        restrictionDetails: 'Permitted in specified food items up to 100 mg/kg maximum limit under FSSAR 2011.',
        regulationRef: 'FSSAI Standards 2.4.5'
      },
      {
        countryCode: 'EU',
        countryName: 'European Union (EFSA)',
        flagEmoji: '🇪🇺',
        status: 'RESTRICTED',
        restrictionDetails: 'Requires mandatory warning label: "May have an adverse effect on activity and attention in children". Banned in Norway and Austria previously.',
        regulationRef: 'EU Regulation No 1333/2008 Annex V'
      },
      {
        countryCode: 'US',
        countryName: 'United States (FDA)',
        flagEmoji: '🇺🇸',
        status: 'RESTRICTED',
        restrictionDetails: 'Approved with mandatory label disclosure requirement due to bronchial asthma trigger risks.',
        regulationRef: '21 CFR 74.705'
      },
      {
        countryCode: 'JP',
        countryName: 'Japan (MHLW)',
        flagEmoji: '🇯🇵',
        status: 'RESTRICTED',
        restrictionDetails: 'Strict upper concentration limits enforced for confectionery.',
        regulationRef: 'Japan Food Sanitation Act List 1'
      }
    ],
    citations: [
      {
        id: 'pmid_17825405',
        title: 'Food additives and hyperactive behaviour in 3-year-old and 8/9-year-old children in the community: a randomised, double-blinded, placebo-controlled trial',
        journal: 'The Lancet',
        year: 2007,
        doi: '10.1016/S0140-6736(07)61306-3',
        summary: 'Rigorous Southampton clinical trial demonstrating significant increase in hyperactivity in children consuming mixtures containing Tartrazine.',
        evidenceStrength: 'STRONG'
      }
    ]
  },
  {
    id: 'ing_e150d',
    canonicalName: 'Sulfite Ammonia Caramel',
    scientificName: 'Class IV Caramel Color',
    synonyms: ['Caramel IV', 'INS 150d', 'E150d', 'Caramel Color Class IV'],
    insNumber: '150d',
    eNumber: 'E150d',
    category: 'ARTIFICIAL_COLOR',
    riskLevel: 'HIGH',
    baseRiskWeight: -15,
    description: 'Dark brown color produced by heating carbohydrates with ammonium and sulfite compounds. Contains 4-Methylimidazole (4-MEI), a potential carcinogen formed during manufacture.',
    processingLevel: 'NOVA_4_ULTRA_PROCESSED',
    regulatoryRecords: [
      {
        countryCode: 'IN',
        countryName: 'India (FSSAI)',
        flagEmoji: '🇮🇳',
        status: 'RESTRICTED',
        restrictionDetails: 'Permitted in carbonated soft drinks up to 1000 mg/kg.',
        regulationRef: 'FSSAI Additives Schedule 2'
      },
      {
        countryCode: 'EU',
        countryName: 'European Union (EFSA)',
        flagEmoji: '🇪🇺',
        status: 'RESTRICTED',
        restrictionDetails: 'EFSA established combined ADI of 300 mg/kg bw/day; 4-MEI impurities strictly capped.',
        regulationRef: 'EFSA Journal 2011;9(3):2004'
      },
      {
        countryCode: 'US',
        countryName: 'United States (FDA)',
        flagEmoji: '🇺🇸',
        status: 'RESTRICTED',
        restrictionDetails: 'California Proposition 65 requires cancer warning labels for products exposing consumers to >29 mcg/day of 4-MEI.',
        regulationRef: 'Cal. Code Regs. tit. 27, § 27001'
      },
      {
        countryCode: 'JP',
        countryName: 'Japan (MHLW)',
        flagEmoji: '🇯🇵',
        status: 'APPROVED',
        restrictionDetails: 'Approved food color additive under standard specifications.',
        regulationRef: 'MHLW Japan Additive Standard'
      }
    ],
    citations: [
      {
        id: 'ntp_tr535',
        title: 'NTP Toxicology and Carcinogenesis Studies of 4-Methylimidazole in F344/N Rats and B6C3F1 Mice',
        journal: 'National Toxicology Program Technical Report',
        year: 2007,
        doi: '10.2307/NTP-TR-535',
        summary: 'Clear evidence of carcinogenic activity of 4-MEI (impurity in Caramel IV) in alveolar/bronchiolar neoplasms in male and female mice.',
        evidenceStrength: 'STRONG'
      }
    ]
  },
  {
    id: 'ing_e621',
    canonicalName: 'Monosodium Glutamate',
    scientificName: 'Sodium 2-aminopentanedioate',
    synonyms: ['MSG', 'INS 621', 'E621', 'Sodium Glutamate', 'Ajinomoto'],
    insNumber: '621',
    eNumber: 'E621',
    category: 'FLAVOR_ENHANCER',
    riskLevel: 'MEDIUM',
    baseRiskWeight: -8,
    description: 'Sodium salt of glutamic acid used to impart umami flavor. While generally recognized as safe by major regulators, high doses cause transient symptoms in sensitive individuals and encourage overeating of ultra-processed food.',
    processingLevel: 'NOVA_4_ULTRA_PROCESSED',
    regulatoryRecords: [
      {
        countryCode: 'IN',
        countryName: 'India (FSSAI)',
        flagEmoji: '🇮🇳',
        status: 'RESTRICTED',
        restrictionDetails: 'Prohibited in food intended for infants below 12 months. Mandatory declaration: "CONTAINS MONOSODIUM GLUTAMATE. NOT RECOMMENDED FOR INFANTS UNDER 12 MONTHS".',
        regulationRef: 'FSSAI Packaging & Labelling Reg 2.4.5:18'
      },
      {
        countryCode: 'EU',
        countryName: 'European Union (EFSA)',
        flagEmoji: '🇪🇺',
        status: 'RESTRICTED',
        restrictionDetails: 'EFSA re-evaluated in 2017 establishing a safe intake level of 30 mg/kg body weight per day.',
        regulationRef: 'EFSA Journal 2017;15(7):4911'
      },
      {
        countryCode: 'US',
        countryName: 'United States (FDA)',
        flagEmoji: '🇺🇸',
        status: 'APPROVED',
        restrictionDetails: 'Classified as GRAS (Generally Recognized as Safe). Must be declared on label.',
        regulationRef: '21 CFR 182.1'
      },
      {
        countryCode: 'JP',
        countryName: 'Japan (MHLW)',
        flagEmoji: '🇯🇵',
        status: 'APPROVED',
        restrictionDetails: 'Widely approved with standard manufacturing practices.',
        regulationRef: 'Japan Food Additive Guidelines'
      }
    ],
    citations: [
      {
        id: 'pmid_10736382',
        title: 'Monosodium glutamate: a review of its physiological and toxicological properties',
        journal: 'Clinical & Experimental Allergy',
        year: 2000,
        doi: '10.1046/j.1365-2222.2000.00787.x',
        summary: 'Evaluated MSG symptom complex; confirms transient flushing and headache in susceptible individuals at >3g fasting intake.',
        evidenceStrength: 'MODERATE'
      }
    ]
  },
  {
    id: 'ing_e951',
    canonicalName: 'Aspartame',
    scientificName: 'N-(L-α-Aspartyl)-L-phenylalanine 1-methyl ester',
    synonyms: ['NutraSweet', 'Equal', 'INS 951', 'E951', 'Artificial Sweetener 951'],
    insNumber: '951',
    eNumber: 'E951',
    category: 'SWEETENER',
    riskLevel: 'HIGH',
    baseRiskWeight: -15,
    description: 'An intense artificial non-nutritive sweetener ~200 times sweeter than sucrose. Classified as "possibly carcinogenic to humans" (Group 2B) by IARC (WHO) in July 2023.',
    processingLevel: 'NOVA_4_ULTRA_PROCESSED',
    regulatoryRecords: [
      {
        countryCode: 'IN',
        countryName: 'India (FSSAI)',
        flagEmoji: '🇮🇳',
        status: 'RESTRICTED',
        restrictionDetails: 'Mandatory warning: "CONTAINS ARTIFICIAL SWEETENER AND FOR CALORIE CONSCIOUS. NOT RECOMMENDED FOR CHILDREN. CONTAINS PHENYLALANINE".',
        regulationRef: 'FSSAI Labelling Regulations 2020'
      },
      {
        countryCode: 'EU',
        countryName: 'European Union (EFSA)',
        flagEmoji: '🇪🇺',
        status: 'RESTRICTED',
        restrictionDetails: 'ADI set at 40 mg/kg body weight. Must display phenylketonuria warning.',
        regulationRef: 'EFSA ANS Panel 2013'
      },
      {
        countryCode: 'US',
        countryName: 'United States (FDA)',
        flagEmoji: '🇺🇸',
        status: 'RESTRICTED',
        restrictionDetails: 'FDA ADI set at 50 mg/kg bw/day. Phenylketonurics warning required on all retail packages.',
        regulationRef: '21 CFR 172.804'
      },
      {
        countryCode: 'JP',
        countryName: 'Japan (MHLW)',
        flagEmoji: '🇯🇵',
        status: 'APPROVED',
        restrictionDetails: 'Approved high-intensity sweetener.',
        regulationRef: 'MHLW Approved Additive List'
      }
    ],
    citations: [
      {
        id: 'who_iarc_2023',
        title: 'IARC Monographs evaluate the carcinogenicity of aspartame, methyleugenol, and isoeugenol',
        journal: 'WHO / IARC News Release',
        year: 2023,
        doi: '10.1016/S1470-2045(23)00341-8',
        summary: 'IARC classified Aspartame as possibly carcinogenic to humans (Group 2B) based on limited evidence for hepatocellular carcinoma.',
        evidenceStrength: 'STRONG'
      }
    ]
  },
  {
    id: 'ing_palm_oil',
    canonicalName: 'Palm Oil',
    scientificName: 'Elaeis guineensis oil',
    synonyms: ['Palmolein', 'Hydrogenated Palm Fat', 'Refined Palm Oil', 'Vegetable Fat (Palm)'],
    category: 'WHOLE_FOOD',
    riskLevel: 'MEDIUM',
    baseRiskWeight: -8,
    description: 'Vegetable oil derived from oil palms. High in saturated fatty acids (~50%) and prone to forming 3-MCPD and glycidyl fatty acid esters during high-temperature industrial refining.',
    processingLevel: 'NOVA_3_PROCESSED_FOOD',
    regulatoryRecords: [
      {
        countryCode: 'IN',
        countryName: 'India (FSSAI)',
        flagEmoji: '🇮🇳',
        status: 'APPROVED',
        restrictionDetails: 'Widely permitted edible oil. Blend limits regulated.',
        regulationRef: 'FSSAI Fats & Oils Standards 2.2'
      },
      {
        countryCode: 'EU',
        countryName: 'European Union (EFSA)',
        flagEmoji: '🇪🇺',
        status: 'RESTRICTED',
        restrictionDetails: 'EFSA warned of genotoxic 3-MCPD & Glycidyl esters formed during palm oil refining above 200°C.',
        regulationRef: 'EFSA Journal 2016;14(5):4426'
      },
      {
        countryCode: 'US',
        countryName: 'United States (FDA)',
        flagEmoji: '🇺🇸',
        status: 'APPROVED',
        restrictionDetails: 'GRAS status for edible oil applications.',
        regulationRef: 'FDA GRAS Notice No. GRN 000882'
      },
      {
        countryCode: 'JP',
        countryName: 'Japan (MHLW)',
        flagEmoji: '🇯🇵',
        status: 'APPROVED',
        restrictionDetails: 'Standard edible oil regulatory approval.',
        regulationRef: 'MHLW Japan Food Standards'
      }
    ],
    citations: [
      {
        id: 'pmid_27173787',
        title: 'Process contaminants in vegetable oils: 3-MCPD and glycidyl esters risk evaluation',
        journal: 'EFSA Scientific Opinion',
        year: 2016,
        doi: '10.2903/j.efsa.2016.4426',
        summary: 'Identified significant health risks for younger age groups consuming refined palm oil containing elevated glycidyl esters.',
        evidenceStrength: 'STRONG'
      }
    ]
  },
  {
    id: 'ing_e319',
    canonicalName: 'TBHQ (Tertiary Butylhydroquinone)',
    scientificName: '2-(1,1-Dimethylethyl)-1,4-benzenediol',
    synonyms: ['TBHQ', 'INS 319', 'E319', 'Antioxidant 319'],
    insNumber: '319',
    eNumber: 'E319',
    category: 'PRESERVATIVE',
    riskLevel: 'HIGH',
    baseRiskWeight: -15,
    description: 'A synthetic aromatic organic compound which is a type of phenol. Used to preserve fats and oils against rancidity. Animal studies associate high exposure with immune dysfunction and DNA damage.',
    processingLevel: 'NOVA_4_ULTRA_PROCESSED',
    regulatoryRecords: [
      {
        countryCode: 'IN',
        countryName: 'India (FSSAI)',
        flagEmoji: '🇮🇳',
        status: 'RESTRICTED',
        restrictionDetails: 'Max limit 0.02% of fat content in edible oils and fats.',
        regulationRef: 'FSSAI Additives Schedule 2'
      },
      {
        countryCode: 'EU',
        countryName: 'European Union (EFSA)',
        flagEmoji: '🇪🇺',
        status: 'RESTRICTED',
        restrictionDetails: 'Strict ADI limit of 0.7 mg/kg body weight per day.',
        regulationRef: 'EFSA ANS Panel 2004'
      },
      {
        countryCode: 'US',
        countryName: 'United States (FDA)',
        flagEmoji: '🇺🇸',
        status: 'RESTRICTED',
        restrictionDetails: 'FDA caps concentration at 0.02% of total oil/fat content of the food.',
        regulationRef: '21 CFR 172.185'
      },
      {
        countryCode: 'JP',
        countryName: 'Japan (MHLW)',
        flagEmoji: '🇯🇵',
        status: 'BANNED',
        restrictionDetails: 'Not on the list of permitted food additives in Japan for human consumption.',
        regulationRef: 'Japan Ministry of Health Approved List'
      }
    ],
    citations: [
      {
        id: 'pmid_33758066',
        title: 'Evaluation of the immunotoxic potential of tBHQ using high-throughput screening data',
        journal: 'International Journal of Environmental Research and Public Health',
        year: 2021,
        doi: '10.3390/ijerph18073532',
        summary: 'Found tBHQ impairs immune response by suppressing T-cell activation and altering cytokine production.',
        evidenceStrength: 'STRONG'
      }
    ]
  },
  {
    id: 'ing_e171',
    canonicalName: 'Titanium Dioxide',
    scientificName: 'Titanium(IV) oxide',
    synonyms: ['INS 171', 'E171', 'CI 77891', 'Titanium White'],
    insNumber: '171',
    eNumber: 'E171',
    category: 'ARTIFICIAL_COLOR',
    riskLevel: 'HIGH',
    baseRiskWeight: -15,
    description: 'An inorganic whitening pigment. Banned in the European Union in 2022 due to genotoxicity concerns regarding nanoparticle accumulation in human organs.',
    processingLevel: 'NOVA_4_ULTRA_PROCESSED',
    regulatoryRecords: [
      {
        countryCode: 'IN',
        countryName: 'India (FSSAI)',
        flagEmoji: '🇮🇳',
        status: 'RESTRICTED',
        restrictionDetails: 'Currently permitted under GMP in chewing gum and select foods (under regulatory review).',
        regulationRef: 'FSSAI Additives Schedule 2011'
      },
      {
        countryCode: 'EU',
        countryName: 'European Union (EFSA)',
        flagEmoji: '🇪🇺',
        status: 'BANNED',
        restrictionDetails: 'BANNED across all 27 EU member states as a food additive (E171) since August 2022 due to non-excludable genotoxicity.',
        regulationRef: 'EU Regulation 2022/63'
      },
      {
        countryCode: 'US',
        countryName: 'United States (FDA)',
        flagEmoji: '🇺🇸',
        status: 'RESTRICTED',
        restrictionDetails: 'Permitted up to 1% by weight of food (currently under consumer petition for ban).',
        regulationRef: '21 CFR 73.575'
      },
      {
        countryCode: 'JP',
        countryName: 'Japan (MHLW)',
        flagEmoji: '🇯🇵',
        status: 'RESTRICTED',
        restrictionDetails: 'Permitted under technical specifications.',
        regulationRef: 'Japan Food Additives Act'
      }
    ],
    citations: [
      {
        id: 'efsa_e171_2021',
        title: 'Safety assessment of titanium dioxide (E 171) as a food additive',
        journal: 'EFSA Journal',
        year: 2021,
        doi: '10.2903/j.efsa.2021.6585',
        summary: 'EFSA concluded Titanium Dioxide can no longer be considered safe as a food additive because genotoxicity after nanoparticle ingestion cannot be ruled out.',
        evidenceStrength: 'STRONG'
      }
    ]
  },
  {
    id: 'ing_e330',
    canonicalName: 'Citric Acid',
    scientificName: '2-hydroxypropane-1,2,3-tricarboxylic acid',
    synonyms: ['INS 330', 'E330', 'Acidulant 330'],
    insNumber: '330',
    eNumber: 'E330',
    category: 'PRESERVATIVE',
    riskLevel: 'EXCELLENT',
    baseRiskWeight: 0,
    description: 'A weak organic acid naturally found in citrus fruits. Manufactured via fermentation. Used as an acidity regulator and antioxidant. Completely safe.',
    processingLevel: 'NOVA_2_PROCESSED_INGREDIENT',
    regulatoryRecords: [
      { countryCode: 'IN', countryName: 'India (FSSAI)', flagEmoji: '🇮🇳', status: 'APPROVED', regulationRef: 'FSSAI GMP' },
      { countryCode: 'EU', countryName: 'European Union (EFSA)', flagEmoji: '🇪🇺', status: 'APPROVED', regulationRef: 'EFSA Annex II' },
      { countryCode: 'US', countryName: 'United States (FDA)', flagEmoji: '🇺🇸', status: 'APPROVED', regulationRef: '21 CFR 184.1033' },
      { countryCode: 'JP', countryName: 'Japan (MHLW)', flagEmoji: '🇯🇵', status: 'APPROVED', regulationRef: 'MHLW Safe List' }
    ],
    citations: [
      {
        id: 'fao_who_330',
        title: 'Evaluation of Certain Food Additives (Citric Acid)',
        journal: 'JECFA Technical Report',
        year: 2018,
        doi: '10.1002/jecfa.330',
        summary: 'JECFA established ADI "not specified", confirming high safety margin for human consumption.',
        evidenceStrength: 'STRONG'
      }
    ]
  },
  {
    id: 'ing_whole_wheat',
    canonicalName: 'Whole Wheat Flour',
    scientificName: 'Triticum aestivum flour',
    synonyms: ['Atta', 'Whole Wheat', 'Whole Grain Flour'],
    category: 'WHOLE_FOOD',
    riskLevel: 'EXCELLENT',
    baseRiskWeight: 5,
    description: 'Nutritious unrefined flour made by grinding the entire wheat kernel including germ, endosperm, and bran. Rich in dietary fiber, B vitamins, and minerals.',
    processingLevel: 'NOVA_1_UNPROCESSED',
    regulatoryRecords: [
      { countryCode: 'IN', countryName: 'India (FSSAI)', flagEmoji: '🇮🇳', status: 'APPROVED', regulationRef: 'FSSAI Grain Standards' },
      { countryCode: 'EU', countryName: 'European Union (EFSA)', flagEmoji: '🇪🇺', status: 'APPROVED', regulationRef: 'EU Agricultural Reg' },
      { countryCode: 'US', countryName: 'United States (FDA)', flagEmoji: '🇺🇸', status: 'APPROVED', regulationRef: '21 CFR 137.200' },
      { countryCode: 'JP', countryName: 'Japan (MHLW)', flagEmoji: '🇯🇵', status: 'APPROVED', regulationRef: 'Japan Grain Standard' }
    ],
    citations: [
      {
        id: 'pmid_27144663',
        title: 'Whole grain consumption and risk of cardiovascular disease, cancer, and all cause and cause specific mortality: systematic review and dose-response meta-analysis',
        journal: 'BMJ',
        year: 2016,
        doi: '10.1136/bmj.i2716',
        summary: 'High whole grain consumption reduces cardiovascular and all-cause mortality significantly.',
        evidenceStrength: 'STRONG'
      }
    ]
  },
  {
    id: 'ing_cereal_extract',
    canonicalName: 'Cereal Extract (Malt Barley & Wheat)',
    scientificName: 'Hordeum vulgare / Triticum extractum',
    synonyms: ['Malt Extract', 'Barley Malt', 'Cereal Extract'],
    category: 'WHOLE_FOOD',
    riskLevel: 'LOW',
    baseRiskWeight: 0,
    description: 'Grain extract produced by malting barley and wheat. Provides natural carbohydrates, maltose, and distinctive flavor.',
    processingLevel: 'NOVA_2_PROCESSED_INGREDIENT',
    regulatoryRecords: [
      { countryCode: 'IN', countryName: 'India (FSSAI)', flagEmoji: '🇮🇳', status: 'APPROVED', regulationRef: 'FSSAI Standards 2.4' },
      { countryCode: 'EU', countryName: 'European Union (EFSA)', flagEmoji: '🇪🇺', status: 'APPROVED', regulationRef: 'EFSA Food Reg' }
    ],
    citations: []
  },
  {
    id: 'ing_sugar',
    canonicalName: 'Added Refined Sugar (Sucrose)',
    scientificName: 'Sucrose',
    synonyms: ['Sugar', 'Refined Sugar', 'Sucrose', 'White Sugar'],
    category: 'SWEETENER',
    riskLevel: 'MEDIUM',
    baseRiskWeight: -5,
    description: 'Refined disaccharide derived from sugarcane or sugar beet. High intake drives dental caries, metabolic dysfunction, obesity, and cardiovascular risk.',
    processingLevel: 'NOVA_2_PROCESSED_INGREDIENT',
    regulatoryRecords: [
      { countryCode: 'IN', countryName: 'India (FSSAI)', flagEmoji: '🇮🇳', status: 'RESTRICTED', restrictionDetails: 'FSSAI guidelines advise reducing added sugar consumption.', regulationRef: 'FSSAI Eat Right India' }
    ],
    citations: []
  },
  {
    id: 'ing_cocoa_solids',
    canonicalName: 'Cocoa Solids',
    scientificName: 'Theobroma cacao powder',
    synonyms: ['Cocoa Powder', 'Cocoa Solids'],
    category: 'WHOLE_FOOD',
    riskLevel: 'LOW',
    baseRiskWeight: 0,
    description: 'Non-fat cocoa solids containing natural polyphenols, flavonoids, and minerals.',
    processingLevel: 'NOVA_2_PROCESSED_INGREDIENT',
    regulatoryRecords: [],
    citations: []
  },
  {
    id: 'ing_milk_solids',
    canonicalName: 'Milk Solids',
    scientificName: 'Bovine milk solids',
    synonyms: ['Skimmed Milk Powder', 'Dairy Solids'],
    category: 'WHOLE_FOOD',
    riskLevel: 'LOW',
    baseRiskWeight: 0,
    description: 'Dehydrated milk component containing dairy proteins (casein, whey) and lactose.',
    processingLevel: 'NOVA_2_PROCESSED_INGREDIENT',
    regulatoryRecords: [],
    citations: []
  },
  {
    id: 'ing_e150c',
    canonicalName: 'Ammonia Caramel (INS 150c)',
    scientificName: 'Caramel Class III - Ammonia Process',
    synonyms: ['Caramel III', 'INS 150c', 'E150c', 'Ammonia Caramel'],
    insNumber: '150c',
    eNumber: 'E150c',
    category: 'ARTIFICIAL_COLOR',
    riskLevel: 'MEDIUM',
    baseRiskWeight: -8,
    description: 'Synthetic brown color produced by heating carbohydrates in the presence of ammonium compounds. May contain trace 4-MEI residues.',
    processingLevel: 'NOVA_4_ULTRA_PROCESSED',
    regulatoryRecords: [
      { countryCode: 'IN', countryName: 'India (FSSAI)', flagEmoji: '🇮🇳', status: 'RESTRICTED', restrictionDetails: 'Permitted in specified foods with strict ADI limits.', regulationRef: 'FSSAI Standards 2.4.5' },
      { countryCode: 'EU', countryName: 'European Union (EFSA)', flagEmoji: '🇪🇺', status: 'RESTRICTED', restrictionDetails: 'ADI established at 300 mg/kg bw/day.', regulationRef: 'EFSA Opinion 2011' }
    ],
    citations: []
  },
  {
    id: 'ing_e471',
    canonicalName: 'Mono- and Diglycerides of Fatty Acids (INS 471)',
    scientificName: 'Mono- and Diglycerides of Fatty Acids',
    synonyms: ['INS 471', 'E471', 'Emulsifier 471'],
    insNumber: '471',
    eNumber: 'E471',
    category: 'EMULSIFIER',
    riskLevel: 'LOW',
    baseRiskWeight: 0,
    description: 'Synthetic emulsifier derived from vegetable or animal fats used to blend fat and water components.',
    processingLevel: 'NOVA_4_ULTRA_PROCESSED',
    regulatoryRecords: [],
    citations: []
  },
  {
    id: 'ing_e322',
    canonicalName: 'Soy Lecithin (INS 322)',
    scientificName: 'Phosphatidylcholine from Glycine max',
    synonyms: ['Lecithin', 'INS 322', 'E322', 'Soya Lecithin', 'Sunflower Lecithin'],
    insNumber: '322',
    eNumber: 'E322',
    category: 'EMULSIFIER',
    riskLevel: 'LOW',
    baseRiskWeight: 0,
    description: 'Natural phospholipid emulsifier derived from soybeans or sunflowers. Generally recognized as safe (GRAS). Minor allergen concern for severe soy allergy sufferers.',
    processingLevel: 'NOVA_3_PROCESSED_FOOD',
    regulatoryRecords: [
      {
        countryCode: 'IN',
        countryName: 'India (FSSAI)',
        flagEmoji: '🇮🇳',
        status: 'APPROVED',
        restrictionDetails: 'Permitted emulsifier in most food categories under FSSAI.',
        regulationRef: 'FSSAI Food Additives Regulations 2011'
      },
      {
        countryCode: 'EU',
        countryName: 'European Union (EFSA)',
        flagEmoji: '🇪🇺',
        status: 'APPROVED',
        restrictionDetails: 'Quantum satis in most food categories. No ADI specified (safe at normal use levels).',
        regulationRef: 'EU Regulation No 1333/2008'
      },
      {
        countryCode: 'US',
        countryName: 'United States (FDA)',
        flagEmoji: '🇺🇸',
        status: 'APPROVED',
        restrictionDetails: 'GRAS status. Soy must be declared as an allergen on label.',
        regulationRef: '21 CFR 184.1400'
      },
      {
        countryCode: 'JP',
        countryName: 'Japan (MHLW)',
        flagEmoji: '🇯🇵',
        status: 'APPROVED',
        restrictionDetails: 'Widely approved emulsifier with standard use levels.',
        regulationRef: 'Japan Food Additive Guidelines'
      }
    ],
    citations: []
  },
  {
    id: 'ing_e500ii',
    canonicalName: 'Sodium Hydrogen Carbonate (INS 500(ii))',
    scientificName: 'Sodium Bicarbonate (NaHCO₃)',
    synonyms: ['Baking Soda', 'INS 500(ii)', 'E500(ii)', 'Sodium Bicarbonate', 'Raising Agent 500'],
    insNumber: '500(ii)',
    eNumber: 'E500(ii)',
    category: 'RAISING_AGENT',
    riskLevel: 'LOW',
    baseRiskWeight: 0,
    description: 'Sodium bicarbonate used as a leavening and raising agent. Releases carbon dioxide when heated or in contact with acids, producing a light texture. Generally recognized as safe (GRAS).',
    processingLevel: 'NOVA_3_PROCESSED_FOOD',
    regulatoryRecords: [
      {
        countryCode: 'IN',
        countryName: 'India (FSSAI)',
        flagEmoji: '🇮🇳',
        status: 'APPROVED',
        restrictionDetails: 'Permitted raising agent in bakery and malt-based products. Quantum satis.',
        regulationRef: 'FSSAI Food Additives Regulations 2011'
      },
      {
        countryCode: 'EU',
        countryName: 'European Union (EFSA)',
        flagEmoji: '🇪🇺',
        status: 'APPROVED',
        restrictionDetails: 'Quantum satis in most food categories. No ADI required.',
        regulationRef: 'EU Regulation No 1333/2008'
      },
      {
        countryCode: 'US',
        countryName: 'United States (FDA)',
        flagEmoji: '🇺🇸',
        status: 'APPROVED',
        restrictionDetails: 'GRAS status. Widely used in baked goods and beverage mixes.',
        regulationRef: '21 CFR 184.1736'
      },
      {
        countryCode: 'JP',
        countryName: 'Japan (MHLW)',
        flagEmoji: '🇯🇵',
        status: 'APPROVED',
        restrictionDetails: 'Approved leavening agent with no quantity restrictions for standard food use.',
        regulationRef: 'Japan Food Additive Guidelines'
      }
    ],
    citations: []
  },
  {
    id: 'ing_orange_juice',
    canonicalName: 'Whole Squeezed Orange Juice',
    scientificName: 'Citrus sinensis juice',
    synonyms: ['Orange Juice', 'Squeezed Orange Juice', 'Whole Squeezed Orange Juice'],
    category: 'WHOLE_FOOD',
    riskLevel: 'LOW',
    baseRiskWeight: 0,
    description: '100% natural squeezed orange juice rich in Vitamin C, potassium, and antioxidants.',
    processingLevel: 'NOVA_1_UNPROCESSED',
    regulatoryRecords: [],
    citations: []
  },
  {
    id: 'ing_vitamin_min_premix',
    canonicalName: 'Fortified Vitamin & Mineral Premix',
    scientificName: 'Micronutrient Fortification Blend',
    synonyms: ['Vitamin & Mineral Premix', 'Fortified Premix', 'Micronutrient Premix'],
    category: 'WHOLE_FOOD',
    riskLevel: 'LOW',
    baseRiskWeight: 0,
    description: 'Essential micronutrient fortification blend containing Iron, Zinc, and B-Vitamins (Folic Acid, Thiamine).',
    processingLevel: 'NOVA_1_UNPROCESSED',
    regulatoryRecords: [],
    citations: []
  }
];
