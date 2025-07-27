# AI Assistant Evaluation Guide

## 🎯 **Overview**

This evaluation framework helps you assess your Aven Assistant's performance across 50 realistic user questions, scoring for:

- **Accuracy**: How well responses address the expected keywords
- **Helpfulness**: How actionable and useful the responses are
- **Citation Quality**: How well responses cite specific information

## 📁 **Files Created**

1. **`evaluation_dataset.json`** - 50 realistic questions with expected keywords
2. **`evaluate_assistant.py`** - Simulation-based evaluation script
3. **`evaluate_with_real_api.py`** - Real API integration evaluation
4. **`requirements_evaluation.txt`** - Python dependencies
5. **`EVALUATION_GUIDE.md`** - This guide

## 🚀 **Quick Start**

### **Step 1: Install Dependencies**
```bash
pip install -r requirements_evaluation.txt
```

### **Step 2: Set Up Environment Variables**
Add to your `.env.local`:
```bash
OPENAI_API_KEY=your-openai-api-key
```

### **Step 3: Run Evaluation**

#### **Option A: Simulation-Based Evaluation**
```bash
python evaluate_assistant.py
```
This uses OpenAI to simulate responses (good for testing the framework).

#### **Option B: Real API Evaluation**
```bash
# Start your Next.js app first
npm run dev

# Then run the evaluation
python evaluate_with_real_api.py
```
This connects to your actual Aven Assistant API.

## 📊 **Evaluation Criteria**

### **Accuracy (1-5 scale)**
- **5**: Completely accurate - directly answers with correct information
- **4**: Mostly accurate - addresses question with minor inaccuracies
- **3**: Somewhat accurate - partially addresses the question
- **2**: Minimally accurate - barely addresses the question
- **1**: Inaccurate - does not address or provides wrong information

### **Helpfulness (1-5 scale)**
- **5**: Extremely helpful - provides clear, actionable information
- **4**: Very helpful - provides useful information with minor gaps
- **3**: Somewhat helpful - provides some useful information
- **2**: Minimally helpful - provides limited useful information
- **1**: Not helpful - does not provide useful information

### **Citation Quality (1-5 scale)**
- **5**: Excellent citations - references specific policies, terms, procedures
- **4**: Good citations - references general information accurately
- **3**: Some citations - provides some specific references
- **2**: Poor citations - vague or general references
- **1**: No citations - no specific references provided

## 📋 **Question Categories**

The evaluation dataset includes 50 questions across:

### **Difficulty Levels**
- **Basic**: Simple, straightforward questions
- **Intermediate**: More complex questions requiring specific knowledge
- **Advanced**: Complex questions about card benefits and policies
- **Urgent**: Time-sensitive questions (lost cards, fraud)

### **Question Types**
- Credit card fees and rates
- Application processes
- Account management
- Security and fraud
- Travel and international use
- Rewards and benefits
- Customer service procedures

## 📈 **Understanding Results**

### **Generated Reports**
1. **JSON Report**: Detailed results with all scores and responses
2. **CSV File**: Spreadsheet-friendly format for analysis
3. **Console Output**: Real-time scoring and progress

### **Key Metrics**
- **Overall Score**: Average of accuracy, helpfulness, and citation quality
- **Success Rate**: Percentage of questions answered successfully
- **Difficulty Breakdown**: Performance by question difficulty
- **Category Breakdown**: Performance by question type

### **Sample Output**
```
📈 EVALUATION SUMMARY
Total Questions: 50
Successful Questions: 48
Success Rate: 96.0%

📊 AVERAGE SCORES
Accuracy: 4.2/5
Helpfulness: 3.8/5
Citation Quality: 3.5/5
Overall: 3.8/5
```

## 🔧 **Customization**

### **Adding New Questions**
Edit `evaluation_dataset.json`:
```json
{
  "id": 51,
  "category": "credit_cards",
  "question": "Your new question here?",
  "expected_response_contains": ["keyword1", "keyword2", "keyword3"],
  "difficulty": "basic",
  "context": "Description of the question context"
}
```

### **Modifying Scoring Criteria**
Edit the evaluation functions in the Python scripts:
- `evaluate_accuracy()`: Adjust keyword matching logic
- `evaluate_helpfulness()`: Modify helpfulness indicators
- `evaluate_citation_quality()`: Update citation criteria

### **Changing API Endpoint**
In `evaluate_with_real_api.py`, modify:
```python
response = requests.post(
    f"{self.api_base_url}/api/search",  # Change endpoint
    json={"query": question, "max_results": 5}
)
```

## 📊 **Advanced Analysis**

### **Using the CSV Results**
```python
import pandas as pd

# Load results
df = pd.read_csv('evaluation_results_20241227_143022.csv')

# Filter by difficulty
basic_questions = df[df['difficulty'] == 'basic']
print(f"Basic questions average score: {basic_questions['average_score'].mean():.2f}")

# Find worst performing questions
worst_questions = df.nsmallest(5, 'average_score')
print("Worst performing questions:")
for _, row in worst_questions.iterrows():
    print(f"- {row['question']}: {row['average_score']:.2f}")
```

### **Creating Visualizations**
```python
import matplotlib.pyplot as plt

# Score distribution
plt.figure(figsize=(10, 6))
df['average_score'].hist(bins=10)
plt.title('Score Distribution')
plt.xlabel('Average Score')
plt.ylabel('Number of Questions')
plt.show()
```

## 🚨 **Troubleshooting**

### **Common Issues**

1. **API Connection Errors**
   - Ensure your Next.js app is running (`npm run dev`)
   - Check the API URL in the evaluation script
   - Verify your API endpoint returns the expected format

2. **OpenAI API Errors**
   - Verify your `OPENAI_API_KEY` is set correctly
   - Check your OpenAI account has sufficient credits
   - Ensure the API key has the correct permissions

3. **Missing Dependencies**
   ```bash
   pip install pandas openai requests python-dotenv
   ```

4. **File Not Found Errors**
   - Ensure `evaluation_dataset.json` is in the same directory
   - Check file permissions

### **Performance Optimization**

1. **Reduce API Calls**: Increase the delay between questions
2. **Batch Processing**: Process questions in smaller batches
3. **Caching**: Cache responses to avoid duplicate API calls

## 📈 **Interpreting Scores**

### **Excellent Performance (4.0-5.0)**
- Your assistant is performing exceptionally well
- Consider expanding to more complex scenarios
- Focus on edge cases and unusual questions

### **Good Performance (3.0-4.0)**
- Solid performance with room for improvement
- Identify weak areas and enhance training data
- Consider adding more specific FAQ entries

### **Needs Improvement (2.0-3.0)**
- Significant improvements needed
- Review and expand your knowledge base
- Consider retraining or fine-tuning your AI model

### **Poor Performance (1.0-2.0)**
- Major issues that need immediate attention
- Review your entire AI pipeline
- Consider fundamental changes to your approach

## 🔄 **Continuous Evaluation**

### **Regular Testing Schedule**
- **Weekly**: Run a subset of critical questions
- **Monthly**: Full evaluation with all 50 questions
- **After Updates**: Test after any system changes

### **Tracking Improvements**
- Keep historical reports to track progress
- Compare scores before and after updates
- Identify trends in performance

### **A/B Testing**
- Test different AI models or configurations
- Compare different knowledge base versions
- Evaluate different response generation strategies

## 📞 **Support**

If you encounter issues or need help customizing the evaluation framework:

1. Check the troubleshooting section above
2. Review the console output for error messages
3. Verify all dependencies are installed correctly
4. Ensure your API endpoints are working properly

---

**Happy Evaluating! 🎯** 