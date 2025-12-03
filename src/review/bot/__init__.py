"""OpenAI LLM powered Review-bot."""

try:
    import importlib.metadata as importlib_metadata
except ModuleNotFoundError:
    import importlib_metadata

__version__ = importlib_metadata.version("pr-review-bot")

from .misc import open_logger
from .open_ai_interface import review_file, review_folder, review_patch, review_patch_local
