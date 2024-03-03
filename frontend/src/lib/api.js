import qs from "qs"
import { access_token, email, is_login } from "./store"
import { get } from 'svelte/store'
import { push } from 'svelte-spa-router'

const fastapi = (operation, url, params, success_callback, failure_callback) => {
    let method = operation
    let content_type = 'application/json'
    let body = JSON.stringify(params)

    if(operation === 'login') {
        method = 'post'
        content_type = 'application/x-www-form-urlencoded'
        body = qs.stringify(params)
    }
    
    // prod
    let _url = url

    if (import.meta.env.DEV) {
        // dev
        _url = import.meta.env.VITE_SERVER_URL+url
        console.log("url: ", _url)
    }

    // prod 
    if(method === 'get') {
        _url += "?" + new URLSearchParams(params)
    }

    let options = {
        method: method,
        headers: {
            "Content-Type": content_type
        }
    }

    const _access_token = get(access_token)
    if (_access_token) {
        options.headers["Authorization"] = "Bearer " + _access_token
    }

    if (method !== 'get') {
        options['body'] = body
    }

    if (import.meta.env.DEV) {
        console.time("fetch time");
    }
    fetch(_url, options)
        .then(response => {
            if(response.status === 204) {  // No content
                if(success_callback) {
                    success_callback()
                }
                return
            }
            response.json()
                .then(json => {
                    if(response.status >= 200 && response.status < 300) {  // 200 ~ 299
                        if(success_callback) {
                            success_callback(json)
                        }
                    }else if(operation !== 'login' && response.status === 401) { // token time out
                        access_token.set('')
                        email.set('')
                        is_login.set(false)
                        alert("로그인이 필요합니다.")
                        push('/login')
                    }else {
                        if (failure_callback) {
                            failure_callback(json)
                        }else {
                            alert("알 수 없는 오류 발생.\n 관리자에게 문의하세요.\n", JSON.stringify(json))
                        }
                    }
                })
                .catch(error => {
                    alert("새로고침 후 이용해주세요.\n 지속적인 문제가 발생시 관리자에게 문의하세요.\n", JSON.stringify(error))
                    // alert(JSON.stringify(error))
                })
        })
    if (import.meta.env.DEV) {
        // time2 = console.time();
        // console.log("fetch time: ", time2-time1)
        console.timeEnd("fetch time");
    }
}

export default fastapi