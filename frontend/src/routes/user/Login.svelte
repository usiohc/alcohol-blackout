<script>
    import { push, link } from 'svelte-spa-router'
    import fastapi from "../../lib/api" 
    import Error from "../../components/Error.svelte"
    import { access_token, email, is_login } from "../../lib/store"

    let isLoaded = false;
    $: isLoaded;

    let error = {detail:[]}
    let login_email = ""
    let login_password = ""
    
    $: isValidEmail = /^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$/g.test(login_email);
    $: isValidPassword = login_password.length >= 8 && login_password.length <= 20;
    $: isFormFilled = isValidEmail && isValidPassword;

    async function login(event) {
        event.preventDefault()
        isLoaded = true;
        let url = "/api/users/login"
        let params = {
            username: login_email,
            password: login_password,
        }

        await fastapi('login', url, params, 
            (json) => {
                $access_token = json.access_token
                $email = json.email
                $is_login = true
                push("/")
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
    <h5 class="my-3 border-bottom mt-3 p-2">로그인</h5>
    <form method="post" class="row g-3">
        <div class="form-floating">
            <input type="email" class="form-control" id="email" placeholder="name@example.com" maxlength="100" bind:value="{login_email}">
            <label for="email">이메일</label>
        </div>
        <div class="form-floating">
            <input type="password" class="form-control" id="password" placeholder="Password" minlength="8" maxlength="20" bind:value="{login_password}">
            <label for="password">비밀번호</label>
        </div>

        {#if isLoaded}
            <button type="submit" class="btn btn-primary disabled">
                <div class="d-flex justify-content-center">
                    <div class="spinner-border text-white" role="status">
                        <span class="visually-hidden">Loading...</span>
                    </div>
                </div>
            </button>
        {:else}
            <button type="submit" class="btn btn-primary" on:click={login} disabled={ !isFormFilled || isLoaded }>로그인</button>
        {/if}
        <!-- <button class="btn btn-primary" disabled="true"><div class="spinner-border spinner-border-sm" role="status"/> </button> -->
    </form>
</div>

<div class="container pt-4">
    <form method="post">
        <!-- Register buttons -->
        <div class="text-center">
            <p> 아이디가 없으신가요? <a use:link href="/register" class="link-primary">회원가입하기</a></p>

            <p style="text-decoration: line-through">다른 방법으로 로그인 하기</p>
            
            <!-- <button type="button" class="btn btn-link btn-floating mx-1">
                <i class="fab fa-facebook-f"></i>
            </button> -->
        
            <button type="button" class="btn btn-link btn-floating mx-1">
                <i class="fab fa-google"></i>
            </button>
        
            <!-- <button type="button" class="btn btn-link btn-floating mx-1">
                <i class="fab fa-twitter"></i>
            </button> -->
        
            <!-- <button type="button" class="btn btn-link btn-floating mx-1">
                <i class="fab fa-github"></i>
            </button> -->
        </div>
    </form>
</div>