mkdir -p ~/.streamlit/
echo "[theme]
primaryColor='#00FF67'
backgroundColor='#05192D'
secondaryBackgroundColor='#031425'
textColor = '#FFFFFF'
font = 'sans serif'
[server]
headless = true
port = $PORT
enableCORS = false
" > ~/.streamlit/config.toml
