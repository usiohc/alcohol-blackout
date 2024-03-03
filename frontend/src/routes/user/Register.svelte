<script>
    import { push } from 'svelte-spa-router'
    import fastapi from "../../lib/api"
    import Error from "../../components/Error.svelte"

    let isLoaded = false;

    let error = {detail:[]}
    let username = ''
    let email = ''
    let password = ''
    let passwordCheck = ''

    $: isValidUsername = username.length >= 2 && username.length <= 15;
    $: isValidEmail = /^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$/g.test(email);
    $: isValidPassword = password.length >= 8 && password.length <= 20;
    $: isValidPasswordCheck = password === passwordCheck;
    $: isFormFilled = isValidUsername && isValidEmail && isValidPassword && isValidPasswordCheck;


    function register(event) {
        event.preventDefault()
        isLoaded = true;
        let url = "/api/users/register"
        let params = {
            username: username,
            email: email,
            password: password,
            passwordCheck: passwordCheck
        }

        fastapi('post', url, params, 
            (json) => {
                push('/login') 
            },
            (json_error) => {
                error = json_error
                isLoaded = false;
            }
        )
    }

</script>




<div class="container">
    <div class="mt-3">
        <Error error={error} />
    </div>
    <h5 class="my-3 border-bottom mt-3 p-2">회원가입</h5>
    <form method="post" class="row g-3">
        <div class="form-floating">
            <input type="text" class="form-control" id="username" placeholder="Nickname" minlength="2" maxlength="15" bind:value="{username}">
            <label for="username">닉네임</label>
            {#if !isValidUsername}
            <div class="alert alert-danger m-0" role="alert">
                닉네임은 2자 이상 15자 이하로 입력해주세요.
            </div>
            {/if}
        </div>
        <div class="form-floating">
            <input type="email" class="form-control" id="email" placeholder="name@example.com" maxlength="100" bind:value="{email}">
            <label for="email">이메일</label>
            {#if !isValidEmail}
            <div class="alert alert-danger m-0" role="alert">
                이메일 형식이 올바르지 않습니다.
            </div>
            {/if}
        </div>
        <div class="form-floating">
            <input type="password" class="form-control" id="password" placeholder="Password" minlength="8" maxlength="20" bind:value="{password}">
            <label for="password">비밀번호</label>
            {#if !isValidPassword}
            <div class="alert alert-danger m-0" role="alert">
                비밀번호는 8자 이상으로 입력해주세요.
            </div>
            {/if}
        </div>
        <div class="form-floating">
            <input type="password" class="form-control" id="passwordCheck" placeholder="Password" bind:value="{passwordCheck}">
            <label for="passwordCheck">비밀번호 확인</label>
        </div>
        {#if !isValidPasswordCheck}
        <div class="alert alert-danger m-0" role="alert">
            비밀번호가 일치하지 않습니다.
        </div>
        {/if}
        
        
        {#if isLoaded}
            <button type="submit" class="btn btn-primary">
                <div class="d-flex justify-content-center">
                    <div class="spinner-border text-white" role="status">
                        <span class="visually-hidden">Loading...</span>
                    </div>
                </div>
            </button>
        {:else}
            <button type="submit" class="btn btn-primary"  on:click="{ register }" disabled={ !isFormFilled }>회원가입</button>
        {/if}
    </form>
</div>