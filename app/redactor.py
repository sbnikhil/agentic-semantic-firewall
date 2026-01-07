import re
from presidio_analyzer import AnalyzerEngine, PatternRecognizer, Pattern
from presidio_anonymizer import AnonymizerEngine

analyzer = AnalyzerEngine()
anonymizer = AnonymizerEngine()

local_phone_pattern = Pattern(
    name="local_phone_pattern",
    regex=r'(\b\d{3}[-.\s]\d{4}\b)', 
    score=0.5 # Lower score because 7 digits can sometimes be other data
)

local_phone_recognizer = PatternRecognizer(
    supported_entity="PHONE_NUMBER", 
    patterns=[local_phone_pattern],
    context=["phone", "call", "cell", "contact", "mobile"] 
)

analyzer.registry.add_recognizer(local_phone_recognizer)

api_key_pattern = Pattern(
    name="api_key_pattern",
    regex=r'(sk-[a-zA-Z0-9]{32,})', # Matches common AI API key formats
    score=1.0
)
api_key_recognizer = PatternRecognizer(
    supported_entity="API_KEY", 
    patterns=[api_key_pattern]
)
analyzer.registry.add_recognizer(api_key_recognizer)

def redact_pii(text: str) -> str:
    """
    Analyzes text for PII (Names, Locations, Emails, etc.) 
    and returns a redacted version.
    """

    analysis_results = analyzer.analyze(
        text=text, 
        language='en',
        entities=["PERSON", "LOCATION", "EMAIL_ADDRESS", "PHONE_NUMBER", "API_KEY"]
    )

    anonymized_result = anonymizer.anonymize(
        text=text,
        analyzer_results=analysis_results
    )

    return anonymized_result.text