// mock.js
import Mock from 'mockjs'

// 模拟客户数据
const contracts = Mock.mock({
    'contracts|3': [{
        'id|+1': 1,
        'name': '@cname',
        'date': "2023.6.13"
    }]
})

// 拦截请求并返回模拟数据
Mock.mock("http://localhost:10087/contract/selectContractByType", 'post', (options) => {
    // 解析请求参数
    const params = new URLSearchParams(options.body)
    const token = params.get('token')
    const sign = params.get("type")
    //alert("hhhhhhhhhh")
    // 返回成功响应
    return {
        code: token,
        message: 'success',
        contracts: contracts.contracts.map((item, index) => {
            // 根据customer属性封装对象
            //alert("sendtocontract:"+ item.name)
            if(sign === "sign"){
                //alert("sign ctrct")
                return {
                    id: item.id,
                    name: item.name,
                    beginTime:item.date,
                    index: index
                }
            }
            else {
                return {
                    id: item.id,
                    contract_name: item.name,
                    date:item.date,
                    index: index
                }
            }
        })
    }
})
