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
st.markdown("## Terms and Conditions")
st.markdown("**Effective Date:** March 10, 2025")

st.markdown("#### 1. Introduction")
st.write("""
AI Project Asti("Asti", "we", "us", or "our") is a not-for-profit, open-source platform provided by Neural Edge AI that allows users to interact with AI models, hosted on 
Streamlit Community Cloud. By accessing and using this web application, you agree to comply with these Terms and Conditions. If you do not agree with 
these terms, you should not use Asti. 
""")

st.markdown("#### 2. Use Of the Service")
st.write("""
You agree to use Asti responsibly and ethically. You are solely responsible for any content you generate or submit through the platform. You agree not to use Asti for any 
unlawful or harmful purposes, including but not limited to: Generating or distributing harmful, offensive, or illegal content, Attempting to disrupt or interfere with the 
operation of Asti, Impersonating any person or entity, Violating any applicable laws or regulations. You must be at least 13 years old to use this platform.
""")

st.markdown("#### 3. Open Source and Third-Party Models")
st.write("""
Asti utilizes open-source AI models from Together AI. Your interactions with these models, including prompts and responses, are subject to Together AI's terms of service 
and privacy policy. We encourage you to review their policies carefully. Asti is provided as an open-source platform, and we do not guarantee the 
accuracy, completeness, or reliability of the AI models or their outputs.
""")

st.markdown("#### 4. No Warranty")
st.write("""
Asti is provided "as is" and "as available" without any warranties of any kind, either express or implied. We do not warrant that the platform will 
be uninterrupted, error-free, or fully secure. We disclaim all warranties, including but not limited to, implied warranties of merchantability, fitness for a 
particular purpose, and non-infringement.
""")

st.markdown("#### 5. Limitation of Liability")
st.write("""
In no event shall Neural Edge AI or its affiliates, officers, directors, employees, or agents be liable for any direct, indirect, incidental, special, or consequential
damages arising out of or in connection with your use of Asti, even if we have been advised of the possibility of such damages.
""")

st.markdown("#### 6. Changes to Terms")
st.write("""
We reserve the right to modify these Terms and Conditions at any time. We will post any changes on this page. Your continued use of Asti after any changes constitutes 
your acceptance of the new terms.
""")

st.markdown("#### 6. Intellectual Property")
st.write("""
Asti is an open-source platform. You retain ownership of any content you generate through the platform, and users should verify information independently before relying on it.
""")

st.markdown("#### 7. Contact Us")
st.write("""
For any questions or concerns regarding these Terms and Conditions, please contact us.
""")
