import streamlit as st

from demo_app.components.faq import faq


def set_open_api_key(api_key: str):
    st.session_state["OPENAI_API_KEY"] = api_key
    st.session_state["open_api_key_configured"] = True
    print('OPENAI API key is Configured Successfully!')

def set_patent_link(patent_link: str):
    st.session_state["PATENT_LINK"] = patent_link
    st.session_state["patent_link_configured"] = True
    print('Google Patent Link is set Successfully!')



def sidebar():
    with st.sidebar:
        st.markdown(
            "## How to use\n"
            "1. Enter your [OpenAI API key](https://platform.openai.com/account/api-keys) below🔑\n"  # noqa: E501
        )
        open_api_key_input = st.text_input(
            "Openai API Key",
            type="password",
            placeholder="Paste your API key here (sk-...)",
            help="You can get your API key from https://platform.openai.com/account/api-keys.",  # noqa: E501
            value=st.session_state.get("OPEN_API_KEY", ""),
        )

        if open_api_key_input:
            # print(f'Entered API is {open_api_key_input}')
            set_open_api_key(open_api_key_input)

        if not st.session_state.get("open_api_key_configured"):
            st.error("Please configure your Open API key!")
        else:
            st.markdown("Open API Key Configured!")

        st.markdown(
            "2. Enter google patent link below🔑\n"  # noqa: E501
        )
        patent_link_input = st.text_input(
            "Google Patent Link",
            type="default",
            placeholder="Paste the Google patent link here (sk-...)",
            help="You can goto patents.google.com to get the link from the browser.",  # noqa: E501
            value=st.session_state.get("PATENT_LINK", ""),
        )

        if patent_link_input:
            # print(f'Entered patent link is {patent_link_input}')
            set_patent_link(patent_link_input)

        if not st.session_state.get("patent_link_configured"):
            st.error("Set the Google patent link!")
        else:
            st.markdown("Google Patent link is set!")



        st.markdown("---")
        st.markdown("# About")
        st.markdown(
            "📖 This App is template of lanchain-streamlit-docker example"
        )
        st.markdown("Made by [Jeffry Copps](https://www.linkedin.com/in/jcopps/)")
        st.markdown("Credits for parent repo [amjadraza](https://github.com/amjadraza/langchain-streamlit-docker-template)")
        st.markdown("Credits for patent download [lorenzbr](https://github.com/lorenzbr/GooglePatentsPdfDownloader)")

        st.markdown("Credits for Template [hwchase17](https://github.com/hwchase17/langchain-streamlit-template)")
        st.markdown("---")

        faq()
