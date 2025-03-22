import anthropic
import base64
import json
import os
import re

client = anthropic.Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY"),
)


def extract_json_from_text(text):
    # Look for content between ```json and ``` markers
    pattern = r'```json\s*(.*?)\s*```'
    match = re.search(pattern, text, re.DOTALL)

    if match:
        json_str = match.group(1)
        return json.loads(json_str)
    else:
        return None

def extract_content_from_pdf(pdf_path):
    """Stage 1: Extract content from PDF and divide into logical sections."""
    with open(pdf_path, "rb") as f:
        pdf_data = base64.b64encode(f.read()).decode("utf-8")

    response = client.messages.create(
        model="claude-3-7-sonnet-20250219",
        max_tokens=4000,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "document",
                        "source": {
                            "type": "base64",
                            "media_type": "application/pdf",
                            "data": pdf_data
                        }
                    },
                    {
                        "type": "text",
                        "text": "Analyze the content of this PDF. Identify logical sections based on topics or chapters. Extract each section's main concepts, formulas, and examples. Create a JSON structure with the following format: {\"sections\": [{\"id\": \"unique_id\", \"title\": \"section_title\", \"concepts\": [...], \"formulas\": [{\"description\": \"...\", \"latex\": \"...\"}], \"examples\": [...]}]}. Make sure all formulas are correctly represented in LaTeX."
                    }
                ]
            }
        ]
    )

    # Extract JSON from response
    content = response.content[0].text
    try:

        structured_content = extract_json_from_text(content)
        return structured_content
    except:
        return {"error": "Error parsing JSON", "raw_content": content}


def plan_animation_for_section(section):
    """Stage 2: Plan animation for a single section."""
    section_json = json.dumps(section)

    response = client.messages.create(
        model="claude-3-7-sonnet-20250219",
        max_tokens=4000,
        messages=[
            {
                "role": "user",
                "content": f"""
                Here is a section from the PDF:

                {section_json}

                Create a detailed animation plan for this section, including all concepts and formulas.
                For each formula describe:
                1. How it should appear (e.g., gradually, all at once)
                2. Which elements should be highlighted or explained separately
                3. What visual examples could help understand the formula

                Present the result in JSON format:
                {{
                    "section_id": "{section.get('id', '')}",
                    "section_title": "{section.get('title', '')}",
                    "animations": [
                        {{
                            "type": "formula|concept|example",
                            "content": "what to display",
                            "latex": "latex representation if applicable",
                            "steps": [
                                {{
                                    "description": "step description",
                                    "action": "animation type (Write, Transform, etc.)"
                                }}
                            ]
                        }}
                    ]
                }}
                """
            }
        ]
    )

    # Extract JSON from response
    content = str(response.content[0])
    content = response.content[0].text
    try:

        structured_content = extract_json_from_text(content)
        return structured_content

    except:
        return {"error": "Error parsing JSON", "raw_content": content}


def generate_manim_code_for_section(animation_plan):
    """Stage 3: Generate ManimLib code for a single section."""
    plan_json = json.dumps(animation_plan)

    response = client.messages.create(
        model="claude-3-7-sonnet-20250219",
        max_tokens=4000,
        messages=[
            {
                "role": "user",
                "content": f"""
                Here is the animation plan for a section:

                {plan_json}

                Generate ManimLib code for this specific section. Create a Scene class named after the section title.

                Use ManimLib syntax (3Blue1Brown's original Manim library, NOT the Community Edition).

                Important syntax guidelines:
                - Use 'from manimlib import *' instead of 'from manim import *'
                - Use TexMobject or TextMobject instead of MathTex
                - Use COLOR constants like RED, BLUE, etc. for colors
                - Position objects with .to_edge(), .next_to(), etc.

                Important requirements:
                - Include code comments
                - Use TexMobject for LaTeX formulas
                - Add visual elements (colors, arrows, boxes) to highlight important parts
                - Include self.play() methods for smooth animations
                - Add self.wait() between key animations

                Make sure the code is fully functional and can be run independently.
                """
            }
        ]
    )

    # Extract code blocks
    manim_code = response.content[0].text
    code_blocks = re.findall(r'```python(.*?)```', manim_code, re.DOTALL)
    if code_blocks:
        return "\n".join(code_blocks).strip()
    else:
        return manim_code



# instead of that, we can use Timur's version
def merge_manim_code(code_sections):
    """Combine multiple ManimLib code sections into a single file."""
    imports = []
    scene_classes = []

    for code in code_sections:
        # Extract import statements
        import_lines = []
        for line in code.split('\n'):
            if line.startswith('import ') or line.startswith('from '):
                import_lines.append(line)
        imports.extend(import_lines)

        # Extract class definitions
        class_pattern = r'class\s+\w+\(Scene\):.*?(?=class|\Z)'
        scene_pattern = re.compile(class_pattern, re.DOTALL)
        for scene_match in scene_pattern.finditer(code):
            scene_classes.append(scene_match.group(0))

    # Remove duplicate imports
    unique_imports = list(dict.fromkeys(imports))

    # Combine everything
    combined_code = "\n".join(unique_imports) + "\n\n" + "\n\n".join(scene_classes)

    # Add main function to run all scenes
    scene_names = []
    for scene_class in scene_classes:
        match = re.search(r'class\s+(\w+)\(Scene\)', scene_class)
        if match:
            scene_names.append(match.group(1))

    if scene_names:
        main_function = "\n\nif __name__ == \"__main__\":\n"
        main_function += "    # To run all scenes sequentially, uncomment this block\n"
        main_function += "    # import sys\n"
        main_function += "    # from os import path\n"
        main_function += "    # sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))\n"
        for scene in scene_names:
            main_function += f"    # {scene}().render()\n"

        combined_code += main_function

    return combined_code


def pdf_to_manim_sections(pdf_path, output_dir):
    """Complete pipeline from PDF to multiple ManimLib code files, one per section."""
    os.makedirs(output_dir, exist_ok=True)

    print("Stage 1: Extracting content and dividing into sections...")
    structured_content = extract_content_from_pdf(pdf_path)

    if "error" in structured_content:
        print(f"Error in content extraction: {structured_content}")
        return

    # Extract sections
    sections = structured_content.get("sections", [])
    if not sections:
        print("No sections found in the PDF.")
        return

    print(f"Found {len(sections)} sections.")

    animation_plans = []
    code_sections = []

    for i, section in enumerate(sections):
        section_id = section.get("id", f"section_{i + 1}")
        section_title = section.get("title", f"Section {i + 1}")
        clean_title = re.sub(r'[^\w]', '_', section_title).lower()

        print(f"Processing section {i + 1}/{len(sections)}: {section_title}")

        # Stage 2: Plan animation for this section
        print(f"  Planning animation...")
        animation_plan = plan_animation_for_section(section)
        animation_plans.append(animation_plan)

        # Stage 3: Generate ManimLib code for this section
        print(f"  Generating ManimLib code...")
        manim_code = generate_manim_code_for_section(animation_plan)
        code_sections.append(manim_code)

        # Save individual section code
        with open(f"{output_dir}/{clean_title}.py", "w") as f:
            f.write(manim_code)

        print(f"  Saved to {output_dir}/{clean_title}.py")

    # Save combined results
    with open(f"{output_dir}/all_sections.json", "w") as f:
        json.dump(structured_content, f, indent=2)

    with open(f"{output_dir}/all_animation_plans.json", "w") as f:
        json.dump(animation_plans, f, indent=2)

    # Create combined Manim code file
    combined_code = merge_manim_code(code_sections)
    with open(f"{output_dir}/combined_animation.py", "w") as f:
        f.write(combined_code)

    print(f"Done! Results saved to {output_dir}/")
    print(f"Combined animation saved to {output_dir}/combined_animation.py")


# Usage example
if __name__ == "__main__":
    pdf_to_manim_sections("statistics_formulas.pdf", "output/statistics_animations")