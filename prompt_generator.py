from pathlib import Path


class PromptGenerator:

    def generate(self, output_folder):

        output_folder = Path(output_folder)

        # Create folder if it doesn't exist
        output_folder.mkdir(
            parents=True,
            exist_ok=True
        )

        prompt = """You are an expert manga recap writer.

Read ALL uploaded images in order.
Wait until every image has been analyzed.

Then generate:

• Complete chronological recap
• 60 second Shorts script
• 3 minute recap
• 5 minute recap

Requirements:

- Natural storytelling
- Character names
- No skipped events
- No repeated information
- Strong hook
- Cliffhanger ending
"""

        prompt_file = output_folder / "prompt.txt"

        with open(prompt_file, "w", encoding="utf-8") as f:
            f.write(prompt)

        return prompt_file