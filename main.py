import streamlit as st
from core_api.gigachat import get_token, send_prompt


st.title('Чат с ИИ')

if "access_token" not in st.session_state:
    try:
        st.session_state.access_token = get_token()
        st.toast('Токен получен')
    except Exception as e:
        st.error(f'Ошибка при получении токена - {e}', icon="🚨")

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "ai", "content": "Здравствуйте, чем помочь?"}]

for msg in st.session_state.messages:
    st.chat_message(name=msg["role"]).write(msg["content"])

if user_message := st.chat_input('Сообщение...'):
    st.chat_message(name='user').write(user_message)
    st.session_state.messages.append({"role": "user", "content": user_message})

    with st.spinner('Получаем ответ...'):
        ai_response = send_prompt(user_message, st.session_state.access_token)
        st.chat_message(name='ai').write(ai_response)
        st.session_state.messages.append({"role": "ai", "content": ai_response})
