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


brand_world_plain_text_prompt = """

convert the input file 
"""