#!/usr/bin/env python3
"""
Prepare Dataset for Google Colab Training

This script creates a clean dataset zip file optimized for Google Colab training.
It ensures the correct directory structure and includes all necessary files.

Usage:
    python prepare_colab_dataset.py

Output:
    colab_dataset.zip - Ready to upload to Google Colab
"""

import os
import shutil
import zipfile
from pathlib import Path

def create_colab_dataset():
    """Create a clean dataset structure for Colab training"""

    print("🚀 Preparing dataset for Google Colab training...")

    # Source directories
    source_base = Path("dataset/images/train")
    source_train = source_base / "train" / "images"
    source_valid = source_base / "valid" / "images"
    source_test = source_base / "test" / "images"
    source_data_yaml = source_base / "data.yaml"

    # Destination structure for Colab
    colab_dir = Path("colab_dataset")
    colab_images = colab_dir / "images"
    colab_train = colab_images / "train" / "images"
    colab_valid = colab_images / "valid" / "images"
    colab_test = colab_images / "test" / "images"

    # Clean up any existing colab_dataset
    if colab_dir.exists():
        shutil.rmtree(colab_dir)
        print(f"🧹 Cleaned up existing {colab_dir}")

    # Create directory structure
    colab_train.mkdir(parents=True, exist_ok=True)
    colab_valid.mkdir(parents=True, exist_ok=True)
    colab_test.mkdir(parents=True, exist_ok=True)

    # Copy images (handle zipped training images)
    print("📸 Copying training images...")
    if source_train.exists():
        # Check if images are in a zip file
        zip_file = source_train.parent / "images.zip"
        if zip_file.exists():
            print("   📦 Extracting training images.zip...")
            with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                zip_ref.extractall(source_train.parent)
            print("   ✅ Extracted training images from zip")

        for img_file in source_train.glob("*.jpg"):
            shutil.copy2(img_file, colab_train)
        print(f"   ✅ Copied {len(list(colab_train.glob('*.jpg')))} training images")
    else:
        print(f"   ⚠️  Training images directory not found: {source_train}")

    print("📸 Copying validation images...")
    if source_valid.exists():
        for img_file in source_valid.glob("*.jpg"):
            shutil.copy2(img_file, colab_valid)
        print(f"   ✅ Copied {len(list(colab_valid.glob('*.jpg')))} validation images")
    else:
        print(f"   ⚠️  Validation images directory not found: {source_valid}")

    print("📸 Copying test images...")
    if source_test.exists():
        for img_file in source_test.glob("*.jpg"):
            shutil.copy2(img_file, colab_test)
        print(f"   ✅ Copied {len(list(colab_test.glob('*.jpg')))} test images")
    else:
        print(f"   ⚠️  Test images directory not found: {source_test}")

    # Copy and modify data.yaml
    if source_data_yaml.exists():
        print("📄 Setting up data.yaml...")
        shutil.copy2(source_data_yaml, colab_dir / "data.yaml")

        # Update paths in data.yaml to be relative to colab_dataset
        data_yaml_path = colab_dir / "data.yaml"
        with open(data_yaml_path, 'r') as f:
            content = f.read()

        # Replace absolute paths with relative paths
        content = content.replace('train: train/images', 'train: images/train/images')
        content = content.replace('val: valid/images', 'val: images/valid/images')
        content = content.replace('test: test/images', 'test: images/test/images')

        with open(data_yaml_path, 'w') as f:
            f.write(content)

        print("   ✅ Updated data.yaml paths for Colab")
    else:
        print(f"   ❌ data.yaml not found at {source_data_yaml}")

    # Copy model weights if they exist
    yolov8m_path = Path("yolov8m.pt")
    if yolov8m_path.exists():
        shutil.copy2(yolov8m_path, colab_dir)
        print("   ✅ Copied YOLOv8 model weights")

    # Create zip file
    zip_path = Path("colab_dataset.zip")
    print(f"📦 Creating {zip_path}...")

    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in colab_dir.rglob('*'):
            if file_path.is_file():
                arcname = file_path.relative_to(colab_dir.parent)
                zipf.write(file_path, arcname)

    # Clean up
    shutil.rmtree(colab_dir)
    print("🧹 Cleaned up temporary files")

    # Show results
    zip_size = zip_path.stat().st_size / (1024 * 1024)
    print(f"📦 Zip file size: {zip_size:.1f} MB")
    print(f"📁 Contents: {len(list(zipfile.ZipFile(zip_path).namelist()))} files")

    print("\n🎉 Dataset preparation complete!")
    print("\n📋 Next steps:")
    print("1. Upload colab_dataset.zip to Google Colab")
    print("2. Use Option B (Manual Upload) in the notebook")
    print("3. The dataset should now work correctly!")

    return zip_path

def main():
    try:
        zip_file = create_colab_dataset()
        print(f"\n✅ Success! Upload {zip_file} to Google Colab and use Option B.")
    except Exception as e:
        print(f"\n❌ Error preparing dataset: {e}")
        print("\nTroubleshooting:")
        print("- Make sure you're running this from the ml-service directory")
        print("- Check that dataset/images/train/ contains the expected structure")
        print("- Ensure you have write permissions")

if __name__ == "__main__":
    main()
