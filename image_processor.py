from pathlib import Path
from PIL import Image


class ImageProcessor:
    """
    Handles:
    - Opening images
    - Flattening transparency
    - Resizing
    - Saving as JPEG
    """

    def __init__(self, max_width=1200, quality=85):
        self.max_width = int(max_width)
        self.quality = int(quality)

    # ---------------------------------------------------------
    # Resize while maintaining aspect ratio
    # ---------------------------------------------------------

    def resize_image(self, image):
        width, height = image.size

        if width <= self.max_width:
            return image

        ratio = self.max_width / width
        new_height = int(height * ratio)

        return image.resize(
            (self.max_width, new_height),
            Image.Resampling.LANCZOS
        )

    # ---------------------------------------------------------
    # Remove transparency
    # ---------------------------------------------------------

    def flatten_transparency(self, image):

        if image.mode in ("RGBA", "LA"):

            background = Image.new(
                "RGB",
                image.size,
                (255, 255, 255)
            )

            background.paste(image, mask=image.split()[-1])

            return background

        if image.mode == "P":

            image = image.convert("RGBA")

            background = Image.new(
                "RGB",
                image.size,
                (255, 255, 255)
            )

            background.paste(image, mask=image.split()[-1])

            return background

        return image.convert("RGB")

    # ---------------------------------------------------------
    # Process one image
    # ---------------------------------------------------------

    def process_image(self, image_path):
        """
        Returns a processed Pillow Image object.
        """

        image = Image.open(image_path)

        image = self.flatten_transparency(image)

        image = self.resize_image(image)

        return image

    # ---------------------------------------------------------
    # Save image as JPEG
    # ---------------------------------------------------------

    def save_jpeg(self, image, output_path):

        output_path = Path(output_path)

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        image.save(
            output_path,
            format="JPEG",
            quality=self.quality,
            optimize=True
        )

    # ---------------------------------------------------------
    # Convenience method
    # ---------------------------------------------------------

    def process_and_save(
        self,
        input_path,
        output_path
    ):

        image = self.process_image(input_path)

        self.save_jpeg(
            image,
            output_path
        )

        image.close()