# Demo-of-an-AI-Negotiation-Robot-
调用智谱API智能体搭建ai竞价客服。采用streamlit实现简单demo。理想产品应在购物app中能够调用多种商品信息，根据商家最低底价与C端用户进行竞价。用户能不断与ai客服竞价成交价，增加趣味性。

不断优化prompt，使得成交价不低于商家底价，但能在清仓价格上给予用户一定优惠，用户在聊天对话中砍价，购买意图上升。

以下是部分prompt语句(实际prompt还应包含更多，需进行优化)：
>>请根据顾客的出价进行回应：
>>- 如果出价远高于底价（如345），可以直接成交，现在的出价变为协商价格，请直接接受并表示感谢。
>>-如果出价略高于底价（如320），可以与客户协商，提出一个协商价格（如330）。
>>-如果出价一般（如300），可以与客户协商，提出一个介于此前协商价格和客户出价间的新协商价格（如330）.
>>- 如果客户继续杀价，请保持礼貌进行磋商，逐步降低协商价格，让步幅度不要太大。
>>- 保持礼貌、专业、略带销售技巧，可以适当使用“库存紧张”、“限时优惠”等措辞，但避免承诺价格以外的优惠活动（如第二件半价、送配饰送小挂件等）。
>>- 请用自然、亲切的语气与顾客对话，不要暴露底价，也不要让客户知道有底价的存在。
## © 2025 清仓竞价系统 | Powered by 智谱清言 & Streamlit
Chat with me during the clearance sale: Intelligent bidding robot, making your shopping more cost-effective
### using Streamlit(Anaconda CMD)
![Image text](https://github.com/Lijianing789/Demo-of-an-AI-Negotiation-Robot-/blob/main/streamlit.png)

### opening the address( assuming it is a dress product)
![Image text](https://github.com/Lijianing789/Demo-of-an-AI-Negotiation-Robot-/blob/main/original.png)

### Consumers can bid according to the prompt
![Image text](https://github.com/Lijianing789/Demo-of-an-AI-Negotiation-Robot-/blob/main/output.jpg)

>Here are more prompts
>·1
>>![Image text](https://github.com/Lijianing789/Demo-of-an-AI-Negotiation-Robot-/blob/main/test.png)
>·2
>>>![Image text](https://github.com/Lijianing789/Demo-of-an-AI-Negotiation-Robot-/blob/main/answer.png)
>·3
>>>>![Image text](https://github.com/Lijianing789/Demo-of-an-AI-Negotiation-Robot-/blob/main/test2.png)
