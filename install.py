from pathlib import Path
import shutil

working_dir = Path(__file__).parent
install_path = working_dir / Path("install")

if __name__ == "__main__":
    shutil.copytree(
        working_dir / "deps" / "bin",
        install_path,
        ignore=shutil.ignore_patterns(
            "*MaaDbgControlUnit*",
            "*MaaThriftControlUnit*",
            "*MaaWin32ControlUnit*",
            "*MaaRpc*",
        ),
        dirs_exist_ok=True,
    )
    shutil.copytree(
        working_dir / "deps" / "share" / "MaaAgentBinary",
        install_path / "MaaAgentBinary",
        dirs_exist_ok=True,
    )

    shutil.copytree(
        working_dir / "assets" / "resource",
        install_path / "resource",
        dirs_exist_ok=True,
    )
    shutil.copy2(
        working_dir / "assets" / "interface.json",
        install_path,
    )
    shutil.copytree(
        working_dir / "assets" / "MaaCommonAssets" / "OCR" / "ppocr_v4" / "zh_cn",
        install_path / "resource" / "base" / "model" / "ocr",
        dirs_exist_ok=True,
    )
