import streamlit as st

# Apply custom styles for better formatting
st.markdown("""
    <style>
        body {
            font-family: sans-serif;
            line-height: 1.6;
        }
        h1 {
            font-size: 26px;
            color: #333;
            margin-bottom: 15px;
        }
        h2 {
            font-size: 22px;
            color: #444;
            margin-bottom: 10px;
        }
        h3 {
            font-size: 18px;
            color: #555;
            margin-bottom: 8px;
        }
        p, li {
            font-size: 16px;
            color: #666;
            line-height: 1.5;
        }
        ul {
            padding-left: 20px;
        }
        a {
            color: #007BFF;
            text-decoration: none;
        }
        a:hover {
            text-decoration: underline;
        }
    </style>
""", unsafe_allow_html=True)

# Privacy Policy Content
st.markdown("# Privacy Policy for AI Project Asti")
st.markdown("**Effective Date:** March 10, 2025")

st.markdown("### 1. Introduction")
st.write("""
AI Project Asti ("Asti", "we", "us", or "our") is a not-for-profit, open-source platform provided by Neural Edge AI that allows users to interact with AI models. 
We are committed to protecting the privacy of our users and strive to provide a transparent experience. This Privacy Policy outlines how we collect, use, and share 
information when you use Asti. Please read it carefully.
""")

st.markdown("### 2. Information We Collect")
st.markdown("##### 2.1 Information You Provide")
st.write("""
Currently, Asti does not require any personal information such as your name, email address, or contact details. 
There is no sign-in or registration process.
""")

st.markdown("##### 2.2 Information Collected Automatically")
st.markdown("""
- **Usage Data:** We may collect information about how you interact with Asti, such as the models you use and the prompts you submit. 
  This data is used to improve the platform and analyze usage trends.
- **Bug Reports and User Feedback:** If you report bugs or issues, we may collect information you provide, 
  such as prompts, responses, screenshots, or other relevant details, to help us address the problem.
""")

st.markdown("**Important Note:** Asti does **not** collect IP addresses, session duration information, or use cookies.")

st.markdown("### 3. Use of Information")
st.write("""
We use the information we collect to:
""")

st.markdown("""
- **Provide and improve Asti:** We analyze usage patterns to enhance the platform's performance, features, and user experience.
- **Address bug reports and user feedback:** We use the information provided in bug reports and feedback to diagnose and fix issues, 
  and to improve the platform's functionality.
""")

st.markdown("### 4. Sharing of Information")
st.markdown("#### 4.1 Third-Party AI Models")
st.write("""
Asti utilizes open-source AI models from Together AI. Your interactions with these models, including prompts and responses, may be subject to 
Together AI's privacy policy, which can be found 
[here](https://together.ai/privacy-policy). We encourage you to review their policy carefully.
""")

st.markdown("#### 4.2 No Third-Party Sharing")
st.write("We **do not** share your information with any other third parties.")

st.markdown("#### 4.3 Legal Requirements")
st.write("""
We may disclose your information if required to do so by law or in the good faith belief that such action is necessary to:
""")
st.markdown("""
- Comply with a legal obligation
- Protect and defend our rights or property
- Prevent or investigate possible wrongdoing in connection with Asti
- Protect the personal safety of users or the public
""")

st.markdown("### 5. Data Security")
st.write("""
We take reasonable measures to protect your information from unauthorized access, use, or disclosure. However, no method of transmission 
over the internet or method of electronic storage is completely secure. Therefore, we cannot guarantee absolute security.
""")

st.markdown("### 6. Children's Privacy")
st.write("""
Asti is not intended for children under the age of 13. We do not knowingly collect personal information from children under 13. 
If you are a parent or guardian and believe your child has provided us with personal information, please contact us immediately.
""")

st.markdown("### 7. Changes to this Privacy Policy")
st.write("""
We may update this Privacy Policy from time to time. We will post any changes on this page and, if significant, notify you by email or through the platform.
""")

st.markdown("### 8. Contact Us")
st.write("""
If you have any questions about this Privacy Policy, please contact us at 
[asti-support@example.com](mailto:asti-support@example.com).
""")
