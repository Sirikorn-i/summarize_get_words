import openai
import re
import json
import pandas as pd
import streamlit as st
import base64

# Get the API key from the sidebar called OpenAI API key
user_api_key = st.sidebar.text_input("OpenAI API key", type="password")
client = openai.OpenAI(api_key=user_api_key)

prompt = """Act as a AI translator and English teacher.
        You will recieve a text or a URL of the article from user and you should summarize the given text or article. 
        After summarize the text, you should also extract 10 words from the article that the user gives you.
        Remember to respond in the following format only:
        "The text is about 'summary of the article'
        Check out some of the interesting words here:" 
        Then list the 10 extracted words in another JSON array.
        The words could be adjectives, nouns, verbs, adverbs, etc.
        Each vocab should have 2 fields:
        - "vocab" - the list of words that you extracted from the article that the user gives you
        - "meaning" - the meaning of each extracted word
        The list should immediately follow the format above.
        Remember that the summarized text and the vocab must be in a JSON array.
        Don't say anything at first. Wait for the user to say something.
        """


# Your Streamlit app content

st.title(':books: :blue[Summarize and Extract Vocab]')
st.markdown('Input the article that you want to summarize. \n\
            Our app will give you summary and a few useful words.')

user_input = st.text_area("Input your writing or URL here", height=300)
st.markdown('*Please wait a moment for the app to generate the output.*')

if st.button('Submit your article or URL'):

# if the API key is not valid, show an error message
    if user_api_key == "":
        st.error("Please enter your OpenAI API key.")
        st.stop()

    messages_so_far = [
        {"role": "system", "content": prompt},
        {'role': 'user', 'content': user_input},
    ]
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages_so_far
    )
    response_dictionary = response.choices[0].message.content

    text = response_dictionary
    pattern = re.compile(r'The.*?here:', re.DOTALL)
    result = re.search(pattern, text)

    if result:
        captured_text = result.group(0)
        st.markdown(captured_text)
    else:
        st.markdown("Pattern not found.")

    text = response_dictionary
    pattern = re.compile(r'The.*?here:', re.DOTALL)
    replace = r''
    result = re.sub(pattern, replace, text)
    #print(result)

    sd = json.loads(result)
    print(sd)

    df = pd.DataFrame.from_dict(sd)

    st.table(df)

    st.markdown("#### Download Output")
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="translated_summarized_output.csv">Download CSV</a>'
    st.markdown(href, unsafe_allow_html=True)