# 登录注册界面
pass
## 操作员
111

### 添加用户
1. 前端传递值 data{
                cusForm: {
                    name: '',
                    address: '',
                    telephone: '',
                    //fax: '',
                    postcode: '',//mail
                    bank: '',
                    account: '',
                    },
                }
2. 后端返回state=0 成功，1-失败 

#### 创建草稿
1.前端传递
data: {
        token: this.$store.state.token,
        contract_name: this.draftForm.contract_name,
        customer: this.draftForm.customer,
        start_time: this.draftForm.date[0],
        end_time: this.draftForm.date[1],
        content: this.draftForm.info,
        user_name:this.draftForm.user_name,
        file_name:this.draftForm.file
},////但是文件传输好像有问题
2. 后端返回state=0 成功，其他-失败 
#### 会签
> url = operator/counter
request method = **get**
前端需要传给我： user_name： 当前用户的名字
我会传给前端一个: contracts : []此数组表此用户待会签的合同名字

> url = operator/counter
request method = **post**
前端点击合同名字后面的**会签**然后前端自己跳转界面但是url的是我前面提及的url，然后点击完成之后给次url发送post请求，同时给后端传参:
contract_name : 合同名字， content ： 会签的内容

#### 定稿
> url = oprator/finalize
request method = **get**
前端需要传给我：user_name : 登录此用户的名字
我会返回的东西：finalizations : []代表着待定稿的合同

> url = operator/finalize/fill
这个地方就是在待定稿的合同中选择一个合同然后点击定稿，然后跳转到上述的url
request method = **get**
前端需要传给的：user_name
我会返回的值：customer : 客户的名字, start_time : 开始时间, end_time : 结束时间， content : 起草时的内容, file ： 文件（目前返回的时文件的名字）

> url = operator/finalize/fill
这个地方就是点击提交
request method = **post**
前端需要传入的值为：contract_name: 合同的名字， content ：更改之后的起草的内容（我们现在默认就是我们的定稿只能修改起草的内容不能更改文件）

#### 审核
> url = operator/approve
reqeust method = **get**
前端需要传给我：user_nane: 登录此用户的名字
我返回的东西：approves : []此用户待审核的列表

> url = operator/approve
 request method = **post**
 前端需要传给我： user_name : 用户的名字, contract_name : 合同的名字, accep
 t : 0 | 1 0表示拒绝，1表示同意， content : 建议

#### 签订
> url = operator/sign
request method = **get**
前端需要传给的：user_name : 用户的名字
后端传回的值 : signs : []返回一个数组，代表此用户待定稿的合同的名字

> url = operator/sign/fill
reqeust metohd = **get**
前端需要传给：contract_name : 合同名字
后端传入：customer : 此合同的客户的名字

> url = operator/sign/fill
request method = **post**
前端点击提交按钮，前端需要传的值：content : 签订的建议, user_name : 用户的名字, contract_name : 合同的名字


## 管理员
#### 管理员给操作员分配合同管理(已测试)
- > url =manager/display
- 模糊搜索合同的名字
    > url = manager/display/search
    > request method = **post**
    - **我返回的东西**: contracts : [] 左边代表字典的key的名字，右边为我传入的一个value类型，此数组中存放的是模糊搜索到的合同的名字
- 搜索到合同之后我们会在合同后面出现**分配**两个字，然后点击分配，前端需要传入
    > contract_name 就是选择的这个合同的名字，同时跳转
    url = manager/display/distribute
    request method = **get**
    **我返回的东西** counter : [], approve : [], sign : []数组中存储的就是一些拥有对应权限的操作员的名字

    > 同样的url但是request method = **post** 也就是点击完成之后向后端发送完成并且传给后端
    contract_name : 合同名称， counter_names : []会签的所有人的名单, approve_names : []审核的所有名单, sign_names : []签订的名单
#### 管理员分配起草等权利(已测试)
> url = manager/operators
request method = **get**
我返回的东西：operators : []代表着所有的操作员的名字

> url = manager/contribute
request method = **post**
前端点击完成，传给后端: user_name : 用户的名字, isDraft : 表示的是否被分配起草 0 | 1, isAcounter: 0 | 1, isApprove : 0 | 1, isSign : 0 | 1