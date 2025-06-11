import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Brief_Gap_Filling.utils import main

# Import deepseek_chat from the root utils module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import deepseek_chat

# Standard dimension list (same as used in Brand_World)
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

# Sample brief from Constants (ballantine_poland)
SAMPLE_BRIEF = """
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

def test_gap_filling():
    """
    Test the gap filling functionality with a sample brief
    """
    print("🧪 Testing Brief Gap Filling System")
    print("="*60)
    
    # Path to the Skrewball brandworld analysis
    brandworld_path = "Brand_World/Skrewball Brand World_analysis.json"
    
    if not os.path.exists(brandworld_path):
        print(f"❌ Brandworld analysis file not found: {brandworld_path}")
        print("Please run the Brand_World analysis first to generate the required file.")
        return
    
    print(f"📋 Brief length: {len(SAMPLE_BRIEF)} characters")
    print(f"📊 Dimensions to fill: {len(STANDARD_DIMENSIONS)}")
    print(f"🎯 Brandworld source: {brandworld_path}")
    
    try:
        # Run the gap filling process
        result = main(
            brief_text=SAMPLE_BRIEF,
            dimension_list=STANDARD_DIMENSIONS,
            brandworld_analysis_path=brandworld_path,
            deepseek_chat_func=deepseek_chat,
            output_filename="Brief_Gap_Filling/test_ballantine_gap_filled.json"
        )
        
        print("\n" + "="*60)
        print("🎉 TEST COMPLETED SUCCESSFULLY!")
        print("="*60)
        
        # Print summary of what was achieved
        metadata = result['metadata']
        print(f"\n📈 Final Summary:")
        print(f"  ✅ DeepSeek extracted: {metadata['extraction_summary']['deepseek_filled']} dimensions")
        print(f"  🎯 Brandworld filled: {metadata['extraction_summary']['brandworld_filled']} dimensions")
        print(f"  ❌ No data available: {metadata['extraction_summary']['no_data']} dimensions")
        
        total_filled = metadata['extraction_summary']['deepseek_filled'] + metadata['extraction_summary']['brandworld_filled']
        fill_rate = (total_filled / metadata['total_dimensions']) * 100
        print(f"  📊 Overall fill rate: {fill_rate:.1f}%")
        
        return result
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        return None

if __name__ == "__main__":
    test_gap_filling() 