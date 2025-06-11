dimension_extraction_prompt = """
You are an expert in marketing analysis and parametric modeling. Below is a plain-text marketing brief. Your task is to analyze the content and extract a list of key parametric dimensions that define the structure of the brief. These dimensions will be used later to build a comparative table across multiple briefs (good and bad), so consistency and granularity are important.
Please follow these rules:
Extract only the dimensions (i.e., column names) — do not return any values.
Focus on identifying clear, consistently measurable or comparable parameters (e.g., type of shot, camera angle, background object, position etc.).
Avoid vague or redundant terms; aim for a consistent level of abstraction.
Pay Special attention to photographic terms like angles or type of shot
Return the dimensions as a flat, bullet-point list in the order they appear logically in the brief.
Include between 10–15 core dimensions, depending on content richness.
only return the dimensions as a list in csv format where I will put it into a datatable later, no extra words
"""

dimension_value_extract_prompt = """
You are a marketing analyst AI. Below is a marketing brief in plain text, followed by a finalized list of dimensions.
Your task is to extract the most relevant value for each dimension based on the content of the brief. If a dimension is not mentioned or not clearly stated, leave it blank (do not guess).
Only Return Output JSON with keys 
"""

dimension_gap_filling_prompt = """
You are an expert marketing brief analyst specializing in gap filling for incomplete briefs. You will be provided with:

1. A DIMENSION NAME that needs to be filled
2. A DISTINCT WORD LIST from brand world analysis that contains relevant brand vocabulary
3. CONTEXT from other filled dimensions in the same brief

Your task is to create a meaningful, coherent description for the unfilled dimension using primarily words from the provided distinct word list.

Guidelines:
- USE WORDS FROM THE DISTINCT WORD LIST whenever possible to maintain brand consistency
- Create a 2-4 word phrase or short description that fits the dimension
- Ensure the fill-in is coherent with other dimension values in the brief
- If no relevant words are available in the list, provide a logical inference based on context
- Focus on marketing brief appropriateness and brand voice consistency

Return your response as a JSON object with this exact format:
{
    "filled_value": "<your 2-4 word description using words from the list>",
    "words_used_from_list": ["word1", "word2", "word3"],
    "reasoning": "<brief explanation of why this fill-in makes sense>"
}

Be creative but stay within brand vocabulary and marketing brief conventions.
"""

dimension_evaluation_prompt = """
You are an expert marketing analyst evaluating the quality of dimension fill-in values. You will be given:
1. A dimension name
2. A fill-in value for that dimension
3. All other dimension values in the same table/row

Your task is to evaluate TWO aspects and provide scores from 1-5 (where 5 is the best):

1. DIMENSION-VALUE MATCH: How well does the fill-in value match/align with what the dimension name expects?
   - Score 5: Perfect semantic match, exactly what the dimension should contain
   - Score 4: Very good match, appropriate content with minor issues
   - Score 3: Decent match, generally appropriate but could be better
   - Score 2: Weak match, somewhat related but not quite right
   - Score 1: Poor match, doesn't fit the dimension at all

2. CONTEXT COHERENCE: How well does the fill-in value fit with the other dimension values in the same row?
   - Score 5: Perfect coherence, creates a consistent and logical marketing brief
   - Score 4: Very good coherence, fits well with most other values
   - Score 3: Decent coherence, generally consistent with other values
   - Score 2: Weak coherence, some inconsistencies with other values
   - Score 1: Poor coherence, conflicts or doesn't align with other values

Return your response as a JSON object with exactly this format:
{
    "dimension_value_match_score": <score_1_to_5>,
    "context_coherence_score": <score_1_to_5>,
    "dimension_value_match_reasoning": "<brief explanation for score 1>",
    "context_coherence_reasoning": "<brief explanation for score 2>"
}

Be objective and consistent in your scoring. Focus on marketing brief logic and coherence.
"""

brand_world_plain_text_prompt = """

convert the input file 
"""