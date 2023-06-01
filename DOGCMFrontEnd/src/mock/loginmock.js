// 引入mockjs
import Mock from 'mockjs'

// 模拟登录成功的数据
const loginSuccess = {
    state: 0, // 状态码，0表示成功
    //group: Mock.Random.integer(0, 1), // 用户组，0表示普通用户，1表示管理员
    token: Mock.Random.guid(), // 令牌
}

// 模拟账号不存在的数据
const loginFail1 = {
    state: 1, // 状态码，1表示账号不存在
}

// 模拟密码错误的数据
const loginFail2 = {
    state: -1, // 状态码，-1表示密码错误
}

// 根据请求参数返回不同的数据
// 根据请求参数返回不同的数据
Mock.mock('http://localhost:10086/user/login', 'post', (options) => {
    // 获取请求参数
    const params = new URLSearchParams(options.body)
    const user = params.get('user')
    const passwd = params.get('passwd')
    // 判断用户名和密码是否正确
    if (user === 'admin' && passwd === '123456') {
        // 返回登录成功的数据，并设置用户组为1（管理员）
        return {
            ...loginSuccess,
            group: 1,
            // 添加响应头
            headers: {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST',
                'Access-Control-Allow-Headers': 'Content-Type'
            }
        }
    } else if (user === 'user' && passwd === '654321') {
        // 返回登录成功的数据，并设置用户组为0（普通用户）
        return {
            ...loginSuccess,
            group: 0,
            // 添加响应头
            headers: {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST',
                'Access-Control-Allow-Headers': 'Content-Type'
            }
        }
    } else if (user !== 'admin' && user !== 'user') {
        // 返回账号不存在的数据
        return {
            ...loginFail1,
            // 添加响应头
            headers: {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST',
                'Access-Control-Allow-Headers': 'Content-Type'
            }
        }
    } else {
        // 返回密码错误的数据
        return {
            ...loginFail2,
            // 添加响应头
            headers: {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST',
                'Access-Control-Allow-Headers': 'Content-Type'
            }
        }
    }
})

