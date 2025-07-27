#!/usr/bin/env python3
"""
Excel to Evaluation Dataset Converter
Converts your Excel file with columns C and D into the evaluation format
"""

import pandas as pd
import json
from typing import List, Dict, Any
import os

def convert_excel_to_evaluation(excel_file_path: str, output_file: str = "custom_evaluation_dataset.json"):
    """
    Convert Excel file to evaluation dataset format
    
    Args:
        excel_file_path: Path to your Excel file
        output_file: Output JSON file name
    """
    
    print(f"📊 Loading Excel file: {excel_file_path}")
    
    try:
        # Read Excel file
        df = pd.read_excel(excel_file_path)
        
        print(f"✅ Excel file loaded successfully")
        print(f"📋 Columns found: {list(df.columns)}")
        print(f"📊 Total rows: {len(df)}")
        
        # Display first few rows to understand structure
        print("\n📋 First 5 rows:")
        print(df.head())
        
        # Get column names (assuming C and D are the 3rd and 4th columns)
        column_names = list(df.columns)
        
        if len(column_names) >= 4:
            column_c = column_names[2]  # 3rd column (C)
            column_d = column_names[3]  # 4th column (D)
        else:
            print("⚠️  Warning: Not enough columns found. Using first available columns.")
            column_c = column_names[0] if len(column_names) > 0 else "Column_C"
            column_d = column_names[1] if len(column_names) > 1 else "Column_D"
        
        print(f"\n🎯 Using columns:")
        print(f"Column C: {column_c}")
        print(f"Column D: {column_d}")
        
        # Convert to evaluation format
        evaluation_questions = []
        
        for index, row in df.iterrows():
            # Get the question from column C
            question = str(row[column_c]) if pd.notna(row[column_c]) else ""
            
            # Get expected keywords from column D
            keywords_raw = str(row[column_d]) if pd.notna(row[column_d]) else ""
            
            # Process keywords (split by commas, semicolons, or other delimiters)
            keywords = process_keywords(keywords_raw)
            
            if question and keywords:  # Only add if we have both question and keywords
                evaluation_question = {
                    "id": index + 1,
                    "category": "custom",  # You can modify this based on your data
                    "question": question.strip(),
                    "expected_response_contains": keywords,
                    "difficulty": "basic",  # Default difficulty, you can customize
                    "context": f"User question from row {index + 1}"
                }
                
                evaluation_questions.append(evaluation_question)
        
        # Create the evaluation dataset structure
        evaluation_dataset = {
            "evaluation_questions": evaluation_questions,
            "evaluation_criteria": {
                "accuracy": {
                    "description": "How accurately the response addresses the user's question",
                    "scoring": {
                        "5": "Completely accurate - directly answers the question with correct information",
                        "4": "Mostly accurate - addresses the question with minor inaccuracies",
                        "3": "Somewhat accurate - partially addresses the question",
                        "2": "Minimally accurate - barely addresses the question",
                        "1": "Inaccurate - does not address the question or provides wrong information"
                    }
                },
                "helpfulness": {
                    "description": "How helpful and actionable the response is for the user",
                    "scoring": {
                        "5": "Extremely helpful - provides clear, actionable information",
                        "4": "Very helpful - provides useful information with minor gaps",
                        "3": "Somewhat helpful - provides some useful information",
                        "2": "Minimally helpful - provides limited useful information",
                        "1": "Not helpful - does not provide useful information"
                    }
                },
                "citation_quality": {
                    "description": "How well the response cites or references specific information",
                    "scoring": {
                        "5": "Excellent citations - references specific policies, terms, or procedures",
                        "4": "Good citations - references general information accurately",
                        "3": "Some citations - provides some specific references",
                        "2": "Poor citations - vague or general references",
                        "1": "No citations - no specific references provided"
                    }
                }
            }
        }
        
        # Save to JSON file
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(evaluation_dataset, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Conversion completed!")
        print(f"📁 Output file: {output_file}")
        print(f"📊 Total questions converted: {len(evaluation_questions)}")
        
        # Show sample of converted data
        if evaluation_questions:
            print(f"\n📋 Sample converted question:")
            sample = evaluation_questions[0]
            print(f"Question: {sample['question']}")
            print(f"Expected keywords: {sample['expected_response_contains']}")
        
        return output_file
        
    except Exception as e:
        print(f"❌ Error converting Excel file: {str(e)}")
        return None

def process_keywords(keywords_raw: str) -> List[str]:
    """
    Process keywords from column D into a list
    """
    if not keywords_raw or keywords_raw.lower() in ['nan', 'none', '']:
        return []
    
    # Try different delimiters
    delimiters = [',', ';', '|', '\n', '\t']
    
    for delimiter in delimiters:
        if delimiter in keywords_raw:
            keywords = [kw.strip() for kw in keywords_raw.split(delimiter) if kw.strip()]
            return keywords
    
    # If no delimiter found, treat as single keyword
    return [keywords_raw.strip()]

def main():
    """Main function to run the conversion"""
    print("🔄 Excel to Evaluation Dataset Converter")
    print("=" * 50)
    
    # Get Excel file path from user
    excel_file = input("📁 Enter the path to your Excel file: ").strip()
    
    if not excel_file:
        print("❌ No file path provided")
        return
    
    if not os.path.exists(excel_file):
        print(f"❌ File not found: {excel_file}")
        return
    
    # Convert the file
    output_file = convert_excel_to_evaluation(excel_file)
    
    if output_file:
        print(f"\n🎉 Success! Your evaluation dataset is ready.")
        print(f"📁 File: {output_file}")
        print(f"\n🚀 Next steps:")
        print(f"1. Update the evaluation scripts to use '{output_file}'")
        print(f"2. Run: python evaluate_assistant.py")
        print(f"3. Or run: python evaluate_with_real_api.py")

if __name__ == "__main__":
    main() 