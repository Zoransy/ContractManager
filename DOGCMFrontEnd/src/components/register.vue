<template>
    <div class="register">

        <h1 style="text-align: center">注册</h1>
        <el-form ref="registerForm" :model="registerForm" :rules="rules" label-width="100px">
            <el-form-item label="用户名：" prop="name">
                <el-input v-model="registerForm.name" placeholder="请输入用户名"></el-input>
            </el-form-item>

            <el-form-item label="邮箱:" prop="email">
                <el-input v-model="registerForm.email" placeholder="请输入邮箱"></el-input>
            </el-form-item>


            <el-form-item label="密码：" prop="passwd">
                <el-input v-model="registerForm.passwd" placeholder="请输入密码" show-password clearable></el-input>
            </el-form-item>

            <el-form-item label="再次密码：" prop="passwdagain">
                <el-input v-model="registerForm.passwdagain" placeholder="请确认密码" show-password clearable></el-input>
            </el-form-item>

            <el-form-item label-width="0px">
                <el-button size="medium" style="border-color: #ffffff; margin-right: 43%; left: 0px;" @click="clickLogin">登录</el-button>
                <el-button type="primary" size="medium" :loading = "isLoading"  @click="clickRegister">{{text}}</el-button>
            </el-form-item>

        </el-form>
    </div>
</template>

<script>
    export default {
        name: "register",
        data() {
            var validatePass2 = (rule, value, callback) => {
                if (value === '') {
                    callback(new Error('请再次输入密码'));
                } else if (value !== this.registerForm.passwd) {
                    callback(new Error('两次输入密码不一致!'));
                } else {
                    callback();
                }
            };

            return {
                state: -1,
                text: "创建账号",
                isDisabled: false,
                isLoading: false,
                registerForm: {
                    name: '',
                    email:'',
                    passwd: '',
                    passwdagain: ''
                },
                rules: {
                    name: [
                        {
                            required: true, message: "请输入用户名", trigger: 'blur'
                        },
                    ],
                    email: [//如果为空就显示message
                        {
                            required: true, message: "请输入email", trigger: 'blur'
                        },
                    ],
                    passwd: [
                        {
                            required: true, message: "请输入密码", trigger: 'blur'
                        },
                        {
                            min: 6, message: "密码必须大于6", trigger: 'blur'
                        }
                    ],
                    passwdagain: [
                        {
                            required: true, message: "请输入密码", trigger: 'blur'
                        },
                        {
                            min: 6, message: "密码必须大于6", trigger: 'blur'
                        },
                        {
                            validator: validatePass2, trigger: 'blur'
                        }
                    ]
                },
            }
        },

        methods: {
            clickRegister() {
                if (this.isLoading) {
                    this.text = ""
                }
                //获取到的是添加了ref="registerForm"属性的这个组件 前端判断
                this.$refs["registerForm"].validate((valid) => {
                    if(valid) {
                        //alert("valid"+this.$registerUrl);//http://localhost:10087/user/register
                        this.$axios({
                            url: this.$registerUrl,
                            method: 'post',
                            data: {
                                user: this.registerForm.name,
                                email: this.registerForm.email,//邮箱
                                //passwd: this.$md5(this.registerForm.passwd + this.$salt)
                                passwd : this.registerForm.passwd,
                            },
                            transformRequest: [function (data) {
                                let ret = '';
                                for (let it in data) {
                                    ret += encodeURIComponent(it) + '=' + encodeURIComponent(data[it]) + '&'
                                }
                                return ret
                            }],
                            headers: {'Content-Type': 'application/x-www-form-urlencoded'}
                        }).then(res => {
                            if (res.data.state === 0) {
                                // alert("qianduan 成功 "+this.$loginUrl);
                                this.$axios({
                                    url: this.$loginUrl,
                                    method: 'post',
                                    data: {
                                        types : 1, 
                                        user: this.registerForm.name,
                                        email: this.registerForm.email,
                                        //passwd: this.$md5(this.registerForm.passwd + this.$salt)
                                        passwd: this.registerForm.passwd,
                                    },

                                    transformRequest: [function (data) {
                                        let ret = '';
                                        for (let it in data) {
                                            ret += encodeURIComponent(it) + '=' + encodeURIComponent(data[it]) + '&'
                                        }
                                        return ret
                                    }],
                                    headers: {'Content-Type': 'application/x-www-form-urlencoded'}
                                    // headers: {
                                    //     'Content-Type': 'application/x-www-form-urlencoded'
                                    // }
                                }).then(res => {
                                    // alert("后端 "+res.data.state);
                                    this.state = res.data.state;
                                    this.$store.state.userName = this.registerForm.name;
                                    this.$store.state.email = this.registerForm.emial;
                                    this.$store.state.passwd = this.registerForm.passwd;
                                    this.$store.state.token = res.data.token;
                                    this.$store.state.group = res.data.group;
                                    this.$router.push('/mainFrame')
                                })
                            } else {
                                alert("账号已存在！")
                            }
                        })
                        // console.log('success')
                    }else  {
                        this.text = "创建账户";
                        this.isLoading = false;
                        this.$alert('账号不成立！', '警告', {
                            confirmButtonText: '确定',
                            callback: {
                            }
                        });
                        // console.log('error submit!!');
                        return false;
                    }
                })
            },

            loginProcess() {
                if (this.state === 0) {
                    this.$router.push('/mainFrame')
                } else {
                    this.text = "登录";
                    this.isLoading = false;
                }
            },
            clickLogin() {
                this.$router.push("/login")
            }
        }
    }
</script>

<style scoped>

    .register {
        margin: auto;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 25rem;
        position: absolute;
        background-color: white;
        padding: 20px 20px 10px 20px;
        border-radius: 10px;
        box-shadow: 0px 15px 25px 0px rgba(0, 0, 0, 0.11);
    }

</style>
