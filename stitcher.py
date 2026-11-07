from pathlib import Path
from PIL import Image

from image_processor import ImageProcessor


class Stitcher:
    """
    Stitches processed images vertically into strips.
    """

    def __init__(
        self,
        max_width=1200,
        quality=85,
        pages_per_strip=10,
        output_root="Output"
    ):

        self.processor = ImageProcessor(
            max_width=max_width,
            quality=quality
        )

        self.pages_per_strip = int(pages_per_strip)
        self.output_root = Path(output_root)

    # --------------------------------------------------

    def stitch(self, image_files, chapter_name=None, start_part_number=1):

        # All chapters share one output folder; chapter_name remains accepted
        # for backwards compatibility with callers using the old signature.
        output_folder = self.output_root
        output_folder.mkdir(
            parents=True,
            exist_ok=True
        )

        total = len(image_files)

        part = int(start_part_number)

        for start in range(0, total, self.pages_per_strip):

            group = image_files[
                start:start + self.pages_per_strip
            ]

            self.create_strip(
                group,
                output_folder,
                part
            )

            part += 1

        return output_folder

    # --------------------------------------------------

    def create_strip(
        self,
        image_paths,
        output_folder,
        part_number
    ):

        processed_images = []

        widths = []
        heights = []

        # Process one image at a time
        for path in image_paths:

            img = self.processor.process_image(path)

            processed_images.append(img)

            widths.append(img.width)
            heights.append(img.height)

        strip_width = max(widths)
        strip_height = sum(heights)

        strip = Image.new(
            "RGB",
            (strip_width, strip_height),
            "white"
        )

        y = 0

        for img in processed_images:

            strip.paste(img, (0, y))

            y += img.height

            img.close()

        filename = f"{part_number:03d}.jpg"

        output_path = output_folder / filename

        self.processor.save_jpeg(
            strip,
            output_path
        )

        strip.close()