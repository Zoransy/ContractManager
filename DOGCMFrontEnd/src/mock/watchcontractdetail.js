// mock.js
import Mock from 'mockjs'

// 模拟合同数据
const contractData = Mock.mock({
    'contract|3': [{
        'id|+1': 1,
        'name': '@ctitle',
        'customer': '@cname',
        'beginTime': '@date',
        'endTime': '@date',
        'content': '@cparagraph'
    }]
})

// 拦截请求并返回模拟数据
Mock.mock("http://localhost:10087/contract/selContract", 'post', (options) => {
    // 解析请求参数
    const params = new URLSearchParams(options.body)
    const token = params.get('token')
    //const id = params.get('id')
    alert("successgetdetail")
    // 查找对应的合同数据
    //const contractData = contract.contract.find(item => item.id == id)
    // 判断是否存在合同数据
        // 返回成功响应
        return {
            code: token,
            message: 'success',
            state: 0,
            data: [contractData]
        }
})
