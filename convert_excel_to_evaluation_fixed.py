#!/usr/bin/env python3
"""
Fixed Excel to Evaluation Dataset Converter
Converts your Excel file using the correct columns: question and answer
"""

import pandas as pd
import json
from typing import List, Dict, Any
import os

def convert_excel_to_evaluation_fixed(excel_file_path: str, output_file: str = "fixed_evaluation_dataset.json"):
    """
    Convert Excel file to evaluation dataset format using correct columns
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
        
        # Use the correct columns based on the actual structure
        column_names = list(df.columns)
        
        # Find the question and answer columns
        question_col = None
        answer_col = None
        
        for col in column_names:
            if 'question' in col.lower():
                question_col = col
            elif 'answer' in col.lower():
                answer_col = col
        
        if not question_col or not answer_col:
            print("❌ Could not find 'question' and 'answer' columns")
            print("Available columns:", column_names)
            return None
        
        print(f"\n🎯 Using columns:")
        print(f"Question column: {question_col}")
        print(f"Answer column: {answer_col}")
        
        # Convert to evaluation format
        evaluation_questions = []
        
        for index, row in df.iterrows():
            # Get the question from the question column
            question = str(row[question_col]) if pd.notna(row[question_col]) else ""
            
            # Get the answer from the answer column
            answer_raw = str(row[answer_col]) if pd.notna(row[answer_col]) else ""
            
            # Process the answer to extract keywords
            keywords = process_answer_to_keywords(answer_raw)
            
            if question and keywords:  # Only add if we have both question and keywords
                evaluation_question = {
                    "id": index + 1,
                    "category": "loan_support",  # Based on your data structure
                    "question": question.strip(),
                    "expected_response_contains": keywords,
                    "difficulty": "basic",  # Default difficulty
                    "context": f"Loan application question from row {index + 1}"
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

def process_answer_to_keywords(answer_raw: str) -> List[str]:
    """
    Process the answer to extract meaningful keywords
    """
    if not answer_raw or answer_raw.lower() in ['nan', 'none', '']:
        return []
    
    # Clean up the answer
    answer_clean = answer_raw.strip()
    
    # Remove quotes if they exist
    if answer_clean.startswith('"') and answer_clean.endswith('"'):
        answer_clean = answer_clean[1:-1]
    
    # Split by common delimiters
    delimiters = [',', ';', '|', '\n', '\t', '. ']
    
    for delimiter in delimiters:
        if delimiter in answer_clean:
            keywords = [kw.strip() for kw in answer_clean.split(delimiter) if kw.strip()]
            # Filter out very short keywords
            keywords = [kw for kw in keywords if len(kw) > 3]
            return keywords
    
    # If no delimiter found, treat as single keyword
    if len(answer_clean) > 3:
        return [answer_clean]
    
    return []

def main():
    """Main function to run the conversion"""
    print("🔄 Fixed Excel to Evaluation Dataset Converter")
    print("=" * 50)
    
    # Use the data.xlsx file directly
    excel_file = "data.xlsx"
    
    if not os.path.exists(excel_file):
        print(f"❌ File not found: {excel_file}")
        return
    
    # Convert the file
    output_file = convert_excel_to_evaluation_fixed(excel_file)
    
    if output_file:
        print(f"\n🎉 Success! Your fixed evaluation dataset is ready.")
        print(f"📁 File: {output_file}")
        print(f"\n🚀 Next steps:")
        print(f"1. Run evaluation with: python evaluate_custom_dataset.py {output_file}")
        print(f"2. Or run: python evaluate_assistant.py")

if __name__ == "__main__":
    main() 