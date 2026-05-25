import pytest
from unittest.mock import patch
from click.testing import CliRunner

from kraggle import download_dataset, cli, DEFAULT_DATASET_ID
from kagglehub.exceptions import KaggleApiHTTPError


class TestDownloadDataset:
    """Test suite for download_dataset function."""
    
    def test_successful_download(self, tmp_path):
        """Test successful dataset download and validation."""
        # Create a fake dataset directory with files
        fake_dataset = tmp_path / "dataset"
        fake_dataset.mkdir()
        (fake_dataset / "data.csv").write_text("id,name\n1,test\n")
        (fake_dataset / "metadata.txt").write_text("info")
        
        with patch("kraggle.kagglehub.dataset_download", return_value=str(fake_dataset)):
            result = download_dataset("test/dataset")
            assert result == str(fake_dataset)
    
    def test_missing_path(self):
        """Test error when downloaded path doesn't exist."""
        with patch("kraggle.kagglehub.dataset_download", return_value="/nonexistent/path"):
            with pytest.raises(FileNotFoundError, match="does not exist"):
                download_dataset("test/dataset")
    
    def test_path_is_file_not_directory(self, tmp_path):
        """Test error when path is a file, not a directory."""
        fake_file = tmp_path / "file.csv"
        fake_file.write_text("data")
        
        with patch("kraggle.kagglehub.dataset_download", return_value=str(fake_file)):
            with pytest.raises(NotADirectoryError, match="not a directory"):
                download_dataset("test/dataset")
    
    def test_empty_directory(self, tmp_path):
        """Test error when dataset directory is empty."""
        empty_dir = tmp_path / "empty"
        empty_dir.mkdir()
        
        with patch("kraggle.kagglehub.dataset_download", return_value=str(empty_dir)):
            with pytest.raises(ValueError, match="empty"):
                download_dataset("test/dataset")
    
    def test_kaggle_api_error(self):
        """Test handling of Kaggle API errors (e.g., auth failure)."""
        error = KaggleApiHTTPError("403 Forbidden")
        with patch("kraggle.kagglehub.dataset_download", side_effect=error):
            with pytest.raises(KaggleApiHTTPError):
                download_dataset("test/dataset")
    
    def test_generic_exception(self):
        """Test handling of unexpected exceptions."""
        with patch("kraggle.kagglehub.dataset_download", side_effect=RuntimeError("Network timeout")):
            with pytest.raises(RuntimeError):
                download_dataset("test/dataset")


class TestCLI:
    """Test suite for CLI commands."""
    
    def test_cli_help(self):
        """Test CLI help output."""
        runner = CliRunner()
        result = runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        assert "--dataset-id" in result.output
        assert DEFAULT_DATASET_ID in result.output
    
    def test_cli_with_custom_dataset(self, tmp_path):
        """Test CLI with custom dataset ID."""
        fake_dataset = tmp_path / "dataset"
        fake_dataset.mkdir()
        (fake_dataset / "data.csv").write_text("test")
        
        runner = CliRunner()
        with patch("kraggle.kagglehub.dataset_download", return_value=str(fake_dataset)):
            result = runner.invoke(cli, ["--dataset-id", "custom/dataset"])
            assert result.exit_code == 0
            assert "✓ Downloaded to:" in result.output
    
    def test_cli_uses_default_dataset(self, tmp_path):
        """Test CLI uses default dataset ID when not specified."""
        fake_dataset = tmp_path / "dataset"
        fake_dataset.mkdir()
        (fake_dataset / "data.csv").write_text("test")
        
        runner = CliRunner()
        with patch("kraggle.kagglehub.dataset_download", return_value=str(fake_dataset)) as mock_download:
            result = runner.invoke(cli, [])
            assert result.exit_code == 0
            mock_download.assert_called_once_with(DEFAULT_DATASET_ID)
