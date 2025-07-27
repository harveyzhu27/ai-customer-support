#!/usr/bin/env python3
"""
Real API Integration for AI Assistant Evaluation
Connects to your actual Aven Assistant API for evaluation
"""

import json
import time
import requests
from typing import Dict, List, Any
import pandas as pd
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class RealAssistantEvaluator:
    def __init__(self, api_base_url: str = "http://localhost:3000"):
        """Initialize the evaluator with your actual API"""
        self.api_base_url = api_base_url
        
        # Load evaluation dataset
        with open('evaluation_dataset.json', 'r') as f:
            self.dataset = json.load(f)
        
        # Results storage
        self.results = []
        
    def get_assistant_response(self, question: str) -> str:
        """
        Get response from your actual Aven Assistant API
        """
        try:
            # Call your actual search API endpoint
            response = requests.post(
                f"{self.api_base_url}/api/search",
                json={
                    "query": question,
                    "max_results": 5
                },
                headers={
                    "Content-Type": "application/json"
                },
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                # Extract the assistant's response from your API
                # Adjust this based on your actual API response structure
                if 'response' in data:
                    return data['response']
                elif 'answer' in data:
                    return data['answer']
                elif 'message' in data:
                    return data['message']
                else:
                    return str(data)  # Fallback to string representation
            else:
                return f"API Error: {response.status_code} - {response.text}"
                
        except requests.exceptions.RequestException as e:
            return f"Connection Error: {str(e)}"
        except Exception as e:
            return f"Error: {str(e)}"
    
    def test_question(self, question_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Test a single question and get the assistant's response
        """
        question = question_data['question']
        expected_keywords = question_data['expected_response_contains']
        
        print(f"\n🔍 Testing Question {question_data['id']}: {question}")
        print(f"📋 Expected keywords: {expected_keywords}")
        
        try:
            # Get response from your actual assistant
            response = self.get_assistant_response(question)
            
            # Evaluate the response
            accuracy_score = self.evaluate_accuracy(response, expected_keywords)
            helpfulness_score = self.evaluate_helpfulness(response, question)
            citation_score = self.evaluate_citation_quality(response)
            
            result = {
                'question_id': question_data['id'],
                'question': question,
                'category': question_data['category'],
                'difficulty': question_data['difficulty'],
                'expected_keywords': expected_keywords,
                'assistant_response': response,
                'accuracy_score': accuracy_score,
                'helpfulness_score': helpfulness_score,
                'citation_score': citation_score,
                'average_score': (accuracy_score + helpfulness_score + citation_score) / 3,
                'timestamp': datetime.now().isoformat()
            }
            
            print(f"✅ Accuracy: {accuracy_score}/5")
            print(f"✅ Helpfulness: {helpfulness_score}/5")
            print(f"✅ Citation Quality: {citation_score}/5")
            print(f"📊 Average Score: {result['average_score']:.2f}/5")
            
            return result
            
        except Exception as e:
            print(f"❌ Error testing question {question_data['id']}: {str(e)}")
            return {
                'question_id': question_data['id'],
                'question': question,
                'error': str(e),
                'accuracy_score': 0,
                'helpfulness_score': 0,
                'citation_score': 0,
                'average_score': 0,
                'timestamp': datetime.now().isoformat()
            }
    
    def evaluate_accuracy(self, response: str, expected_keywords: List[str]) -> int:
        """
        Evaluate how accurately the response addresses the expected keywords
        """
        response_lower = response.lower()
        keyword_matches = sum(1 for keyword in expected_keywords if keyword.lower() in response_lower)
        
        # Calculate accuracy score based on keyword matches
        match_percentage = keyword_matches / len(expected_keywords)
        
        if match_percentage >= 0.8:
            return 5  # Completely accurate
        elif match_percentage >= 0.6:
            return 4  # Mostly accurate
        elif match_percentage >= 0.4:
            return 3  # Somewhat accurate
        elif match_percentage >= 0.2:
            return 2  # Minimally accurate
        else:
            return 1  # Inaccurate
    
    def evaluate_helpfulness(self, response: str, question: str) -> int:
        """
        Evaluate how helpful and actionable the response is
        """
        # Check for helpful indicators
        helpful_indicators = [
            'how to', 'steps', 'process', 'contact', 'call', 'visit',
            'website', 'online', 'app', 'login', 'account', 'customer service',
            'support', 'help', 'assist', 'guide', 'instructions'
        ]
        
        response_lower = response.lower()
        helpful_count = sum(1 for indicator in helpful_indicators if indicator in response_lower)
        
        # Check response length (longer responses tend to be more helpful)
        word_count = len(response.split())
        
        # Calculate helpfulness score
        if helpful_count >= 3 and word_count >= 50:
            return 5  # Extremely helpful
        elif helpful_count >= 2 and word_count >= 30:
            return 4  # Very helpful
        elif helpful_count >= 1 and word_count >= 20:
            return 3  # Somewhat helpful
        elif word_count >= 10:
            return 2  # Minimally helpful
        else:
            return 1  # Not helpful
    
    def evaluate_citation_quality(self, response: str) -> int:
        """
        Evaluate how well the response cites specific information
        """
        # Check for citation indicators
        citation_indicators = [
            'according to', 'policy states', 'terms and conditions',
            'card agreement', 'fee schedule', 'interest rate',
            'annual fee', 'late payment fee', 'foreign transaction fee',
            'credit limit', 'APR', 'grace period', 'billing cycle',
            'customer service', 'support team', 'fraud department'
        ]
        
        response_lower = response.lower()
        citation_count = sum(1 for indicator in citation_indicators if indicator in response_lower)
        
        # Check for specific numbers/percentages (indicating specific information)
        import re
        numbers = re.findall(r'\d+\.?\d*%?', response)
        
        if citation_count >= 3 and len(numbers) >= 2:
            return 5  # Excellent citations
        elif citation_count >= 2 and len(numbers) >= 1:
            return 4  # Good citations
        elif citation_count >= 1:
            return 3  # Some citations
        elif len(numbers) >= 1:
            return 2  # Poor citations
        else:
            return 1  # No citations
    
    def run_evaluation(self) -> None:
        """
        Run the complete evaluation on all questions
        """
        print("🚀 Starting Real API Evaluation")
        print(f"🌐 API Base URL: {self.api_base_url}")
        print("=" * 50)
        
        questions = self.dataset['evaluation_questions']
        total_questions = len(questions)
        
        for i, question_data in enumerate(questions, 1):
            print(f"\n📝 Progress: {i}/{total_questions}")
            result = self.test_question(question_data)
            self.results.append(result)
            
            # Add a small delay to avoid overwhelming your API
            time.sleep(2)
        
        self.generate_report()
    
    def generate_report(self) -> None:
        """
        Generate comprehensive evaluation report
        """
        print("\n📊 Generating Evaluation Report")
        print("=" * 50)
        
        # Convert results to DataFrame for analysis
        df = pd.DataFrame(self.results)
        
        # Calculate overall statistics
        total_questions = len(df)
        successful_questions = len(df[df['average_score'] > 0])
        
        # Calculate average scores
        avg_accuracy = df['accuracy_score'].mean()
        avg_helpfulness = df['helpfulness_score'].mean()
        avg_citation = df['citation_score'].mean()
        avg_overall = df['average_score'].mean()
        
        # Calculate scores by difficulty
        difficulty_stats = df.groupby('difficulty').agg({
            'accuracy_score': 'mean',
            'helpfulness_score': 'mean',
            'citation_score': 'mean',
            'average_score': 'mean'
        }).round(2)
        
        # Calculate scores by category
        category_stats = df.groupby('category').agg({
            'accuracy_score': 'mean',
            'helpfulness_score': 'mean',
            'citation_score': 'mean',
            'average_score': 'mean'
        }).round(2)
        
        # Generate report
        report = {
            'evaluation_summary': {
                'total_questions': total_questions,
                'successful_questions': successful_questions,
                'success_rate': f"{(successful_questions/total_questions)*100:.1f}%",
                'average_scores': {
                    'accuracy': round(avg_accuracy, 2),
                    'helpfulness': round(avg_helpfulness, 2),
                    'citation_quality': round(avg_citation, 2),
                    'overall': round(avg_overall, 2)
                }
            },
            'difficulty_breakdown': difficulty_stats.to_dict(),
            'category_breakdown': category_stats.to_dict(),
            'detailed_results': self.results
        }
        
        # Save detailed report
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_filename = f"real_api_evaluation_report_{timestamp}.json"
        
        with open(report_filename, 'w') as f:
            json.dump(report, f, indent=2)
        
        # Print summary
        print(f"\n📈 EVALUATION SUMMARY")
        print(f"Total Questions: {total_questions}")
        print(f"Successful Questions: {successful_questions}")
        print(f"Success Rate: {report['evaluation_summary']['success_rate']}")
        print(f"\n📊 AVERAGE SCORES")
        print(f"Accuracy: {avg_accuracy:.2f}/5")
        print(f"Helpfulness: {avg_helpfulness:.2f}/5")
        print(f"Citation Quality: {avg_citation:.2f}/5")
        print(f"Overall: {avg_overall:.2f}/5")
        
        print(f"\n📁 Detailed report saved to: {report_filename}")
        
        # Save results to CSV for further analysis
        csv_filename = f"real_api_evaluation_results_{timestamp}.csv"
        df.to_csv(csv_filename, index=False)
        print(f"📊 Results saved to CSV: {csv_filename}")

def main():
    """Main function to run the evaluation"""
    try:
        # You can change the API URL if your app is running on a different port
        evaluator = RealAssistantEvaluator(api_base_url="http://localhost:3000")
        evaluator.run_evaluation()
    except Exception as e:
        print(f"❌ Evaluation failed: {str(e)}")

if __name__ == "__main__":
    main() 