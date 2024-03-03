<script>
    import { access_token, email, is_login } from '../../lib/store';
    import { push } from 'svelte-spa-router'
    import fastapi from "../../lib/api"
    import Error from "../../components/Error.svelte"
    import { onMount } from 'svelte';
    import Loding from "../../components/Loding.svelte"


    let error_me = {detail:[]}
    let error_username = {detail:[]}
    let error_password = {detail:[]}
    let error_delete = {detail:[]}

    let isLoaded_me = false;
    let isLoaded_username = false;
    let isLoaded_password = false;
    let isLoaded_delete = false;

    let username = ''
    let myemail = ''
    let password = ''
    let passwordCheck = ''

    let isValidUsername;
    let isValidPassword;
    let isValidPasswordCheck;

    $: isValidUsername = username.length >= 2 && username.length <= 15;
    $: isValidPassword = password.length >= 8 && password.length <= 20;
    $: isValidPasswordCheck = password === passwordCheck;


    async function get_user_me() {
        let url = "/api/users/me"
        let params = {}
        fastapi('get', url, params, 
            (json) => {
                username = json.username
                myemail = json.email
                error_me = {detail:[]}
            },
            (json_error) => {
                error_me = json_error
            }
        )
    
    }

    async function patch_username(event) {
        event.preventDefault()
        isLoaded_me = true;
        let url = "/api/users/username"
        let params = {
            "username": username
        }
        fastapi('PATCH', url, params, 
            (json) => {
                alert("닉네임이 변경되었습니다.")
                error_username = {detail:[]}
                isLoaded_me = false;
            },
            (json_error) => {
                error_username = json_error
                isLoaded_me = false;
            }
        )
    }

    async function patch_password(event) {
        event.preventDefault()
        isLoaded_password = true;
        let url = "/api/users/password"
        let params = {
            "password": password,
            "passwordCheck": passwordCheck
        }
        fastapi('PATCH', url, params, 
            (json) => {
                alert("비밀번호가 변경되었습니다.")
                password = ''
                passwordCheck = ''
                error_password = {detail:[]}
                isLoaded_password = false;
            },
            (json_error) => {
                error_password = json_error
                isLoaded_password = false;
            }
        )
    }

    async function delete_user(event) {
        event.preventDefault()
        isLoaded_delete = true;
        let url = "/api/users"
        let params = {}
        fastapi('delete', url, params, 
            (json) => {
                alert("회원탈퇴가 완료되었습니다.")
                $access_token = '';
                $email = '';
                $is_login = false;
                isLoaded_delete = false;
                push('/login')
            },
            (json_error) => {
                error_delete = json_error
                isLoaded_delete = false;
            }
        )
    }

    onMount(() => {
        get_user_me();
    })


</script>

<div class="mt-3">
</div>

<div class="container-md">
    <h5 class="my-3 border-bottom mt-3 p-2">마이페이지</h5>
    <div class="row g-3 align-items-center">
        <label for="username" class="col-3 col-form-label">닉네임</label>
        <form method="post" class="col-6">
            <input type="text" class="form-control" id="username" placeholder="닉네임" minlength="2" maxlength="15" bind:value="{username}">
        </form>
        <div class="col-3 d-grid">
            {#if isLoaded_me}
                <button type="submit" class="btn btn-primary disabled">
                    <Loding />    
                </button>
            {:else}
                <button type="submit" class="btn btn-primary {isValidUsername ? "" : "disabled"}" on:click={patch_username}>변경</button>
            {/if}
        </div>
    </div>
    <Error error={error_me} />
    {#if !isValidUsername}
    <div class="alert alert-danger mt-0" role="alert">
        닉네임은 2자 이상 15자 이하로 입력해주세요.
    </div>
    {/if}
    <div class="row g-3 align-items-center">
        <label for="email" class="col-3 col-form-label">이메일</label>
        <div class="col">
            <input type="text" class="form-control" id="email" placeholder="email" bind:value="{myemail}" disabled>
        </div>
    </div>
    <div class="row g-3 align-items-center">
        <div class="col-6 d-grid">
            <button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#passwordModal">
                비밀번호 변경
            </button>
        </div>

        <div class="modal fade" id="passwordModal" tabindex="-1" aria-labelledby="passwordModalLabel" aria-hidden="true">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header ">
                        <h5 class="modal-title" id="passwordModalLabel">비밀번호 변경</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>

                    <Error error={error_password} />

                    <div class="alert alert-secondary m-1" role="alert">
                        비밀번호는 8자 이상으로 입력해주세요. <br>
                    </div>

                    <form method="post">
                        <div class="modal-body">
                            <div class="form-floating">
                                <input type="password" class="form-control {isValidPassword ? "is-valid" : "is-invalid"}" id="password" placeholder="Password" minlength="8" maxlength="20" bind:value="{password}">
                                <label for="password">비밀번호</label>
                            </div>
                            <div class="form-floating">
                                <input type="password" class="form-control {isValidPassword && isValidPasswordCheck ? "is-valid" : "is-invalid"}" id="passwordCheck" placeholder="Password" bind:value="{passwordCheck}">
                                <label for="passwordCheck">비밀번호 확인</label>
                            </div>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">닫기</button>
                            {#if isLoaded_password}
                                <button type="submit" class="btn btn-primary disabled">
                                    <Loding />
                                </button>
                            {:else}
                                <button type="submit" class="btn btn-primary { isValidPassword && isValidPasswordCheck ? "" : "disabled"}" on:click={patch_password}>변경</button>
                            {/if}
                        </div>
                    </form>
                </div>
            </div>
        </div>
        
        <div class="col-6 d-grid">
            <button type="button" class="btn btn-danger" data-bs-toggle="modal" data-bs-target="#withdrawalModal">
                회원탈퇴
            </button>

            <div class="modal fade" id="withdrawalModal" tabindex="-1" aria-labelledby="withdrawalModalLabel" aria-hidden="true">
                <div class="modal-dialog">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title" id="withdrawalModalLabel">회원탈퇴</h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                        </div>
                        <div class="modal-body text-center">
                            <p>정말로 탈퇴하시겠습니까?</p>
                            <p>탈퇴하시면 복구가 불가능합니다.</p>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">취소</button>
                            {#if isLoaded_delete}
                                <button type="submit" class="btn btn-danger disabled">
                                    <Loding />
                                </button>
                            {:else}
                                <button type="submit" class="btn btn-danger" on:click={delete_user} data-bs-dismiss="modal">탈퇴</button>
                            {/if}
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <Error error={error_password} />
        <Error error={error_delete} />

    </div>
</div>