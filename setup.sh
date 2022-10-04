mkdir -p ~/.streamlit/

echo "\
[general]\n\
email = \"kareemrasheed89@outlook.com\"\n\
" > ~/.streamlit/credentials.toml

echo "\
[general]\n\
deta_key = \'a0luep6m_EYw5WwXALTwCGsGu1RsXngaioCLJLLcr'\n\
public_gsheets_url = \'https://docs.google.com/spreadsheets/d/1rtXErtmvIE1agsT6eWYUX4ma945M6QqeR8P0VwL0DTE/edit#gid=0'\n\
" > ~/.streamlit/secrets.toml

echo "
[theme]\n\
primaryColor = '#FF4B4B'\n\
backgroundColor = '#FFFFFF'
secondaryBackgroundColor = '#F0F2F6'
textColor = '#31333F'
font = 'sans serif'
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
" > ~/.streamlit/config.toml
