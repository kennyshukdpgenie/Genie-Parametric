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

# Minimal brief to test brandworld filling
MINIMAL_BRIEF = """
Create a whiskey campaign that's fun and playful.
Target young adults who like to try new things.
"""

def test_minimal_brief_gap_filling():
    """
    Test the gap filling functionality with a minimal brief to trigger brandworld filling
    """
    print("🧪 Testing Brief Gap Filling with Minimal Brief")
    print("="*60)
    
    # Path to the Skrewball brandworld analysis
    brandworld_path = "Brand_World/Skrewball Brand World_analysis.json"
    
    if not os.path.exists(brandworld_path):
        print(f"❌ Brandworld analysis file not found: {brandworld_path}")
        print("Please run the Brand_World analysis first to generate the required file.")
        return
    
    print(f"📋 Brief length: {len(MINIMAL_BRIEF)} characters")
    print(f"📊 Dimensions to fill: {len(STANDARD_DIMENSIONS)}")
    print(f"🎯 Brandworld source: {brandworld_path}")
    print(f"📝 Brief content: '{MINIMAL_BRIEF.strip()}'")
    
    try:
        # Run the gap filling process
        result = main(
            brief_text=MINIMAL_BRIEF,
            dimension_list=STANDARD_DIMENSIONS,
            brandworld_analysis_path=brandworld_path,
            deepseek_chat_func=deepseek_chat,
            output_filename="Brief_Gap_Filling/test_minimal_gap_filled.json"
        )
        
        print("\n" + "="*60)
        print("🎉 MINIMAL BRIEF TEST COMPLETED!")
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
        
        # Show some examples of brandworld-filled dimensions
        brandworld_filled = result['detailed_analysis']['source_breakdown']['brandworld_probability']
        if brandworld_filled:
            print(f"\n🎯 Brandworld-filled dimensions ({len(brandworld_filled)}):")
            for dim in brandworld_filled[:3]:  # Show first 3
                value = result['filled_table']['dimensions'][dim]
                print(f"  • {dim}: {value}")
        
        return result
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        return None

if __name__ == "__main__":
    test_minimal_brief_gap_filling() 