import openai
from secret_key import openai_key
import json
import pandas as pd


openai.api_key = openai_key

def extract_financial_data(text):
    prompt = get_prompt_financial() + text
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    content = response.choices[0].message.content

    try:
        data = json.loads(content)
        return pd.DataFrame(data.items(), columns=["Measure", "Value"])

    except (json.JSONDecoder, IndexError):
        pass

    return pd.DataFrame({
        "Measure": ["Company Name", "Stock Symbol", "Revenue", "Net Income", "EPS"],
        "Value": ["", "", "", "", ""]
    })

def get_prompt_financial():
    return '''Retrieve company name, revenue, net income and earnings per share (a.k.a. EPS)
    from the following articles. If you can't find the information from this article 
    then return "". Do not make things up.
    Then retrieve a stock symbol corresponding to that company. For this you can use your
    general knowledge (it does not have to be from this article). Always return your 
    response as a valid JSON string. The format of the string should be this,

    {
    "Company Name": "Alibaba",
    "Stock Symbol":  "BABA",
    "Revenue": "$130.4 billion",
    "Net Income": "$9.9 billion",
    "EPS": "0.0 $" 
    }

    Article
    ========'''


if __name__ == "__main__":
    text = '''
    Apple today announced financial results for its fiscal 2024 fourth quarter ended September 28, 2024. The Company posted quarterly revenue of $94.9 billion, up 6 percent year over year, and quarterly diluted earnings per share of $0.97. Diluted earnings per share was $1.64,1 up 12 percent year over year when excluding the one-time charge recognized during the fourth quarter of 2024 related to the impact of the reversal of the European General Court’s State Aid decision.
    '''

    df = extract_financial_data(text)

    print(df.to_string())



