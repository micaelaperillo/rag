#!/usr/bin/env python3
"""
Dataset Cleaning Script
Removes duplicate videos from the combined dataset based on video_id
"""

import pandas as pd
import os
from pathlib import Path

def clean_dataset(input_file=None, output_file=None, backup=True):
    """
    Remove duplicate videos from the dataset based on video_id
    
    Args:
        input_file (str): Path to input CSV file. If None, uses default combined_dataset.csv
        output_file (str): Path to output CSV file. If None, creates cleaned version
        backup (bool): Whether to create a backup of the original file
    
    Returns:
        pd.DataFrame: The cleaned dataset
    """
    
    # Set default paths
    if input_file is None:
        script_dir = Path(__file__).parent
        project_root = script_dir.parent
        input_file = project_root / "dataset" / "combined_dataset.csv"
    
    if output_file is None:
        input_path = Path(input_file)
        output_file = input_path.parent / f"{input_path.stem}_cleaned{input_path.suffix}"
    
    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"❌ Error: Input file '{input_file}' not found!")
        return None
    
    print(f"📁 Loading dataset from: {input_file}")
    
    try:
        # Load the dataset
        df = pd.read_csv(input_file)
        
        print(f"📊 Original dataset statistics:")
        print(f"   Total rows: {len(df):,}")
        print(f"   Unique video_ids: {df['video_id'].nunique():,}")
        print(f"   Duplicates found: {len(df) - df['video_id'].nunique():,}")
        
        # Show some examples of duplicates if they exist
        duplicates = df[df.duplicated(subset=['video_id'], keep=False)]
        if len(duplicates) > 0:
            print(f"\n🔍 Sample duplicate video_ids:")
            duplicate_ids = duplicates['video_id'].value_counts().head(5)
            for video_id, count in duplicate_ids.items():
                print(f"   {video_id}: {count} occurrences")
        
        # Create backup if requested
        if backup:
            backup_file = str(input_path).replace('.csv', '_backup.csv')
            df.to_csv(backup_file, index=False)
            print(f"💾 Backup created: {backup_file}")
        
        # Remove duplicates based on video_id, keeping the first occurrence
        print(f"\n🧹 Cleaning dataset...")
        df_cleaned = df.drop_duplicates(subset=['video_id'], keep='first')
        
        print(f"✅ Cleaning completed!")
        print(f"📊 Cleaned dataset statistics:")
        print(f"   Total rows: {len(df_cleaned):,}")
        print(f"   Unique video_ids: {df_cleaned['video_id'].nunique():,}")
        print(f"   Rows removed: {len(df) - len(df_cleaned):,}")
        
        # Save the cleaned dataset
        df_cleaned.to_csv(output_file, index=False)
        print(f"💾 Cleaned dataset saved to: {output_file}")
        
        return df_cleaned
        
    except Exception as e:
        print(f"❌ Error processing dataset: {str(e)}")
        return None

def analyze_dataset(input_file=None):
    """
    Analyze the dataset for duplicates and other issues
    
    Args:
        input_file (str): Path to input CSV file
    """
    
    if input_file is None:
        script_dir = Path(__file__).parent
        project_root = script_dir.parent
        input_file = project_root / "dataset" / "combined_dataset.csv"
    
    if not os.path.exists(input_file):
        print(f"❌ Error: Input file '{input_file}' not found!")
        return
    
    print(f"📊 Analyzing dataset: {input_file}")
    
    try:
        df = pd.read_csv(input_file)
        
        print(f"\n📈 Dataset Overview:")
        print(f"   Total rows: {len(df):,}")
        print(f"   Columns: {list(df.columns)}")
        
        print(f"\n🔍 Duplicate Analysis:")
        print(f"   Unique video_ids: {df['video_id'].nunique():,}")
        print(f"   Duplicate video_ids: {len(df) - df['video_id'].nunique():,}")
        
        # Check for other potential duplicates
        title_duplicates = df.duplicated(subset=['title'], keep=False).sum()
        print(f"   Duplicate titles: {title_duplicates:,}")
        
        # Show most common duplicates
        if len(df) - df['video_id'].nunique() > 0:
            print(f"\n🔍 Top duplicate video_ids:")
            duplicate_counts = df['video_id'].value_counts()
            duplicates = duplicate_counts[duplicate_counts > 1].head(10)
            for video_id, count in duplicates.items():
                print(f"   {video_id}: {count} occurrences")
        
        # Check for missing values
        print(f"\n❓ Missing Values:")
        missing_values = df.isnull().sum()
        for col, missing in missing_values.items():
            if missing > 0:
                print(f"   {col}: {missing:,} missing values")
        
        # Show data types
        print(f"\n📋 Data Types:")
        for col, dtype in df.dtypes.items():
            print(f"   {col}: {dtype}")
            
    except Exception as e:
        print(f"❌ Error analyzing dataset: {str(e)}")

def main():
    """
    Main function to run the cleaning script
    """
    import argparse
    
    parser = argparse.ArgumentParser(description='Clean dataset by removing duplicate videos')
    parser.add_argument('--input', '-i', help='Input CSV file path')
    parser.add_argument('--output', '-o', help='Output CSV file path')
    parser.add_argument('--no-backup', action='store_true', help='Skip creating backup file')
    parser.add_argument('--analyze-only', action='store_true', help='Only analyze dataset, do not clean')
    
    args = parser.parse_args()
    
    if args.analyze_only:
        analyze_dataset(args.input)
    else:
        clean_dataset(
            input_file=args.input,
            output_file=args.output,
            backup=not args.no_backup
        )

if __name__ == "__main__":
    main()
