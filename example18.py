
import streamlit as st
from openai import OpenAI
from common import get_llm_response

def get_answer(question:str):
    """
    从大模型获取答案
    :param question: 用户问题
    :return: 迭代器对象
    """
    try:         #异常捕获
        client = OpenAI(base_url=base_url,api_key=api_key)
        stream = get_llm_response(client,model=model_name,user_prompt=question,stream=True)
        for chunk in stream:
            yield chunk.choices[0].delta.content or ''
    except BaseException as e:
        # print(e)
        yield from '暂时无法提供回复，请检查你提供的配置是否正确'

with st.sidebar:
    api_vendor = st.radio(label='请选择服务商：',options=['OpenAI','DeepSeek'])
    if api_vendor == 'OpenAI':
        base_url = 'https://twapi.openai-hk.com/v1'
        model_options = ['gpt-4o-mini','gpt-3.5-turbo','gpt-4o','gpt-4.1-mini','gpt-4.1']
    elif api_vendor =='DeepSeek':
        base_url ="https://api.deepseek.com"
        model_options = ['deepseek-chat','deep-reasoner']
    model_name = st.selectbox(label='请选择要使用的模型：',options=model_options)
    api_key = st.text_input(label='请输入你的key：',type='password')

if 'messages' not in st.session_state:
    st.session_state['messages'] = [('ai','你好，我是你的ai助手，我叫阿祖')]

st.write('## 吴德志的聊天机器人')
if not api_key:
    st.error('请提供访问大模型需要的API Key！！！')
    st.stop()

for role, content in st.session_state['messages']:
    st.chat_message(role).write(content)

user_input = st.chat_input(placeholder='请输入')
if user_input:
    _, history = st.session_state['messages'][-1]   #拿到最后一句对话使得ai具有记忆
    st.session_state['messages'].append(('human',user_input))
    st.chat_message('human').write(user_input)
    with st.spinner('AI正在思考，请耐心等待....'):
        answer = get_answer(f'{history},{user_input}')  #调用历史语句，使得ai回答与前面的问题具有连续性
        result = st.chat_message('ai').write_stream(answer)  #answer为迭代器，并输出完整内容
        st.session_state['messages'].append(('ai', result))

