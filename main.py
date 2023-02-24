import openai
import clueai
from flask import Flask, request, render_template, redirect

server = Flask(__name__)


def generate_response(prompt):
    '''
    调用openai的API
    :param prompt:
    :return:
    '''
    try:
        # openai.api_key ="你自己的API KEY"   # 开发测试时去掉注释
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
    except Exception as e:

        print(e)
        return e
    return response["choices"][0].text


def generate_yuanyu_response(prompt):
    '''
    调用ChatYuan API
    :param prompt:
    :return:
    '''
    try:
        # initialize the Clueai Client with an API Key
        api_key = "你的api key"
        cl = clueai.Client(api_key, check_api_key=True)
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


@server.route("/chat_yuanyu/get")
def get_yuanyu_response():
    user_text = request.args.get('msg')
    return str(generate_yuanyu_response(user_text))


if __name__ == '__main__':
    server.run(debug=False, host='0.0.0.0', port=8088)
