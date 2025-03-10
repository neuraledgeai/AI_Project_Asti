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
st.markdown("## Privacy Policy for AI Project Asti")
st.markdown("**Effective Date:** March 10, 2025")

st.markdown("#### 1. Introduction")
st.write("""
AI Project Asti ("Asti", "we", "us", or "our") is a not-for-profit, open-source platform developed by Neural Edge AI that allows users to interact with AI models. 
We try to provide a concise AI interaction experience while maintaining a privacy-first approach with minimal data collection. This Privacy Policy outlines how we collect, use, and share 
information when you use Asti. We are committed to transparency, security, and user privacy. By using Asti, you acknowledge and agree to the practices outlined in this policy.
""")

st.markdown("#### 2. Information We Collect")

st.markdown("###### 2.1 Information You Provide")
st.write("""
Asti does not require users to provide any personal information, such as name, email address, or contact details, to use its core services. However, we may collect such 
information if you choose to share it with us, for example, when reaching out for support or providing feedback. There is no sign-in or registration process, and we do not 
collect identifiable user data. Additionally, since Asti operates on services like Together AI, Streamlit, and GitHub, interactions with the platform—such as 
submitting prompts, accessing the web app, or viewing the open-source repository—may involve data processing in accordance with their respective privacy policies.
""")

st.markdown("###### 2.2 Information Collected")
st.markdown("""
- **Usage Data:** We may collect non-personal information about how you interact with Asti, such as the AI 
models you use and the prompts you submit. This data helps us analyze usage trends and enhance platform 
performance. However, we do not track users individually or store identifiable session data.
- **Bug Reports and User Feedback:** If you report bugs or issues, we may collect information you provide, 
  such as prompts, responses, screenshots, or other relevant details, to help us address the problem. Sharing this 
  information is entirely optional.
""")

st.markdown("**Important Note:** Asti does **not** collect IP addresses, session duration information, or use cookies.")

st.markdown("#### 3. Use of Information")
st.write("""
We use the information we collect to:
""")

st.markdown("""
- **Provide and improve Asti:** We analyze usage patterns to enhance the platform's performance, features, and user experience.
- **Address bug reports and user feedback:** We use the information provided in bug reports and feedback to diagnose and fix issues, 
  and to improve the platform's functionality.
""")

st.markdown("#### 4. Sharing of Information")
st.markdown("###### 4.1 Third-Party AI Models")
st.write("""
Asti integrates open-source AI models from Together AI to power its functionality. When you interact with these models—such as 
submitting prompts and receiving responses—your data may be processed according to Together AI's Privacy Policy. To understand how 
your interactions are handled, we recommend reviewing Together AI's Privacy Policy here:
[Together AI Privacy Policy](https://www.together.ai/privacy). We encourage you to review their policy carefully.
""")

st.markdown("###### 4.2 Use of Streamlit Services")
st.write("""
This web application is fully powered by Streamlit Community Cloud, which provides hosting and deployment services for this platform. Since 
Streamlit's services are used, certain data collection and processing may be subject to Streamlit's Privacy Policy. We recommend users review 
Streamlit's Privacy Notice to understand how their data may be handled:
[Streamlit Privacy Policy](https://streamlit.io/privacy-policy). We encourage you to review their policy carefully.
""")

st.markdown("###### 4.3 Use of GitHub Services")
st.write("""
Development of AI Project Asti is entirely managed through GitHub, within 
an [open-source repository available at GitHub](https://github.com/neuraledgeai/AI_Project_Asti). - Neural Edge AI: AI Project Asti. Since GitHub 
provides hosting and version control for the project's codebase, certain interactions—such as accessing, forking, or contributing to 
the repository—may be subject to GitHub's Privacy Policy. For more details on how GitHub handles data, we encourage users to review GitHub’s Privacy Policy here:
[GitHub Privacy Policy](https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement). We encourage you to review their policy carefully.
""")

st.markdown("###### 4.4 No Third-Party Sharing")
st.write("""
We do not share any user data with third parties intentionally. However, since this platform relies on services from Together AI, Streamlit, and GitHub, some 
interactions—such as AI model usage, web hosting, and code management—may involve data processing in accordance with their respective privacy policies. Beyond these 
essential services, no data is shared with any other third parties. Our goal is to keep Asti a transparent, minimalistic, and privacy-focused platform, ensuring secure 
and responsible data handling at all times.
""")

st.markdown("###### 4.5 Legal Requirements")
st.write("""
We may disclose your information if required to do so by law or in the good faith belief that such action is necessary to:
""")
st.markdown("""
- Comply with a legal obligation
- Protect and defend our rights or property
- Prevent or investigate possible wrongdoing in connection with Asti
- Protect the personal safety of users or the public
""")

st.markdown("#### 5. Data Security")
st.write("""
We take data security seriously and implement reasonable measures to protect any collected information from unauthorized access, misuse, or disclosure. Since 
Asti follows a minimalistic data collection approach, we ensure that only essential data is processed through trusted services like Together AI, Streamlit, and 
GitHub. However, while we strive to maintain a secure environment, it's important to note that no online platform can guarantee absolute security. Users are 
encouraged to be mindful of the data they share and review the privacy policies of the services integrated into this platform. We remain committed to 
transparency, security, and user privacy as core principles of Asti.
""")

st.markdown("#### 6. Children's Privacy")
st.write("""
Asti is not intended for children under the age of 13. We do not knowingly collect personal information from children under 13. 
If you are a parent or guardian and believe your child has provided us with personal information, please contact us immediately.
""")

st.markdown("#### 7. Changes to this Privacy Policy")
st.write("""
We may update this Privacy Policy from time to time to reflect improvements, legal requirements, or changes in the services we use. Any 
modifications will be posted on this page, and if the updates are significant, we may provide additional notifications through the platform. We encourage 
users to review this Privacy Policy periodically to stay informed about how we handle data. Continued use of Asti after any changes means you acknowledge 
and accept the updated policy.
""")

st.markdown("#### 8. Contact Us")
st.write("""
If you have any questions about this Privacy Policy, please contact us.
""")
