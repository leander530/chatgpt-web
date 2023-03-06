import openai
import clueai
import os
from PIL import Image
from datetime import timedelta
from flask import Flask, request, render_template, redirect, session

server = Flask(__name__)
server.config['SECRET_KEY'] = os.urandom(24)
server.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

# openai.api_key = "你的api key"  # 开发测试时去掉注释

def generate_response(prompt):
    '''
    调用openai的API
    :param prompt:
    :return:
    '''
    try:

        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            temperature=0.8,
            max_tokens=2048,
            top_p=1,
            frequency_penalty=0.4,
            presence_penalty=0.3,
            stop=None
        )
        print(response)
    except Exception as e:

        print(e)
        return e
    return response["choices"][0].text


def generate_response_35(prompt):
    '''
    调用chatgpt最新版本gpt-3.5-turbo模型库
    简单实现多人对话
    :param prompt:
    :return:
    '''
    remote_addr = request.remote_addr
    try:

        ip_messages = session.get(remote_addr)
        if ip_messages:
            messages = list(ip_messages)
        else:
            messages = [{"role":"system", "content": "You are a helpful assistant."}]

        messages.append({"role": "user", "content": prompt})
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        #print(response["choices"][0])
    except Exception as e:

        print(e)
        return e
    response_msg = response['choices'][0]['message']['content']
    messages.append({"role": "assistant", "content": response_msg})
    session[remote_addr] = messages
    return response_msg


clueai_api_key = "你的api key"  # ChatYuan的API key


def generate_yuanyu_response(prompt):
    '''
    调用ChatYuan API
    :param prompt:
    :return:
    '''
    try:
        # initialize the Clueai Client with an API Key

        cl = clueai.Client(clueai_api_key, check_api_key=True)
        prompt_ = '''用户：{}
        小元：'''.format(prompt)

        # generate a prediction for a prompt
        # 需要返回得分的话，指定return_likelihoods="GENERATION"
        prediction = cl.generate(
            model_name='ChatYuan-large',
            prompt=prompt_)

        # print the predicted text
        # print('prediction: {}'.format(prediction.generations[0].text))
    except Exception as e:
        print(e)
        return e

    return prediction.generations[0].text


def generate_image_response(prompt, style):
    cl = clueai.Client(clueai_api_key, check_api_key=True)
    response = cl.text2image(
        model_name='clueai-base',
        prompt=prompt,
        style=style,
        out_file_path="test.jpg")
    print(response)

    # im = Image.open('test.jpg')
    # im.show()


def check_chatyuan_api_usage():
    cl = clueai.Client(clueai_api_key)
    print("API用量：{}".format(cl.check_usage(finetune_user=False)))


@server.route("/chat")
def home():
    return render_template("chat.html")


@server.route("/")
def chat_wx():
    return render_template("chat_wx.html")


@server.route("/yuan")
def chat_yuan():
    return render_template("chat_yuan.html")


@server.route("/chat/get")
def get_bot_response():
    user_text = request.args.get('msg')
    return str(generate_response(user_text))


@server.route("/chat_35/get")
def get_bot_response_35():
    user_text = request.args.get('msg')
    return str(generate_response_35(user_text))


@server.route("/chat_yuanyu/get")
def get_yuanyu_response():
    user_text = request.args.get('msg')
    return str(generate_yuanyu_response(user_text))


if __name__ == '__main__':
    server.run(debug=False, host='0.0.0.0', port=8088)
