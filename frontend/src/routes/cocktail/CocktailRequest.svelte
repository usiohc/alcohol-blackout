<script>
    import { push } from "svelte-spa-router"
    import Error from "../../components/Error.svelte"
    import fastapi from "../../lib/api"


    let isLoaded = false;
    $: isLoaded;

    let spirit = {
        "type": "",
        "name": "",
        "name_ko": "",
        "unit": "ml",
        "amount": "",
    }

    let material = {
        "type": "",
        "name": "",
        "name_ko": "",
        "unit": "",
        "amount": "",
    }

    let cocktail = {
        "name": "",
        "name_ko": "",
        "skill": "",
        "abv": "",
        // "image": "",
        "spirits": [],
        "materials": [],
    };
    let spiritFilled = true;
    let materialFilled = false;

    $: isFormFilled = cocktail.name_ko && cocktail.skill && cocktail.abv && spiritFilled && materialFilled;
    
    $: {
        if (cocktail.spirits.length > 0) {
            cocktail.spirits.forEach(spirit => {
                if (spirit.type && spirit.amount) {
                    spiritFilled = true;
                } else {
                    spirit.isFilled = false;
                }
            });
        } 

        if (cocktail.materials.length > 0) {
            cocktail.materials.forEach(material => {
                if (material.type && material.name_ko && material.amount && material.unit) {
                    materialFilled = true;
                } else {
                    material.isFilled = false;
                }
            });
        } 
    }


    let error = {detail:[]};
    
    // $: cocktail.spirits;
    function addSpirit() {
        cocktail.spirits.push({ ...spirit });
        cocktail = { ...cocktail };
    }

    function removeSpirit() {
        cocktail.spirits.pop();
        cocktail = { ...cocktail };
    }

    function addMaterial() {
        cocktail.materials.push({ ...material });
        cocktail = { ...cocktail };
    }

    function removeMaterial() {
        cocktail.materials.pop();
        cocktail = { ...cocktail };
    }

    function cocktailRequest(event) {
        event.preventDefault()
        isLoaded = true;
        let url = '/api/cocktails/request'
        let params = {
            "name": cocktail.name,
            "name_ko": cocktail.name_ko,
            "skill": cocktail.skill,
            "abv": cocktail.abv,
            "spirits": cocktail.spirits,
            "materials": cocktail.materials,
        }

        fastapi('post', url, params, 
            (json) => { 
                alert("칵테일 요청이 완료되었습니다.")
                push('/')
            }, 
            (json_error) => { 
                error = json_error
            }
        )
        isLoaded = false;
    }

    function test(event) {
        event.preventDefault()
        console.log(cocktail)
    }
</script>


<div class="mt-3">
    <Error error={error} />
</div>
<div class="container-md mt-3">
    <div class="alert alert-secondary" role="alert">
        <h4 class="alert-heading">유의사항</h4>
        <hr>
        <div class="text-start">
            <p class="mb-1">- 기주는 필수가 아닙니다.</p>
            <p class="mb-1">- 재료는 필수 입니다.</p>
            <p class="mb-1">- 칵테일의 기주가 리큐어라면 재료에서 입력해주세요.</p>
        </div>
    </div>
    <form method="post" class="row g-3">
        <!-- 칵테일 -->
        <div class="mt-3 mb-4">
            <h5 class="my-3 border-top border-bottom p-2">칵테일</h5>
            <div class="row row-cols-1 {import.meta.env.DEV? "row-cols-sm-2":""}">
                <div class = "col form-floating">
                    <input type="text" class="form-control { cocktail.name_ko.length > 0 ? 'is-valid':'is-invalid'}" id="name_ko" placeholder="Name_ko" maxlength="20" bind:value="{cocktail.name_ko}">
                    <label for="name_ko">칵테일 이름</label>
                </div>
                <!-- <div class = "col form-floating">
                    <input type="text" class="form-control" id="name" placeholder="Name" minlength="0" maxlength="50" bind:value="{cocktail.name}">
                    <label for="name">영문 칵테일 이름</label>
                </div> -->
            </div>
            <div class="row g-2">
                <div class="col form-floating">
                    <select class="form-select { cocktail.skill ? 'is-valid':'is-invalid'}" id="skill" bind:value="{cocktail.skill}">
                        <option value="Build">빌드</option>
                        <option value="Stir">스터</option>
                        <option value="Shake">쉐이킹</option>
                        <option value="Float">플로트</option>
                        <option value="Blend">블랜드</option>
                    </select>
                    <label for="skill">제조기법</label>
                </div>
                <div class="col input-group">
                    <div class="form-floating">
                        <input type="number" class="form-control { cocktail.abv && cocktail.abv < 100 ? 'is-valid':'is-invalid'}" id="abv" placeholder="None" maxlength="2" bind:value="{cocktail.abv}">
                        <label for="abv">알코올 도수</label>
                    </div>
                    <span class="input-group-text">도</span>
                </div>
            </div>
            {#if import.meta.env.DEV}
            <div class="col input-group mt-2">
                <label class="input-group-text" for="image">이미지</label>
                <input class="form-control" type="file" accpet="image/*" id="image" placeholder="이미지">
            </div>
            {/if}
        </div>
        <!-- 칵테일 끝 -->

        <!-- 기주 -->
        <div class="mt-3 mb-4">
            <h5 class="border-top border-bottom p-2">기주</h5>
            {#if cocktail.spirits.length > 0}
                <div class="alert alert-secondary mb-0" role="alert">
                        특정한 기주가 필요하지 않다면, <b>[ 기주 이름 ]</b> 을 비워두고 양만 입력해주세요.
                </div>
            {/if}

            
            {#each cocktail.spirits as { type, name_ko, name, amount, unit }}
                <div class="row g-2 p-0 m-0">
                    <div class="col-3 form-floating">
                        <select class="form-select { type ? 'is-valid':'is-invalid'}" id="type" bind:value="{type}">
                            <option value="Vodka">보드카</option>
                            <option value="Gin">진</option>
                            <option value="Rum">럼</option>
                            <option value="Tequila">데킬라</option>
                            <option value="Whisky">위스키</option>
                            <option value="Brandy">브랜디</option>
                            <!-- <option value="Liqueur">블랜드</option> -->
                            <option value="Beer">맥주</option>
                            <option value="Wine">와인</option>
                        </select>
                        <label for="type">종류</label>
                    </div>
                    <div class = "col form-floating">
                        <input type="text" class="form-control { name_ko.length > 0 ? 'is-valid':'is-invalid'}" id="name_ko" placeholder="Name_ko" maxlength="20" bind:value="{name_ko}">
                        <label for="name_ko">기주 이름</label>
                    </div>
                    <!-- <div class = "col form-floating">
                        <input type="text" class="form-control" id="name" placeholder="Name" minlength="0" maxlength="50" bind:value="{name}">
                        <label for="name">영문 기주 이름</label>
                    </div> -->
                    <div class="col input-group">
                        <div class="form-floating">
                            <input type="number" class="form-control { amount ? 'is-valid':'is-invalid'}" id="amount" placeholder="None" maxlength="3" bind:value="{amount}">
                            <label for="amount">양</label>
                        </div>
                        <span class="input-group-text" id="inputGroup-sizing-sm">ml</span>
                    </div>
                </div>
            {/each}
            <div class="btn-group col-8 mt-3" role="group">
                <button type="button" class="btn btn-primary" on:click={addSpirit}>추가</button>
                <button type="button" class="btn btn-danger {cocktail.spirits.length === 0 ? 'disabled':''}" on:click={removeSpirit}>제거</button>
            </div>
        </div>
        <!-- 기주 끝 -->

        <!-- 재료 -->
        <div class="mt-3 mb-4">
            <h5 class="border-top border-bottom p-2 mb-0">재료</h5>

            {#each cocktail.materials as { type, name_ko, name, amount, unit }}
                <div class="row g-2 p-0 m-0">
                    <div class="col-3 form-floating">
                        <select class="form-select { type ? 'is-valid':'is-invalid'}" id="type" bind:value="{type}">
                            <option value="Liqueur">리큐어</option>
                            <option value="Syrup">시럽</option>
                            <option value="Juice">주스</option>
                            <option value="Soda">탄산</option>
                            <option value="Garnish">가니쉬</option>
                            <option value="Etc">기타</option>
                        </select>
                        <label for="type">종류</label>
                    </div>
                    <div class = "col form-floating">
                        <input type="text" class="form-control { name_ko.length > 0 ? 'is-valid':'is-invalid'}" id="name_ko" placeholder="Name_ko" maxlength="20" bind:value="{name_ko}">
                        <label for="name_ko">재료 이름</label>
                    </div>
                    <!-- <div class = "col form-floating">
                        <input type="text" class="form-control" id="name" placeholder="Name" minlength="0" maxlength="50" bind:value="{name}">
                        <label for="name">영문 재료 이름</label>
                    </div> -->
                    <div class="col input-group">
                        {#if unit === "Full_up"}
                            {amount=''}
                            <div class="form-floating">
                                <input type="number" class="form-control is-valid" id="amount" placeholder="None" maxlength="3" disabled>
                                <label for="amount">양</label>
                            </div>
                        {:else}
                        <div class="form-floating">
                            <input type="number" class="form-control { amount ? 'is-valid':'is-invalid'}" id="amount" placeholder="None" maxlength="3" bind:value="{amount}">
                            <label for="amount">양</label>
                        </div>
                        {/if}
                        <div class="form-floating">
                            <select class="form-select text-start { unit ? 'is-valid':'is-invalid'}" id="unit" bind:value="{unit}">
                                <option value="ml">ml</option>
                                <option value="piece">ea</option>
                                <option value="drop">drop</option>
                                <option value="Full_up">가득</option>
                                <option value="dash">tsp</option>
                                <option value="tsp">dash</option>
                                <option value="pinch">꼬집</option>
                            <!-- <span class="input-group-text" id="inputGroup-sizing-sm">{unit = "ml"}</span> -->
                            </select>
                            <label for="unit">단위</label>
                        </div>
                    </div>
                </div>
            {/each}
            <div class="btn-group col-8 mt-3" role="group">
                <button type="button" class="btn btn-primary" on:click={addMaterial}>추가</button>
                <button type="button" class="btn btn-danger {cocktail.materials.length === 0 ? 'disabled':''}" on:click={removeMaterial}>제거</button>
            </div>
            <!-- 재료 끝 -->
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
            <button type="submit" class="btn btn-primary mb-5" on:click="{ cocktailRequest }" disabled={ !isFormFilled }>칵테일 요청</button>
        {/if}
    </form>
    {#if import.meta.env.DEV}
        <button type="button" class="btn btn-primary mb-5" on:click="{ test }">테스트</button>
    {/if}
</div>