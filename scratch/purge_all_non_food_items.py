import pandas as pd
import re

all_supabase_csv = "all_supabase_products.csv"
confirmed_csv = "india_products_confirmed.csv"
needs_ver_csv = "india_products_needs_verification.csv"

# Comprehensive Non-Food Keywords and Regex Patterns
NON_FOOD_PATTERNS = [
    # Personal Care / Cosmetics / Hygiene
    r'\bSOAP\b', r'\bSHAMPOO\b', r'\bCONDITIONER\b', r'\bFACE WASH\b', r'\bBODY WASH\b',
    r'\bMOISTURIZER\b', r'\bLOTION\b', r'\bCREAM\b.*(SKIN|FACE|BODY|BEAUTY|NIGHT|DAY|HAND|FOOT)',
    r'\bTALC\b', r'\bTALCUM\b', r'\bDEODORANT\b', r'\bDEO\b', r'\bPERFUME\b', r'\bATTAR\b',
    r'\bLIPSTICK\b', r'\bLIP BALM\b', r'\bSUNSCREEN\b', r'\bHAIR OIL\b', r'\bHAIR COLOUR\b',
    r'\bHAIR COLOR\b', r'\bHENNA\b', r'\bMEHENDI\b', r'\bTOOTHPASTE\b', r'\bTOOTHBRUSH\b',
    r'\bMOUTHWASH\b', r'\bSANITARY\b', r'\bDIAPER\b', r'\bTISSUE\b', r'\bCOTTON SWAB\b',
    r'\bEARBUD\b', r'\bBEAUTY\b.*(PRODUCT|BAR|PAD)', r'\bSKINCARE\b', r'\bHAIRCARE\b',
    r'\bPERSONAL CARE\b', r'\bCOSMETIC\b', r'\bVASELINE\b', r'\bNIVEA\b', r'\bPOND\'?S\b',
    r'\bFAIR & LOVELY\b', r'\bGLOW & LOVELY\b', r'\bCINTHOL\b', r'\bLIFEBUOY\b', r'\bLUX\b',
    r'\bSANTOR\b', r'\bSantoor\b', r'\bPEARS\b', r'\bDOVE\b', r'\bDETTOL\b', r'\bSAVLON\b',
    r'\bBOROPLUS\b', r'\bBOROLINE\b', r'\bVICCO\b', r'\bCHARMIS\b', r'\bEMAMI\b.*(HANDSOME|CREAM|LOTION)',
    r'\bNYCIL\b', r'\bDERMICOOL\b',

    # Medicines / Healthcare / Ayurvedic Drugs / Pain Relievers
    r'\bMEDICINE\b', r'\bTABLET\b', r'\bTAB\b', r'\bCAPSULE\b', r'\bCAP\b', r'\bINJECTION\b',
    r'\bOINTMENT\b', r'\bBALM\b', r'\bPAIN RELIEF\b', r'\bAYURVEDIC MEDICINE\b', r'\bPHARMA\b',
    r'\bDRUG\b', r'\bSYRUP\b.*(COUGH|COLD|FEVER|LAXATIVE|SF|ANTACID)', r'\bSOFTOVAC\b',
    r'\bGASEX\b', r'\bAMRUTANJAN\b', r'\bVICKS\b.*(VAPORUB|INHALER|LOZENGE|DROPS)', r'\bMOOV\b',
    r'\bVOLINI\b', r'\bIODEX\b', r'\bZANDU BALM\b', r'\bDISPIRIN\b', r'\bCROCIN\b', r'\bPACIMOL\b',
    r'\bCALPOL\b', r'\bDOLO\b', r'\bCOMBIFLAM\b', r'\bBRUFEN\b', r'\bCLOPIDOGREL\b',
    r'\bSTAMLO\b', r'\bTETRACICLINA\b', r'\bRANITIDINA\b', r'\bORBIX\b', r'\bOROFER\b',
    r'\bSIMILAC\b', r'\bNON-FOOD\b', r'\bNON FOOD\b', r'\bPURGE\b',

    # Cleaning / Household / Laundry
    r'\bDETERGENT\b', r'\bFABRIC SOFTENER\b', r'\bCOMFORT\b.*(MORNING|LILY|FRESH|LIQUID)',
    r'\bSURF EXCEL\b', r'\bTIDE\b', r'\bARIEL\b', r'\bRIN\b', r'\bWHEEL\b', r'\bGHADI\b',
    r'\bDISHWASH\b', r'\bVIM\b', r'\bPRIL\b', r'\bEXO\b', r'\bFLOOR CLEANER\b', r'\bLYSOL\b',
    r'\bHARPIC\b', r'\bCOLIN\b', r'\bTOILET CLEANER\b', r'\bAIR FRESHENER\b', r'\bAER SPRAY\b',
    r'\bODONIL\b', r'\bGODREJ AER\b', r'\bCOTTON MOP\b', r'\bMOP\b', r'\bWIPER\b', r'\bBROOM\b',
    r'\bSPONGE\b', r'\bSCRUB\b', r'\bCLEANING\b',

    # Electronics / Puja / Misc Household Non-Food
    r'\bSTABILIZER\b', r'\bVOLTAGE\b', r'\bBATTERY\b', r'\bCHARGER\b', r'\bCABLE\b', r'\bWIRE\b',
    r'\bELECTRICAL\b', r'\bELECTRONIC\b', r'\bTOY\b', r'\bSTATIONERY\b', r'\bPEN\b', r'\bPENCIL\b',
    r'\bNOTEBOOK\b', r'\bPUJA\b', r'\bCAMPHOR\b', r'\bAGARBATTI\b', r'\bDHOOP\b', r'\bINCENSE\b',
    r'\bCANDLE\b', r'\bMATCHBOX\b', r'\bMATCHES\b', r'\bMOSQUITO\b', r'\bPEST CONTROL\b',
    r'\bCOIL\b', r'\bLIQUIDATOR\b', r'\bGOODKNIGHT\b', r'\bHIT\b.*(SPRAY|MOSQUITO|ROACH)',
    r'\bALL OUT\b', r'\bANIMAL FEED\b', r'\bPET FOOD\b', r'\bDOG FOOD\b', r'\bCAT FOOD\b',
    r'\bPEDIGREE\b', r'\bWHISKAS\b'
]

COMPILED_PATTERN = re.compile('|'.join(NON_FOOD_PATTERNS), re.IGNORECASE)

def is_non_food(row):
    pname = str(row.get('product_name', '') or '')
    brand = str(row.get('brands', '') or '')
    ing = str(row.get('ingredients_text', '') or '')
    add_flags = str(row.get('additive_flags', '') or '')
    
    text = f"{pname} | {brand} | {ing} | {add_flags}"
    
    if COMPILED_PATTERN.search(text):
        return True
    return False

def main():
    print("=== SWEEPING & PURGING ALL NON-FOOD ITEMS ACROSS ALL DATABASES ===")
    
    df_all = pd.read_csv(all_supabase_csv, dtype=str)
    df_confirmed = pd.read_csv(confirmed_csv, dtype=str)
    df_needs_ver = pd.read_csv(needs_ver_csv, dtype=str)

    init_all_len = len(df_all)
    init_conf_len = len(df_confirmed)
    init_nv_len = len(df_needs_ver)

    # Filter out non-food rows
    non_food_all_mask = df_all.apply(is_non_food, axis=1)
    df_all_clean = df_all[~non_food_all_mask].copy()

    non_food_conf_mask = df_confirmed.apply(is_non_food, axis=1)
    df_confirmed_clean = df_confirmed[~non_food_conf_mask].copy()

    non_food_nv_mask = df_needs_ver.apply(is_non_food, axis=1)
    df_needs_ver_clean = df_needs_ver[~non_food_nv_mask].copy()

    purged_all = init_all_len - len(df_all_clean)
    purged_conf = init_conf_len - len(df_confirmed_clean)
    purged_nv = init_nv_len - len(df_needs_ver_clean)

    print(f"Purged from Master CSV ({all_supabase_csv}): {purged_all} records")
    print(f"Purged from Confirmed CSV ({confirmed_csv}): {purged_conf} records")
    print(f"Purged from Needs Verification CSV ({needs_ver_csv}): {purged_nv} records")

    # Save cleaned files
    df_all_clean.to_csv(all_supabase_csv, index=False)
    df_confirmed_clean.to_csv(confirmed_csv, index=False)
    df_needs_ver_clean.to_csv(needs_ver_csv, index=False)

    print(f"Final Clean Master CSV Count: {len(df_all_clean)}")
    print(f"Final Clean Confirmed CSV Count: {len(df_confirmed_clean)}")
    print(f"Final Clean Needs Verification CSV Count: {len(df_needs_ver_clean)}")

if __name__ == '__main__':
    main()
