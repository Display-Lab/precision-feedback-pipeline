## Dictionary of vignette-determined persona, measure, and causal pathway pairings:
vignAccPairs = {
    "alice": [
        {"acceptable_by": "social loss", "measure": "PONV05"},
        {"acceptable_by": "social better", "measure": "SUS04"},
        {"acceptable_by": "goal approach", "measure": "GLU03"}
    ],
    "bob": [
        {"acceptable_by": "social loss", "measure": "PONV05"},
        {"acceptable_by": "social approach", "measure": "TOC02"}
    ],
    "chikondi": [
        {"acceptable_by": "social gain", "measure": "PUL01"},
        {"acceptable_by": "goal approach", "measure": "GLU03"}
    ],
    "deepa": [
        {"acceptable_by": "social worse", "measure": "GLU01"},
        {"acceptable_by": "social approach", "measure": "TOC02"},
        {"acceptable_by": "improving", "measure": "BP03"}
    ],
    "eugene": [
        {"acceptable_by": "social worse", "measure": "GLU01"},
        {"acceptable_by": "goal gain", "measure": "TOC01"}
    ],
    "fahad": [
        {"acceptable_by": "social gain", "measure": "PUL01"},
        {"acceptable_by": "worsening", "measure": "SUS02"},
        {"acceptable_by": "goal loss", "measure": "NMB03Peds"}
    ],
    "gaile": [
        {"acceptable_by": "social better", "measure": "SUS04"},
        {"acceptable_by": "improving", "measure": "BP03"},
        {"acceptable_by": "worsening", "measure": "SUS02"},
        {"acceptable_by": "goal loss", "measure": "NMB03Peds"},
        {"acceptable_by": "goal gain", "measure": "TOC01"}
    ]
}
## Extracted JSON content for CSV file read-in and posting:
payloadHeader = '''
{
  "@context": {
    "@vocab": "http://schema.org/",
    "slowmo": "http://example.com/slowmo#",
    "csvw": "http://www.w3.org/ns/csvw#",
    "dc": "http://purl.org/dc/terms/",
    "psdo": "http://purl.obolibrary.org/obo/",
    "slowmo:Measure": "http://example.com/slowmo#Measure",
    "slowmo:IsAboutPerformer": "http://example.com/slowmo#IsAboutPerformer",
    "slowmo:ColumnUse": "http://example.com/slowmo#ColumnUse",
    "slowmo:IsAboutTemplate": "http://example.com/slowmo#IsAboutTemplate",
    "slowmo:spek": "http://example.com/slowmo#spek",
    "slowmo:IsAboutCausalPathway": "http://example.com/slowmo#IsAboutCausalPathway",
    "slowmo:IsAboutOrganization": "http://example.com/slowmo#IsAboutOrganization",
    "slowmo:IsAboutMeasure": "http://example.com/slowmo#IsAboutMeasure",
    "slowmo:InputTable": "http://example.com/slowmo#InputTable",
    "slowmo:WithComparator": "http://example.com/slowmo#WithComparator",
    "has_part": "http://purl.obolibrary.org/obo/bfo#BFO_0000051",
    "has_disposition": "http://purl.obolibrary.org/obo/RO_0000091"
  },
  "Performance_data":[
    ["staff_number","measure","month","passed_count","flagged_count","denominator","peer_average_comparator","peer_90th_percentile_benchmark","peer_75th_percentile_benchmark","MPOG_goal"],
'''

payloadFooter = '''
  ],
  "History":{
  },
  "Preferences":{
    "Utilities": {
    "Message_Format": 
      {
        "1": "0.0",
        "2": "0.1",
        "16": "7.5",
        "24": "9.4",
        "18": "11.3",
        "11": "13.2",
        "22": "15.1" ,
        "14": "22.6" ,
        "21": "62.3" ,
        "5":"0.2",
        "15":"4.0",
        "4":"0.9"
      },
    "Display_Format":
      {
        "short_sentence_with_no_chart": "0.0",
        "bar": "37.0",
        "line": "0.0"
      }
  }
}
}
'''
