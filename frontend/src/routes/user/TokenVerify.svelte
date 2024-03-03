<script>
    import { push } from 'svelte-spa-router'
    import fastapi from "../../lib/api"
    import Error from "../../components/Error.svelte"
    import { onMount } from 'svelte';

    export let params;
    let token = params.token
    let error = {detail:[]}
    let isLoaded = false;

    function verifyToken() {
        let url = "/api/oauth2/token/"
        let params = {
            "token": token
        }
        fastapi('post', url, params, 
            (json) => {
                alert("이메일 인증이 완료되었습니다.")
                push('/login')
            },
            (json_error) => {
                alert("이메일 인증에 실패했습니다.")
                error = json_error
                isLoaded = true;
            }
        )
    }

    verifyToken();
</script>

<div class="mt-3">
    <Error error={error} />
</div>
{#if !isLoaded}
    <div class="d-flex justify-content-center">
        <div class="spinner-border mt-5 p-4 text-primary" role="status">
            <span class="visually-hidden">Loading...</span>
        </div>
    </div>
{:else}
<div class="container-md text-center px-3 mt-3">
    <a href="/" class="btn btn-primary">홈으로</a>
</div>
{/if}
