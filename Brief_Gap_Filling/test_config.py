# Test Configuration for Enhanced Gap Filling
# This file contains all necessary test data without Brand_World dependencies

# Standard dimension list for gap filling
STANDARD_DIMENSIONS = [
    'Campaign Theme',
    'Marketing Objectives',
    'Universal Consumer Challenge',
    'Local Consumer Challenge (Market-Specific)',
    'Brand Context/Heritage',
    'Campaign Ambition/Scope',
    'Target Audience (Strategic Segment)',
    'Audience Demographics/Behavior',
    'Single-Minded Message',
    'Tone of Voice',
    'Key Deliverables/Assets',
    'Success Metrics (KPIs)',
    'Mandatory Channels/Formats',
    'Representation/Inclusivity Guidelines',
    'Cultural Adaptation Requirements'
]

# Ballantine Poland brief content
BALLANTINE_POLAND_BRIEF = """
AI Prompt for Poland
Project Brief: AI-Generated Image of Highland Honey Hot Toddy
Objective: To create a visually appealing and realistic image of a Highland Honey Hot Toddy presented in a glass mug, situated on a table with a picturesque mountain landscape in the background. The image will also feature a bottle of Ballantine's Finest next to the drink. This image will be used for promotional purposes, showcasing the warmth and comfort of the drink in a beautiful winter setting.
Image Description:
Main Subject: A glass mug of Highland Honey Hot Toddy
Contents: The mug should be filled with a warm, amber-coloured liquid.
Garnish: A cinnamon stick and a lemon wheel should be visible in the mug.
Steam: Gentle steam rising from the mug, indicating the hot temperature of the drink.
Bottle: A bottle of Ballantine's Finest
Placement: Positioned next to the glass mug, label facing forward and clearly visible.
Details: Ensure the bottle looks realistic with accurate branding and details.
Background: A stunning mountain landscape
Mountains: Snow-capped peaks, possibly part of the Tatra Mountains in Poland.
Sky: Clear blue sky or a slightly overcast sky to evoke a winter atmosphere.
Snow: Snow-covered ground and coniferous trees to enhance the winter setting.
Table Setting:
Table: A rustic wooden table, adding to the cozy, mountain lodge feel.
Additional Elements: Optional elements such as a small jar of honey, a spoon, or a sprig of pine to complement the drink and enhance the winter theme.
Style and Mood:
Warm and Inviting: The overall tone should be warm and inviting, emphasizing the comfort and warmth of the drink.
Natural and Realistic: The image should look natural and realistic, with attention to detail in the textures of the mug, bottle, table, and background scenery.
Cozy Winter Atmosphere: Convey the feeling of a cozy winter retreat in the mountains, making viewers want to experience the drink in that setting.
Technical Specifications:
Resolution: High resolution (at least 72 dpi) suitable for both digital and print use.
Format: JPEG or PNG
Dimensions: 1080x1080 pixels or higher to ensure clarity and detail.
Target Audience:
Demographics: Adults aged 25 and above, particularly those who enjoy winter sports, mountain vacations, and whisky-based drinks.
Purpose: To attract and engage potential customers by showcasing the Highland Honey Hot Toddy and Ballantine's Finest in an appealing and relatable winter setting.
Deadline: Friday 17th January
Additional Notes:
Ensure that the Ballantine's brand is clearly recognizable through the bottle placement, but maintain a natural look.
The image should evoke a sense of relaxation and enjoyment, perfect for promotional materials such as social media posts, website banners, and print advertisements.
By following this brief, the AI platform should be able to generate a compelling and visually stunning image that effectively captures the essence of the Highland Honey Hot Toddy and Ballantine's Finest in a beautiful mountain setting.
"""

# Default brandworld analysis file path
DEFAULT_BRANDWORLD_PATH = "files/brandword_distribution/dimensions_ballantine_poland.json"

# Test configuration
TEST_CONFIG = {
    'brief_name': 'ballantine_poland',
    'brief_content': BALLANTINE_POLAND_BRIEF,
    'dimensions': STANDARD_DIMENSIONS,
    'brandworld_path': DEFAULT_BRANDWORLD_PATH,
    'default_n_versions': 5
} 