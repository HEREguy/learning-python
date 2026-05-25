
from pathlib import Path
import rich_click as click
import kagglehub
from kagglehub.exceptions import KaggleApiHTTPError

click.rich_click.TEXT_MARKUP = True

DEFAULT_DATASET_ID = "cedricaubin/ai-ml-salaries"


def download_dataset(dataset_id: str) -> str:
    """Download a Kaggle dataset and validate the output."""
    try:
        path = kagglehub.dataset_download(dataset_id)
        # Validate path exists and contains files
        dataset_path = Path(path)
        if not dataset_path.exists():
            raise FileNotFoundError(f"Downloaded dataset path does not exist: {path}")
        if not dataset_path.is_dir():
            raise NotADirectoryError(f"Dataset path is not a directory: {path}")

        files = list(dataset_path.iterdir())
        if not files:
            raise ValueError(f"Downloaded dataset directory is empty: {path}")

        click.echo(f"✓ Downloaded to: {path}")
        click.echo(f"✓ Found {len(files)} file(s)/folder(s)")
        return path
    except KaggleApiHTTPError as e:
        click.echo(f"✗ Kaggle API error: {e}", err=True)
        raise
    except Exception as e:
        click.echo(f"✗ Unexpected error: {e}", err=True)
        raise


@click.command()
@click.option(
    "--dataset-id",
    default=DEFAULT_DATASET_ID,
    show_default=True,
    help="Kaggle dataset ID (owner/dataset-name)",
)
def cli(dataset_id: str) -> None:
    """Download and validate a Kaggle dataset."""
    download_dataset(dataset_id)


if __name__ == "__main__":
    cli()
