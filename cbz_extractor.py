from pathlib import Path
import shutil
import zipfile
from natsort import natsorted


class CBZExtractor:
    """
    Handles:
    - Cleaning temp directory
    - Extracting CBZ archives
    - Listing images in natural order
    - Cleaning extracted files
    """

    SUPPORTED_EXTENSIONS = {
        ".jpg",
        ".jpeg",
        ".png",
        ".webp"
    }

    def __init__(self):
        self.project_root = Path(__file__).parent
        self.temp_dir = self.project_root / "temp"

    # ---------------------------------------------------------
    # Create/Clean temp directory
    # ---------------------------------------------------------
    def clear_temp(self):
        """Delete old temp directory and recreate it."""

        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)

        self.temp_dir.mkdir(parents=True, exist_ok=True)

    # ---------------------------------------------------------
    # Extract CBZ
    # ---------------------------------------------------------
    def extract_cbz(self, cbz_path):
        """
        Extracts the CBZ archive.

        Parameters
        ----------
        cbz_path : str or Path

        Returns
        -------
        Path
            Extraction directory
        """

        cbz_path = Path(cbz_path)

        if not cbz_path.exists():
            raise FileNotFoundError(cbz_path)

        self.clear_temp()

        with zipfile.ZipFile(cbz_path, "r") as archive:
            archive.extractall(self.temp_dir)

        return self.temp_dir

    # ---------------------------------------------------------
    # Find images
    # ---------------------------------------------------------
    def get_image_files(self, folder=None):
        """
        Returns every supported image in natural order.
        """

        if folder is None:
            folder = self.temp_dir

        folder = Path(folder)

        images = []

        for file in folder.rglob("*"):

            if (
                file.is_file()
                and file.suffix.lower() in self.SUPPORTED_EXTENSIONS
            ):
                images.append(file)

        images = natsorted(images, key=lambda p: str(p))

        return images

    # ---------------------------------------------------------
    # Cleanup
    # ---------------------------------------------------------
    def cleanup(self):
        """Delete extracted files."""

        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)

    # ---------------------------------------------------------
    # Convenience method
    # ---------------------------------------------------------
    def extract_and_list(self, cbz_path):
        """
        Extract archive and immediately return image list.
        """

        folder = self.extract_cbz(cbz_path)

        return self.get_image_files(folder)