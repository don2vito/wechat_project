import random

def select_question(question_list):
    return random.choice(question_list)

def answer_question(question,answer):
    if question == '打开灯光':
        if answer == '1':
            print('回答正确')
        else:
            print('回答错误，正确答案应是 1')
    elif question == '通过急弯':
        if answer == '2':
            print('回答正确')
        else:
            print('回答错误，正确答案应是 2')
    elif question == '通过拱桥':
        if answer == '2':
            print('回答正确')
        else:
            print('回答错误，正确答案应是 2')
    elif question == '通过人行横道':
        if answer == '2':
            print('回答正确')
        else:
            print('回答错误，正确答案应是 2')
    elif question == '通过没有交通信号灯控制的路口':
        if answer == '2':
            print('回答正确')
        else:
            print('回答错误，正确答案应是 2')
    elif question == '同方向近距离跟车行驶':
        if answer == '3':
            print('回答正确')
        else:
            print('回答错误，正确答案应是 3')
    elif question == '与机动车会车':
        if answer == '3':
            print('回答正确')
        else:
            print('回答错误，正确答案应是 3')
    elif question == '通过交通信号灯控制的路口':
        if answer == '3':
            print('回答正确')
        else:
            print('回答错误，正确答案应是 3')
    elif question == '在有路灯照明良好的道路上行驶':
        if answer == '3':
            print('回答正确')
        else:
            print('回答错误，正确答案应是 3')
    elif question == '在照明不良的道路行驶':
        if answer == '4':
            print('回答正确')
        else:
            print('回答错误，正确答案应是 4')
    elif question == '在无照明的道路行驶':
        if answer == '4':
            print('回答正确')
        else:
            print('回答错误，正确答案应是 4')
    elif question == '超越前方车辆':
        if answer == '5':
            print('回答正确')
        else:
            print('回答错误，正确答案应是 5')
    elif question == '路边临时停车':
        if answer == '6':
            print('回答正确')
        else:
            print('回答错误，正确答案应是 6')
    else:
        print('异常情况')
        
def main():
    while True:
        question = select_question(question_list)
        print(question)
        answer = str(input('开大灯请输入 1\n远近交替请输入 2\n近光灯请输入 3\n远光灯请输入 4\n左转灯——>远近交替——>右转灯——>复位请输入 5\n示宽灯 + 报警灯请输入 6\n请输入数字：'))
        answer_question(question,answer)
        print('================================================================================================')
        continue
        
if __name__ == '__main__':
    question_list = ['打开灯光','通过急弯','通过坡路','通过拱桥','通过人行横道','通过没有交通信号灯控制的路口',\
                '同方向近距离跟车行驶','与机动车会车','通过交通信号灯控制的路口','在有路灯照明良好的道路上行驶',\
                '在照明不良的道路行驶','在无照明的道路行驶','超越前方车辆','路边临时停车']
    main()